#!/usr/bin/env python3

# =======================================
# Purpose: Test custom performance measurement in the front-end application using Faro
#          and verifying the custom performance log in the Loki.
#
# Steps: 1. Define variables
#        2. Backup app.ts & app.html
#        3. Update app.html
#        4. Update app.ts
#        5. Run the application in the browser
#        6. Click the data processing button to trigger measurement
#        7. Verify the custom performance log in the console
#        8. Restore the original app.ts & app.html files after testing
#        9. Main
#
# =======================================

# =============================================
# 1. Define Variables
# =============================================

from pathlib import Path
import shutil
from helpers.loki import LokiClient

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

# =============================================
# 2. Backup app.ts & app.html
# =============================================

def backup_app_files() -> None:

    """
    Backup the app.ts and app.html files by copying them to their respective .bak files.
    
    Returns:
        None
    """

    shutil.copy2(APP_HTML_PATH, APP_HTML_BAK_PATH)
    shutil.copy2(APP_PATH, APP_BAK_PATH)

# =============================================
# 3. Update app.html
# =============================================

def update_app_html() -> None:
    """
    Update the app.html file with custom performance measurement code.
    
    Returns:
        None
    """

    # Define the content to be added to app.html
    app_html_content = """
<h3>Faro Custom Performance Measurement Test</h3>

<button id="data-processing-button" (click)="measureDataProcessing()">
    Measure Data Processing
</button>

<router-outlet></router-outlet>
"""

    # Write the content to app.html
    APP_HTML_PATH.write_text(
        app_html_content.strip() + "\n",
        encoding='utf-8'
    )

# =============================================
# 4. Update app.ts
# =============================================

def update_app_ts() -> None:
    """
    Update the app.ts file with custom performance measurement code.
    
    Returns:
        None
    """

    # Define the content to be added to app.ts
    app_ts_content = """
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { faro } from '@grafana/faro-web-sdk';

@Component({
selector: 'app-root',
imports: [RouterOutlet],
templateUrl: './app.html',
styleUrl: './app.scss'
})
export class App {
protected readonly title = signal('front-end');

measureDataProcessing(): void {

    // Mark the start of data processing
    performance.mark('data-processing-start');

    // Simulate application-specific data processing
    let result = 0;

    // Perform a computationally intensive task to simulate data processing
    for (let i = 0; i < 10000000; i++) {
    result += Math.sqrt(i);
    }

    // Mark the end of data processing
    performance.mark('data-processing-end');

    // Measure the duration of data processing
    const measurement = performance.measure(
        'data-processing',
        'data-processing-start',
        'data-processing-end',
    );

    // Push the measurement to Faro
    faro.api.pushMeasurement({
    type: 'custom',
    values: {
        'data-processing-duration-ms': measurement.duration
      }
    });

    console.log('Custom performance measurement:', {
        name: measurement.name,
        duration: measurement.duration,
        result,
    });

  }
}
"""

    # Write the updated content back to app.ts
    APP_PATH.write_text(
        app_ts_content.strip() + "\n",
        encoding="utf-8"
    )

# =============================================
# 6. Click button to trigger data processing
# =============================================

def click_data_processing_button(browser) -> None:

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
    data_processing_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "data-processing-button"))
    )
    data_processing_button.click()

# =============================================
# 7. Verify logs in Loki
# =============================================

def verify_logs_in_loki() -> None:

    # Initialize Loki client
    loki = LokiClient()

    # Query Loki for logs related to the custom performance measurement
    custom_perf_log = loki.wait_for_log(
        logql_query=(
            '{service_name=~".+"}'
            '|= "kind=measurement"'
            '|= "type=custom"'

        ),
        timeout=30,
        expected_text='data-processing'
    )

    # Verify log exists
    assert custom_perf_log is not None, "Custom performance log not found in Loki"

    # Verify the log contains the expected detials
    assert "kind=measurement" in custom_perf_log
    assert "type=custom" in custom_perf_log
    assert "data-processing-duration-ms=" in custom_perf_log
    assert "value_data-processing-duration-ms=" in custom_perf_log
    assert "sdk_name=faro-web" in custom_perf_log

# =============================================
# 8. Restore app.ts & app.html
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
# 9. Main
# =============================================

def test_custom_performance_measurement(browser) -> None:
    try:
        # Step 2: Backup app.ts & app.html
        backup_app_files()
        # Step 3: Update app.html
        update_app_html()
        # Step 4: Update app.ts with the test run ID
        update_app_ts()
        # Step 5. Run the application in the browser  
        browser.get("http://localhost:4200")
        # Step 6. Click button to trigger data processing
        click_data_processing_button(browser)
        # Step 7. Verify logs in Loki
        verify_logs_in_loki()
    finally:
        # Step 8. Restore files
        restore_files()
