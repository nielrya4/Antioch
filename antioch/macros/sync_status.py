"""
Sync Status Indicator Macro for Antioch

Displays current sync status with visual feedback.
"""

from antioch import Div, Span, Button
from antioch.macros.base import Macro
from antioch.core.sync_queue import SyncStatus


class SyncStatusIndicator(Macro):
    """
    Visual indicator showing filesystem sync status.

    Features:
    - Status icon (✓, ↻, ⚠, ⚡)
    - Status text
    - Last sync time
    - Error messages
    - Click to view details or retry
    """

    def __init__(self, sync_queue=None, show_details=True):
        """
        Initialize sync status indicator.

        Args:
            sync_queue: SyncQueue instance to monitor
            show_details: Whether to show detailed status text
        """
        super().__init__('sync_status_indicator')

        self.sync_queue = sync_queue
        self.show_details = show_details
        self.current_status = SyncStatus.IDLE

        # Initialize the macro (creates elements)
        self._init_macro()

    def _create_elements(self):
        """Create the UI elements."""
        # Main container
        container = Div()
        container.style.display = "inline-flex"
        container.style.align_items = "center"
        container.style.gap = "8px"
        container.style.padding = "6px 12px"
        container.style.border_radius = "20px"
        container.style.background_color = "#f5f5f5"
        container.style.cursor = "pointer"
        container.style.transition = "all 0.3s"
        container.style.user_select = "none"

        # Status icon
        self.icon = Span("🌐")
        self.icon.style.font_size = "16px"
        self.icon.style.transition = "transform 0.3s"
        self._register_element('icon', self.icon)

        # Status text
        self.status_text = Span("Idle")
        self.status_text.style.font_size = "13px"
        self.status_text.style.color = "#666"
        self.status_text.style.font_weight = "500"
        self._register_element('status_text', self.status_text)

        if self.show_details:
            container.add(self.icon, self.status_text)
        else:
            container.add(self.icon)

        # Click handler
        container.on_click(self._on_click)

        self._register_element('container', container)

        # Register with sync queue if provided
        if self.sync_queue:
            self.sync_queue.add_status_callback(self._on_status_change)

        return container

    def _on_status_change(self, status: SyncStatus, details: dict):
        """Handle sync status changes."""
        self.current_status = status

        # Update icon and text based on status
        if status == SyncStatus.IDLE:
            self._set_status("🌐", "Idle", "#666", "#f5f5f5")

        elif status == SyncStatus.SYNCING:
            self._set_status("↻", "Syncing...", "#2196F3", "#E3F2FD")
            self._animate_icon()

        elif status == SyncStatus.SYNCED:
            last_sync = details.get('last_sync')
            if last_sync:
                time_ago = self._format_time_ago(last_sync)
                self._set_status("✓", f"Synced {time_ago}", "#4CAF50", "#E8F5E9")
            else:
                self._set_status("✓", "Synced", "#4CAF50", "#E8F5E9")

        elif status == SyncStatus.ERROR:
            error_msg = details.get('message', 'Sync failed')
            retry_in = details.get('retry_in')
            if retry_in:
                self._set_status("⚠", f"Retrying in {retry_in}s...", "#FF9800", "#FFF3E0")
            else:
                self._set_status("⚠", error_msg[:30], "#f44336", "#FFEBEE")

        elif status == SyncStatus.OFFLINE:
            self._set_status("⚡", "Offline", "#9E9E9E", "#FAFAFA")

        elif status == SyncStatus.CONFLICT:
            self._set_status("⚠", "Conflict!", "#FF5722", "#FBE9E7")

        # Trigger any registered callbacks
        self._trigger_callbacks('status_change', status, details)

    def _set_status(self, icon: str, text: str, color: str, bg_color: str):
        """Update status display."""
        self.icon.set_text(icon)
        if self.show_details:
            self.status_text.set_text(text)
            self.status_text.style.color = color

        container = self._get_element('container')
        container.style.background_color = bg_color

    def _animate_icon(self):
        """Animate the icon (spinning effect for syncing)."""
        import js

        def animate(timestamp):
            icon_elem = self.icon._dom_element
            if icon_elem:
                # Only animate if still syncing
                if self.current_status == SyncStatus.SYNCING:
                    rotation = (timestamp / 10) % 360
                    icon_elem.style.transform = f"rotate({rotation}deg)"
                    js.requestAnimationFrame(animate_proxy)

        from pyodide.ffi import create_proxy
        animate_proxy = create_proxy(animate)
        js.requestAnimationFrame(animate_proxy)

    def _format_time_ago(self, iso_time: str) -> str:
        """Format ISO time as 'X seconds/minutes ago'."""
        from datetime import datetime

        try:
            then = datetime.fromisoformat(iso_time)
            now = datetime.now()
            delta = (now - then).total_seconds()

            if delta < 60:
                return f"{int(delta)}s ago"
            elif delta < 3600:
                return f"{int(delta/60)}m ago"
            else:
                return f"{int(delta/3600)}h ago"
        except:
            return "just now"

    def _on_click(self, event):
        """Handle click on status indicator."""
        # Trigger callback with current status
        self._trigger_callbacks('click', self.current_status)

        # Show details or retry based on status
        if self.current_status == SyncStatus.ERROR:
            import js
            if js.confirm("Sync error occurred. Retry now?"):
                if self.sync_queue:
                    import asyncio
                    asyncio.create_task(self.sync_queue.force_sync())

        elif self.current_status == SyncStatus.CONFLICT:
            self._trigger_callbacks('show_conflict_dialog')

    def set_sync_queue(self, sync_queue):
        """Set or update the sync queue to monitor."""
        # Remove old callback if exists
        if self.sync_queue:
            self.sync_queue.remove_status_callback(self._on_status_change)

        self.sync_queue = sync_queue

        # Add new callback
        if self.sync_queue:
            self.sync_queue.add_status_callback(self._on_status_change)

    def destroy(self):
        """Cleanup when destroying."""
        if self.sync_queue:
            self.sync_queue.remove_status_callback(self._on_status_change)
        super().destroy()