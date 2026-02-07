"""
Antioch Core Module

Core functionality for the Antioch framework including virtual file system
operations and storage backends with built-in observer pattern and persistence.
"""

from .filesystem import VirtualFileSystem, FileSystemItem, get_filesystem
from .storage import LocalStorageBackend, MemoryStorageBackend, create_storage_backend
from .async_storage import AsyncLocalStorageBackend, GoogleDriveBackend, AsyncStorageBackend
from .sync_queue import SyncQueue, SyncStatus, auto_merge_filesystems

__all__ = [
    # Filesystem
    'VirtualFileSystem',
    'FileSystemItem',
    'get_filesystem',

    # Sync Storage backends
    'LocalStorageBackend',
    'MemoryStorageBackend',
    'create_storage_backend',

    # Async Storage backends
    'AsyncLocalStorageBackend',
    'GoogleDriveBackend',
    'AsyncStorageBackend',

    # Sync Queue
    'SyncQueue',
    'SyncStatus',
    'auto_merge_filesystems',
]
