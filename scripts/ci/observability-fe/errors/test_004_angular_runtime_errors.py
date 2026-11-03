from helpers.loki import LokiClient

def test_angular_runtime_errors_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS-TEST-004"

    # open the Angualar application
    browser.get("http://localhost:4200")

    try:
        # Add temporary button and click handler to trigger runtime error
        browser.execute_script(
            """
            const button = document.createElement('button');
            button.id = 'test-angular-runtime-error-button';
            button.textContent = 'Trigger Runtime Error';

            button.addEventListener('click', () => {
                throw new Error(
                    'OBS-TEST-004: Angular runtime error test'
                );
            });

            document.body.appendChild(button);
            """
        )

        # Find and click the button to trigger the runtime error
        browser.find_element(
            "id",
            "test-angular-runtime-error-button"
        ).click()

        # Wait until the exception appears in Loki.
        log = loki.wait_for_log(
            logql_query='{service_name=~".+"} |= "OBS-TEST-004"',
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

    finally:
        # Remove the temporary button after the test
        browser.execute_script(
            """
            const button = document.getElementById('test-angular-runtime-error-button');
            if (button) {
                button.remove();
            }
            """
        )