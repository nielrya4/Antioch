#!/usr/bin/env python3
"""
Cloud Sync Demo for Antioch

Demonstrates Google Drive integration with the filesystem, including:
- OAuth authentication flow
- Real-time sync status indicators
- Conflict resolution
- Storage settings panel
- Multi-device simulation
"""

from antioch import DOM, Div, H1, H2, P, Button, Hr
from antioch.core import get_filesystem, LocalStorageBackend
from antioch.core import AsyncLocalStorageBackend, GoogleDriveBackend, SyncQueue, SyncStatus
from antioch.macros.sync_status import SyncStatusIndicator
from antioch.macros.storage_settings import StorageSettingsPanel
import js
import asyncio


def main():
    """Demonstrate cloud sync functionality."""

    # Create main container
    container = Div()
    container.style.padding = "20px"
    container.style.max_width = "900px"
    container.style.margin = "0 auto"

    # Header with sync status
    header = Div()
    header.style.display = "flex"
    header.style.justify_content = "space-between"
    header.style.align_items = "center"
    header.style.margin_bottom = "20px"

    title = H1("Cloud Sync Demo")
    title.style.margin = "0"
    title.style.color = "#333"

    # Sync status indicator (will be initialized later)
    status_indicator_container = Div()
    status_indicator_container.set_attribute("id", "sync-status-container")

    header.add(title, status_indicator_container)
    container.add(header)

    # Description
    desc = P(
        "This demo shows how Antioch's filesystem can sync with Google Drive. "
        "Features include automatic syncing, conflict resolution, and offline support."
    )
    desc.style.color = "#666"
    desc.style.margin_bottom = "30px"
    container.add(desc)

    # Quick start section
    quick_start = create_quick_start_section()
    container.add(quick_start)

    container.add(Hr())

    # Demo features section
    features = create_features_section()
    container.add(features)

    container.add(Hr())

    # Live demo section
    demo_section = create_live_demo_section()
    container.add(demo_section)

    # Add to DOM
    DOM.add(container)

    # Initialize sync system (async)
    asyncio.create_task(initialize_sync_system(status_indicator_container))


def create_quick_start_section():
    """Create quick start instructions."""
    section = Div()

    title = H2("Quick Start")
    title.style.color = "#333"
    title.style.margin_bottom = "15px"

    steps = Div()

    step1 = create_step_box(
        "1", "Configure Google API",
        "Get OAuth credentials from Google Cloud Console"
    )
    step2 = create_step_box(
        "2", "Connect to Drive",
        "Click 'Connect Google Drive' and authorize access"
    )
    step3 = create_step_box(
        "3", "Auto-Sync Enabled",
        "Changes sync automatically in the background"
    )

    steps.style.display = "grid"
    steps.style.grid_template_columns = "repeat(auto-fit, minmax(250px, 1fr))"
    steps.style.gap = "15px"
    steps.add(step1, step2, step3)

    section.add(title, steps)
    return section


def create_step_box(number, title_text, desc_text):
    """Create a numbered step box."""
    box = Div()
    box.style.padding = "20px"
    box.style.background_color = "#f5f5f5"
    box.style.border_radius = "8px"
    box.style.border_left = "4px solid #2196F3"

    number_span = Div(number)
    number_span.style.display = "inline-block"
    number_span.style.width = "30px"
    number_span.style.height = "30px"
    number_span.style.line_height = "30px"
    number_span.style.text_align = "center"
    number_span.style.background_color = "#2196F3"
    number_span.style.color = "white"
    number_span.style.border_radius = "50%"
    number_span.style.font_weight = "bold"
    number_span.style.margin_bottom = "10px"

    title = P(title_text)
    title.style.font_weight = "600"
    title.style.margin = "10px 0 5px 0"
    title.style.color = "#333"

    desc = P(desc_text)
    desc.style.margin = "0"
    desc.style.font_size = "14px"
    desc.style.color = "#666"

    box.add(number_span, title, desc)
    return box


def create_features_section():
    """Create features showcase."""
    section = Div()

    title = H2("Features")
    title.style.color = "#333"
    title.style.margin_bottom = "15px"
    section.add(title)

    features_list = Div()
    features_list.style.display = "grid"
    features_list.style.grid_template_columns = "repeat(auto-fit, minmax(200px, 1fr))"
    features_list.style.gap = "15px"

    features = [
        ("✓", "Real-time Sync", "Changes sync automatically"),
        ("✓", "Conflict Resolution", "Smart merging of changes"),
        ("✓", "Offline Support", "Works without internet"),
        ("✓", "Multi-Device", "Access from anywhere"),
        ("✓", "Visual Feedback", "See sync status at a glance"),
        ("✓", "Retry Logic", "Auto-retry on failures")
    ]

    for icon, title_text, desc_text in features:
        feature_box = Div()
        feature_box.style.padding = "15px"
        feature_box.style.background_color = "#E8F5E9"
        feature_box.style.border_radius = "6px"

        icon_span = Div(icon)
        icon_span.style.font_size = "24px"
        icon_span.style.margin_bottom = "8px"

        feature_title = P(title_text)
        feature_title.style.font_weight = "600"
        feature_title.style.margin = "0 0 5px 0"
        feature_title.style.color = "#2E7D32"

        feature_desc = P(desc_text)
        feature_desc.style.margin = "0"
        feature_desc.style.font_size = "13px"
        feature_desc.style.color = "#555"

        feature_box.add(icon_span, feature_title, feature_desc)
        features_list.add(feature_box)

    section.add(features_list)
    return section


def create_live_demo_section():
    """Create live demo interface."""
    section = Div()

    title = H2("Live Demo")
    title.style.color = "#333"
    title.style.margin_bottom = "15px"

    note = P("Note: This demo requires Google API credentials to be configured.")
    note.style.font_size = "14px"
    note.style.color = "#666"
    note.style.font_style = "italic"
    note.style.margin_bottom = "20px"

    # Connect button
    connect_btn = Button("Connect to Google Drive")
    connect_btn.style.padding = "12px 24px"
    connect_btn.style.background_color = "#4285F4"
    connect_btn.style.color = "white"
    connect_btn.style.border = "none"
    connect_btn.style.border_radius = "4px"
    connect_btn.style.cursor = "pointer"
    connect_btn.style.font_size = "16px"
    connect_btn.style.margin_right = "10px"
    connect_btn.on_click(lambda e: on_connect_drive())

    # Settings button
    settings_btn = Button("⚙ Storage Settings")
    settings_btn.style.padding = "12px 24px"
    settings_btn.style.background_color = "#666"
    settings_btn.style.color = "white"
    settings_btn.style.border = "none"
    settings_btn.style.border_radius = "4px"
    settings_btn.style.cursor = "pointer"
    settings_btn.style.font_size = "16px"
    settings_btn.on_click(lambda e: on_show_settings())

    button_row = Div()
    button_row.style.margin_bottom = "20px"
    button_row.add(connect_btn, settings_btn)

    # Settings panel container (hidden initially)
    settings_container = Div()
    settings_container.set_attribute("id", "settings-container")
    settings_container.style.display = "none"
    settings_container.style.margin_top = "20px"

    section.add(title, note, button_row, settings_container)
    return section


async def initialize_sync_system(container):
    """Initialize the sync system with UI components."""
    try:
        # Get filesystem
        local_backend = LocalStorageBackend()
        fs = get_filesystem(local_backend)

        # Create async backends
        async_local = AsyncLocalStorageBackend()

        # Note: Google Drive backend requires actual credentials
        # For demo purposes, we'll show the UI without active syncing
        # In production, replace these with real credentials:
        # CLIENT_ID = "your-client-id.apps.googleusercontent.com"
        # google_drive = GoogleDriveBackend(client_id=CLIENT_ID)

        # Create sync queue (with local-only for now)
        sync_queue = SyncQueue(async_local, async_local, debounce_ms=2000)

        # Create and add sync status indicator
        status_indicator = SyncStatusIndicator(sync_queue, show_details=True)
        container.add(status_indicator.element)

        # Store globally for access from buttons
        js.window.antioch_sync_queue = sync_queue
        js.window.antioch_filesystem = fs

        print("Sync system initialized (local mode)")

    except Exception as e:
        print(f"Error initializing sync: {e}")


def on_connect_drive():
    """Handle connect to Google Drive button click."""
    js.alert(
        "Google Drive Integration Setup:\n\n"
        "To enable Google Drive sync, you need:\n\n"
        "1. Google Cloud Project with Drive API enabled\n"
        "2. OAuth 2.0 Client ID for web application\n"
        "3. Configure authorized JavaScript origins\n\n"
        "See the documentation for setup instructions.\n\n"
        "For this demo, we're using local storage simulation."
    )


def on_show_settings():
    """Show/hide storage settings panel."""
    container = js.document.getElementById("settings-container")

    if container.style.display == "none":
        # Create settings panel if not exists
        if not hasattr(js.window, 'settings_panel_created'):
            fs = js.window.antioch_filesystem
            sync_queue = js.window.antioch_sync_queue

            settings_panel = StorageSettingsPanel(fs, sync_queue)

            # Add to container using direct DOM manipulation
            container.appendChild(settings_panel.element._dom_element)
            js.window.settings_panel_created = True

        container.style.display = "block"
    else:
        container.style.display = "none"


if __name__ == "__main__":
    main()