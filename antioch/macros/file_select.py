"""
File Select Macro - Browse and select files from the Virtual File System.
"""

from antioch import Div, Button, P, Span, Strong, Input
from antioch.macros.base import Macro
from antioch.core import get_filesystem


class FileSelect(Macro):
    """
    File selector UI for browsing and selecting files from the VFS.

    Args:
        on_select: Callback function(file_path, file_content) when a file is selected
        file_filter: Optional list of file extensions to filter (e.g., ['.zip', '.tif'])
        show_directories: Whether to show directory navigation (default True)
        height: Height of the file list container (default '300px')
        style: Optional style dictionary for the container
    """

    def __init__(self, on_select=None, file_filter=None, show_directories=True,
                 height='300px', style=None):
        super().__init__()

        self.on_select_callback = on_select
        self.file_filter = file_filter or []
        self.show_directories = show_directories
        self.height = height

        # Get VFS instance
        self.fs = get_filesystem()

        # Store current path
        self.current_path = list(self.fs.current_path)

        # Create UI
        container_style = {
            "border": "1px solid #ddd",
            "border_radius": "4px",
            "padding": "15px",
            "background": "#fff"
        }
        if style:
            container_style.update(style)

        self._root_element = Div(style=container_style)

        # Header with current path
        self.header = Div(style={
            "margin_bottom": "10px",
            "padding_bottom": "10px",
            "border_bottom": "1px solid #eee"
        })
        self.element.add(self.header)

        # Search/filter input
        if self.file_filter:
            filter_text = P(
                "Showing: ",
                Strong(", ".join(self.file_filter)),
                style={"font_size": "0.9em", "color": "#666", "margin": "5px 0"}
            )
            self.header.add(filter_text)

        # File list container
        self.file_list = Div(style={
            "max_height": self.height,
            "overflow_y": "auto",
            "border": "1px solid #eee",
            "border_radius": "4px",
            "padding": "5px"
        })
        self.element.add(self.file_list)

        # Render initial file list
        self._render_files()

    def _render_files(self):
        """Render the file list based on current path."""
        self.file_list._dom_element.innerHTML = ""

        # Update header with current path
        self.header._dom_element.innerHTML = ""

        path_display = Div(style={"display": "flex", "align_items": "center", "gap": "5px"})
        path_display.add(Strong("Path: "))

        # Add breadcrumb navigation
        if self.current_path:
            # Root button
            root_btn = Button("/", style={
                "padding": "3px 8px",
                "font_size": "0.9em",
                "background": "#f0f0f0",
                "border": "1px solid #ccc",
                "border_radius": "3px",
                "cursor": "pointer"
            })
            root_btn.on_click(lambda e: self._navigate_to([]))
            path_display.add(root_btn)

            # Path segments
            for i, segment in enumerate(self.current_path):
                path_display.add(Span(" / ", style={"color": "#999"}))

                segment_path = self.current_path[:i+1]
                seg_btn = Button(segment, style={
                    "padding": "3px 8px",
                    "font_size": "0.9em",
                    "background": "#f0f0f0",
                    "border": "1px solid #ccc",
                    "border_radius": "3px",
                    "cursor": "pointer"
                })
                seg_btn.on_click(lambda e, p=segment_path: self._navigate_to(p))
                path_display.add(seg_btn)
        else:
            path_display.add(Span("/", style={"color": "#666"}))

        self.header.add(path_display)

        # Add filter info if present
        if self.file_filter:
            filter_text = P(
                "Filter: ",
                Strong(", ".join(self.file_filter)),
                style={"font_size": "0.9em", "color": "#666", "margin": "5px 0"}
            )
            self.header.add(filter_text)

        # Get current directory contents
        try:
            # Navigate to the current path
            original_path = list(self.fs.current_path)
            self.fs.navigate_to(self.current_path)

            current_dir = self.fs.get_current_directory()

            # Restore original path
            self.fs.navigate_to(original_path)

            # List directories first
            if self.show_directories:
                directories = [name for name, item in current_dir.children.items()
                             if item.type == 'directory']

                for dir_name in sorted(directories):
                    self._create_directory_item(dir_name)

            # List files
            files = [(name, item) for name, item in current_dir.children.items()
                    if item.type == 'file']

            # Apply filter if specified
            if self.file_filter:
                files = [(name, item) for name, item in files
                        if any(name.endswith(ext) for ext in self.file_filter)]

            if not files and not (self.show_directories and directories):
                empty_msg = P(
                    "No files found" if self.file_filter else "This directory is empty",
                    style={
                        "padding": "20px",
                        "text_align": "center",
                        "color": "#999",
                        "font_style": "italic"
                    }
                )
                self.file_list.add(empty_msg)
            else:
                for file_name, file_item in sorted(files):
                    self._create_file_item(file_name, file_item)

        except Exception as e:
            error_msg = P(
                f"Error loading directory: {str(e)}",
                style={"color": "#d9534f", "padding": "10px"}
            )
            self.file_list.add(error_msg)

    def _create_directory_item(self, dir_name):
        """Create a directory list item."""
        item = Div(style={
            "padding": "8px 12px",
            "margin": "2px 0",
            "border_radius": "3px",
            "cursor": "pointer",
            "display": "flex",
            "align_items": "center",
            "gap": "8px",
            "background": "#f8f9fa"
        })

        # Folder icon
        icon = Span("📁", style={"font_size": "1.2em"})
        item.add(icon)

        # Directory name
        name = Span(dir_name, style={"font_weight": "500", "color": "#333"})
        item.add(name)

        # Hover effects
        def on_hover(e):
            item.style.background_color = "#e9ecef"

        def on_leave(e):
            item.style.background_color = "#f8f9fa"

        item.on_mouseenter(on_hover)
        item.on_mouseleave(on_leave)

        # Click to navigate
        def on_click(e):
            new_path = self.current_path + [dir_name]
            self._navigate_to(new_path)

        item.on_click(on_click)

        self.file_list.add(item)

    def _create_file_item(self, file_name, file_item):
        """Create a file list item."""
        item = Div(style={
            "padding": "8px 12px",
            "margin": "2px 0",
            "border_radius": "3px",
            "cursor": "pointer",
            "display": "flex",
            "align_items": "center",
            "justify_content": "space_between",
            "background": "#ffffff",
            "border": "1px solid #e9ecef"
        })

        left_section = Div(style={
            "display": "flex",
            "align_items": "center",
            "gap": "8px"
        })

        # File icon based on extension
        icon = self._get_file_icon(file_name)
        left_section.add(Span(icon, style={"font_size": "1.2em"}))

        # File name
        name = Span(file_name, style={"color": "#333"})
        left_section.add(name)

        item.add(left_section)

        # File size
        size_text = self._format_size(len(file_item.content) if file_item.content else 0)
        size = Span(size_text, style={
            "font_size": "0.85em",
            "color": "#999",
            "padding": "2px 6px",
            "background": "#f8f9fa",
            "border_radius": "3px"
        })
        item.add(size)

        # Hover effects
        def on_hover(e):
            item.style.background_color = "#e3f2fd"
            item.style.border_color = "#2196f3"

        def on_leave(e):
            item.style.background_color = "#ffffff"
            item.style.border_color = "#e9ecef"

        item.on_mouseenter(on_hover)
        item.on_mouseleave(on_leave)

        # Click to select
        def on_click(e):
            self._select_file(file_name, file_item)

        item.on_click(on_click)

        self.file_list.add(item)

    def _navigate_to(self, path):
        """Navigate to a specific path."""
        self.current_path = list(path)
        self._render_files()

    def _select_file(self, file_name, file_item):
        """Handle file selection."""
        # Construct full file path
        full_path = '/' + '/'.join(self.current_path + [file_name])

        # Call the callback if provided
        if self.on_select_callback:
            self.on_select_callback(full_path, file_item.content)

        print(f"Selected file: {full_path}")

    def _get_file_icon(self, filename):
        """Get an appropriate icon for the file type."""
        if filename.endswith('.zip'):
            return "🗜️"
        elif filename.endswith(('.tif', '.tiff', '.geotiff')):
            return "🗺️"
        elif filename.endswith(('.json', '.geojson')):
            return "📄"
        elif filename.endswith(('.shp', '.shx', '.dbf')):
            return "🗺️"
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return "🖼️"
        elif filename.endswith(('.txt', '.md')):
            return "📝"
        else:
            return "📄"

    def _format_size(self, size_bytes):
        """Format file size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

    def refresh(self):
        """Refresh the file list."""
        self._render_files()

    def set_filter(self, extensions):
        """Update the file filter."""
        self.file_filter = extensions or []
        self._render_files()

    def get_current_path(self):
        """Get the current path as a string."""
        return '/' + '/'.join(self.current_path)
