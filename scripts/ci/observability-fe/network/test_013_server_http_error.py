#!/usr/bin/env python3

# ================================================
# Purpose: The test verifies that server-side HTTP errors are properly logged in Loki.
#
# Test Scope: 1. Server-side HTTP 500 error logging
#            
# Out of scope: Server-side HTTP errors 501-508
#               See manual test 'Test-013' for details
# ================================================

from helpers.loki import LokiClient

def test_server_http_500_error_logging(browser) -> None:

    """
    Test that server-side HTTP 500 errors are properly logged in Loki.
    
    Arguments:
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

    # Trigger a server-side HTTP 500 error
    browser.execute_async_script("""
    const testRunId = arguments[0];
    const callback = arguments[arguments.length - 1];
    
    fetch(`https://httpbin.org/status/500?obs_test_id=OBS-TEST-013-500-${testRunId}`)
        .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
        .then(data => {
                callback({success: true, status: 200, dataReceived: !!data});
            })
            .catch(error => callback({success: false, error: error.message}));
""", test_run_id)

    # Get the server-side HTTP 500 error logs from Loki
    http_500_tracing_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-013-500-{test_run_id}"'
            '|= "event_name=faro.tracing.fetch"'
        ),
        timeout=30,
        expected_text="httpbin.org/status/500"
    )

    # Get the server-side http 500 error performance logs from Loki
    http_500_perf_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f'|= "obs_test_id=OBS-TEST-013-500-{test_run_id}"'
            '|= "event_name=faro.performance.resource"'
        ),
        timeout=30,
        expected_text="httpbin.org/status/500"
    )

    # Verify that all expected logs were found
    assert http_500_tracing_log is not None, "Expected server-side HTTP 500 tracing log not found"
    assert http_500_perf_log is not None, "Expected server-side HTTP 500 performance log not found"

    # Verify http 500 error tracing details
    assert "kind=event" in http_500_tracing_log
    assert "event_name=faro.tracing.fetch" in http_500_tracing_log
    assert "event_data_http.request.method=GET" in http_500_tracing_log
    assert "event_data_http.response.status_code=500" in http_500_tracing_log
    assert "event_data_server.address=httpbin.org" in http_500_tracing_log
    assert "sdk_name=faro-web" in http_500_tracing_log

    # Verify http 500 error performance details
    assert "kind=event" in http_500_perf_log
    assert "event_name=faro.performance.resource" in http_500_perf_log
    assert "event_data_httpHost=httpbin.org" in http_500_perf_log
    assert "event_data_initiatorType=fetch" in http_500_perf_log
    assert "sdk_name=faro-web" in http_500_perf_log
