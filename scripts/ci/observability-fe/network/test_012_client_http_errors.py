#!/usr/bin/env python3

# ================================================
# Purpose: The test verifies that client-side HTTP errors 
#          are properly logged in Loki.
#
# Test Scope: 1. Client-side HTTP 404 error logging
#             2. Client-side HTTP 400 error logging
# ================================================

from helpers.loki import LokiClient

def test_client_http_errors(browser) -> None:

    """
    - Test that client-side HTTP errors (404 and 400) are logged in Loki.

    Args:
        browser: Selenium WebDriver instance.

    Returns:
        None
    """

    # Create unique identifier for this test run
    import uuid
    test_run_id = uuid.uuid4().hex

    loki = LokiClient()

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)

    # Trigger a client-side HTTP 404 error in Angular application
    browser.execute_async_script("""
        const testRunId = arguments[0];
        const callback = arguments[arguments.length - 1];

        fetch(`https://jsonplaceholder.typicode.com/missing-resource?obs_test_id=OBS-TEST-012-missing-resource-${testRunId}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                callback({success: true, status: 200, dataReceived: !!data});
            })
            .catch(error => callback({success: false, error: error.message}));
    """, test_run_id)

    # Trigger a client-side HTTP 400 error in Angular application
    browser.execute_async_script("""
        const testRunId = arguments[0];
        const callback = arguments[arguments.length - 1];

        fetch(`https://httpbin.org/status/400?obs_test_id=OBS-TEST-012-400-${testRunId}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                callback({success: true, status: 200, dataReceived: !!data});
            })
            .catch(error => callback({success: false, error: error.message}));
    """, test_run_id)

    # Get the client-side HTTP 404 error tracinglog from Loki
    http_404_log_tracing = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-012-missing-resource-{test_run_id}"'
            '|= "event_name=faro.tracing.fetch"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-012-missing-resource-{test_run_id}",
        timeout=30
    )

    # Get the client-side HTTP 404 error performance log from Loki
    http_404_log_performance = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-012-missing-resource-{test_run_id}"'
            '|= "event_name=faro.performance.resource"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-012-missing-resource-{test_run_id}",
        timeout=30
    )
    # Get the client-side HTTP 400 error tracinglog from Loki
    http_400_log_tracing = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-012-400-{test_run_id}"'
            '|= "event_name=faro.tracing.fetch"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-012-400-{test_run_id}",
        timeout=30
    )

    # Get the client-side HTTP 400 error performance log from Loki
    http_400_log_performance = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-012-400-{test_run_id}"'
            '|= "event_name=faro.performance.resource"'
        ),
        expected_text=f"obs_test_id=OBS-TEST-012-400-{test_run_id}",
        timeout=30
    )

    # Verify that all expected logs were found
    assert http_404_log_tracing is not None, "HTTP 404 tracing log not found"
    assert http_404_log_performance is not None, "HTTP 404 performance log not found"
    assert http_400_log_tracing is not None, "HTTP 400 tracing log not found"
    assert http_400_log_performance is not None, "HTTP 400 performance log not found"

    # Verify http 404 error tracing details
    assert "kind=event" in http_404_log_tracing
    assert "event_name=faro.tracing.fetch" in http_404_log_tracing
    assert "event_data_http.request.method=GET" in http_404_log_tracing
    assert "event_data_http.response.status_code=404" in http_404_log_tracing
    assert "event_data_server.address=jsonplaceholder.typicode.com" in http_404_log_tracing
    assert "sdk_name=faro-web" in http_404_log_tracing

    # Verify http 404 error performance details
    assert "kind=event" in http_404_log_performance
    assert "event_name=faro.performance.resource" in http_404_log_performance
    assert "event_data_httpHost=jsonplaceholder.typicode.com" in http_404_log_performance
    assert "event_data_initiatorType=fetch" in http_404_log_performance
    assert "event_data_responseStatus=404" in http_404_log_performance
    assert "sdk_name=faro-web" in http_404_log_performance

    # Verify http 400 error tracing details
    assert "kind=event" in http_400_log_tracing
    assert "event_name=faro.tracing.fetch" in http_400_log_tracing
    assert "event_data_http.request.method=GET" in http_400_log_tracing
    assert "event_data_http.response.status_code=400" in http_400_log_tracing
    assert "event_data_server.address=httpbin.org" in http_400_log_tracing
    assert "sdk_name=faro-web" in http_400_log_tracing

    # Verify http 400 error performance details
    assert "kind=event" in http_400_log_performance
    assert "event_name=faro.performance.resource" in http_400_log_performance
    assert "event_data_httpHost=httpbin.org" in http_400_log_performance
    assert "event_data_initiatorType=fetch" in http_400_log_performance
    assert "event_data_responseStatus=400" in http_400_log_performance
    assert "sdk_name=faro-web" in http_400_log_performance