from helpers.loki import LokiClient

def test_console_errors_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS-TEST-003"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger a console error in the Angular application
    browser.execute_script(
        """
        console.error('OBS-TEST-003: console error test');
        """
    )

    # Wait until the exception appears in Loki.
    log = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "OBS-TEST-003"',
        expected_text=marker,
        timeout=30,
    )

    # Verify exception classification
    assert "kind=exception" in log

    # Verify Javascript Error Type
    assert "type=Error" in log

    # Verify exception message
    assert marker in log

    # Verify stack trace presence
    assert "stacktrace=" in log

    # Verify Faro  SDK metadata.
    assert "sdk_name=faro-web" in log