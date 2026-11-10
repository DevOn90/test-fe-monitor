#!/usr/bin/env python3

# =================================================
# Purpose: This script should test integration of custom application
#          logs in the development environment with Grafana stack. 
#          All logs should be captured and sent to Grafana Loki
#          see (step 6. Verify logs in Loki).
#
# Prerequisites:
#      - Grafana stack should be running (Loki, Grafana, Tempo)
#      - Angular application should be running
# Steps:
#      1. Define Variables
#      2. Create Logging Service
#      3. Update App File
#      4. Update App HTML File
#      5. Click logging buttons
#      6. Verify logs in Loki
#      7. Reset files
#      8. Main
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

# ========================================
# 2. Create Logging Service
# ========================================

def create_logging_service() -> None:

    """
    Create logging.service.ts file with LoggingService implementation.
    
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
    Update app.ts to include logging service and test logging methods.
    """

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
    this.loggingService.error("Payment processing failed", {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_001',
      httpStatus: 500,
      retryAttempt: 2,
      paymentSuccessful: false,
    });
  }

  testWarnLogging(): void {
    this.loggingService.warn("Payment processing warning", {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_002',
      httpStatus: 503,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }

  testInfoLogging(): void {
    this.loggingService.info("Payment processing info", {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_003',
      httpStatus: 200,
      retryAttempt: 2,
      paymentSuccessful: true,
    });
  }

  testTraceLogging(): void {
    this.loggingService.trace("Payment processing trace", {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_004',
      httpStatus: 100,
      retryAttempt: 1,
      paymentSuccessful: true,
    });
  }
  testLogLogging(): void {
    this.loggingService.log("Payment processing log", {
      feature: 'checkout',
      operation: 'payment',
      errorCode: 'PAYMENT_005',
      httpStatus: 200,
      retryAttempt: 1,
      paymentSuccessful: true,
    });
  }

  testDebugLogging(): void {
    this.loggingService.debug("Payment processing debug", {
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
# 5. Click logging buttons
# ========================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_logging_buttons(browser) -> None:

    """
    Click all the logging buttons in the application.

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
# 6. Verify logs in Loki
# ========================================
from helpers.loki import LokiClient

def verify_logs_in_loki() -> None:

    """
    Verify that the expected logs are present in Loki for each log level.

    Log levels:
    - error
    - warn
    - info
    - debug
    - trace
    - log
    """

    loki = LokiClient()

    # Store the logs retrieved from Loki for each log level
    log_error = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing failed" |= "level=error"',
        expected_text="Payment processing",
        timeout=30,  # Wait for up to 30 seconds for the log to appear
    )

    log_warn = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing warning" |= "level=warn"',
        expected_text="Payment processing",
        timeout=30,
    )

    log_info = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing info" |= "level=info"',
        expected_text="Payment processing",
        timeout=30,
    )

    log_debug = loki.wait_for_log(
    logql_query='{service_name=~".+"} |= "Payment processing debug" |= "level=debug"',
    expected_text="Payment processing debug",
    timeout=30,
)

    log_trace = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing trace" |= "level=trace"',
        expected_text="Payment processing trace",
        timeout=30,
    )

    log_log = loki.wait_for_log(
        logql_query='{service_name=~".+"} |= "Payment processing log" |= "level=log"',
        expected_text="Payment processing log",
        timeout=30,
    )

    # Verify that all expected logs were found
    assert log_error is not None, "Error log not found"
    assert log_warn is not None, "Warn log not found"
    assert log_info is not None, "Info log not found"
    assert log_debug is not None, "Debug log not found"
    assert log_trace is not None, "Trace log not found"
    assert log_log is not None, "LOG level not found"

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

    # Verify Debug log contains the expected text
    assert "kind=log" in log_debug
    assert "context_feature=checkout" in log_debug
    assert "context_operation=payment" in log_debug
    assert "context_errorCode=PAYMENT_006" in log_debug
    assert "context_httpStatus=200" in log_debug
    assert "context_retryAttempt=1" in log_debug    
    assert "context_paymentSuccessful=true" in log_debug
    assert "sdk_name=faro-web" in log_debug

    # Verify Trace log contains the expected text
    assert "kind=log" in log_trace
    assert "context_feature=checkout" in log_trace
    assert "context_operation=payment" in log_trace
    assert "context_errorCode=PAYMENT_004" in log_trace
    assert "context_httpStatus=100" in log_trace
    assert "context_retryAttempt=1" in log_trace    
    assert "context_paymentSuccessful=true" in log_trace
    assert "sdk_name=faro-web" in log_trace

    # Verify LOG log contains the expected text
    assert "kind=log" in log_log
    assert "context_feature=checkout" in log_log
    assert "context_operation=payment" in log_log
    assert "context_errorCode=PAYMENT_005" in log_log
    assert "context_httpStatus=200" in log_log
    assert "context_retryAttempt=1" in log_log    
    assert "context_paymentSuccessful=true" in log_log
    assert "sdk_name=faro-web" in log_log

# ========================================
# 7. Reset files
# ========================================

def reset_files() -> None:

    """
    Reset modified files to their original state and 
    wait for the Angular application to reload

    Modified files:
    - logging.service.ts
    - app.ts
    - app.html
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

   
    # Wait for Angular application to reload
    import requests
    import time

    print("Waiting for Angular application to become available")

    for _ in range(30):
        try:
            response = requests.get(
                "http://localhost:4200",
                timeout=2
            )
            if response.status_code == 200:
                print("Angular application is available")
                return
        
        except requests.RequestException:
            print("Angular application not available yet") # pass

        time.sleep(1)

    raise RuntimeError("Angular application did not become available within the expected time")

# ========================================
# 8. Main
# ========================================

def test_custom_application_logs(browser) -> None:

    """
    Test custom application logs by interacting with the Angular application
    and verifying the logs in Loki.
    """

    try:
        # Create the logging service
        create_logging_service()

        # Update the app TypeScript file
        update_app_file()

        # Update the app HTML file
        update_app_html_file()

        # Navigate to the application
        browser.get("http://localhost:4200")

        # Click logging buttons
        click_logging_buttons(browser)

        # Verify logs in Loki
        verify_logs_in_loki()

    finally:
        # Always restore the original files
        reset_files()

        