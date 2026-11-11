#!/usr/bin/env python3

# =========================================
# Purpose: Test Angular runtime errors and verify observability
#          logs capture them in Loki.
#
# Step: 1. Define Variables
#       2. Backup app.ts and app.html files
#       3. Modify app.ts and app.html to trigger runtime errors
#       X. Load the application in the browser
#       4. Click the button to trigger the runtime error
#       5. Verify the runtime error is captured in observability logs (Loki)
#       6. Restore backup files
#       7. Main function to execute the test steps
# =========================================

from pathlib import Path
from helpers.loki import LokiClient
import shutil 

# =========================================
# 1. Define Variables
# =========================================

FRONTEND_ROOT = Path(__file__).resolve().parents[4] / 'apps' / 'front-end'

APP_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.ts'

APP_BACKUP_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.ts.bak'

APP_HTML_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html'

APP_HTML_BACKUP_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html.bak'

# =========================================
# 2. Backup app.ts and app.html files
# =========================================

def backup_and_existing_files() -> None:

    """
    Backup the existing app.ts and app.html files.

    Returns:
        None
    """

    # Backup app.ts
    assert APP_PATH.is_file(), f"Missing file {APP_PATH}"
    shutil.copy2(APP_PATH, APP_BACKUP_PATH)

    # Backup app.html
    assert APP_HTML_PATH.is_file(), f"Missing file {APP_HTML_PATH}"
    shutil.copy2(APP_HTML_PATH, APP_HTML_BACKUP_PATH)

# =========================================
# 3. Modify app.ts and app.html to trigger runtime errors
# =========================================

def modify_files_to_trigger_runtime_errors() -> None:

    """
    Modify the app.ts and app.html files to trigger Angular runtime errors.

    Returns:
        None
    """

    # Define the content for app.ts that will trigger a runtime error
    app_ts_content = """
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('front-end');

  triggerRuntimeError(): void {
       throw new Error('OBS-TEST-004: Angular runtime error test');
    }
}
"""

    # Define the content for app.html that will trigger a runtime error
    app_html_content = """
<router-outlet></router-outlet>
<button id="trigger-error-btn" (click)="triggerRuntimeError()">Test Angular runtime error</button>
""" 
  
    # Modify app.ts to trigger runtime error
    APP_PATH.write_text(
            app_ts_content.strip() + "\n",
            encoding="utf-8"
        )

    # Modify app.html to trigger runtime error
    APP_HTML_PATH.write_text(
            app_html_content.strip() + "\n",
            encoding="utf-8"
        )

# =========================================
# 4. Click the button to trigger the runtime error
# =========================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_trigger_error_button(browser) -> None:

    """
    Click the button with ID "trigger-error-btn" to trigger the Angular runtime error.

    Returns:
        None
    """

    wait = WebDriverWait(browser, 15)
    trigger_error_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "trigger-error-btn"))
    )
    trigger_error_btn.click()

# =========================================
# 5. Verify that the runtime error is captured in the observability logs (Loki)
# =========================================

def verify_runtime_error_in_observability_logs() -> None:

    """
    Verify that the Angular runtime error is captured in the observability logs (Loki).

    Returns:
        None
    """

    loki = LokiClient()

    # Wait for the runtime error log to appear in Loki
    runtime_error_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}' 
            '|= "OBS-TEST-004"'
        ),
        expected_text="OBS-TEST-004",
        timeout=30
    )  

    # Assert that the runtime error log contains the expected details
    assert runtime_error_log is not None, "Runtime error log not found"

    # Verify that the runtime error log contains the expected details
    assert "kind=exception" in runtime_error_log
    assert "type=Error" in runtime_error_log
    assert "value=" in runtime_error_log
    assert 'value="console.error: ERROR Error: OBS-TEST-004: Angular runtime error test"' in runtime_error_log
    assert "stacktrace=" in runtime_error_log
    assert "sdk_name=faro-web" in runtime_error_log

# =========================================
# 6. Restore backup files
# =========================================

def restore_backup_files() -> None:

    """
    Restore the backup files for app.ts and app.html if they exist.

    Returns:
        None
    """ 

    # Restore app.ts
    assert APP_BACKUP_PATH.is_file(), f"Missing backup file {APP_BACKUP_PATH}"
    shutil.move(APP_BACKUP_PATH, APP_PATH)

    # Restore app.html
    assert APP_HTML_BACKUP_PATH.is_file(), f"Missing backup file {APP_HTML_BACKUP_PATH}"
    shutil.move(APP_HTML_BACKUP_PATH, APP_HTML_PATH)

# =========================================
# 7. Main
# =========================================

def test_angular_runtime_errors(browser) -> None:

    """
    Test to verify that Angular runtime errors are captured in the observability logs.
    
    Args:
        browser: The Selenium WebDriver instance used to interact with the application.

    Returns:
        None
    """
    
    try:
        # Backup existing application files
        backup_and_existing_files()

        # Modify the application files to trigger runtime errors
        modify_files_to_trigger_runtime_errors()

        # Load the application in the browser
        browser.get("http://localhost:4200")

        # Click the button to trigger the runtime error
        click_trigger_error_button(browser)

        # Verify that the runtime error is captured in the observability logs
        verify_runtime_error_in_observability_logs()

    finally:
        # Restore backup files to their original state
        restore_backup_files()