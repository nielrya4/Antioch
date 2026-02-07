#!/usr/bin/env python3
"""
Core Virtual File System Module for Antioch

Provides abstracted file system operations for virtual files and directories
in a browser environment using Pyodide.
"""

from typing import Dict, List, Optional
from datetime import datetime


class FileSystemItem:
    """Represents a file or directory in the virtual file system."""

    def __init__(self, name: str, item_type: str, size: int = 0,
                 modified: Optional[str] = None, content: str = ""):
        self.name = name
        self.type = item_type  # 'file' or 'directory'
        self.size = size
        self.modified = modified or datetime.now().isoformat()
        self.content = content
        self.children: Dict[str, 'FileSystemItem'] = {}

    def is_directory(self) -> bool:
        return self.type == 'directory'

    def is_file(self) -> bool:
        return self.type == 'file'

    def add_child(self, item: 'FileSystemItem'):
        """Add a child item (for directories)."""
        if self.is_directory():
            self.children[item.name] = item

    def get_child(self, name: str) -> Optional['FileSystemItem']:
        """Get a child item by name."""
        return self.children.get(name)

    def remove_child(self, name: str) -> bool:
        """Remove a child item."""
        if name in self.children:
            del self.children[name]
            return True
        return False

    def get_extension(self) -> str:
        """Get file extension."""
        if self.is_file() and '.' in self.name:
            return self.name.split('.')[-1].lower()
        return ""

    def to_dict(self) -> dict:
        """Convert FileSystemItem to dictionary for serialization."""
        return {
            'name': self.name,
            'type': self.type,
            'size': self.size,
            'modified': self.modified,
            'content': self.content,
            'children': {name: child.to_dict() for name, child in self.children.items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'FileSystemItem':
        """Create FileSystemItem from dictionary."""
        item = cls(
            name=data['name'],
            item_type=data['type'],
            size=data.get('size', 0),
            modified=data.get('modified'),
            content=data.get('content', '')
        )

        # Recursively create children
        if 'children' in data:
            for child_name, child_data in data['children'].items():
                child_item = cls.from_dict(child_data)
                item.add_child(child_item)

        return item


class VirtualFileSystem:
    """
    Manages a virtual file system for the browser environment.

    Includes built-in observer pattern for universal observability across
    all calls, and singleton pattern to ensure shared state.
    """

    _instance: Optional['VirtualFileSystem'] = None
    _observers = []

    def __new__(cls, storage_backend=None):
        """Ensure only one instance exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, storage_backend=None):
        # Only initialize once
        if self._initialized:
            return

        self.current_path = []
        self.storage_backend = storage_backend
        self._load_or_create_filesystem()
        self._initialized = True

    def _load_or_create_filesystem(self):
        """Load filesystem from storage or create default if none exists."""
        if self.storage_backend:
            stored_data = self.storage_backend.load_filesystem()
            if stored_data:
                self.root = FileSystemItem.from_dict(stored_data)
                print("Loaded filesystem from storage")
                return

        # Create new filesystem with defaults
        self.root = FileSystemItem("root", "directory")
        self._setup_default_files()
        self._save_filesystem()
        print("Created new filesystem with default files")

    def _setup_default_files(self):
        """Create some default files and directories."""
        # Create documents directory
        docs_dir = FileSystemItem("documents", "directory")
        self.root.add_child(docs_dir)

        readme = FileSystemItem("README.txt", "file", 100,
                               content="Welcome to Antioch Virtual File System!\n\nThis is a browser-based file system that persists across sessions.")
        docs_dir.add_child(readme)

        # Create data directory
        data_dir = FileSystemItem("data", "directory")
        self.root.add_child(data_dir)

        sample_json = FileSystemItem("sample.json", "file", 50,
                                    content='{\n  "name": "Example",\n  "value": 42\n}')
        data_dir.add_child(sample_json)

        # Create scripts directory
        scripts_dir = FileSystemItem("scripts", "directory")
        self.root.add_child(scripts_dir)

        hello_py = FileSystemItem("hello.py", "file", 80,
                                 content="# Sample Python script\nprint('Hello from Antioch!')")
        scripts_dir.add_child(hello_py)

    def _save_filesystem(self):
        """Save the current filesystem to storage."""
        if self.storage_backend:
            self.storage_backend.save_filesystem(self.root.to_dict())

    def add_observer(self, callback) -> None:
        """
        Add an observer that will be notified of filesystem changes.

        Args:
            callback: Function to call when filesystem changes occur.
                     Should accept (event_type, details) parameters.
        """
        if callback not in self._observers:
            self._observers.append(callback)

    def remove_observer(self, callback) -> None:
        """Remove an observer."""
        if callback in self._observers:
            self._observers.remove(callback)

    def _notify_observers(self, event_type: str, details: dict = None) -> None:
        """
        Notify all observers of a filesystem change.

        Args:
            event_type: Type of change ('create', 'delete', 'modify', 'navigate', 'rename', 'reset')
            details: Additional details about the change
        """
        details = details or {}

        for callback in self._observers[:]:  # Use slice to avoid issues if observers are modified
            try:
                callback(event_type, details)
            except Exception as e:
                print(f"Error in filesystem observer: {e}")

    def get_current_directory(self) -> FileSystemItem:
        """Get the current directory."""
        current = self.root
        for part in self.current_path:
            current = current.get_child(part)
            if not current or not current.is_directory():
                # Reset to root if path is invalid
                self.current_path = []
                return self.root
        return current

    def navigate_to(self, path: List[str]) -> bool:
        """Navigate to a specific path and notify observers."""
        # Test if path exists
        current = self.root
        for part in path:
            current = current.get_child(part)
            if not current or not current.is_directory():
                return False

        self.current_path = path[:]
        self._notify_observers('navigate', {
            'path': self.get_path_string(),
            'current_items': len(self.get_current_items())
        })
        return True

    def go_up(self) -> bool:
        """Navigate to parent directory and notify observers."""
        if self.current_path:
            self.current_path.pop()
            self._notify_observers('navigate', {
                'path': self.get_path_string(),
                'current_items': len(self.get_current_items())
            })
            return True
        return False

    def create_file(self, name: str, content: str = "") -> bool:
        """Create a new file in current directory and notify observers."""
        current_dir = self.get_current_directory()
        if current_dir.get_child(name):
            return False  # File already exists

        file_item = FileSystemItem(name, "file", len(content), content=content)
        current_dir.add_child(file_item)
        self._save_filesystem()
        self._notify_observers('create', {
            'type': 'file',
            'name': name,
            'path': self.get_path_string()
        })
        return True

    def create_directory(self, name: str) -> bool:
        """Create a new directory in current directory and notify observers."""
        current_dir = self.get_current_directory()
        if current_dir.get_child(name):
            return False  # Directory already exists

        dir_item = FileSystemItem(name, "directory")
        current_dir.add_child(dir_item)
        self._save_filesystem()
        self._notify_observers('create', {
            'type': 'directory',
            'name': name,
            'path': self.get_path_string()
        })
        return True

    def delete_item(self, name: str) -> bool:
        """Delete a file or directory and notify observers."""
        current_dir = self.get_current_directory()
        success = current_dir.remove_child(name)
        if success:
            self._save_filesystem()
            self._notify_observers('delete', {
                'name': name,
                'path': self.get_path_string()
            })
        return success

    def rename_item(self, old_name: str, new_name: str) -> bool:
        """Rename a file or directory and notify observers."""
        current_dir = self.get_current_directory()
        item = current_dir.get_child(old_name)

        if not item or current_dir.get_child(new_name):
            return False  # Item doesn't exist or new name already taken

        # Update the name
        item.name = new_name
        item.modified = datetime.now().isoformat()

        # Update the dictionary key
        current_dir.children[new_name] = item
        del current_dir.children[old_name]

        self._save_filesystem()
        self._notify_observers('rename', {
            'old_name': old_name,
            'new_name': new_name,
            'path': self.get_path_string()
        })
        return True

    def get_current_items(self) -> List[FileSystemItem]:
        """Get items in current directory."""
        current_dir = self.get_current_directory()
        return list(current_dir.children.values())

    def get_path_string(self) -> str:
        """Get current path as string."""
        if not self.current_path:
            return "/"
        return "/" + "/".join(self.current_path)

    def get_file_content(self, name: str) -> Optional[str]:
        """Get content of a file in the current directory."""
        current_dir = self.get_current_directory()
        file_item = current_dir.get_child(name)
        if file_item and file_item.is_file():
            return file_item.content
        return None

    def update_file_content(self, name: str, content: str) -> bool:
        """Update content of a file in the current directory and notify observers."""
        current_dir = self.get_current_directory()
        file_item = current_dir.get_child(name)
        if file_item and file_item.is_file():
            file_item.content = content
            file_item.size = len(content)
            file_item.modified = datetime.now().isoformat()
            self._save_filesystem()
            self._notify_observers('modify', {
                'type': 'file',
                'name': name,
                'path': self.get_path_string(),
                'size': file_item.size
            })
            return True
        return False

    def get_item_by_path(self, path: str) -> Optional[FileSystemItem]:
        """Get an item by its absolute path."""
        if path == "/" or path == "":
            return self.root

        # Remove leading/trailing slashes and split
        path_parts = path.strip("/").split("/")
        current = self.root

        for part in path_parts:
            current = current.get_child(part)
            if not current:
                return None

        return current

    def reset_filesystem(self):
        """Reset the filesystem to defaults, clear storage, and notify observers."""
        if self.storage_backend:
            self.storage_backend.clear_filesystem()

        self.root = FileSystemItem("root", "directory")
        self.current_path = []
        self._setup_default_files()
        self._save_filesystem()
        self._notify_observers('reset', {})
        print("Filesystem reset to defaults")


# Global function to get the shared filesystem instance
def get_filesystem(storage_backend=None) -> VirtualFileSystem:
    """
    Get the shared filesystem instance.

    This is the recommended way to access the filesystem.
    It ensures a singleton instance is used throughout the application.

    Args:
        storage_backend: Optional storage backend (only used on first call)

    Returns:
        Shared VirtualFileSystem instance
    """
    return VirtualFileSystem(storage_backend)
