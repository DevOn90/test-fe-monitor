from helpers.loki import LokiClient

def test_successfull_http_request_reaches_loki(browser):

    loki = LokiClient()

    # open the Angualar application
    browser.get("http://localhost:4200")

    # Trigger a successful HTTP request in Angular application
    browser.execute_script(f"""
          fetch('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => response.json())
            .then(data => console.log('OBS-TEST-011', data));
    """)

    # Wait for the HTTP tracing event in Loki.
    tracing_log = loki.wait_for_log(
        logql_query=(
            '{service_name="front-end"} '
            '|= "jsonplaceholder.typicode.com" '
            '|= "faro.tracing.fetch"'
        ),
        expected_text="jsonplaceholder.typicode.com",
        timeout=30,
    )

    # Wait for browser performance log
    performance_log = loki.wait_for_log(
        logql_query=(
            '{service_name="front-end"} '
            '|= "jsonplaceholder.typicode.com" '
            '|= "faro.performance.resource"'
        ),
        expected_text="jsonplaceholder.typicode.com",
        timeout=30,
    )
    
    # Assert that both logs are found
    assert tracing_log, "HTTP tracing log not found"
    assert performance_log, "Browser performance log not found"

    # Verify HTTP possitive response is logged
    assert "kind=event" in tracing_log
    assert "event_domain=browser" in tracing_log
    assert "event_data_http.request.method=GET" in tracing_log
    assert "event_data_http.response.status_code=200" in tracing_log
    assert "event_data_server.address=jsonplaceholder.typicode.com" in tracing_log
    assert "sdk_name=faro-web" in tracing_log
    # Verify browser performance log

    assert "kind=event" in performance_log
    assert "event_domain=browser" in performance_log
    assert "event_data_httpHost=jsonplaceholder.typicode.com" in performance_log
    assert "sdk_name=faro-web" in performance_log