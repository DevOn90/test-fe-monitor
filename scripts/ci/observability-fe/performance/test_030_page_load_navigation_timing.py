#!/usr/bin/env python3

# ===========================================
# Purpose:  Verify that Faro Page Load and Navigation
#           timing telemetry is received by Loki.
#
#============================================

import uuid
from helpers.loki import LokiClient

def test_page_load_navigation_timing(browser) -> None:

    """
    Test to verify that Faro Page Load and Navigation timing telemetry is received by Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """

    # Create unique identifier for the test
    test_run_id = f"OBS-TEST-030-{uuid.uuid4().hex}"

    # Create loki instance for logging
    loki = LokiClient()

    # Navigate to the test page with the unique test run ID as a query parameter
    browser.get(f"http://localhost:4200/?test_run_id={test_run_id}")  # Replace with the URL you want to test

    # Set the script timeout to 30 seconds to allow for LCP measurement
    browser.set_script_timeout(30)

    # Get timing data from Loki log
    timing_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "kind=event"'
            f'|= "{test_run_id}"'
            '|= "faro.performance.navigation"'
        ),
        timeout=30,
        expected_text=test_run_id
    )
    
    # Verify that timing data was retrieved successfully
    assert timing_data is not None, "Failed to retrieve timing data from Loki logs"

    # Verify that the timing data contains the expected navigation timing information
    assert "kind=event" in timing_data
    assert f"test_run_id={test_run_id}" in timing_data
    assert "faro.performance.navigation" in timing_data
    assert "event_domain=browser" in timing_data
    assert "event_data_duration=" in timing_data
    assert "event_data_name=" in timing_data
    assert "event_data_pageLoadTime=" in timing_data
    assert "event_data_responseStatus=" in timing_data
    assert "event_data_ttfb=" in timing_data
    assert "sdk_name=faro-web" in timing_data