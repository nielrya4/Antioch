#!/usr/bin/env python3
"""
Filesystem Demo for Antioch

Demonstrates the virtual filesystem with observer pattern and persistence.
"""

from antioch import DOM, Div, H2, P, Button, Pre, Ul, Li, Input, Span
from antioch.core import get_filesystem, LocalStorageBackend
import js


def main():
    """Demonstrate the virtual filesystem functionality."""

    # Create a container for the demo
    container = Div()
    container.style.padding = "20px"
    container.style.max_width = "800px"
    container.style.margin = "0 auto"

    # Title
    title = H2("Virtual Filesystem Demo")
    title.style.color = "#333"
    container.add(title)

    # Description
    desc = P("This demo shows the virtual filesystem with observer pattern. "
             "All changes persist across browser sessions using localStorage.")
    desc.style.color = "#666"
    container.add(desc)

    # Get the shared filesystem instance
    storage = LocalStorageBackend()
    fs = get_filesystem(storage)

    # Current path display
    path_display = Div()
    path_display.style.background_color = "#f0f0f0"
    path_display.style.padding = "10px"
    path_display.style.border_radius = "5px"
    path_display.style.margin_bottom = "20px"

    path_label = Span("Current Path: ")
    path_label.style.font_weight = "bold"
    path_text = Span(fs.get_path_string())
    path_display.add(path_label, path_text)

    container.add(path_display)

    # File list container
    file_list = Ul()
    file_list.style.list_style = "none"
    file_list.style.padding = "0"
    container.add(file_list)

    # Controls
    controls = Div()
    controls.style.margin_top = "20px"
    controls.style.display = "flex"
    controls.style.gap = "10px"
    controls.style.flex_wrap = "wrap"

    # File name input
    file_input = Input()
    file_input.set_attribute("type", "text")
    file_input.set_attribute("placeholder", "New file/folder name")
    file_input.style.padding = "8px"
    file_input.style.border = "1px solid #ddd"
    file_input.style.border_radius = "3px"
    controls.add(file_input)

    # Create file button
    create_file_btn = Button("Create File")
    create_file_btn.style.padding = "8px 15px"
    create_file_btn.style.background_color = "#4CAF50"
    create_file_btn.style.color = "white"
    create_file_btn.style.border = "none"
    create_file_btn.style.border_radius = "3px"
    create_file_btn.style.cursor = "pointer"

    # Create directory button
    create_dir_btn = Button("Create Folder")
    create_dir_btn.style.padding = "8px 15px"
    create_dir_btn.style.background_color = "#2196F3"
    create_dir_btn.style.color = "white"
    create_dir_btn.style.border = "none"
    create_dir_btn.style.border_radius = "3px"
    create_dir_btn.style.cursor = "pointer"

    # Go up button
    up_btn = Button("Go Up")
    up_btn.style.padding = "8px 15px"
    up_btn.style.background_color = "#FF9800"
    up_btn.style.color = "white"
    up_btn.style.border = "none"
    up_btn.style.border_radius = "3px"
    up_btn.style.cursor = "pointer"

    # Reset button
    reset_btn = Button("Reset Filesystem")
    reset_btn.style.padding = "8px 15px"
    reset_btn.style.background_color = "#f44336"
    reset_btn.style.color = "white"
    reset_btn.style.border = "none"
    reset_btn.style.border_radius = "3px"
    reset_btn.style.cursor = "pointer"

    controls.add(create_file_btn, create_dir_btn, up_btn, reset_btn)
    container.add(controls)

    # Observer log
    log_title = H2("Event Log")
    log_title.style.margin_top = "30px"
    log_title.style.color = "#333"
    container.add(log_title)

    log_display = Pre()
    log_display.style.background_color = "#f9f9f9"
    log_display.style.padding = "10px"
    log_display.style.border_radius = "5px"
    log_display.style.max_height = "200px"
    log_display.style.overflow = "auto"
    log_display.style.font_size = "12px"
    container.add(log_display)

    # Function to render the file list
    def render_files():
        # Clear the file list
        file_list._dom_element.innerHTML = ""

        items = fs.get_current_items()
        for item in items:
            # Create list item
            li_elem = Li()
            li_elem.style.padding = "8px"
            li_elem.style.margin = "5px 0"
            li_elem.style.background_color = "#fff"
            li_elem.style.border = "1px solid #ddd"
            li_elem.style.border_radius = "3px"
            li_elem.style.display = "flex"
            li_elem.style.justify_content = "space-between"
            li_elem.style.align_items = "center"

            # Item name and type
            icon = "📁" if item.is_directory() else "📄"
            name_span = Span(f"{icon} {item.name}")
            if item.is_directory():
                name_span.style.cursor = "pointer"
                name_span.style.color = "#2196F3"
                name_span.style.font_weight = "bold"

                # Navigation handler for directories
                def create_nav_handler(item_name):
                    def handler(event):
                        fs.navigate_to(fs.current_path + [item_name])
                    return handler

                name_span.on_click(create_nav_handler(item.name))

            # Delete button
            del_btn = Button("Delete")
            del_btn.style.padding = "4px 8px"
            del_btn.style.background_color = "#f44336"
            del_btn.style.color = "white"
            del_btn.style.border = "none"
            del_btn.style.border_radius = "3px"
            del_btn.style.cursor = "pointer"

            def create_delete_handler(item_name):
                def handler(event):
                    fs.delete_item(item_name)
                return handler

            del_btn.on_click(create_delete_handler(item.name))

            li_elem.add(name_span, del_btn)
            file_list.add(li_elem)

        # Update path display
        path_text.set_text(fs.get_path_string())

    # Observer callback
    def fs_observer(event_type, details):
        timestamp = js.Date.new().toLocaleTimeString()
        log_msg = f"[{timestamp}] {event_type.upper()}: {details}\n"
        log_display.set_text(log_msg + log_display._dom_element.textContent)
        render_files()

    # Register observer
    fs.add_observer(fs_observer)

    # Event handlers
    def on_create_file(event):
        name = file_input.value.strip()
        if name:
            if fs.create_file(name, f"Content of {name}"):
                file_input.value = ""
            else:
                js.alert(f"Failed to create file: {name} (may already exist)")

    def on_create_dir(event):
        name = file_input.value.strip()
        if name:
            if fs.create_directory(name):
                file_input.value = ""
            else:
                js.alert(f"Failed to create directory: {name} (may already exist)")

    def on_go_up(event):
        fs.go_up()

    def on_reset(event):
        if js.confirm("Are you sure you want to reset the filesystem? This will delete all files."):
            fs.reset_filesystem()

    create_file_btn.on_click(on_create_file)
    create_dir_btn.on_click(on_create_dir)
    up_btn.on_click(on_go_up)
    reset_btn.on_click(on_reset)

    # Add to DOM first
    DOM.add(container)

    # Initial render after DOM is ready
    render_files()


if __name__ == "__main__":
    main()