"""
File Select Demo - Demonstration of the FileSelect macro.
Shows how to browse and select files from the Virtual File System.
"""

from antioch import Div, H1, H2, P, Button, DOM
from antioch.macros import FileSelect
from antioch.core import get_filesystem, LocalStorageBackend


def main():
    """Main entry point for FileSelect demo."""
    # Get or initialize filesystem
    fs = get_filesystem(LocalStorageBackend())

    # Create some demo files if the filesystem is empty
    _create_demo_files(fs)

    # Create page container
    page = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Add title
    page.add(H1("File Select Demo", style={
        "color": "#333",
        "margin_bottom": "10px"
    }))

    # Add description
    page.add(P(
        "Browse and select files from the Virtual File System. "
        "The FileSelect macro provides a file browser UI for picking files stored in the VFS.",
        style={"color": "#666", "margin_bottom": "30px"}
    ))

    # Section 1: Basic file selector
    section1 = Div(style={"margin_bottom": "40px"})
    section1.add(H2("Basic File Selector", style={"color": "#444", "margin_bottom": "10px"}))
    section1.add(P(
        "Select any file from the filesystem:",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Selected file display
    selected_display1 = Div(style={
        "padding": "15px",
        "background": "#e3f2fd",
        "border_left": "4px solid #2196f3",
        "border_radius": "4px",
        "margin_bottom": "15px"
    })
    selected_display1.add(P("No file selected", style={"margin": "0", "color": "#666"}))
    section1.add(selected_display1)

    def on_file_selected1(file_path, file_content):
        selected_display1._dom_element.innerHTML = ""
        size = len(file_content) if file_content else 0
        selected_display1.add(P(
            f"Selected: {file_path} ({_format_size(size)})",
            style={"margin": "0", "color": "#333", "font_weight": "bold"}
        ))
        if file_content:
            preview = file_content[:200] if isinstance(file_content, str) else f"Binary data ({size} bytes)"
            selected_display1.add(P(
                f"Preview: {preview}...",
                style={"margin": "5px 0 0 0", "color": "#666", "font_family": "monospace", "font_size": "0.9em"}
            ))

    file_select1 = FileSelect(on_select=on_file_selected1, height='250px')
    section1.add(file_select1)

    page.add(section1)

    # Section 2: Filtered file selector (geospatial files only)
    section2 = Div(style={"margin_bottom": "40px"})
    section2.add(H2("Filtered File Selector", style={"color": "#444", "margin_bottom": "10px"}))
    section2.add(P(
        "Only show geospatial files (.zip, .tif, .geojson):",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Selected file display
    selected_display2 = Div(style={
        "padding": "15px",
        "background": "#f1f8e9",
        "border_left": "4px solid #8bc34a",
        "border_radius": "4px",
        "margin_bottom": "15px"
    })
    selected_display2.add(P("No geospatial file selected", style={"margin": "0", "color": "#666"}))
    section2.add(selected_display2)

    def on_file_selected2(file_path, file_content):
        selected_display2._dom_element.innerHTML = ""
        size = len(file_content) if file_content else 0
        selected_display2.add(P(
            f"Selected: {file_path} ({_format_size(size)})",
            style={"margin": "0", "color": "#333", "font_weight": "bold"}
        ))

    file_select2 = FileSelect(
        on_select=on_file_selected2,
        file_filter=['.zip', '.tif', '.tiff', '.geotiff', '.geojson', '.json'],
        height='250px'
    )
    section2.add(file_select2)

    page.add(section2)

    # Section 3: Compact selector without directory navigation
    section3 = Div(style={"margin_bottom": "40px"})
    section3.add(H2("Compact Selector (No Directories)", style={"color": "#444", "margin_bottom": "10px"}))
    section3.add(P(
        "Show only files in the current directory:",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Selected file display
    selected_display3 = Div(style={
        "padding": "15px",
        "background": "#fff3e0",
        "border_left": "4px solid #ff9800",
        "border_radius": "4px",
        "margin_bottom": "15px"
    })
    selected_display3.add(P("No file selected", style={"margin": "0", "color": "#666"}))
    section3.add(selected_display3)

    def on_file_selected3(file_path, file_content):
        selected_display3._dom_element.innerHTML = ""
        size = len(file_content) if file_content else 0
        selected_display3.add(P(
            f"Selected: {file_path} ({_format_size(size)})",
            style={"margin": "0", "color": "#333", "font_weight": "bold"}
        ))

    file_select3 = FileSelect(
        on_select=on_file_selected3,
        show_directories=False,
        height='200px'
    )
    section3.add(file_select3)

    page.add(section3)

    # Add refresh button
    refresh_section = Div(style={
        "margin_top": "30px",
        "padding": "20px",
        "background": "#f8f9fa",
        "border_radius": "4px"
    })

    refresh_btn = Button("Refresh All File Lists", style={
        "padding": "10px 20px",
        "background_color": "#2196f3",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "1em"
    })

    def refresh_all(e):
        file_select1.refresh()
        file_select2.refresh()
        file_select3.refresh()
        print("All file lists refreshed")

    refresh_btn.on_click(refresh_all)
    refresh_section.add(refresh_btn)

    page.add(refresh_section)

    # Add page to DOM
    DOM.add(page)

    print("✅ File Select Demo loaded!")


def _create_demo_files(fs):
    """Create some demo files if filesystem is empty."""
    # Check if we already have files
    if len(fs.root.children) > 0:
        return

    print("Creating demo files...")

    # Create directories
    fs.navigate_to([])
    try:
        fs.create_directory('maps')
        fs.create_directory('documents')
        fs.create_directory('data')
    except:
        pass  # Directories might already exist

    # Create some demo files
    try:
        fs.navigate_to(['maps'])
        fs.create_file('example.geojson', '{"type": "FeatureCollection", "features": []}')
        fs.create_file('elevation.tif', b'FAKE_TIFF_DATA')  # Binary data

        fs.navigate_to(['documents'])
        fs.create_file('readme.txt', 'This is a demo file system.\n\nYou can upload your own files here!')
        fs.create_file('notes.md', '# Notes\n\n- Item 1\n- Item 2\n- Item 3')

        fs.navigate_to(['data'])
        fs.create_file('shapefile.zip', b'FAKE_ZIP_DATA')  # Binary data
        fs.create_file('data.json', '{"name": "Demo Dataset", "values": [1, 2, 3, 4, 5]}')

        fs.navigate_to([])  # Return to root
        print("Demo files created!")
    except Exception as e:
        print(f"Note: {e}")


def _format_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


if __name__ == "__main__":
    main()
