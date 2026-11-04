from helpers.loki import LokiClient

def test_errors_with_stack_trace_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS-TEST-008"
    message = f"{marker}: stack trace test"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger an error with stack trace in the Angular application
    browser.execute_script(
        """
        function testStackTraceLevel1() {
           testStackTraceLevel2();
        }

        function testStackTraceLevel2() {
           testStackTraceLevel3();
        }

        function testStackTraceLevel3() {
           throw new Error('OBS-TEST-008: stack trace test');
        }

        setTimeout(() => testStackTraceLevel1(), 0);
        """
    )

    # Wait until the exception appears in Loki.
    logs = loki.wait_for_logs(
        logql_query='{service_name=~".+"} |= "OBS-TEST-008"',
        expected_count=2,
        expected_text=marker,
        timeout=30,
    )

    # Console/ErrorHandler path
    console_logs = [
        log for log in logs
        if "console.error:" in log
    ]

    # Original JavaScript exception
    original_error_logs = [
        log for log in logs
        if message in log and "console.error:" not in log
    ]


    # Verify both capture paths.
    assert console_logs, "Console/ErrorHandler exception record was not found."
    assert original_error_logs, "Original JavaScript exception record was not found."

    # Verify the original exception's stack trace.
    original_log = original_error_logs[0]

    assert "kind=exception" in original_log
    assert "type=Error" in original_log
    assert "stacktrace=" in original_log
    assert "testStackTraceLevel3" in original_log
    assert "testStackTraceLevel2" in original_log
    assert "testStackTraceLevel1" in original_log
    assert "sdk_name=faro-web" in original_log