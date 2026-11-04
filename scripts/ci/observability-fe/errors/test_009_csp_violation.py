from helpers.loki import LokiClient

def test_csp_violations_reaches_loki(browser):

    loki = LokiClient()

    marker = "OBS-TEST-009"

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger a CSP violation in the Angular application
    browser.execute_script(
        """
        const meta = document.createElement('meta')
        meta.httpEquiv="Content-Security-Policy"
        meta.content="img-src 'self'"
        document.head.appendChild(meta)

        const img = new Image();
        img.src = 'https://example.com/OBS-TEST-009-csp-image.png';
        document.body.appendChild(img);
        """
    )

    # Wait until the exception appears in Loki.
    logs = loki.wait_for_logs(
        logql_query='{service_name=~".+"} |= "OBS-TEST-009"',
        expected_count=2,
        expected_text=marker,
        timeout=30,
    )

    # Identify the two different capture paths
    scp_event_log = next(
        (log for log in logs if "kind=event" in log),
        None,
    )

    resource_error_log = next(
        (
            log for log in logs
            if "type=ResourceLoadError" in log
        ),
        None,
    )

    # Verify SCP violation
    assert scp_event_log is not None
    assert "kind=event" in scp_event_log
    assert marker in scp_event_log
    assert "event_name=securitypolicyviolation" in scp_event_log
    assert "event_domain=browser" in scp_event_log
    assert "event_data_blockedURI=https://example.com/OBS-TEST-009-csp-image.png" in scp_event_log
    assert "event_data_effectiveDirective=img-src" in scp_event_log
    assert "event_data_violatedDirective=img-src" in scp_event_log
    assert "event_data_disposition=enforce" in scp_event_log
    assert 'event_data_originalPolicy="img-src \'self\'"' in scp_event_log
    assert "sdk_name=faro-web" in scp_event_log

    # Verify resource load error
    assert resource_error_log is not None
    assert "kind=exception" in resource_error_log
    assert "type=ResourceLoadError" in resource_error_log
    assert marker in resource_error_log
    assert "stacktrace=" in resource_error_log
    assert "sdk_name=faro-web" in resource_error_log
    assert "OBS-TEST-009-csp-image.png" in resource_error_log
    