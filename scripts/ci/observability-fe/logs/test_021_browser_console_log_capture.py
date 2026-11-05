from helpers.loki import LokiClient

def test_browser_console_log_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS-TEST-021"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger an console logs in the Angular application
    browser.execute_script(
        """
        const marker = `OBS-TEST-021`;

        console.error(`${marker}: error message`);
        console.warn(`${marker}: warning message`);
        console.info(`${marker}: info message`);

        console.debug(`${marker}: debug message`);
        console.log(`${marker}: log message`);
        console.trace(`${marker}: trace message`);
        """
    )

    # Wait until the exception appears in Loki.
    log_error = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "OBS-TEST-021" |= "type=Error"',
        expected_text=marker,
        timeout=30,
    )

    log_warn = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "OBS-TEST-021" |= "level=warn"',
        expected_text=marker,
        timeout=30,
    )

    log_info = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "OBS-TEST-021" |= "level=info"',
        expected_text=marker,
        timeout=30,
    )

    # Verify logs are captured
    assert log_error is not None
    assert log_warn is not None
    assert log_info is not None

    # Verify Error log content
    assert "kind=exception" in log_error
    assert "stacktrace=" in log_error
    assert "sdk_name=faro-web" in log_error

    # Verify Warn log content
    assert "level=warn" in log_warn
    assert "sdk_name=faro-web" in log_warn

    # Verify Info log content
    assert "kind=log" in log_info
    assert "sdk_name=faro-web" in log_info