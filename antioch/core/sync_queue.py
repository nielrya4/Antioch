#!/usr/bin/env python3
"""
Sync Queue for Antioch Filesystem

Manages background syncing with retry logic, batching, and status tracking.
"""

import asyncio
import json
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
from enum import Enum


class SyncStatus(Enum):
    """Sync status states."""
    IDLE = "idle"
    SYNCING = "syncing"
    SYNCED = "synced"
    ERROR = "error"
    OFFLINE = "offline"
    CONFLICT = "conflict"


class SyncQueue:
    """
    Manages background syncing with batching and retry logic.

    Features:
    - Debounced syncing (waits for pause in changes)
    - Retry with exponential backoff
    - Conflict detection
    - Status callbacks for UI updates
    """

    def __init__(self,
                 local_backend,
                 cloud_backend,
                 debounce_ms: int = 2000,
                 max_retries: int = 3):
        """
        Initialize sync queue.

        Args:
            local_backend: Local storage backend (for cache)
            cloud_backend: Cloud storage backend (Google Drive, etc.)
            debounce_ms: Milliseconds to wait before syncing after changes
            max_retries: Maximum number of retry attempts
        """
        self.local_backend = local_backend
        self.cloud_backend = cloud_backend
        self.debounce_ms = debounce_ms
        self.max_retries = max_retries

        self.status = SyncStatus.IDLE
        self.last_sync_time = None
        self.pending_save = False
        self.pending_data = None
        self.retry_count = 0
        self.error_message = None

        self._status_callbacks: List[Callable] = []
        self._sync_task = None
        self._debounce_task = None

    def add_status_callback(self, callback: Callable[[SyncStatus, Dict[str, Any]], None]):
        """Add a callback that will be notified of status changes."""
        if callback not in self._status_callbacks:
            self._status_callbacks.append(callback)

    def remove_status_callback(self, callback: Callable):
        """Remove a status callback."""
        if callback in self._status_callbacks:
            self._status_callbacks.remove(callback)

    def _notify_status(self, status: SyncStatus, details: Dict[str, Any] = None):
        """Notify all callbacks of status change."""
        self.status = status
        details = details or {}
        details['status'] = status.value
        details['last_sync'] = self.last_sync_time
        details['error'] = self.error_message

        for callback in self._status_callbacks[:]:
            try:
                callback(status, details)
            except Exception as e:
                print(f"Error in sync status callback: {e}")

    async def queue_save(self, filesystem_data: dict):
        """
        Queue a filesystem save operation.

        Changes are batched and synced after a debounce period.
        """
        self.pending_save = True
        self.pending_data = filesystem_data

        # Save to local cache immediately
        try:
            await self.local_backend.save_filesystem(filesystem_data)
        except Exception as e:
            print(f"Error saving to local cache: {e}")

        # Cancel existing debounce timer
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()

        # Start new debounce timer
        self._debounce_task = asyncio.create_task(self._debounce_and_sync())

    async def _debounce_and_sync(self):
        """Wait for debounce period, then sync."""
        try:
            # Wait for debounce period
            await asyncio.sleep(self.debounce_ms / 1000.0)

            # If still have pending data, sync it
            if self.pending_save and self.pending_data:
                await self._perform_sync()

        except asyncio.CancelledError:
            pass  # Normal cancellation
        except Exception as e:
            print(f"Error in debounce: {e}")

    async def _perform_sync(self):
        """Perform the actual sync operation."""
        if not self.pending_data:
            return

        data_to_sync = self.pending_data
        self.pending_save = False

        try:
            self._notify_status(SyncStatus.SYNCING, {'changes': 1})

            # Check for conflicts before saving
            conflict = await self._check_for_conflicts(data_to_sync)
            if conflict:
                self._notify_status(SyncStatus.CONFLICT, conflict)
                return

            # Save to cloud
            success = await self.cloud_backend.save_filesystem(data_to_sync)

            if success:
                self.retry_count = 0
                self.error_message = None
                self.last_sync_time = datetime.now().isoformat()
                self._notify_status(SyncStatus.SYNCED, {
                    'timestamp': self.last_sync_time
                })
            else:
                await self._handle_sync_error("Save failed")

        except Exception as e:
            await self._handle_sync_error(str(e))

    async def _check_for_conflicts(self, local_data: dict) -> Optional[Dict[str, Any]]:
        """
        Check if cloud version has changed since last sync.

        Returns conflict details if conflict detected, None otherwise.
        """
        try:
            # Get cloud metadata
            cloud_metadata = await self.cloud_backend.get_metadata()
            if not cloud_metadata:
                return None  # No cloud file yet

            # Get local metadata
            local_metadata = await self.local_backend.get_metadata()
            if not local_metadata:
                return None  # No local history

            # Compare modification times
            cloud_modified = cloud_metadata.get('modified')
            local_last_sync = local_metadata.get('modified')

            if cloud_modified and local_last_sync:
                # If cloud was modified after our last sync, we have a conflict
                if cloud_modified > local_last_sync:
                    # Load both versions for comparison
                    cloud_data = await self.cloud_backend.load_filesystem()

                    return {
                        'local_data': local_data,
                        'cloud_data': cloud_data,
                        'local_modified': local_last_sync,
                        'cloud_modified': cloud_modified
                    }

            return None

        except Exception as e:
            print(f"Error checking for conflicts: {e}")
            return None

    async def _handle_sync_error(self, error_msg: str):
        """Handle sync error with retry logic."""
        self.error_message = error_msg
        self.retry_count += 1

        if self.retry_count <= self.max_retries:
            # Exponential backoff: 5s, 10s, 20s
            retry_delay = 5 * (2 ** (self.retry_count - 1))

            self._notify_status(SyncStatus.ERROR, {
                'message': error_msg,
                'retry_in': retry_delay,
                'retry_attempt': self.retry_count
            })

            # Schedule retry
            await asyncio.sleep(retry_delay)
            if self.pending_data:  # Still have data to sync
                await self._perform_sync()
        else:
            # Max retries exceeded
            self._notify_status(SyncStatus.ERROR, {
                'message': f"Sync failed after {self.max_retries} attempts: {error_msg}",
                'retry_attempt': self.retry_count
            })

    async def force_sync(self) -> bool:
        """Force an immediate sync, bypassing debounce."""
        if self.pending_data:
            await self._perform_sync()
            return self.status == SyncStatus.SYNCED
        return True

    async def pull_from_cloud(self) -> Optional[dict]:
        """Pull latest filesystem from cloud."""
        try:
            self._notify_status(SyncStatus.SYNCING, {'operation': 'pull'})

            data = await self.cloud_backend.load_filesystem()

            if data:
                # Save to local cache
                await self.local_backend.save_filesystem(data)
                self.last_sync_time = datetime.now().isoformat()
                self._notify_status(SyncStatus.SYNCED, {'operation': 'pull'})
                return data
            else:
                self._notify_status(SyncStatus.IDLE)
                return None

        except Exception as e:
            self._notify_status(SyncStatus.ERROR, {'message': str(e)})
            return None

    async def resolve_conflict(self, resolution: str, merged_data: dict = None) -> bool:
        """
        Resolve a sync conflict.

        Args:
            resolution: 'local', 'cloud', or 'merge'
            merged_data: Required if resolution is 'merge'

        Returns:
            True if conflict resolved successfully
        """
        try:
            if resolution == 'local':
                # Use local version, overwrite cloud
                if self.pending_data:
                    await self.cloud_backend.save_filesystem(self.pending_data)
                    self.last_sync_time = datetime.now().isoformat()
                    self._notify_status(SyncStatus.SYNCED)
                    return True

            elif resolution == 'cloud':
                # Use cloud version, overwrite local
                cloud_data = await self.cloud_backend.load_filesystem()
                if cloud_data:
                    await self.local_backend.save_filesystem(cloud_data)
                    self.pending_data = cloud_data
                    self.last_sync_time = datetime.now().isoformat()
                    self._notify_status(SyncStatus.SYNCED)
                    return True

            elif resolution == 'merge':
                # Use merged data
                if merged_data:
                    await self.cloud_backend.save_filesystem(merged_data)
                    await self.local_backend.save_filesystem(merged_data)
                    self.pending_data = merged_data
                    self.last_sync_time = datetime.now().isoformat()
                    self._notify_status(SyncStatus.SYNCED)
                    return True

            return False

        except Exception as e:
            self._notify_status(SyncStatus.ERROR, {'message': f"Conflict resolution failed: {e}"})
            return False

    def get_status_summary(self) -> Dict[str, Any]:
        """Get current sync status summary."""
        return {
            'status': self.status.value,
            'last_sync': self.last_sync_time,
            'pending': self.pending_save,
            'retry_count': self.retry_count,
            'error': self.error_message
        }

    async def stop(self):
        """Stop sync queue and cleanup."""
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()

        if self._sync_task and not self._sync_task.done():
            self._sync_task.cancel()


def auto_merge_filesystems(local_data: dict, cloud_data: dict) -> dict:
    """
    Automatically merge two filesystem versions.

    Strategy:
    - Combine all files and directories from both versions
    - For files with same name, use the one with newer modified time
    - Keep all directories from both versions
    """
    from antioch.core.filesystem import FileSystemItem

    def merge_items(local_item: dict, cloud_item: dict) -> dict:
        """Merge two FileSystemItem dictionaries."""
        if local_item['type'] == 'file' and cloud_item['type'] == 'file':
            # Both are files - use newer one
            local_time = local_item.get('modified', '')
            cloud_time = cloud_item.get('modified', '')
            return local_item if local_time > cloud_time else cloud_item

        elif local_item['type'] == 'directory' and cloud_item['type'] == 'directory':
            # Both are directories - merge children
            merged = local_item.copy()
            local_children = local_item.get('children', {})
            cloud_children = cloud_item.get('children', {})

            # Combine children
            all_child_names = set(local_children.keys()) | set(cloud_children.keys())
            merged_children = {}

            for name in all_child_names:
                if name in local_children and name in cloud_children:
                    # Child exists in both - recurse
                    merged_children[name] = merge_items(local_children[name], cloud_children[name])
                elif name in local_children:
                    merged_children[name] = local_children[name]
                else:
                    merged_children[name] = cloud_children[name]

            merged['children'] = merged_children
            return merged

        else:
            # Type mismatch - use local
            return local_item

    # Merge the root items
    return merge_items(local_data, cloud_data)