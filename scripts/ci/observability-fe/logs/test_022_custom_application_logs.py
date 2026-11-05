#!/usr/bin/env python3

# =================================================
# Purpose: This script should test integration of custom application logs
#          with Grafana stack.
#
# Steps:
#      1. Define Variables
#      2. Create Logging Service
#      3. Update App File
#      4. Update App HTML File
#      5. Re-start Angular application
#      6. Click buttons to trigger custom application logs
#      7. Verify logs in Loki
#      8. Reset files
#      9. Main
# =================================================

from pathlib import Path

# ========================================
# 1. Define Variables
# ========================================
FRONTEND_ROOT = Path(__file__).resolve().parents[4] / 'apps' / 'front-end'
LOGGING_SERVICE_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'core' \
    / 'services' \
    / 'logging.service.ts'
APP_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.ts'
APP_HTML_PATH = FRONTEND_ROOT \
    / 'src' \
    / 'app' \
    / 'app.html'

print(APP_HTML_PATH)

# ========================================
# 2. Create Logging Service
# ========================================

def create_logging_service():

    LOGGING_SERVICE_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging_service_code = """
import { Injectable } from '@angular/core';
import { faro, LogLevel } from '@grafana/faro-web-sdk';

export type LogContextInput = Record<
string,
string | number | boolean | null | undefined
>;

@Injectable({
providedIn: 'root',
})
export class LoggingService {

debug(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.DEBUG, context);
}

info(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.INFO, context);
}

warn(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.WARN, context);
}

error(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.ERROR, context);
}

private write(
    message: string,
    level: LogLevel,
    context?: LogContextInput
): void {
    const faroContext = context
    ? Object.fromEntries(
        Object.entries(context)
            .filter(([, value]) => value !== null && value !== undefined)
            .map(([key, value]) => [key, String(value)])
        )
    : undefined;

    faro.api.pushLog([message], {
    level,
    context: faroContext,
    });
}
}
"""

    LOGGING_SERVICE_PATH.write_text(
        logging_service_code.strip() + "\n",
        encoding='utf-8'
    )

# ========================================
# 3. Update App File
# ========================================

def update_app_file():

    app_ts_code = """
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoggingService } from './core/services/logging.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('front-end');

  constructor (private readonly loggingService: LoggingService) { }

  testErrorLogging(): void {
    this.loggingService.error('Payment processing failed', {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_001',
      httpStatus: 500,
      retryAttempt: 2,
      paymentSuccessful: false,
    });
  }

  testWarnLogging(): void {
    this.loggingService.warn('Payment processing warning', {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_002',
      httpStatus: 503,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }

  testInfoLogging(): void {
    this.loggingService.info('Payment processing info', {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_003',
      httpStatus: 200,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }
}
"""
    APP_PATH.write_text(
        app_ts_code.strip() + "\n",
        encoding='utf-8'
    )

# ========================================
# 4. Update App HTML File
# ========================================

def update_app_html_file():

    app_html_code = """
<router-outlet></router-outlet>
<button id="test-error-logging" (click)="testErrorLogging()">Test Error Logging</button>
<button id="test-warn-logging" (click)="testWarnLogging()">Test Warn Logging</button>
<button id="test-info-logging" (click)="testInfoLogging()">Test Info Logging</button>
"""

    APP_HTML_PATH.write_text(
        app_html_code.strip() + "\n",
        encoding='utf-8'
    )

update_app_html_file()

# ========================================
# 5. Re-start Angular application
# ========================================

# def restart_angular_application():

#     import os
#     import subprocess
#     import signal
#     import time
#     import requests


#     # Search process listening on port 4200 (Angular app)
#     result = subprocess.run(
#         ["lsof", "-it", "tcp:4200", "-sTCP:LISTEN"],
#         capture_output=True,
#         text=True
#     )


#     if result.returncode == 0 and result.stdout.strip():
#         # Store the PID of the Angular process
#         angular_pid = int(result.stdout.strip().splitlines()[0])

#         print("Stopping Angular process with PID:", angular_pid)
#         # Kill the Angular process to stop the running application
#         os.kill(angular_pid, signal.SIGTERM)

#     else:
#         print("No Angular process found on port 4200")

#     # Wait until port become available
#     for _ in range(30):
#         result = subprocess.run(
#             ["bash", "-c", "curl -s http://localhost:4200 > /dev/null"],
#             capture_output=True,
#         )
#         if result.returncode != 0:
#             break
        
#         time.sleep(1)

#     # Start the Angular application again
#     # Use a log file to capture the output of the Angular application, the same as
#     # ci-observability-fe.yml step 9 uses the same log file to capture Angular output
#     log_file_path = Path("/tmp/angular.log")

#     with open(log_file_path, "w") as log_file:
#         process = subprocess.Popen(
#             ["npm", "start", "--", "--host", "127.0.0.1"],
#             cwd=FRONTEND_ROOT,
#             stdout=log_file,
#             stderr=subprocess.STDOUT,
#             start_new_session=True
#         )

#     # Write the PID of the new Angular process to the PID file
#     # Use a PID file to capture the PID of the running Angular process, the same as
#     # ci-observability-fe.yml step 9 uses the same PID file to capture Angular PID
#     pid_file = Path("/tmp/angular.pid")
#     pid_file.write_text(str(process.pid))

#     # Wait for the Angular application to become available on port 4200
#     for _ in range(30):
#         try:
#             response = requests.get(
#                 "http://localhost:4200",
#                 timeout=2,
#             )
#             if response.status_code == 200:
#                 return
#         except:
#             print("Angular application not yet available on port 4200")
#         time.sleep(1)

#     raise RuntimeError("Angular application did not become available on port 4200 within the expected time")

# ========================================
# 6. Trigger custom application logs by clicking the buttons in the front-end application
# ========================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_logging_buttons(browser):

    wait = WebDriverWait(browser, 20)

    # Click the "Test Error Logging" button
    error_button = wait.until(EC.element_to_be_clickable((By.ID, "test-error-logging")))
    error_button.click()

    # Click the "Test Warn Logging" button
    warn_button = wait.until(EC.element_to_be_clickable((By.ID, "test-warn-logging")))
    warn_button.click()

    # Click the "Test Info Logging" button
    info_button = wait.until(EC.element_to_be_clickable((By.ID, "test-info-logging")))
    info_button.click()

# ========================================
# 7. Verify logs in Loki
# ========================================
from helpers.loki import LokiClient

def verify_logs_in_loki():

    loki = LokiClient()
    
    log_error = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing" |= "level=error"',
        expected_text="Payment processing",
        timeout=30,  # Wait for up to 30 seconds for the log to appear
    )

    log_warn = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing" |= "level=warn"',
        expected_text="Payment processing",
        timeout=30,
    )

    log_info = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing" |= "level=info"',
        expected_text="Payment processing",
        timeout=30,
    )

    # Verify that all expected logs were found
    assert log_error is not None, "Error log not found"
    assert log_warn is not None, "Warn log not found"
    assert log_info is not None, "Info log not found"

    # Verify Error log contains the expected text
    assert "kind=log" in log_error
    assert "context_feature=checkout" in log_error
    assert "context_operation=payment" in log_error
    assert "context_errorCode=PAYMENT_001" in log_error
    assert "context_httpStatus=500" in log_error
    assert "context_retryAttempt=2" in log_error    
    assert "context_paymentSuccessful=false" in log_error
    assert "sdk_name=faro-web" in log_error

    # Verify Warn log contains the expected text
    assert "kind=log" in log_warn
    assert "context_feature=checkout" in log_warn
    assert "context_operation=payment" in log_warn
    assert "context_errorCode=PAYMENT_002" in log_warn
    assert "context_httpStatus=503" in log_warn
    assert "context_retryAttempt=2" in log_warn    
    assert "context_paymentSuccessful=true" in log_warn
    assert "sdk_name=faro-web" in log_warn

    # Verify Info log contains the expected text
    assert "kind=log" in log_info
    assert "context_feature=checkout" in log_info
    assert "context_operation=payment" in log_info
    assert "context_errorCode=PAYMENT_003" in log_info
    assert "context_httpStatus=200" in log_info
    assert "context_retryAttempt=2" in log_info    
    assert "context_paymentSuccessful=true" in log_info
    assert "sdk_name=faro-web" in log_info

# ========================================
# 8. Reset files
# ========================================

def reset_files():

    # Reset any modified files to their original state

    # Remove the sercive file if it exists
    if LOGGING_SERVICE_PATH.exists():
        LOGGING_SERVICE_PATH.unlink()

    # Update the app file to orignal state

    original_app_ts_code = """
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

  constructor () {
    console.log("Logging Something")
    console.warn("Waring log")
    console.debug("Debug log")
    console.error("Error log")
    console.info("Info log")
  }
}
"""

    APP_PATH.write_text(
        original_app_ts_code.strip() + "\n",
        encoding="utf-8"
    )

    # Update the app HTML file to original state

    original_app_html_code = """
<router-outlet></router-outlet>
"""

    APP_HTML_PATH.write_text(
        original_app_html_code.strip() + "\n",
        encoding="utf-8"
    )


# ========================================
# 9. Main
# ========================================

def test_custom_application_logs(browser):  # keep 'test' in function name for conftest.py @pytest.fixture
                                            # to supply the browser for selenium tests
    try: 
        print("Starting script execution")
        print("Creating logging service")
        create_logging_service()

        print("Updating app file")
        update_app_file()

        print("Updating app HTML file")
        update_app_html_file()

        #print("Restarting Angular application")
        #restart_angular_application()

        # Navigate to angular application
        browser.get("http://localhost:4200")

        print("Triggering custom application logs")
        click_logging_buttons(browser)

        print("Verifying logs in Loki")
        verify_logs_in_loki()
    
    finally:
        print("Resetting files to original state")
        reset_files()

        print("Script execution completed")