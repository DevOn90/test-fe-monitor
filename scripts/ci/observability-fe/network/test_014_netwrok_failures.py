#!/usr/bin/env python3

# ================================================
# Purpose: The test verifies that network failures, including fetch failures, 
#          request timeouts, and CORS errors, are properly logged in Loki.
#
# Test Scope: 1. Network faetch failure
#             2. Request timeout failure
#             3. CORS failure
# ================================================

from helpers.loki import LokiClient

def test_network_failures_reaches_loki(browser) -> None:

    """
    - Test that network failures, including fetch failures, request timeouts, and CORS errors, are logged in Loki.

    Args:
        browser: Selenium WebDriver instance.

    Returns:
        None
    """

    loki = LokiClient()

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)

    # Simulate a network fetch failure by requesting an unavailable endpoint
    browser.execute_async_script("""
    const callback = arguments[arguments.length - 1];

    fetch('http://127.0.0.1:59999/unavailable/OBS-TEST-014-Network')
        .then(() => callback({success: false, reason: 'Request unexpectedly succeeded'}))
        .catch(() => callback({success: true}));
""")

    # Simulate a request timeout failure
    browser.execute_async_script("""
    const callback = arguments[arguments.length - 1];

    const controller = new AbortController();

    setTimeout(() => controller.abort(), 1000);

    fetch('https://httpbin.org/delay/5', {
        signal: controller.signal
    })
        .then(() => callback({success: false, reason: 'Request unexpectedly succeeded'}))
        .catch(() => callback({success: true}));
""")

    # Simulate a CORS failure
    browser.execute_async_script("""
    const callback = arguments[arguments.length - 1];

    fetch('https://example.com/OBS-TEST-014-cors')
        .then(() => callback({success: false, reason: 'Request unexpectedly succeeded'}))
        .catch(() => callback({success: true}));

""")

    # Get network failure logs from Loki
    network_failure_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "OBS-TEST-014-Network"'
            '|= "event_name=faro.tracing.fetch"'
        ),
        timeout=30,
        expected_text='OBS-TEST-014-Network'
    )

    # Get network failure log performance metrics from Loki
    network_failure_perf_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "OBS-TEST-014-Network"'
            '|= "event_name=faro.performance.resource"'
        ),
        timeout=30,
        expected_text='OBS-TEST-014-Network'
    )

    # Get request timeout failure logs from Loki
    timeout_failure_log = loki.wait_for_log(
            logql_query=(
                '{service_name=~".+"}' 
                '|= "httpbin.org"'
                '|= "event_name=faro.tracing.fetch"'
            ),
            timeout=30,
            expected_text='httpbin.org'
        )

    # Verify Timeout Failure Performance Logs
    timeout_failure_perf_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "httpbin.org"'
            '|= "event_name=faro.performance.resource"'
        ),
        timeout=30,
        expected_text='httpbin.org'
    )

    # Get CORS failure logs from Loki
    cors_failure_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "OBS-TEST-014-cors"'
            '|= "event_name=faro.tracing.fetch"'
        ),
        timeout=30,
        expected_text='OBS-TEST-014-cors'
    )

    # Get CORS failure performance logs from Loki
    cors_failure_perf_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "OBS-TEST-014-cors"'
            '|= "event_name=faro.performance.resource"'
        ),
        timeout=30,
        expected_text='OBS-TEST-014-cors'
    )

    # Verify that all network failure logs were captured
    assert network_failure_log is not None, "Network failure log not found"
    assert timeout_failure_log is not None, "Timeout failure log not found"
    assert cors_failure_log is not None, "CORS failure log not found"

    # Verify Network Failure Logs
    assert "kind=event" in network_failure_log
    assert "event_name=faro.tracing.fetch" in network_failure_log
    assert "event_data_http.response.status_code=0" in network_failure_log
    assert "sdk_name=faro-web" in network_failure_log
    
    # Verify Network Failure Performance Logs
    assert "kind=event" in network_failure_perf_log
    assert "event_name=faro.performance.resource" in network_failure_perf_log
    assert "event_data_initiatorType=fetch" in network_failure_perf_log
    assert "sdk_name=faro-web" in network_failure_perf_log

    # Verify Timeout Failure Logs
    assert "kind=event" in timeout_failure_log
    assert "event_name=faro.tracing.fetch" in timeout_failure_log
    assert "event_data_http.response.status_code=0" in timeout_failure_log
    assert "event_data_server.address=httpbin.org" in timeout_failure_log
    assert "sdk_name=faro-web" in timeout_failure_log

    # Verify Timeout Failure Performance Logs
    assert "kind=event" in timeout_failure_perf_log
    assert "event_name=faro.performance.resource" in timeout_failure_perf_log
    assert "event_data_initiatorType=fetch" in timeout_failure_perf_log
    assert "event_data_httpHost=httpbin.org" in timeout_failure_perf_log
    assert "sdk_name=faro-web" in timeout_failure_perf_log

    # Verify CORS Failure Logs
    assert "kind=event" in cors_failure_log
    assert "event_name=faro.tracing.fetch" in cors_failure_log
    assert "event_data_http.response.status_code=0" in cors_failure_log
    assert "event_data_server.address=example.com" in cors_failure_log
    assert "sdk_name=faro-web" in cors_failure_log

    # Verify CORS Failure Performance Logs
    assert "kind=event" in cors_failure_perf_log
    assert "event_name=faro.performance.resource" in cors_failure_perf_log
    assert "event_data_initiatorType=fetch" in cors_failure_perf_log
    assert "event_data_httpHost=example.com" in cors_failure_perf_log
    assert "sdk_name=faro-web" in cors_failure_perf_log