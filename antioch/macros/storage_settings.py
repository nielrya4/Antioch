"""
Storage Settings Panel Macro for Antioch

UI for managing storage backend configuration.
"""

from antioch import Div, H3, P, Button, Span, Select, Option, Input, Label
from antioch.macros.base import Macro
from antioch.core.sync_queue import SyncStatus
import js


class StorageSettingsPanel(Macro):
    """
    Settings panel for storage backend configuration.

    Features:
    - Switch between local and cloud storage
    - Connect/disconnect Google Drive
    - Configure sync settings
    - View storage usage
    - Export/import backups
    """

    def __init__(self, filesystem, sync_queue=None):
        """
        Initialize storage settings panel.

        Args:
            filesystem: VirtualFileSystem instance
            sync_queue: Optional SyncQueue instance
        """
        super().__init__('storage_settings_panel')

        self.filesystem = filesystem
        self.sync_queue = sync_queue
        self.current_backend = "local"

        # Initialize the macro (creates elements)
        self._init_macro()

    def _create_elements(self):
        """Create the settings panel UI."""
        # Main container
        panel = Div()
        panel.style.padding = "20px"
        panel.style.background_color = "#fff"
        panel.style.border_radius = "8px"
        panel.style.box_shadow = "0 2px 8px rgba(0,0,0,0.1)"
        panel.style.max_width = "500px"

        # Title
        title = H3("Storage Settings")
        title.style.margin_top = "0"
        title.style.color = "#333"
        panel.add(title)

        # Current storage section
        current_section = self._create_current_storage_section()
        panel.add(current_section)

        # Sync settings section (if using cloud)
        if self.sync_queue:
            sync_section = self._create_sync_settings_section()
            panel.add(sync_section)

        # Storage actions section
        actions_section = self._create_actions_section()
        panel.add(actions_section)

        # Usage statistics
        usage_section = self._create_usage_section()
        panel.add(usage_section)

        self._register_element('panel', panel)
        return panel

    def _create_current_storage_section(self):
        """Create current storage display section."""
        section = Div()
        section.style.margin_bottom = "20px"
        section.style.padding_bottom = "20px"
        section.style.border_bottom = "1px solid #eee"

        label = P("Current Storage:")
        label.style.margin = "0 0 10px 0"
        label.style.font_weight = "600"
        label.style.color = "#555"

        # Storage type display
        storage_display = Div()
        storage_display.style.display = "flex"
        storage_display.style.align_items = "center"
        storage_display.style.gap = "10px"

        storage_icon = Span("💾")
        storage_icon.style.font_size = "24px"

        storage_text = Div()
        storage_name = Span("Browser Storage")
        storage_name.style.font_weight = "600"
        storage_name.style.display = "block"
        self._register_element('storage_name', storage_name)

        storage_desc = Span("Fast, local storage")
        storage_desc.style.font_size = "13px"
        storage_desc.style.color = "#666"
        storage_desc.style.display = "block"
        self._register_element('storage_desc', storage_desc)

        storage_text.add(storage_name, storage_desc)
        storage_display.add(storage_icon, storage_text)

        # Change button
        change_btn = Button("Change Storage")
        change_btn.style.margin_top = "10px"
        change_btn.style.padding = "8px 16px"
        change_btn.style.background_color = "#2196F3"
        change_btn.style.color = "white"
        change_btn.style.border = "none"
        change_btn.style.border_radius = "4px"
        change_btn.style.cursor = "pointer"
        change_btn.on_click(self._on_change_storage)

        section.add(label, storage_display, change_btn)
        return section

    def _create_sync_settings_section(self):
        """Create sync configuration section."""
        section = Div()
        section.style.margin_bottom = "20px"
        section.style.padding_bottom = "20px"
        section.style.border_bottom = "1px solid #eee"

        title = P("Sync Settings:")
        title.style.margin = "0 0 10px 0"
        title.style.font_weight = "600"
        title.style.color = "#555"

        # Auto-sync toggle
        auto_sync_row = Div()
        auto_sync_row.style.display = "flex"
        auto_sync_row.style.justify_content = "space-between"
        auto_sync_row.style.align_items = "center"
        auto_sync_row.style.margin_bottom = "10px"

        auto_sync_label = Label("Auto-sync enabled")
        auto_sync_label.style.color = "#333"

        auto_sync_toggle = Input(input_type="checkbox")
        auto_sync_toggle.set_attribute("checked", "true")
        auto_sync_toggle.on_change(self._on_toggle_autosync)
        self._register_element('auto_sync_toggle', auto_sync_toggle)

        auto_sync_row.add(auto_sync_label, auto_sync_toggle)

        # Sync frequency
        freq_row = Div()
        freq_row.style.display = "flex"
        freq_row.style.justify_content = "space-between"
        freq_row.style.align_items = "center"
        freq_row.style.margin_bottom = "10px"

        freq_label = Label("Sync frequency:")
        freq_label.style.color = "#333"

        freq_select = Select()
        freq_select.style.padding = "4px"
        freq_select.style.border = "1px solid #ddd"
        freq_select.style.border_radius = "4px"
        freq_select.add(
            Option("Every 10 seconds", value="10"),
            Option("Every 30 seconds", value="30"),
            Option("Every minute", value="60")
        )
        freq_select.value = "30"
        freq_select.on_change(self._on_change_frequency)
        self._register_element('freq_select', freq_select)

        freq_row.add(freq_label, freq_select)

        # Force sync button
        sync_btn = Button("Sync Now")
        sync_btn.style.width = "100%"
        sync_btn.style.padding = "8px"
        sync_btn.style.background_color = "#4CAF50"
        sync_btn.style.color = "white"
        sync_btn.style.border = "none"
        sync_btn.style.border_radius = "4px"
        sync_btn.style.cursor = "pointer"
        sync_btn.on_click(self._on_sync_now)

        section.add(title, auto_sync_row, freq_row, sync_btn)
        return section

    def _create_actions_section(self):
        """Create storage action buttons."""
        section = Div()
        section.style.margin_bottom = "20px"

        title = P("Actions:")
        title.style.margin = "0 0 10px 0"
        title.style.font_weight = "600"
        title.style.color = "#555"

        # Button container
        button_grid = Div()
        button_grid.style.display = "grid"
        button_grid.style.grid_template_columns = "1fr 1fr"
        button_grid.style.gap = "10px"

        # Export backup
        export_btn = Button("Export Backup")
        export_btn.style.padding = "10px"
        export_btn.style.background_color = "#FF9800"
        export_btn.style.color = "white"
        export_btn.style.border = "none"
        export_btn.style.border_radius = "4px"
        export_btn.style.cursor = "pointer"
        export_btn.on_click(self._on_export_backup)

        # Import backup
        import_btn = Button("Import Backup")
        import_btn.style.padding = "10px"
        import_btn.style.background_color = "#9C27B0"
        import_btn.style.color = "white"
        import_btn.style.border = "none"
        import_btn.style.border_radius = "4px"
        import_btn.style.cursor = "pointer"
        import_btn.on_click(self._on_import_backup)

        # Disconnect (if using cloud)
        disconnect_btn = Button("Disconnect")
        disconnect_btn.style.padding = "10px"
        disconnect_btn.style.background_color = "#f44336"
        disconnect_btn.style.color = "white"
        disconnect_btn.style.border = "none"
        disconnect_btn.style.border_radius = "4px"
        disconnect_btn.style.cursor = "pointer"
        disconnect_btn.on_click(self._on_disconnect)
        self._register_element('disconnect_btn', disconnect_btn)

        # Reset filesystem
        reset_btn = Button("Reset Filesystem")
        reset_btn.style.padding = "10px"
        reset_btn.style.background_color = "#666"
        reset_btn.style.color = "white"
        reset_btn.style.border = "none"
        reset_btn.style.border_radius = "4px"
        reset_btn.style.cursor = "pointer"
        reset_btn.on_click(self._on_reset)

        button_grid.add(export_btn, import_btn, disconnect_btn, reset_btn)
        section.add(title, button_grid)
        return section

    def _create_usage_section(self):
        """Create storage usage display."""
        section = Div()

        title = P("Storage Usage:")
        title.style.margin = "0 0 10px 0"
        title.style.font_weight = "600"
        title.style.color = "#555"

        usage_text = P("Local: calculating...")
        usage_text.style.font_size = "13px"
        usage_text.style.color = "#666"
        usage_text.style.margin = "5px 0"
        self._register_element('usage_text', usage_text)

        section.add(title, usage_text)
        return section

    # Event handlers
    def _on_change_storage(self, event):
        """Handle change storage backend button click."""
        # Show dialog to choose storage type
        choice = js.prompt("Choose storage:\n1. Browser Storage (Local)\n2. Google Drive (Cloud)\n\nEnter 1 or 2:")

        if choice == "2":
            js.alert("Google Drive integration coming soon!\n\nThis will allow you to:\n- Access files from any device\n- Automatic cloud backup\n- Share with others")
            # TODO: Implement Google Drive connection flow
        elif choice == "1":
            js.alert("Already using Browser Storage")

    def _on_toggle_autosync(self, event):
        """Handle auto-sync toggle."""
        enabled = self._get_element('auto_sync_toggle')._dom_element.checked
        if self.sync_queue:
            # TODO: Implement enable/disable auto-sync
            pass

    def _on_change_frequency(self, event):
        """Handle sync frequency change."""
        freq_select = self._get_element('freq_select')
        frequency = int(freq_select.value)
        if self.sync_queue:
            self.sync_queue.debounce_ms = frequency * 1000

    def _on_sync_now(self, event):
        """Handle sync now button click."""
        if self.sync_queue:
            import asyncio
            asyncio.create_task(self.sync_queue.force_sync())
            js.alert("Syncing now...")

    def _on_export_backup(self, event):
        """Handle export backup button click."""
        import json

        # Get filesystem data
        data = self.filesystem.root.to_dict()
        json_str = json.dumps(data, indent=2)

        # Create download link
        blob = js.Blob.new([json_str], js.Object.fromEntries([["type", "application/json"]]))
        url = js.URL.createObjectURL(blob)

        # Create temporary link and click it
        a = js.document.createElement('a')
        a.href = url
        a.download = f"antioch_backup_{js.Date.new().toISOString()[:10]}.json"
        a.click()

        js.URL.revokeObjectURL(url)

    def _on_import_backup(self, event):
        """Handle import backup button click."""
        # Create file input
        file_input = js.document.createElement('input')
        file_input.type = 'file'
        file_input.accept = '.json'

        def on_file_selected(e):
            file = e.target.files[0]
            if file:
                reader = js.FileReader.new()

                def on_load(e):
                    try:
                        import json
                        from antioch.core.filesystem import FileSystemItem

                        data = json.loads(e.target.result)
                        self.filesystem.root = FileSystemItem.from_dict(data)
                        self.filesystem.current_path = []
                        self.filesystem._save_filesystem()
                        js.alert("Backup imported successfully!")
                        self._trigger_callbacks('filesystem_changed')
                    except Exception as ex:
                        js.alert(f"Error importing backup: {ex}")

                from pyodide.ffi import create_proxy
                reader.onload = create_proxy(on_load)
                reader.readAsText(file)

        from pyodide.ffi import create_proxy
        file_input.onchange = create_proxy(on_file_selected)
        file_input.click()

    def _on_disconnect(self, event):
        """Handle disconnect button click."""
        if js.confirm("Disconnect from cloud storage?\n\nLocal files will not be deleted."):
            # TODO: Implement disconnect logic
            js.alert("Disconnected from cloud storage")

    def _on_reset(self, event):
        """Handle reset filesystem button click."""
        if js.confirm("Reset filesystem to defaults?\n\nThis will delete all files and cannot be undone!"):
            self.filesystem.reset_filesystem()
            js.alert("Filesystem reset to defaults")