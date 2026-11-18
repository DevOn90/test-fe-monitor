#!/usr/bin/env python3

# ============================================
# Purpose: Test and monitor web vitals performance metrics 
#          for the front-end application. 
#
# In scope: 1. Resource Timing
#           2. Long Tasks
#           3. Web-vitals - CLS (Cumulative Layout Shift)
#           4. Web-vitals - INP (Interaction to Next Paint)
#           5. Web-vitals FCP (First Contentful Paint)
#           6. Web-vitals LCP (Largest Contentful Paint)
#           7. Web-vitals TTFB (Time to First Byte)
#
# Tests: 1. Define Variables
#        2. Resource Timing
#        3. Long Tasks
#        4. Web-vitals - CLS
#        5. Web-vitals - INP
#        6. Web-vitals - FCP
#        7. Web-vitals - LCP
#        8. Web-vitals - TTFB
# ============================================ 

# ============================================
# 1. Define Variables
# ============================================

from pathlib import Path
from helpers.loki import LokiClient
import time
import shutil
import uuid
import requests

FRONTEND_ROOT = Path(__file__).resolve().parents[4] \
    / 'apps' \
    / 'front-end'

APP_HTML = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html'

APP_HTML_BACKUP = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html.bak'

# ============================================
# 2. Resource Timing
# ============================================

def test_resource_timing_reaches_loki(browser):

    """
    Test the Resource Timing web-vital measures the performance of resource loading 
    and if the resource timing measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """
    
    loki = LokiClient()

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)
    
    # Get resource timing data from Loki
    resource_timing_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "faro.performance.resource"'
        ),
        timeout=30,
        expected_text="faro.performance.resource"
    )

    # Verify that resource timing data was found in Loki
    assert resource_timing_data is not None, "Resource timing data not found in Loki"

    # Verify the structure of the resource timing data
    assert "kind=event" in resource_timing_data
    assert "event_name=faro.performance.resource" in resource_timing_data
    assert "event_data_initiatorType=xmlhttprequest" in resource_timing_data
    assert "event_data_decodedBodySize=" in resource_timing_data
    assert "event_data_duration=" in resource_timing_data
    assert "event_data_name=http://localhost:4200/config/config.json" in resource_timing_data
    assert "event_data_responseStatus=200" in resource_timing_data
    assert "event_data_transferSize=" in resource_timing_data
    assert "event_data_ttfb=" in resource_timing_data
    assert "sdk_name=faro-web sdk" in resource_timing_data

# ============================================
# 3. Long Tasks
# ============================================

def test_long_tasks_reaches_loki(browser):

    """
    Test the Long Tasks web-vital measures the main thread blocking time 
    and if the long task measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """
    
    loki = LokiClient()

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)

    browser.execute_script("""
    setTimeout(() => {
        const start = performance.now();

        // Block the main thread for approximately 200 ms
        while (performance.now() - start < 200) {
            // Intentionally busy
        }
    }, 1000);
""")

    # Get long task data from Loki
    long_task_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "faro.performance.longtask"'
        ),
        timeout=30,
        expected_text="faro.performance.longtask"
    )

    # Verify that long task data was found in Loki
    assert long_task_data is not None, "Long task data not found in Loki"

    # Verify the structure of the long task data
    assert "kind=event" in long_task_data
    assert "event_name=faro.performance.longtask" in long_task_data
    assert "event_data_duration_ms=" in long_task_data
    assert "event_data_entry_type=longtask" in long_task_data
    assert "event_data_start_time_ms=" in long_task_data
    assert "sdk_name=faro-web sdk" in long_task_data

# ============================================
# 4. Web Vitals - CLS
# ============================================

def test_web_vitals_cls_reaches_loki(browser):
   
    """
    Test the Cumulative Layout Shift (CLS) web-vital measures the visual stability 
    of the application and if the CLS measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """
    
    loki = LokiClient()

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)

    # Execute a script to trigger a CLS (Cumulative Layout Shift) event
    browser.execute_script("""
    (() => {
        window.__clsTestEntries = [];

        const observer = new PerformanceObserver(list => {
            window.__clsTestEntries.push(...list.getEntries());
        });

        observer.observe({ type: 'layout-shift' });
        window.__clsTestObserver = observer;

        const content = document.createElement('div');
        content.id = 'OBS-TEST-031-CONTENT';
        content.style.cssText =
            'height:200px;width:100%;background:lightblue;padding:20px;box-sizing:border-box';
        content.textContent = 'CLS test content';

        document.body.appendChild(content);

        setTimeout(() => {
            const banner = document.createElement('div');
            banner.id = 'OBS-TEST-031-BANNER';
            banner.style.cssText = 'height:100px;width:100%;background:orange';

            document.body.insertBefore(banner, content);
        }, 2000);
    })();
""")

    # Wait for the CLS event
    time.sleep(2.5)

    # Save the application tab
    app_tab = browser.current_window_handle

    # Open a new tab to trigger the CLS event
    browser.switch_to.new_window('tab')
    browser.get("about:blank")
    time.sleep(5)

    # Switch back to the application tab
    browser.switch_to.window(app_tab)

    # Get the CLS entries from Loki
    cls_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "kind=measurement"'
            '|= "cls"'
            '|= "OBS-TEST-031-CONTENT"'
        ),
        timeout=30,
        expected_text='OBS-TEST-031-CONTENT'
    )

    # Verify that the CLS event was captured
    assert cls_data is not None, "CLS event not found in Loki logs"

    # Veify that the CLS event contains the expected content
    assert "kind=measurement" in cls_data
    assert "type=web-vitals" in cls_data
    assert "cls=" in cls_data
    assert "delta=" in cls_data
    assert "context_largest_shift_target=#OBS-TEST-031-CONTENT" in cls_data
    assert "sdk_name=faro-web" in cls_data


# ============================================
# 5. Web Vitals - INP
# ============================================

def test_web_vitals_inp_reaches_loki(browser) -> None:

    """
    Test the Interaction to Next Paint (INP) web-vital measures the responsiveness 
    of the application and if the INP measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """
    
    test_run_id = f"TEST-OBS-031-INP-{uuid.uuid4().hex}"
    
    loki = LokiClient()  # Assuming you have a Loki client instance available

    browser.get("http://localhost:4200")

    browser.set_script_timeout(30)

    browser.execute_script("""
    const test_run_id = arguments[0];
    (() => {
        const button = document.createElement('button');

        button.id = test_run_id;
        button.textContent = 'INP test: click me';

        button.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 999999;
            padding: 20px;
            font-size: 18px;
        `;

        button.addEventListener('click', () => {
            const start = performance.now();

            // Deliberately block the main thread for 300 ms.
            while (performance.now() - start < 300) {
                // Intentional blocking for this test.
            }

            button.textContent = 'Completed';
        });

        document.body.appendChild(button);
    })();
""", test_run_id)

    # Click the button to trigger the INP measurement
    button = browser.find_element("id", test_run_id)
    button.click()

    # Wait for the INP measurement to be recorded
    time.sleep(2)

    # Save the application tab
    app_tab = browser.current_window_handle

    # Open a new tab to trigger the CLS event
    browser.switch_to.new_window('tab')
    browser.get("about:blank")
    time.sleep(5)

    # Switch back to the application tab
    browser.switch_to.window(app_tab)

    # Get the INP event from Loki logs
    inp_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "kind=measurement"'
            '|= "inp"'
            f'|= "{test_run_id}"'
        ),
        timeout=30,
        expected_text=f'{test_run_id}'
    )

    # Verify that the INP event was captured
    assert inp_data is not None, "INP event not found in Loki logs"

    # Verify that the INP event details
    assert "kind=measurement" in inp_data
    assert "type=web-vitals" in inp_data
    assert "delta=" in inp_data
    assert "inp=" in inp_data
    assert f"context_interaction_target=#{test_run_id}" in inp_data
    assert "context_interaction_type=pointer" in inp_data
    assert "context_rating=" in inp_data
    assert "sdk_name=faro-web" in inp_data

# ============================================
# 6. Web-vitals - FCP
# ============================================

def test_web_vitals_fcp_reaches_loki(browser) -> None:

    """
    Test the First Contentful Paint (FCP) web-vital measures how quickly 
    the first content element is rendered in the application and if the FCP measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """
    
    
    # Create unique test marker
    test_run_id = f"OBS-TEST-FCP-031-{uuid.uuid4().hex}" 
    
    # Backup the current app.html
    shutil.copy2(APP_HTML, APP_HTML_BACKUP)

    # Create new content for app.html
    app_html_content = f"""
<div id="{test_run_id}" style="padding: 30px; background: lightblue; color: black;">
    <h1>FCP Test Content</h1>
    <p>Testing First Contentful Paint.</p>
</div>

<router-outlet></router-outlet>
"""

    # Write the new content to app.html
    APP_HTML.write_text(
        app_html_content.strip() + "\n",
        encoding="utf-8"
    )

    # Initialize the Loki client
    loki = LokiClient()

    # Wait for the Angular bundle to include the new test div
    for _ in range(30):
        response = requests.get("http://localhost:4200/main.js")

        if test_run_id in response.text:
            break

        time.sleep(1)

    # Open the application in the browser
    browser.get(f"http://localhost:4200?test_run_id={test_run_id}")

    # Wait for the FCP measurement to be recorded
    time.sleep(2)

    # Get the FCP event from Loki logs
    fcp_data = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            f' |= "{test_run_id}"'
            '| logfmt'
            '| kind="measurement"'
            '| type="web-vitals"'
            '| fcp > 0'
        ),
        timeout=30,
        expected_text=test_run_id
    )

    # Verify that the FCP event was captured
    assert fcp_data is not None, "FCP event not found in Loki logs"

    # Verify that the FCP event details
    assert "kind=measurement" in fcp_data
    assert "type=web-vitals" in fcp_data
    assert "fcp=" in fcp_data
    assert "context_load_state=" in fcp_data
    assert "context_navigation_type=" in fcp_data
    assert "sdk_name=faro-web" in fcp_data

    # Restore the original app.html
    shutil.move(APP_HTML_BACKUP, APP_HTML)

# ============================================
# 7. Web-vitals - LCP
# ============================================

def test_web_vitals_lcp_reaches_loki(browser) -> None:

    """
    Test the Largest Contentful Paint (LCP) web-vital measures how quickly 
    the largest content element is rendered in the application and if the LCP measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """

   
    # Create unique marker for LCP test
    test_run_id = f"OBS-TEST-031-LCP-{uuid.uuid4().hex}"
    
    # Backup the current app.html
    shutil.copy2(APP_HTML, APP_HTML_BACKUP)

    # Generate the new app.html content with the LCP test div
    app_html_content = f"""
<div
 id="{test_run_id}"
 style="
     width: 100%;
     min-height: 400px;
     padding: 30px;
     box-sizing: border-box;
     background: lightblue;
     color: black;
 "
 >
 <h1 style="font-size: 48px;">
     LCP Test — Largest Contentful Paint
 </h1>

 <p style="font-size: 28px;">
     Testing Largest Contentful Paint in the frontend observability reference project.
 </p>
 </div>

 <router-outlet></router-outlet>
"""

    # Write the new content to app.html
    APP_HTML.write_text(
        app_html_content.strip() + "\n",
        encoding="utf-8"
    )

    # Wait for the Angular bundle to include the new test div
    for _ in range(30):
        response = requests.get("http://localhost:4200/main.js")

        if test_run_id in response.text:
            break

        time.sleep(1)

    # Open the application in the browser
    browser.get(f"http://localhost:4200/?test_run_id={test_run_id}")

    # Set the script timeout to 30 seconds to allow for LCP measurement
    browser.set_script_timeout(30)

    # Save the application tab
    app_tab = browser.current_window_handle

    # Open a new tab to trigger the CLS event
    browser.switch_to.new_window('tab')
    browser.get("about:blank")
    time.sleep(5)

    # Switch back to the application tab
    browser.switch_to.window(app_tab)
    
    # Wait for the LCP measurement to be recorded
    time.sleep(2)

    # Initialize the Loki client
    loki = LokiClient()

    # Get the LCP event from Loki logs
    lcp_data = loki.wait_for_log(
        logql_query=(
            '{app_name=~".+"}'
            '|= "kind=measurement"'
            '|= "type=web-vitals"'
            '|= "lcp"'
            f'|= "{test_run_id}"'
        ),
        timeout=30,
        expected_text=test_run_id
    )

    # Verify that the LCP event was found
    assert lcp_data is not None, "LCP event not found in Loki logs"

    # Verify that the LCP event details
    assert "kind=measurement" in lcp_data
    assert "type=web-vitals" in lcp_data
    assert "lcp=" in lcp_data
    assert f"{test_run_id}" in lcp_data
    assert "context_rating=" in lcp_data
    assert "sdk_name=faro-web" in lcp_data

    # Restore the original app.html
    shutil.move(APP_HTML_BACKUP, APP_HTML)

# ============================================
# 8. Web-vitals - TTFB
# ============================================

def test_web_vitals_ttfb_reaches_loki(browser) -> None:

    """
    Test the Time to First Byte (TTFB) web-vital measures how quickly an application
    receives the first byte of the response from the server and if the TTFB measurement log reaches Loki.

    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """

    # Create unique marker for this test run
    test_run_id = f"OBS-TEST-031-TTFB-{uuid.uuid4().hex}"

    # Initialize Loki client
    loki = LokiClient()

    # Disable the browser cache to ensure accurate TTFB measurement
    browser.execute_cdp_cmd(
        "Network.setCacheDisabled",
        {"cacheDisabled": True}
    )

    # Open the application with a unique URL marker
    browser.get(
        f"http://localhost:4200/?test_run_id={test_run_id}"
    )

    # Wait until the application has loaded
    browser.execute_script("""
        return document.readyState === 'complete';
    """)

    # Perform a hard reload
    browser.execute_script("location.reload()")

    # Wait for the Angular to reload with the new test marker in main.js
    for _ in range(30):
        response = requests.get("http://localhost:4200/main.js")

        if test_run_id in response.text:
            break

        time.sleep(1)

    # Wait for the TTFB measurement in Loki
    ttfb_data = loki.wait_for_log(
        logql_query=(
            '{service_name="front-end"}'
            '|= "kind=measurement"'
            '|= "web-vitals"'
            '|= "ttfb"'
            f'|= "{test_run_id}"'
        ),
        timeout=30,
        expected_text=test_run_id
    )

    # Verify that the TTFB event was found
    assert ttfb_data is not None, "TTFB event not found in Loki logs"

    # Verify that the TTFB event details
    assert "kind=measurement" in ttfb_data
    assert "web-vitals" in ttfb_data
    assert "ttfb=" in ttfb_data
    assert f"{test_run_id}" in ttfb_data
    assert "request_duration=" in ttfb_data
    assert "waiting_duration=" in ttfb_data
    assert "context_navigation_type=" in ttfb_data
    assert "context_rating=" in ttfb_data
    assert "sdk_name=faro-web" in ttfb_data

