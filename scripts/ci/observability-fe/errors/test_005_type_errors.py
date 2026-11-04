from helpers.loki import LokiClient

def test_type_errors_reaches_loki(browser):

    loki = LokiClient()

    marker = "ERROR TypeError"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger a console error in the Angular application
    browser.execute_script(
        """
        setTimeout(() => {
            const testValue = undefined;
            testValue.someMethod();
        }, 0);
        """
    )

    # Wait until the exception appears in Loki.
    log = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "ERROR TypeError"',
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