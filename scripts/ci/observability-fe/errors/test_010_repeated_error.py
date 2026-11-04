from helpers.loki import LokiClient


def test_repeated_errors_reach_loki(browser):
    
    loki = LokiClient()

    marker = "OBS-TEST-010"
    message = f"{marker}: repeated error test"

    browser.get("http://localhost:4200")

    browser.execute_script("""
        
        function triggerRepeatedError() {
            throw new Error('OBS-TEST-010: repeated error test');
        }

        for (let i = 0; i < 3; i++) {
            setTimeout(() => {
                try {
                    triggerRepeatedError();
                } catch (error) {
                    window.dispatchEvent(new ErrorEvent('error', {
                        error,
                        message: error.message,
                    }));
                }
            }, i * 500);
        }
        """)

    logs = loki.wait_for_logs(
        logql_query='{service_name=~".+"} |= "OBS-TEST-010"',
        expected_count=6,
        expected_text=message,
        timeout=30,
    )

    console_logs = [
        log for log in logs
        if "console.error:" in log
    ]

    original_error_logs = [
        log for log in logs
        if message in log and "console.error:" not in log
    ]

    # Three Angular/console-related records
    assert len(console_logs) >= 3

    # Three original browser exception records
    assert len(original_error_logs) >= 3

    for log in logs:
        assert "kind=exception" in log
        assert "type=Error" in log
        assert marker in log
        assert "stacktrace=" in log
        assert "sdk_name=faro-web" in log