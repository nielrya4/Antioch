#!/usr/bin/env python3
"""
Async Storage Backend Module for Antioch Core

Provides async storage backends for cloud sync and network operations.
"""

import js
import json
import asyncio
from typing import Optional, Protocol, Dict, Any
from datetime import datetime


class AsyncStorageBackend(Protocol):
    """Protocol defining the interface for async storage backends."""

    async def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to storage asynchronously."""
        ...

    async def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from storage asynchronously."""
        ...

    async def clear_filesystem(self) -> bool:
        """Clear filesystem data from storage asynchronously."""
        ...

    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get metadata about stored filesystem (modified time, version, etc.)."""
        ...


class AsyncLocalStorageBackend:
    """Async wrapper for browser localStorage (for consistent interface)."""

    def __init__(self, storage_key: str = "antioch_filesystem"):
        self.storage_key = storage_key
        self.metadata_key = f"{storage_key}_metadata"

    async def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to browser localStorage."""
        try:
            json_data = json.dumps(filesystem_data)
            js.localStorage.setItem(self.storage_key, json_data)

            # Save metadata
            metadata = {
                'modified': datetime.now().isoformat(),
                'size': len(json_data),
                'version': 1
            }
            js.localStorage.setItem(self.metadata_key, json.dumps(metadata))
            return True
        except Exception as e:
            print(f"Error saving filesystem to localStorage: {e}")
            return False

    async def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from browser localStorage."""
        try:
            json_data = js.localStorage.getItem(self.storage_key)
            if json_data and json_data != "null":
                return json.loads(json_data)
            return None
        except Exception as e:
            print(f"Error loading filesystem from localStorage: {e}")
            return None

    async def clear_filesystem(self) -> bool:
        """Clear filesystem data from browser localStorage."""
        try:
            js.localStorage.removeItem(self.storage_key)
            js.localStorage.removeItem(self.metadata_key)
            return True
        except Exception as e:
            print(f"Error clearing filesystem from localStorage: {e}")
            return False

    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get metadata about stored filesystem."""
        try:
            metadata_json = js.localStorage.getItem(self.metadata_key)
            if metadata_json and metadata_json != "null":
                return json.loads(metadata_json)
            return None
        except Exception as e:
            print(f"Error loading metadata: {e}")
            return None


class GoogleDriveBackend:
    """Storage backend using Google Drive API."""

    def __init__(self,
                 client_id: str,
                 api_key: str = None,
                 filename: str = "antioch_filesystem.json",
                 app_folder: bool = True):
        """
        Initialize Google Drive backend.

        Args:
            client_id: Google OAuth2 client ID
            api_key: Optional Google API key for public data
            filename: Name of the file to store in Drive
            app_folder: If True, use application folder (recommended)
        """
        self.client_id = client_id
        self.api_key = api_key
        self.filename = filename
        self.app_folder = app_folder
        self.file_id = None
        self.access_token = None
        self.token_expiry = None
        self._initialized = False
        self._auth_ready = asyncio.Event()

    async def initialize(self):
        """Initialize Google API client and authenticate."""
        if self._initialized:
            return True

        try:
            # Load Google API client library
            await self._load_google_api()

            # Initialize the Google API client
            await self._init_google_client()

            self._initialized = True
            self._auth_ready.set()
            return True
        except Exception as e:
            print(f"Failed to initialize Google Drive: {e}")
            return False

    async def _load_google_api(self):
        """Load Google API client library if not already loaded."""
        # Check if gapi is already loaded
        if hasattr(js, 'gapi') and js.gapi:
            return

        # Create a promise to wait for script load
        from pyodide.ffi import create_proxy

        def create_load_promise():
            promise = js.Promise.new(create_proxy(lambda resolve, reject: None))
            return promise

        # Inject Google API script
        script = js.document.createElement('script')
        script.src = 'https://apis.google.com/js/api.js'
        script.setAttribute('async', '')

        load_event = asyncio.Event()

        def on_load(event):
            load_event.set()

        script.onload = create_proxy(on_load)
        js.document.head.appendChild(script)

        await load_event.wait()

        # Wait for gapi to be available
        while not hasattr(js, 'gapi'):
            await asyncio.sleep(0.1)

    async def _init_google_client(self):
        """Initialize Google API client."""
        from pyodide.ffi import create_proxy

        # Initialize gapi client
        init_promise = asyncio.Event()

        def on_gapi_load():
            init_promise.set()

        js.gapi.load('client:auth2', create_proxy(on_gapi_load))
        await init_promise.wait()

        # Initialize client with OAuth2
        config = js.Object.new()
        config.apiKey = self.api_key if self.api_key else ''
        config.clientId = self.client_id
        config.discoveryDocs = ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest']
        config.scope = 'https://www.googleapis.com/auth/drive.file' if self.app_folder else 'https://www.googleapis.com/auth/drive'

        await js.gapi.client.init(config)

    async def authenticate(self) -> bool:
        """
        Authenticate with Google and get access token.
        Shows OAuth popup to user.
        """
        try:
            await self._auth_ready.wait()

            auth_instance = js.gapi.auth2.getAuthInstance()

            # Check if already signed in
            if auth_instance.isSignedIn.get():
                user = auth_instance.currentUser.get()
                auth_response = user.getAuthResponse(True)
                self.access_token = auth_response.access_token
                self.token_expiry = auth_response.expires_at
                return True

            # Sign in with popup
            from pyodide.ffi import create_proxy

            try:
                user = await auth_instance.signIn()
                auth_response = user.getAuthResponse(True)
                self.access_token = auth_response.access_token
                self.token_expiry = auth_response.expires_at
                return True
            except Exception as e:
                print(f"Authentication failed: {e}")
                return False

        except Exception as e:
            print(f"Error during authentication: {e}")
            return False

    async def _ensure_authenticated(self):
        """Ensure we have a valid access token."""
        if not self.access_token:
            success = await self.authenticate()
            if not success:
                raise Exception("Authentication required")

        # Check if token expired
        if self.token_expiry:
            now = datetime.now().timestamp() * 1000  # Convert to ms
            if now >= self.token_expiry:
                # Refresh token
                auth_instance = js.gapi.auth2.getAuthInstance()
                user = auth_instance.currentUser.get()
                auth_response = await user.reloadAuthResponse()
                self.access_token = auth_response.access_token
                self.token_expiry = auth_response.expires_at

    async def _find_file(self) -> Optional[str]:
        """Find the filesystem file in Google Drive."""
        await self._ensure_authenticated()

        try:
            # Search for file
            query = f"name='{self.filename}' and trashed=false"
            if self.app_folder:
                query += " and 'appDataFolder' in parents"

            response = await js.gapi.client.drive.files.list(js.Object.fromEntries([
                ['q', query],
                ['spaces', 'appDataFolder' if self.app_folder else 'drive'],
                ['fields', 'files(id, name, modifiedTime)']
            ]))

            files = response.result.files
            if files and len(files) > 0:
                return files[0].id
            return None
        except Exception as e:
            print(f"Error finding file: {e}")
            return None

    async def save_filesystem(self, filesystem_data: dict) -> bool:
        """Save filesystem data to Google Drive."""
        try:
            await self._ensure_authenticated()

            json_data = json.dumps(filesystem_data)

            # Create file metadata
            file_metadata = js.Object.new()
            file_metadata.name = self.filename
            file_metadata.mimeType = 'application/json'

            if self.app_folder:
                file_metadata.parents = ['appDataFolder']

            # Check if file exists
            if not self.file_id:
                self.file_id = await self._find_file()

            # Create or update file
            if self.file_id:
                # Update existing file
                response = await js.gapi.client.request(js.Object.fromEntries([
                    ['path', f'/upload/drive/v3/files/{self.file_id}'],
                    ['method', 'PATCH'],
                    ['params', js.Object.fromEntries([['uploadType', 'media']])],
                    ['body', json_data]
                ]))
            else:
                # Create new file
                boundary = '-------314159265358979323846'
                delimiter = f"\r\n--{boundary}\r\n"
                close_delim = f"\r\n--{boundary}--"

                multipart_body = (
                    delimiter +
                    'Content-Type: application/json\r\n\r\n' +
                    json.dumps({
                        'name': self.filename,
                        'mimeType': 'application/json',
                        'parents': ['appDataFolder'] if self.app_folder else []
                    }) +
                    delimiter +
                    'Content-Type: application/json\r\n\r\n' +
                    json_data +
                    close_delim
                )

                response = await js.gapi.client.request(js.Object.fromEntries([
                    ['path', '/upload/drive/v3/files'],
                    ['method', 'POST'],
                    ['params', js.Object.fromEntries([['uploadType', 'multipart']])],
                    ['headers', js.Object.fromEntries([['Content-Type', f'multipart/related; boundary={boundary}']])],
                    ['body', multipart_body]
                ]))

                self.file_id = response.result.id

            return True

        except Exception as e:
            print(f"Error saving to Google Drive: {e}")
            return False

    async def load_filesystem(self) -> Optional[dict]:
        """Load filesystem data from Google Drive."""
        try:
            await self._ensure_authenticated()

            # Find file if we don't have ID
            if not self.file_id:
                self.file_id = await self._find_file()

            if not self.file_id:
                return None

            # Download file content
            response = await js.gapi.client.drive.files.get(js.Object.fromEntries([
                ['fileId', self.file_id],
                ['alt', 'media']
            ]))

            # Parse JSON
            return json.loads(response.body)

        except Exception as e:
            print(f"Error loading from Google Drive: {e}")
            return None

    async def clear_filesystem(self) -> bool:
        """Delete the filesystem file from Google Drive."""
        try:
            await self._ensure_authenticated()

            if not self.file_id:
                self.file_id = await self._find_file()

            if not self.file_id:
                return True  # Nothing to delete

            await js.gapi.client.drive.files.delete(js.Object.fromEntries([
                ['fileId', self.file_id]
            ]))

            self.file_id = None
            return True

        except Exception as e:
            print(f"Error clearing Google Drive file: {e}")
            return False

    async def get_metadata(self) -> Optional[Dict[str, Any]]:
        """Get metadata about stored filesystem."""
        try:
            await self._ensure_authenticated()

            if not self.file_id:
                self.file_id = await self._find_file()

            if not self.file_id:
                return None

            response = await js.gapi.client.drive.files.get(js.Object.fromEntries([
                ['fileId', self.file_id],
                ['fields', 'id,name,modifiedTime,size,version']
            ]))

            result = response.result
            return {
                'id': result.id,
                'name': result.name,
                'modified': result.modifiedTime,
                'size': int(result.size) if hasattr(result, 'size') else 0,
                'version': int(result.version) if hasattr(result, 'version') else 1
            }

        except Exception as e:
            print(f"Error getting metadata: {e}")
            return None

    async def disconnect(self):
        """Disconnect from Google Drive (sign out)."""
        try:
            if hasattr(js, 'gapi') and js.gapi.auth2:
                auth_instance = js.gapi.auth2.getAuthInstance()
                if auth_instance and auth_instance.isSignedIn.get():
                    await auth_instance.signOut()

            self.access_token = None
            self.token_expiry = None
            self.file_id = None
        except Exception as e:
            print(f"Error disconnecting: {e}")