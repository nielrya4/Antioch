"""
Download Link macro - A reusable download link that can download from URLs, data strings, or VFS files
"""

from .base import Macro
from ..elements import A
from ..core.filesystem import get_filesystem
from typing import Optional
import base64


class DownloadLink(Macro):
    """
    A download link that can download from URLs, data strings, or VFS files.

    Examples:
        # Download from URL
        DownloadLink(href="https://example.com/file.pdf", filename="document.pdf", text="Download PDF")

        # Download from data string
        DownloadLink(data="Hello, World!", mimetype="text/plain", filename="hello.txt", text="Download Text")

        # Download from VFS
        DownloadLink(vfs_path="/documents/report.txt", filename="report.txt", text="Download Report")
    """

    def __init__(self,
                 href: Optional[str] = None,
                 data: Optional[str] = None,
                 vfs_path: Optional[str] = None,
                 mimetype: str = "application/octet-stream",
                 filename: str = "download",
                 text: str = "Download",
                 link_style: Optional[dict] = None):
        """
        Initialize a download link component.

        Args:
            href: URL to download from (mutually exclusive with data and vfs_path)
            data: Data string to download (mutually exclusive with href and vfs_path)
            vfs_path: Path to file in VFS (mutually exclusive with href and data)
            mimetype: MIME type for the download (default: application/octet-stream)
            filename: Name for the downloaded file
            text: Text displayed in the link
            link_style: Style dict for the link element
        """
        # Initialize base macro
        super().__init__(macro_type="download_link")

        # Validate that exactly one source is provided
        sources = sum([href is not None, data is not None, vfs_path is not None])
        if sources == 0:
            raise ValueError("Must provide one of: href, data, or vfs_path")
        if sources > 1:
            raise ValueError("Cannot provide multiple sources (href, data, vfs_path)")

        # Set up state
        self._set_state(
            href=href,
            data=data,
            vfs_path=vfs_path,
            mimetype=mimetype,
            filename=filename,
            text=text
        )

        # Store user-provided style (no defaults)
        self._link_style = link_style or {}

        # Initialize macro
        self._init_macro()

    def _create_elements(self):
        """Create the download link element."""
        # Get the href for the download
        download_href = self._get_download_href()

        # Create the anchor element
        link = self._register_element('link',
            A(self._get_state('text'),
              href=download_href,
              download=self._get_state('filename'),
              style=self._link_style))

        return link

    def _get_download_href(self) -> str:
        """Generate the appropriate href based on the source type."""
        href = self._get_state('href')
        data = self._get_state('data')
        vfs_path = self._get_state('vfs_path')
        mimetype = self._get_state('mimetype')

        # Direct URL
        if href:
            return href

        # Data string
        if data:
            # Encode data as base64 for binary safety
            encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            return f"data:{mimetype};base64,{encoded_data}"

        # VFS file
        if vfs_path:
            vfs = get_filesystem()

            # Parse the path
            path_parts = [p for p in vfs_path.split('/') if p]

            if not path_parts:
                raise ValueError(f"Invalid VFS path: {vfs_path}")

            # Navigate the tree to find the file
            current_item = vfs.root

            # Navigate through directories
            for part in path_parts[:-1]:
                current_item = current_item.get_child(part)
                if not current_item or not current_item.is_directory():
                    raise FileNotFoundError(f"Directory not found in VFS path: {vfs_path}")

            # Get the file
            filename = path_parts[-1]
            file_item = current_item.get_child(filename)

            if not file_item or not file_item.is_file():
                raise FileNotFoundError(f"File not found in VFS: {vfs_path}")

            content = file_item.content

            # Encode as base64
            encoded_data = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            return f"data:{mimetype};base64,{encoded_data}"

        return "#"

    def update_text(self, text: str):
        """Update the link text."""
        self._set_state(text=text)
        link = self._get_element('link')
        link.set_text(text)
        return self

    def update_source(self, href: Optional[str] = None,
                     data: Optional[str] = None,
                     vfs_path: Optional[str] = None):
        """
        Update the download source.

        Args:
            href: New URL to download from
            data: New data string to download
            vfs_path: New VFS path to download from
        """
        # Validate that exactly one source is provided
        sources = sum([href is not None, data is not None, vfs_path is not None])
        if sources != 1:
            raise ValueError("Must provide exactly one of: href, data, or vfs_path")

        # Update state
        self._set_state(
            href=href if href is not None else None,
            data=data if data is not None else None,
            vfs_path=vfs_path if vfs_path is not None else None
        )

        # Update the link href
        link = self._get_element('link')
        link.set_attribute('href', self._get_download_href())

        return self

    def update_filename(self, filename: str):
        """Update the download filename."""
        self._set_state(filename=filename)
        link = self._get_element('link')
        link.set_attribute('download', filename)
        return self