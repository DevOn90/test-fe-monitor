from helpers.loki import LokiClient

def test_reference_errors_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS_TEST_006"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger a reference error in the Angular application
    browser.execute_script(
        """
        setTimeout(() => {
            OBS_TEST_006_NON_EXISTENT_VARIABLE;
        }, 0);
        """
    )

    # Wait until the exception appears in Loki.
    logs = loki.wait_for_logs(
        logql_query='{service_name=~".+"} |= "OBS_TEST_006_NON_EXISTENT_VARIABLE"',
        expected_count=2,
        expected_text=marker,
        timeout=30,
    )

    # Identify the two different capture paths
    console_log = next(
        (log for log in logs if "console.error:" in log),
        None,
    )

    reference_error_log = next(
        (
            log for log in logs
            if "type=ReferenceError" in log
        ),
        None,
    )

    # Verify console/error-handler capture
    assert console_log is not None
    assert "kind=exception" in console_log
    assert "type=Error" in console_log
    assert marker in console_log
    assert "stacktrace=" in console_log
    assert "sdk_name=faro-web" in console_log

    # Verify original JavaScript ReferenceError capture
    assert reference_error_log is not None
    assert "kind=exception" in reference_error_log
    assert marker in reference_error_log
    assert "stacktrace=" in reference_error_log
    assert "sdk_name=faro-web" in reference_error_log