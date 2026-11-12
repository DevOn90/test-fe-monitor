import time

from helpers.loki import LokiClient


def test_faro_sdk_deduplicates_repeated_error_reports(browser):
    loki = LokiClient()

    browser.get("http://localhost:4200")

    marker = browser.execute_script("""
        return (() => {
            const marker = `OBS-TEST-010A-${Date.now()}`;
            const error = new Error(`${marker}: repeated SDK error`);

            for (let i = 0; i < 3; i++) {
                window.faro.api.pushError(error);
            }

            return marker;
        })();
    """)

    assert marker, "Test marker was not returned by the browser"

    first_log = loki.wait_for_log(
        logql_query=f'{{service_name="front-end"}} |= "{marker}"',
        expected_text=marker,
        timeout=30,
    )

    assert "kind=exception" in first_log
    assert "type=Error" in first_log
    assert "stacktrace=" in first_log
    assert "sdk_name=faro-web" in first_log
    assert "sdk_version=2.12.1" in first_log

    # Allow time for any additional records to arrive.
    time.sleep(5)

    matching_logs = [
        log for log in loki.query_logs(
            logql_query=f'{{service_name="front-end"}} |= "{marker}"'
        )
        if marker in log
    ]

    assert len(matching_logs) == 1, (
        f"Expected exactly 1 Loki record after 3 identical pushError calls, "
        f"but found {len(matching_logs)}:\n"
        + "\n".join(matching_logs)
    )