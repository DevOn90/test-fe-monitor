#!/usr/bin/env python3

# ========================================
# Purpose: Test page view navigation and Angular route changes 
#          including logging of view changes & faro.navigation
#          to the observability system (Loki)
#
# Steps: 1. Define vriables
#        2. Backup routing configuration
#        3 & 10. Create home component
#        4 & 11. Create profile component
#        5. Create routing configuration
#        6. Open Angular application
#        7. Click profile button
#        8 & 12. Verify log created in loki
#        9. Restore files
#        13. Main
#
# ========================================

# ========================================
# 1. Define variables
# ========================================

from pathlib import Path
import shutil
from helpers.loki import LokiClient
import uuid

FRONTEND_PATH = Path(__file__).resolve().parents[4]

ROUTING_PATH = FRONTEND_PATH \
      / 'apps' \
      / 'front-end' \
      / 'src' \
      / 'app' \
      / 'app.routes.ts'

ROUTING_PATH_BAK = FRONTEND_PATH \
      / 'apps' \
      / 'front-end' \
      / 'src' \
      / 'app' \
      / 'app.routes.ts.bak'

HOME_PATH = FRONTEND_PATH \
      / 'apps' \
      / 'front-end' \
      / 'src' \
      / 'app' \
      / 'features' \
      / 'home' \
      / 'home.ts'

PROFILE_PATH = FRONTEND_PATH \
      / 'apps' \
      / 'front-end' \
      / 'src' \
      / 'app' \
      / 'features' \
      / 'profile' \
      / 'profile.ts'

# ========================================
# 2. Backup routing configuration
# ========================================

def backup_routing_configuration() -> None:

    """
    Backup the current routing configuration file.

    Arguments:
        None

    Returns:
        None
    """

    shutil.copy2(ROUTING_PATH, ROUTING_PATH_BAK)

# ========================================
# 3. Create home component
# ========================================

def create_home_component() -> None:

    """
    Create home component file with defined content.

    Arguments:
        None

    Returns:
        None
    """

    # Define the content of the home component file
    home_file_content = """
import { Component, OnInit } from '@angular/core';
import { faro } from '@grafana/faro-web-sdk';
import { RouterLink } from '@angular/router';

@Component({
selector: 'app-home',
imports: [RouterLink],
template: `
    <button id='profile-button' routerLink='/profile'>
    Profile
    </button>
`,
styles: ``,
})
export class Home implements OnInit {

    ngOnInit(): void {
    faro.api.setView({ name: 'home'})
    }
}
"""

    # Create the home component file if it doesn't exist
    HOME_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the home component content to the file
    HOME_PATH.write_text(
        home_file_content.strip() + '\n',
        encoding='utf-8'
    )

# ========================================
# 4. Create profile component
# ========================================

def create_profile_component() -> None:

    """
    Create profile component file with defined content.

    Arguments:
        None

    Returns:
        None
    """

    # Define the content of the profile component file
    profile_file_content = """
import { Component, OnInit } from '@angular/core';
import { faro } from '@grafana/faro-web-sdk';

@Component({
selector: 'app-profile',
imports: [],
template: `
    <p>
    profile works!
    </p>
`,
styles: ``,
})
export class Profile implements OnInit {

    ngOnInit(): void {
    faro.api.setView({ name: 'profile' });
    }
}
"""
    # Create the profile component file if it doesn't exist
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write the profile component content to the file
    PROFILE_PATH.write_text(
        profile_file_content.strip() + '\n',
        encoding='utf-8'
    )

# ========================================
# 5. Create routing configuration
# ========================================  

def create_routing_configuration() -> None:

    """
    Create routing configuration file with defined content.

    Arguments:
        None

    Returns:
        None
    """

    # Define the content of the routing configuration file
    routing_file_content = """
import { Routes } from '@angular/router';
import { Home } from './features/home/home';
import { Profile } from './features/profile/profile';

export const routes: Routes = [

    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: 'home', component: Home },
    { path: 'profile', component: Profile }
];
"""

    # Write the routing configuration content to the file
    ROUTING_PATH.write_text(
        routing_file_content.strip() + '\n',
        encoding='utf-8'
    )

# ========================================
# 7. Click profile button
# ========================================

def click_profile_button(browser) -> None:

    """
    Click the profile button in the Angular application.

    Arguments:
        browser: The Selenium WebDriver instance.

    Returns:
        None
    """

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Wait for the "profile" button to be clickable and then click it
    profile_button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "profile-button"))
    )
    profile_button.click()

# ========================================
# 8. Verify logs in Loki
# ========================================

def verify_logs_in_loki() -> None:

    """
    Verify logs in Loki with view_changed event name.

    Arguments:
        None

    Returns:
        None
    """

    # Initialize Loki client
    loki = LokiClient()

    # Get logs with view_changed event name
    view_changed_log = loki.wait_for_log(
        logql_query=(
            '{app_name="front-end"}'
            '|= "view_changed"'
            '|= "event_data_fromView=home"'
            '|= "event_data_toView=profile"'
        ),
        timeout=30,
        expected_text='event_data_toView=profile'
    )

    # Verify that the view_changed log was found
    assert view_changed_log is not None, "view_changed log not found"

    # Verify that log contains details
    assert 'kind=event' in view_changed_log
    assert 'event_name=view_changed' in view_changed_log
    assert 'event_data_fromView=home' in view_changed_log
    assert 'event_data_toView=profile' in view_changed_log
    assert 'sdk_name=faro-web' in view_changed_log

    

# ========================================
# 9. Restore files
# ========================================

def restore_files() -> None:

    """
    Restore any modified files to their original state.

    Arguments:
        None

    Returns:
        None
    """

    # Restore the routing configuration file from the backup
    shutil.move(ROUTING_PATH_BAK, ROUTING_PATH)

    # Remove create files/folders for home and profile components
    shutil.rmtree(HOME_PATH.parent, ignore_errors=True)
    shutil.rmtree(PROFILE_PATH.parent, ignore_errors=True)

# ========================================
# 10. Create home component for Angular route changes test
# ========================================

def create_home_component_route_changes() -> None:

    """
    Create the home component for Angular route changes test.

    Arguments:
        None

    Returns:
        None
    """

    # Define the home component for Angular route changes test
    home_component_content = """
import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
selector: 'app-home',
imports: [RouterLink],
template: `
    <button id='profile-button' routerLink='/profile'>
    Profile
    </button>
`,
styles: ``,
})
export class Home {}
"""
    # Create the home component folder if it doesn't exist
    HOME_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the home component content to the appropriate file
    HOME_PATH.write_text(
        home_component_content.strip() + '\n',
        encoding='utf-8'
    )

# ========================================
# 11. Create profile component for Angular route changes test
# ========================================

def create_profile_component_route_changes() -> None:

    """
    Create the profile component for Angular route changes test.

    Arguments:
        None

    Returns:
        None
    """

    profile_component_content = """
import { Component } from '@angular/core';

@Component({
selector: 'app-profile',
imports: [],
template: `
    <p>
    profile works!
    </p>
`,
styles: ``,
})
export class Profile {}
"""
    # Create the profile component folder if it doesn't exist
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Write the profile component content to the appropriate file
    PROFILE_PATH.write_text(
        profile_component_content.strip() + '\n',
        encoding='utf-8'
    )

# ========================================
# 12. Verify logs in Loki for Angular route changes test
# ========================================

def verify_logs_in_loki_route_changes() -> None:
    """
    Verify logs in Loki for Angular route changes test.

    Arguments:
        None

    Returns:
        None
    """

    # Initialize Loki client
    loki = LokiClient()

    # Get logs from Loki for the Angular route changes test
    route_changes_log = loki.wait_for_log(
        logql_query=(
            '{service_name="front-end"}'
            '|= "faro.navigation"'
        ),
        timeout=30,
        expected_text='faro.navigation'
    ) 

    # Verify logs exist for the Angular route changes test
    assert route_changes_log is not None, "Expected log for Angular route changes not found"

    # Verify log contains the expected details
    assert 'kind=event' in route_changes_log
    assert 'event_name=faro.navigation' in route_changes_log
    assert 'event_data_duration=' in route_changes_log
    assert 'event_data_fromUrl=http://localhost:4200/home' in route_changes_log
    assert 'event_data_toUrl=http://localhost:4200/profile' in route_changes_log
    assert 'sdk_name=faro-web' in route_changes_log
    

# ========================================
# 13. Main
# ========================================

def test_page_views(browser) -> None:

    try:
        # 2. Backup routing configuration
        backup_routing_configuration()
        # 3. Create home component
        create_home_component()
        # 4. Create profile component
        create_profile_component()
        # 5. Create routing configuration
        create_routing_configuration()
        # 6. Open Angular application
        browser.get('http://localhost:4200')
        # 7. Click profile button
        click_profile_button(browser)
        # 8. Verify logs in Loki
        verify_logs_in_loki()
    finally:
        # 9. Restore files
        restore_files()

def test_angular_route_changes(browser) -> None:

    try:
        # 2. Backup routing configuration
        backup_routing_configuration()
        # 10. Create home component for Angular route changes test
        create_home_component_route_changes()
        # 11. Create profile component for Angular route changes test
        create_profile_component_route_changes()
        # 5. Create routing configuration
        create_routing_configuration()
        # 6. Open Angular application
        browser.get('http://localhost:4200')
        # 7. Click profile button
        click_profile_button(browser)
        # 12. Verify logs in Loki
        verify_logs_in_loki_route_changes()

    finally:
        # 9. Restore files
        restore_files()