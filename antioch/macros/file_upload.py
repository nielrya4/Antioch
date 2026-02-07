"""
File Upload Macro - Upload files from the computer to the Virtual File System.
"""

import js
from pyodide.ffi import create_proxy
from antioch import Div, Button, P, Input, Label, Span, Strong
from antioch.macros.base import Macro
from antioch.core import get_filesystem


class FileUpload(Macro):
    """
    File upload UI for uploading files from the computer to the VFS.

    Args:
        destination_path: Default destination path in VFS (e.g., ['maps'])
        allowed_extensions: Optional list of allowed file extensions (e.g., ['.zip', '.tif'])
        max_size_mb: Maximum file size in MB (default 10)
        on_upload: Callback function(file_path, success) called after upload attempt
        multiple: Allow multiple file selection (default False)
        style: Optional style dictionary for the container
    """

    def __init__(self, destination_path=None, allowed_extensions=None, max_size_mb=10,
                 on_upload=None, multiple=False, style=None):
        super().__init__()

        self.destination_path = destination_path or []
        self.allowed_extensions = allowed_extensions or []
        self.max_size_mb = max_size_mb
        self.on_upload_callback = on_upload
        self.multiple = multiple

        # Get VFS instance
        self.fs = get_filesystem()

        # Create UI
        container_style = {
            "border": "2px dashed #ccc",
            "border_radius": "8px",
            "padding": "20px",
            "background": "#fafafa",
            "text_align": "center"
        }
        if style:
            container_style.update(style)

        self._root_element = Div(style=container_style)

        # Upload icon/text
        header = Div(style={"margin_bottom": "15px"})
        header.add(P("📁 Upload Files to Virtual File System", style={
            "font_size": "1.2em",
            "font_weight": "bold",
            "color": "#333",
            "margin": "0 0 5px 0"
        }))

        # Show destination path
        dest_text = "/" + "/".join(self.destination_path) if self.destination_path else "/"
        header.add(P(f"Destination: {dest_text}", style={
            "font_size": "0.9em",
            "color": "#666",
            "margin": "0"
        }))

        self.element.add(header)

        # File input (hidden)
        self.file_input = Input(input_type='file')
        self.file_input.set_attribute('id', f'file_input_{self.id}')
        self.file_input.style.display = 'none'
        if self.multiple:
            self.file_input.set_attribute('multiple', 'true')
        if self.allowed_extensions:
            accept = ','.join(self.allowed_extensions)
            self.file_input.set_attribute('accept', accept)

        self.element.add(self.file_input)

        # Upload button
        self.upload_btn = Button("Choose File" + ("s" if self.multiple else ""), style={
            "padding": "12px 24px",
            "background_color": "#2196f3",
            "color": "white",
            "border": "none",
            "border_radius": "4px",
            "cursor": "pointer",
            "font_size": "1em",
            "margin": "10px 0"
        })

        def trigger_file_input(e):
            self.file_input._dom_element.click()

        self.upload_btn.on_click(trigger_file_input)
        self.element.add(self.upload_btn)

        # Status message area
        self.status = Div(style={
            "margin_top": "15px",
            "min_height": "30px"
        })
        self.element.add(self.status)

        # Info text
        info_lines = []
        if self.allowed_extensions:
            info_lines.append(f"Allowed: {', '.join(self.allowed_extensions)}")
        info_lines.append(f"Max size: {self.max_size_mb} MB")

        info = P(" • ".join(info_lines), style={
            "font_size": "0.85em",
            "color": "#999",
            "margin": "10px 0 0 0"
        })
        self.element.add(info)

        # Set up file input change handler
        change_proxy = create_proxy(self._handle_file_change)
        self.file_input._dom_element.addEventListener('change', change_proxy)

    def _handle_file_change(self, event):
        """Handle file selection from input."""
        files = event.target.files

        if not files or files.length == 0:
            return

        # Clear previous status
        self._show_status("Processing files...", "info")

        # Process each file
        uploaded_count = 0
        failed_count = 0

        for i in range(files.length):
            file = files.item(i)
            success = self._upload_file(file)
            if success:
                uploaded_count += 1
            else:
                failed_count += 1

        # Show final status
        if failed_count == 0:
            msg = f"Successfully uploaded {uploaded_count} file" + ("s" if uploaded_count != 1 else "")
            self._show_status(msg, "success")
        else:
            msg = f"Uploaded {uploaded_count}, Failed {failed_count}"
            self._show_status(msg, "warning")

        # Reset file input
        event.target.value = ""

    def _upload_file(self, file):
        """Upload a single file to VFS."""
        file_name = file.name
        file_size = file.size

        # Validate file extension
        if self.allowed_extensions:
            valid_ext = any(file_name.endswith(ext) for ext in self.allowed_extensions)
            if not valid_ext:
                self._show_status(f"❌ {file_name}: Invalid file type", "error")
                return False

        # Validate file size
        max_bytes = self.max_size_mb * 1024 * 1024
        if file_size > max_bytes:
            self._show_status(f"❌ {file_name}: File too large", "error")
            return False

        try:
            # Read file content
            # For binary files, we need to read as ArrayBuffer
            reader = js.FileReader.new()

            # Determine if this is a binary file
            is_binary = self._is_binary_file(file_name)

            # Create a promise to handle async file reading
            def handle_load(event):
                try:
                    if is_binary:
                        # For binary files, get ArrayBuffer and convert to bytes
                        array_buffer = event.target.result
                        uint8_array = js.Uint8Array.new(array_buffer)
                        # Convert to Python bytes
                        content = bytes(uint8_array.to_py())
                    else:
                        # For text files, use the text result
                        content = event.target.result

                    # Save to VFS
                    original_path = list(self.fs.current_path)
                    self.fs.navigate_to(self.destination_path)

                    # Check if file exists
                    current_dir = self.fs.get_current_directory()
                    if file_name in current_dir.children:
                        # File exists, update it
                        print(f"Updating existing file: {file_name}")
                        self.fs.update_file_content(file_name, content)
                    else:
                        # Create new file
                        self.fs.create_file(file_name, content)

                    self.fs.navigate_to(original_path)

                    file_path = '/' + '/'.join(self.destination_path + [file_name])
                    print(f"✅ Uploaded: {file_path} ({self._format_size(file_size)})")

                    # Call upload callback
                    if self.on_upload_callback:
                        self.on_upload_callback(file_path, True)

                except Exception as e:
                    print(f"❌ Error uploading {file_name}: {str(e)}")
                    if self.on_upload_callback:
                        self.on_upload_callback(file_name, False)

            def handle_error(event):
                print(f"❌ Error reading {file_name}")
                if self.on_upload_callback:
                    self.on_upload_callback(file_name, False)

            load_proxy = create_proxy(handle_load)
            error_proxy = create_proxy(handle_error)

            reader.addEventListener('load', load_proxy)
            reader.addEventListener('error', error_proxy)

            if is_binary:
                reader.readAsArrayBuffer(file)
            else:
                reader.readAsText(file)

            return True

        except Exception as e:
            self._show_status(f"❌ Error: {str(e)}", "error")
            if self.on_upload_callback:
                self.on_upload_callback(file_name, False)
            return False

    def _is_binary_file(self, filename):
        """Determine if a file should be treated as binary."""
        binary_extensions = [
            '.zip', '.tif', '.tiff', '.png', '.jpg', '.jpeg', '.gif',
            '.pdf', '.exe', '.bin', '.dat', '.geotiff'
        ]
        return any(filename.lower().endswith(ext) for ext in binary_extensions)

    def _show_status(self, message, status_type="info"):
        """Show status message."""
        self.status._dom_element.innerHTML = ""

        color_map = {
            "info": "#2196f3",
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336"
        }

        bg_map = {
            "info": "#e3f2fd",
            "success": "#e8f5e9",
            "warning": "#fff3e0",
            "error": "#ffebee"
        }

        msg = P(message, style={
            "margin": "0",
            "padding": "10px",
            "background": bg_map.get(status_type, "#f5f5f5"),
            "color": color_map.get(status_type, "#333"),
            "border_radius": "4px",
            "font_size": "0.9em"
        })
        self.status.add(msg)

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

    def set_destination(self, path):
        """Update the destination path."""
        self.destination_path = path
        # Update the displayed destination
        dest_text = "/" + "/".join(self.destination_path) if self.destination_path else "/"
        # Could update the UI here if needed
        print(f"Destination changed to: {dest_text}")
