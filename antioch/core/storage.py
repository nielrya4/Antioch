#!/usr/bin/env python3
"""
Storage Backend Module for Antioch Core

Provides abstracted storage backends for persistent data storage
in browser environments.
"""

import js
import json
from typing import Optional, Protocol


class StorageBackend(Protocol):
    """Protocol defining the interface for storage backends."""

    def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to storage."""
        ...

    def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from storage."""
        ...

    def clear_filesystem(self) -> bool:
        """Clear filesystem data from storage."""
        ...


class LocalStorageBackend:
    """Storage backend using browser localStorage."""

    def __init__(self, storage_key: str = "antioch_filesystem"):
        self.storage_key = storage_key

    def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to browser localStorage."""
        try:
            json_data = json.dumps(filesystem_data)
            js.localStorage.setItem(self.storage_key, json_data)
            return True
        except Exception as e:
            print(f"Error saving filesystem to localStorage: {e}")
            return False

    def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from browser localStorage."""
        try:
            json_data = js.localStorage.getItem(self.storage_key)
            if json_data and json_data != "null":
                return json.loads(json_data)
            return None
        except Exception as e:
            print(f"Error loading filesystem from localStorage: {e}")
            return None

    def clear_filesystem(self) -> bool:
        """Clear filesystem data from browser localStorage."""
        try:
            js.localStorage.removeItem(self.storage_key)
            return True
        except Exception as e:
            print(f"Error clearing filesystem from localStorage: {e}")
            return False


class MemoryStorageBackend:
    """Storage backend using in-memory storage (for testing)."""

    def __init__(self):
        self._data = None

    def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to memory."""
        try:
            # Deep copy the data to simulate serialization
            self._data = json.loads(json.dumps(filesystem_data))
            return True
        except Exception as e:
            print(f"Error saving filesystem to memory: {e}")
            return False

    def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from memory."""
        try:
            if self._data is not None:
                # Deep copy the data to simulate deserialization
                return json.loads(json.dumps(self._data))
            return None
        except Exception as e:
            print(f"Error loading filesystem from memory: {e}")
            return None

    def clear_filesystem(self) -> bool:
        """Clear filesystem data from memory."""
        try:
            self._data = None
            return True
        except Exception as e:
            print(f"Error clearing filesystem from memory: {e}")
            return False


def create_storage_backend(backend_type: str = "localStorage", **kwargs) -> StorageBackend:
    """
    Factory function to create storage backends.

    Args:
        backend_type: Type of backend ('localStorage' or 'memory')
        **kwargs: Additional arguments passed to the backend constructor

    Returns:
        StorageBackend instance
    """
    if backend_type == "localStorage":
        return LocalStorageBackend(**kwargs)
    elif backend_type == "memory":
        return MemoryStorageBackend(**kwargs)
    else:
        raise ValueError(f"Unknown storage backend type: {backend_type}")