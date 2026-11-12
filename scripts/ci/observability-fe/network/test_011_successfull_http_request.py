#!/usr/bin/env python3

# ================================================
# Purpose: This test verifies that a successfull HTTP & XML requests
#          are successfully logged in Loki, including tracing and performance logs.
#          
# Test Scope:  1. HTTP Fetch API request sucess
#              2. XML request success
#              3. Requests duration logged in performance logs
#              4. Requests metadata logged in performance logs
# ================================================

from helpers.loki import LokiClient

def test_successfull_request_reaches_loki(browser) -> None:

    """
    - Test that a successful HTTP and XML request is logged in Loki. 
    - Test includes verification of `Duration`, `Metadata`.  

    Args:
        browser: Selenium WebDriver instance.

    Returns:
        None
    """

    # Create unique identifier for this test run
    import uuid
    test_run_id = uuid.uuid4().hex


    loki = LokiClient()

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Set script timeout for browser execution
    browser.set_script_timeout(30)

    # Trigger a successful HTTP request in Angular application
    # Arguments is selenium 
    browser.execute_async_script("""
        const testRunId = arguments[0];
        const callback = arguments[arguments.length - 1];

        fetch(`https://jsonplaceholder.typicode.com/posts/1?obs_test_id=OBS-TEST-011-FETCH-${testRunId}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                callback({success: true, status: 200, dataReceived: !!data});
            })
            .catch(error => callback({success: false, error: error.message}));
    """, test_run_id)

    # Trigger a successful XML request in Angular application
    browser.execute_async_script("""
    
    const testRunId = arguments[0];
    const callback = arguments[arguments.length - 1];

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `https://jsonplaceholder.typicode.com/posts/1?obs_test_id=OBS-TEST-011-XHR-${testRunId}`);

    xhr.onload = () => {
        callback({success: xhr.status === 200, status: xhr.status, dataReceived: !!xhr.responseText});
    };

    xhr.onerror = () => callback({success: false, error: 'Network error'});

    xhr.send();
""", test_run_id)

    # Wait for the HTTP tracing event in Loki.
    http_tracing_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"} '
            f'|= "obs_test_id=OBS-TEST-011-FETCH-{test_run_id}" '
            '|= "faro.tracing.fetch"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-011-FETCH-{test_run_id}",
        timeout=30,
    )

    # Wait for the XHR tracing event in Loki.
    xhr_tracing_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"} '
            f'|= "obs_test_id=OBS-TEST-011-XHR-{test_run_id}" '
            '|= "faro.tracing.xml-http-request"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-011-XHR-{test_run_id}",
        timeout=30
    )

    # Wait for HTTP performance log in Loki.
    http_performance_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"} '
            f'|= "obs_test_id=OBS-TEST-011-FETCH-{test_run_id}" '
            '|= "event_data_initiatorType=fetch"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-011-FETCH-{test_run_id}",
        timeout=30,
    )

    # Wait for XHR performance log in Loki.
    xhr_performance_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"} '
            f'|= "obs_test_id=OBS-TEST-011-XHR-{test_run_id}" '
            '|= "event_data_initiatorType=xmlhttprequest"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-011-XHR-{test_run_id}",
        timeout=30,
    )
    
    # Assert that all logs are found
    assert http_tracing_log, "HTTP tracing log not found"
    assert xhr_tracing_log, "XHR tracing log not found"
    assert http_performance_log, "HTTP performance log not found"
    assert xhr_performance_log, "XHR performance log not found"

    # Verify HTTP possitive response is logged
    assert "kind=event" in http_tracing_log
    assert "event_name=faro.tracing.fetch" in http_tracing_log
    # Verify HTTP request metadata
    assert "event_data_http.request.method=GET" in http_tracing_log
    assert "event_data_http.response.status_code=200" in http_tracing_log
    assert "event_data_server.address=jsonplaceholder.typicode.com" in http_tracing_log
    assert "event_data_server.port" in http_tracing_log
    assert "sdk_name=faro-web" in http_tracing_log
    # Verify HTTP duration is logged
    assert "event_data_duration_ns" in http_tracing_log

    # Verify XHR positive response is logged
    assert "kind=event" in xhr_tracing_log
    assert "event_name=faro.tracing.xml-http-request" in xhr_tracing_log
    # Verify XHR request metadata
    assert "event_data_http.request.method=GET" in xhr_tracing_log
    assert "event_data_http.response.status_code=200" in xhr_tracing_log
    assert "event_data_server.address=jsonplaceholder.typicode.com" in xhr_tracing_log
    assert "event_data_server.port" in xhr_tracing_log
    assert "sdk_name=faro-web" in xhr_tracing_log
    # Verify XHR duration is logged
    assert "event_data_duration_ns" in xhr_tracing_log
    
    # Verify HTTP performance log
    assert "kind=event" in http_performance_log
    assert "event_domain=browser" in http_performance_log
    assert "event_data_httpHost=jsonplaceholder.typicode.com" in http_performance_log
    assert "event_data_initiatorType=fetch" in http_performance_log
    assert "sdk_name=faro-web" in http_performance_log
    # Verify HTTP duration
    assert "event_data_duration" in http_performance_log
    

    # Verify XHR performance log
    assert "kind=event" in xhr_performance_log
    assert "event_domain=browser" in xhr_performance_log
    assert "event_data_httpHost=jsonplaceholder.typicode.com" in xhr_performance_log
    assert "event_data_initiatorType=xmlhttprequest" in xhr_performance_log
    assert "sdk_name=faro-web" in xhr_performance_log
    # Verify XHR duration
    assert "event_data_duration" in xhr_performance_log