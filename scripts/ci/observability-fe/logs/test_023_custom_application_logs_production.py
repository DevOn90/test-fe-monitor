#!/usr/bin/env python3

# =================================================
# Purpose: This script should test integration of custom application 
#          logs in the production environment with Grafana stack.
#          Only production environment logs should be captured 
#          see (step X. Verify logs in Loki).
#
# Prerequisites:
#      - Grafana stack should be running (Loki, Grafana, Tempo)
#
# Steps:
#      1. Define Variables
#      2. Create Logging Service
#      3. Update App File
#      4. Update App HTML File
#      5. Backup angular.json
#      6. Create environment files
#      7. Add environments to angular.json
#      8. Start Angular Production Server
#      9. Wait for Angular Production Server to be Ready
#      10. Click logging buttons
#      11. Verify logs in Loki
#      12. Stop Angular production server
#      13. Reset files
#      14. Restore angular.json
#      15. Main
# =================================================

from datetime import time
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

ANGULAR_JSON_PATH = FRONTEND_ROOT / 'angular.json'
ANGULAR_JSON_BACKUP_PATH = FRONTEND_ROOT / 'angular.json.bak'

ENV_FOLDER_PATH = FRONTEND_ROOT / 'src' / 'environments'
DEV_ENV_FILE_PATH = FRONTEND_ROOT / 'src' / 'environments' / 'environment.ts'
PROD_ENV_FILE_PATH = FRONTEND_ROOT / 'src' / 'environments' / 'environment.prod.ts'

# ========================================
# 2. Create Logging Service
# ========================================

def create_logging_service() -> None:

    """
    Create logging.service.ts file with LoggingService implementation.
    Import `environment` config and use it to determine if a log level is enabled.
    
    Add logging for levels:
    - DEBUG
    - INFO
    - WARN
    - ERROR
    - TRACE
    - LOG
    """

    LOGGING_SERVICE_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging_service_code = """
import { Injectable } from '@angular/core';
import { faro, LogLevel } from '@grafana/faro-web-sdk';
import { environment } from '../../../environments/environment';

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

  trace(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.TRACE, context);
  }

  log(message: string, context?: LogContextInput): void {
    this.write(message, LogLevel.LOG, context);
  }

  private write(
    message: string,
    level: LogLevel,
    context?: LogContextInput
  ): void {
    const levelEnabled = environment.logging[
      level.toLowerCase() as keyof typeof environment.logging
    ];

    if (!levelEnabled) {
      return;
    }

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

def update_app_file() -> None:

    """
    - Update app.ts to include logging service 
    - Add test logging methods for all log levels (`error`, `warn`, `info`, `trace`, `log`, `debug`).
    - Add `logMode` property to determine the current environment (`production` or `development`)
    """

    app_ts_code = """
import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LoggingService } from './core/services/logging.service';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('front-end');

  private readonly logMode = environment.production ? 'production' : 'development';

  constructor (private readonly loggingService: LoggingService) { }

  testErrorLogging(): void {
    this.loggingService.error(`Payment processing failed ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_001',
      httpStatus: 500,
      retryAttempt: 2,
      paymentSuccessful: false,
    });
  }

  testWarnLogging(): void {
    this.loggingService.warn(`Payment processing warning ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_002',
      httpStatus: 503,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }

  testInfoLogging(): void {
    this.loggingService.info(`Payment processing info ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_003',
      httpStatus: 200,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }

  testTraceLogging(): void {
    this.loggingService.trace(`Payment processing trace ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_004',
      httpStatus: 100,
      retryAttempt: 1,
      paymentSuccessful: true,
    });
  }
  testLogLogging(): void {
    this.loggingService.log(`Payment processing log ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_005',
      httpStatus: 200,
      retryAttempt: 1,
      paymentSuccessful: true,
    });
  }

  testDebugLogging(): void {
    this.loggingService.debug(`Payment processing debug ${this.logMode}`, {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_006',
      httpStatus: 200,
      retryAttempt: 1,
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

def update_app_html_file() -> None:

    """
    Update the application's HTML file with logging buttons.
        Keep router outlet intact.
        
        Add buttons:
        - Test Error Logging
        - Test Warn Logging
        - Test Info Logging
        - Test Debug Logging
        - Test Trace Logging
        - Test Log Logging
    """

    app_html_code = """
<router-outlet></router-outlet>
<button id="test-error-logging" (click)="testErrorLogging()">Test Error Logging</button>
<button id="test-warn-logging" (click)="testWarnLogging()">Test Warn Logging</button>
<button id="test-info-logging" (click)="testInfoLogging()">Test Info Logging</button>
<button id="test-debug-logging" (click)="testDebugLogging()">Test Debug Logging</button>
<button id="test-trace-logging" (click)="testTraceLogging()">Test Trace Logging</button>
<button id="test-log-logging" (click)="testLogLogging()">Test Log Logging</button>
"""

    APP_HTML_PATH.write_text(
        app_html_code.strip() + "\n",
        encoding='utf-8'
    )

# ========================================
# 5. Backup angular.json
# ========================================

def backup_angular_json() -> None:
    
    """
    Backup the `angular.json` file to a backup location.

    Path:
    - `./angular.json` to
    - `./angular.json.bak`    
    """
    
    import shutil
    shutil.copy2(ANGULAR_JSON_PATH, ANGULAR_JSON_BACKUP_PATH)

# ========================================
# 6. Create environment files
# ========================================

def create_environment_files() -> None:

    """
    Create environment files for development and production with 
    logging configuration.

    Path:
    - `src/environments/environment.ts`
    - `src/environments/environment.prod.ts`
    """

    DEV_ENV_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROD_ENV_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    dev_env_file_code = """
export const environment = {
    production: false,

    logging: {
        console: true,
        debug: true,
        info: true,
        warn: true,
        error: true,
        trace: true,
        log: true
    }
}
"""

    prod_env_file_code = """
export const environment = {
    production: true,

    logging: {
        console: true,
        debug: false,
        info: true,
        warn: true,
        error: true,
        trace: false,
        log: false

    }
}
"""
    DEV_ENV_FILE_PATH.write_text(
        dev_env_file_code.strip() + "\n",
        encoding='utf-8'
    )

    PROD_ENV_FILE_PATH.write_text(
        prod_env_file_code.strip() + "\n",
        encoding='utf-8'
    )

# ========================================
# 7. Add environments to angular.json
# ========================================

def add_environments_to_angular_json() -> None:

    """
    Add environment file replacements to the Angular build configuration `angular.json`.
    """ 
    
    import json

    with open(ANGULAR_JSON_PATH, 'r', encoding='utf-8') as f:
        angular_json = json.load(f)

    # Locate the frontend production build configuration
    build_config = (
        angular_json['projects']['front-end']
        ['architect']['build']['configurations']['production']
    )

    # Add environment file replacement
    build_config['fileReplacements'] = [
        {
            "replace": "src/environments/environment.ts",
            "with": "src/environments/environment.prod.ts"
        }
    ]

    # Write the updated angular.json back to the file
    with open(ANGULAR_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(angular_json, f, indent=2)
        f.write("\n")

# ========================================
# 8. Start Angular Production Server
# ========================================

def start_angular_prod_server() -> None:

    """
    - Start Angular production server in port `4201`.
    - Write the PID of the started process to a file `/tmp/angular-prod.pid`
    - Write Angular server output to a log file `/tmp/angular-prod.log`.
    """
    
    import subprocess
    import os

    pid_file_path = "/tmp/angular-prod.pid"
    log_file_path = "/tmp/angular-prod.log"

    if not os.path.exists(pid_file_path):

        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            process = subprocess.Popen(
                [
                    "npx",
                    "ng",
                    "serve",
                    "--configuration",
                    "production",
                    "--host",
                    "127.0.0.1",
                    "--port",
                    "4201"
                ],
                cwd=FRONTEND_ROOT,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                start_new_session=True
            )            

        with open(pid_file_path, 'w', encoding='utf-8') as pid_file:
            pid_file.write(str(process.pid))

# ========================================
# 9. Wait for Angular Production Server to be Ready
# ========================================

import time

def wait_for_angular_prod_server(timeout=120) -> None:

    """
    Wait for Anglar production server to be ready on port 4201
    started with step 8.
    """
 
    import requests

    url = "http://127.0.0.1:4201"
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)

            if response.status_code == 200:
                print(f"[DEBUG] Angular production server is ready on port 4201 (HTTP {response.status_code}).")
                return

        except requests.RequestException:
            pass

        time.sleep(2)

    raise TimeoutError("Angular server did not become ready.")

# ========================================
# 10. Click logging buttons
# ========================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_logging_buttons(browser) -> None:

    """
    Click all the logging buttons on the Angular application page.

    The buttons clicked are:
        - Test Error Logging
        - Test Warn Logging
        - Test Info Logging
        - Test Debug Logging
        - Test Trace Logging
        - Test Log Logging
    """
    
    wait = WebDriverWait(browser, 30)

    # Click the "Test Error Logging" button
    error_button = wait.until(EC.element_to_be_clickable((By.ID, "test-error-logging")))
    error_button.click()

    # Click the "Test Warn Logging" button
    warn_button = wait.until(EC.element_to_be_clickable((By.ID, "test-warn-logging")))
    warn_button.click()

    # Click the "Test Info Logging" button
    info_button = wait.until(EC.element_to_be_clickable((By.ID, "test-info-logging")))
    info_button.click()

    # Click the "Test Debug Logging" button
    debug_button = wait.until(EC.element_to_be_clickable((By.ID, "test-debug-logging")))
    debug_button.click()

    # Click the "Test Trace Logging" button
    trace_button = wait.until(EC.element_to_be_clickable((By.ID, "test-trace-logging")))
    trace_button.click()

    # Click the "Test logging" button
    test_logging_button = wait.until(EC.element_to_be_clickable((By.ID, "test-log-logging")))
    test_logging_button.click()

# ========================================
# 11. Verify logs in Loki
# ========================================
from helpers.loki import LokiClient

def verify_logs_in_loki() -> None:

    """
    Verify that the only expected logs are present in Loki for each log level.
    
    Expected logs:
    - ERROR
    - WARN
    - INFO

    Not expected logs:
    - DEBUG
    - TRACE
    - LOG
    """

    loki = LokiClient()

    # Store the logs retrieved from Loki for each log level
    log_error = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing failed production" |= "level=error"',
        expected_text="Payment processing",
        timeout=30,  # Wait for up to 30 seconds for the log to appear
    )

    log_warn = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing warning production" |= "level=warn"',
        expected_text="Payment processing",
        timeout=30,
    )

    log_info = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing info production" |= "level=info"',
        expected_text="Payment processing",
        timeout=30,
    )

    log_debug = loki.query_logs(
        logql_query='{service_name=~".+"} |= "Payment processing debug production" |= "level=debug"',
    )

    log_trace = loki.query_logs(
        logql_query='{service_name=~".+"} |= "Payment processing trace production" |= "level=trace"',
    )

    log_log = loki.query_logs(
        logql_query='{service_name=~".+"} |= "Payment processing log production" |= "level=log"',
    )

    # Verify that all expected logs were found
    assert log_error is not None, "Error log not found"
    assert log_warn is not None, "Warn log not found"
    assert log_info is not None, "Info log not found"
    assert log_debug == [], "Debug log should not be found"
    assert log_trace == [], "Trace log should not be found"
    assert log_log == [], "Log log should not be found"

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
# 12. Stop Angular production server
# ========================================

import os
import signal

def stop_angular_prod_server() -> None:
    
    """
    Stop the Angular production server using the PID file 
    created by start_angular_prod_server() in step 8.
    """
    
    # Created by method start_angular_prod_server() step 8.
    pid_file_path = "/tmp/angular-prod.pid"

    if not os.path.exists(pid_file_path):
        print("Angular production server PID file not found.")
        return

    with open(pid_file_path, 'r', encoding='utf-8') as file:
        pid = int(file.read().strip())

    try:
        os.killpg(pid, signal.SIGTERM)

        # Wait up to 10 seconds for termination
        for _ in range(10):
            try:
                os.killpg(pid, 0)
                time.sleep(1)
            except ProcessLookupError:
                print("Angular production server stopped.")
                break
        else:
            # Force termination if the process group is still running.
            print("Production server did not stop. Sending SIGKILL.")
            os.killpg(pid, signal.SIGKILL)
    
    except ProcessLookupError:
        print(f"Angular production server with PID {pid} not found.")

    finally:
        if os.path.exists(pid_file_path):
            os.remove(pid_file_path)

# ========================================
# 13. Reset files
# ========================================

def reset_files() -> None:

    """
    Reset any modified files to their original state 
    and wait for the Angular application to reload.
    
    Modified Files:
    - logging.service.ts
    - app.ts
    - app.html
    - environment.ts
    - environment.prod.ts
    """

    # Remove the service file if it exists
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

    # Remove the development and production environment files if they exist
    if DEV_ENV_FILE_PATH.exists():
       DEV_ENV_FILE_PATH.unlink()

    if PROD_ENV_FILE_PATH.exists():
       PROD_ENV_FILE_PATH.unlink()

    

    # Wait for Angular application to reload
    import requests
    import time

    for _ in range(30):
        try:
            response = requests.get(
                "http://localhost:4200",
                timeout=2
            )
            if response.status_code == 200:
                return
        
        except requests.RequestException:
            print("Angular application not available yet") # pass

        time.sleep(1)

    raise RuntimeError("Angular application did not become available within the expected time")

# ========================================
# 14. Restore angular.json
# ========================================

def restore_angular_json() -> None:
    
    """
    Restore the angular.json file from its backup if it exists.
    """
    import shutil

    if ANGULAR_JSON_BACKUP_PATH.exists():
        shutil.move(ANGULAR_JSON_BACKUP_PATH, ANGULAR_JSON_PATH)

# ========================================
# 15. Main
# ========================================

def test_custom_application_logs(browser) -> None:  # keep 'test' in function name for conftest.py @pytest.fixture
                                            # to supply the browser for selenium tests

    """
    Test custom application logs in production environment.
    This test performs the following steps:
    1. Create the logging service
    2. Update the app TypeScript file
    3. Update the app HTML file
    4. Backup angular.json
    5. Create environment files
    6. Add environment files to angular.json
    7. Start the Angular production server
    8. Wait for the Angular application to become available
    9. Click the logging buttons in the application
    10. Verify the logs in Loki
    11. Ensure the Angular production server is stopped
    12. Reset the modified files to their original state
    13. Restore angular.json
    """

    try:
        # 2. Create the logging service before updating the app files
        create_logging_service()

        # 3. Update the app TypeScript file with the necessary changes
        update_app_file()

        # 4. Update the app HTML file with the necessary changes
        update_app_html_file()

        # 5. Backup angular.json
        backup_angular_json()

        # 6. Create the environment files
        create_environment_files()

        # 7. Add environment files to angular.json
        add_environments_to_angular_json()

        # 8. Start the Angular production server
        start_angular_prod_server()

        # 9. Wait for the Angular application to become available
        wait_for_angular_prod_server()

        # Navigate to the Angular application in the browser
        browser.get("http://localhost:4201")

        # 10. Click the logging buttons in the application
        click_logging_buttons(browser)

        # 11. Verify the logs in Loki
        verify_logs_in_loki()
             
    finally:
        try: 
            # 12. Ensure the Angular production server is stopped
            stop_angular_prod_server()
        finally:
            try:
               # 13. Reset the modified files to their original state
               reset_files()
            finally:
               # 14. Restore angular.json
               restore_angular_json()
       