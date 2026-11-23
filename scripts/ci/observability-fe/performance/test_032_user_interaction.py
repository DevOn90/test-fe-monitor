#!/usr/bin/env python3

# =============================================
# Purpose: Test user interaction with the front-end application
#          and verify logs in Loki.
# 
# Steps: For both tests
#        1. Define Variables
#        2. Backup app.ts & app.html
#        3 & 8. Update app.html
#        4 & 9. Update app.ts
#        5. Open the application in the browser
#        6. Click the "Load Dashboard" button
#        7. Verify logs in Loki
#        10. Verify Faro API user start action
#        11. Restore app.ts & app.html from backup
#        12. Main
#
# =============================================

# =============================================
# 1. Define Variables
# =============================================

from pathlib import Path
import shutil
from helpers.loki import LokiClient
import uuid

FRONTEND_ROOT = Path(__file__).resolve().parents[4] / 'apps' / 'front-end'

APP_HTML_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html'
APP_HTML_BAK_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html.bak'
APP_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.ts'
APP_BAK_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.ts.bak'

# Create unique identifiers for this test runs
test_run_id_html_attr = f"OBS-TEST-032-html-attr-{uuid.uuid4().hex}"
test_run_id_faro_api =  f"OBS-TEST-032-faro-api-{uuid.uuid4().hex}"

# =============================================
# 2. Backup app.ts & app.html
# =============================================

def backup_app_files() -> None:
    """
    Backup the app.ts and app.html files.

    Returns:
        None
    """

    shutil.copy2(APP_HTML_PATH, APP_HTML_BAK_PATH)
    shutil.copy2(APP_PATH, APP_BAK_PATH)

# =============================================
# 3. Update app.html (html.attr)
# =============================================

def update_app_html_html_attr() -> None:
    """
    Update the app.html file for the Faro HTML attribute test with content
    and unique test run ID.

    Returns:
        None
    """

    # Define the content of the app.html file.
    app_html_content = """
<h3>Faro HTML User Action Test</h3>

<button
id="load-dashboard-button"
data-faro-user-action-name="test-load-dashboard-__TEST_RUN_ID__"
(click)="loadDashboard()"
[disabled]="loading"
>
{{ loading ? 'Loading...' : 'Load Dashboard' }}
</button>

@if (results.length > 0) {
<h4>Results</h4>
<ul>
    @for (result of results; track result) {
    <li>{{ result }}</li>
    }
</ul>
}

<router-outlet></router-outlet>
"""
    # Replace placeholder with the actual test run ID in the app.html content
    app_html_content = app_html_content.replace(
        "__TEST_RUN_ID__",
        test_run_id_html_attr
    )
    
    # Write the updated app.html content to the file
    APP_HTML_PATH.write_text(
        app_html_content.strip() + "\n",
        encoding="utf-8"
        )

# =============================================
# 4. Update app.ts (html.attr)
# =============================================

def update_app_ts_html_attr() -> None:
    """
    Update the app.ts file for the Faro HTML attribute test with the correct content.

    Returns:
        None
    """

    # Define the content of the app.ts file.
    app_ts_content = """
import { Component, signal, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { forkJoin } from 'rxjs';

@Component({
selector: 'app-root',
imports: [RouterOutlet],
templateUrl: './app.html',
styleUrl: './app.scss'
})
export class App {
protected readonly title = signal('front-end');

private readonly http = inject(HttpClient);

loading = false;
results: string[] = [];

loadDashboard(): void {
    this.loading = true;
    this.results = [];

    forkJoin({
    request1: this.http.get('https://httpbin.org/delay/1'),
    request2: this.http.get('https://httpbin.org/delay/2'),
    request3: this.http.get('https://httpbin.org/delay/3')
    }).subscribe({
    next: () => {
        this.results = [
        'Request 1 completed',
        'Request 2 completed',
        'Request 3 completed'
        ];
        this.loading = false;
    },
    error: (error) => {
        console.error('HTTP request failed', error);
        this.loading = false;
    }
    });
}
}
"""

    # Write the updated app.ts content to the file
    APP_PATH.write_text(
        app_ts_content.strip() + "\n",
        encoding="utf-8"
        )

# =============================================
# 6. Click the "Load Dashboard" button
# =============================================

def click_load_dashboard_button_html_attr(browser) -> None:

    """
    Click the "Load Dashboard" button in the browser.

    Args:
        browser: The Selenium WebDriver instance.

    Returns:
        None
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Wait for the "Load Dashboard" button to be clickable and then click it
    load_dashboard_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "load-dashboard-button"))
    )
    load_dashboard_button.click()

# =============================================
# 7. Verify logs in Loki
# =============================================

def verify_logs_in_loki_html_attr() -> None:

    """
    Verify that the expected logs are present in Loki for the current test run.

    Returns:
        None
    """
   
    # Initialize the Loki client to query logs
    loki = LokiClient();

    # Get the log entry for the current test run from Loki
    html_attr_log =loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "faro.user.action"'
            f'|= "{test_run_id_html_attr}"'
        ),
        timeout=30,
        expected_text=test_run_id_html_attr
    )

    # Verify that the log exists
    assert html_attr_log is not None, "Log not found in Loki"

    # Verify that the log contains the expected details
    assert "kind=event" in html_attr_log
    assert "event_name=faro.user.action" in html_attr_log
    assert f"event_data_userActionName=test-load-dashboard-{test_run_id_html_attr}" in html_attr_log
    assert "event_data_userActionDuration=" in html_attr_log
    assert "event_data_userActionStartTime=" in html_attr_log
    assert "event_data_userActionTrigger=pointerdown" in html_attr_log
    assert "sdk_name=faro-web" in html_attr_log

# =============================================
# 8. Update app.html (faro.api)
# =============================================

def update_app_html_faro_api() -> None:

    """
    Update the app.html file for the Faro API test with the correct content.

    Returns:
        None
    """

    # Define the content of the app.html file for the Faro API test
    app_html_content = """
<h3>Faro Programmatic User Action Test</h3>

 <button
 id="load-dashboard-button"
 (click)="loadDashboard()"
 [disabled]="loading"
 >
 {{ loading ? 'Loading...' : 'Load Dashboard' }}
 </button>

 @if (results.length > 0) {
 <h4>Results</h4>
 <ul>
     @for (result of results; track result) {
     <li>{{ result }}</li>
     }
 </ul>
 }
 <router-outlet></router-outlet>
"""

    # Write the updated app.html content to the file
    APP_HTML_PATH.write_text(
        app_html_content.strip() + "\n",
        encoding=("utf-8")
    )

# =============================================
# 9. Update app.ts (faro.api)
# =============================================

def update_app_ts_faro_api() -> None:

    """
    Update the app.ts file for the Faro API test with content and
    unique test run ID.

    Returns:
        None
    """

    # Define the content of the app.ts file 
    app_ts_content = """
 import { Component, signal, inject } from '@angular/core';
 import { RouterOutlet } from '@angular/router';
 import { HttpClient } from '@angular/common/http';
 import { forkJoin } from 'rxjs';
 import { faro } from '@grafana/faro-web-sdk';

 @Component({
 selector: 'app-root',
 imports: [RouterOutlet],
 templateUrl: './app.html',
 styleUrl: './app.scss'
 })
 export class App {
 protected readonly title = signal('front-end');

 private readonly http = inject(HttpClient);

 loading = false;
 results: string[] = [];

 loadDashboard(): void {
     this.loading = true;
     this.results = [];

     faro.api.startUserAction('test-load-dashboard', {
     test_type: 'programmatic',
     test_run_id: "__TEST_RUN_ID__",
     });

     forkJoin({
     request1: this.http.get('https://httpbin.org/delay/1'),
     request2: this.http.get('https://httpbin.org/delay/2'),
     request3: this.http.get('https://httpbin.org/delay/3'),
     }).subscribe({
     next: () => {
         this.results = [
         'Request 1 completed',
         'Request 2 completed',
         'Request 3 completed',
         ];
         this.loading = false;
     },
     error: (error) => {
         console.error('HTTP request failed', error);
         this.loading = false;
     },
     });
 }
 }
"""

    # Replace the placeholder test run ID with the actual test run ID
    # in the app.ts content
    app_ts_content = app_ts_content.replace(
        "__TEST_RUN_ID__",
        test_run_id_faro_api
    )

    # Write the updated app.ts content to the file
    APP_PATH.write_text(
        app_ts_content.strip() + "\n",
        encoding=("utf-8")
    )

# =============================================
# 10. Verify Faro API user start action
# =============================================

def verify_faro_api_user_start_action() -> None:
    """
    Verify that the Faro API correctly logs a user start action.

    Returns:
        None
    """

    # Initialize the Loki client to query logs
    loki = LokiClient();

    # Get the Faro API log for the specified test run ID
    faro_api_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "programmatic"'
            f'|= "{test_run_id_faro_api}"'
        ),
        timeout=30,
        expected_text=test_run_id_faro_api
    )

    # Verify that the log exists
    assert faro_api_log is not None, "Faro API log not found"

    # Verify that the log contains the expected details
    assert "kind=event" in faro_api_log
    assert f"event_data_test_run_id={test_run_id_faro_api}" in faro_api_log
    assert "event_name=faro.user.action" in faro_api_log
    assert "event_data_test_type=programmatic" in faro_api_log
    assert "event_data_userActionDuration=" in faro_api_log
    assert "event_data_userActionTrigger=faroApiCall" in faro_api_log
    assert "sdk_name=faro-web" in faro_api_log
 
# =============================================
# 11. Restore files
# =============================================

def restore_files() -> None:
    """
    Restore the original app.ts and app.html files from their backups.

    Returns:
        None
    """

    shutil.move(APP_HTML_BAK_PATH, APP_HTML_PATH)
    shutil.move(APP_BAK_PATH, APP_PATH)

# =============================================
# 12. Main
# =============================================

def test_user_interaction_html_attribute(browser) -> None:

    """
    Test user interaction with HTML attribute.
    This test verifies that user interactions with HTML attributes triggers faro user actions.
    
    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """

    try:
        # Step 2: Backup app.ts & app.html
        backup_app_files()
        # Step 3: Update app.html
        update_app_html_html_attr()
        # Step 4: Update app.ts
        update_app_ts_html_attr()
        # Step 5: Open the application in the browser
        browser.get("http://localhost:4200")
        # Step 6: Click the "Load Dashboard" button
        click_load_dashboard_button_html_attr(browser)
        # Step 7. Verify logs in Loki
        verify_logs_in_loki_html_attr()

    finally:

        # Step 11: Restore original files
        restore_files()

def test_faro_api_user_start_action(browser) -> None:

    """
    Test Faro API user start action.
    This test verifies that the Faro API correctly logs a user start action when interacting with the application.
    
    Arguments:
        browser: The Selenium WebDriver instance used to interact with the front-end application.

    Returns:
        None
    """

    try:
        # Step 2: Backup app.ts & app.html
        backup_app_files()
        # Step 8. Update app.html
        update_app_html_faro_api()
        # Step 9. Update app.ts     
        update_app_ts_faro_api()
        # Step 5: Open the application in the browser
        browser.get("http://localhost:4200")
        # Step 6: Click the "Load Dashboard" button
        click_load_dashboard_button_html_attr(browser)
        # Step 10: Verify Faro API user start action
        verify_faro_api_user_start_action()
    finally:
        # Step 11: Restore original files
        restore_files()