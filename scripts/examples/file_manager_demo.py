"""
File Manager Demo - Complete file management with upload and selection.
Demonstrates FileUpload and FileSelect working together.
"""

from antioch import Div, H1, H2, H3, P, Button, DOM
from antioch.macros import FileUpload, FileSelect
from antioch.core import get_filesystem, LocalStorageBackend


def main():
    """Main entry point for File Manager demo."""
    # Get or initialize filesystem
    fs = get_filesystem(LocalStorageBackend())

    # Ensure directories exist
    _ensure_directories(fs)

    # Create page container
    page = Div(style={
        "max_width": "1400px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Add title
    page.add(H1("File Manager Demo", style={
        "color": "#333",
        "margin_bottom": "10px"
    }))

    # Add description
    page.add(P(
        "Upload files from your computer and browse them in the Virtual File System. "
        "Files are persisted in localStorage and available across sessions.",
        style={"color": "#666", "margin_bottom": "30px"}
    ))

    # Two column layout
    layout = Div(style={
        "display": "grid",
        "grid_template_columns": "1fr 1fr",
        "gap": "20px",
        "margin_bottom": "30px"
    })

    # Left column - Upload
    upload_section = Div(style={
        "background": "#fff",
        "padding": "20px",
        "border_radius": "8px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
    })
    upload_section.add(H2("Upload Files", style={"color": "#444", "margin_top": "0"}))

    # Upload status display
    upload_status = Div(style={
        "margin_bottom": "20px",
        "min_height": "40px"
    })
    upload_section.add(upload_status)

    # Create file selector for destination (this will be refreshed after uploads)
    file_list = None  # Will be set below

    def on_upload_complete(file_path, success):
        if success:
            upload_status._dom_element.innerHTML = ""
            upload_status.add(P(
                f"✅ Uploaded: {file_path}",
                style={
                    "padding": "10px",
                    "background": "#e8f5e9",
                    "color": "#2e7d32",
                    "border_radius": "4px",
                    "margin": "5px 0"
                }
            ))
            # Refresh file list
            if file_list:
                file_list.refresh()
        else:
            upload_status._dom_element.innerHTML = ""
            upload_status.add(P(
                f"❌ Upload failed: {file_path}",
                style={
                    "padding": "10px",
                    "background": "#ffebee",
                    "color": "#c62828",
                    "border_radius": "4px",
                    "margin": "5px 0"
                }
            ))

    # Geospatial files uploader
    upload_section.add(H3("📁 Upload Geospatial Files", style={
        "color": "#555",
        "font_size": "1.1em",
        "margin": "20px 0 10px 0"
    }))

    geo_uploader = FileUpload(
        destination_path=['maps'],
        allowed_extensions=['.zip', '.tif', '.tiff', '.geotiff', '.geojson', '.json'],
        max_size_mb=50,
        on_upload=on_upload_complete,
        multiple=True
    )
    upload_section.add(geo_uploader)

    # General files uploader
    upload_section.add(H3("📄 Upload Any File", style={
        "color": "#555",
        "font_size": "1.1em",
        "margin": "20px 0 10px 0"
    }))

    general_uploader = FileUpload(
        destination_path=['documents'],
        max_size_mb=20,
        on_upload=on_upload_complete,
        multiple=True
    )
    upload_section.add(general_uploader)

    layout.add(upload_section)

    # Right column - Browse/Select
    browse_section = Div(style={
        "background": "#fff",
        "padding": "20px",
        "border_radius": "8px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
    })
    browse_section.add(H2("Browse Files", style={"color": "#444", "margin_top": "0"}))

    # Selected file display
    selected_display = Div(style={
        "padding": "15px",
        "background": "#e3f2fd",
        "border_left": "4px solid #2196f3",
        "border_radius": "4px",
        "margin_bottom": "15px",
        "min_height": "60px"
    })
    selected_display.add(P("Select a file to view details", style={
        "margin": "0",
        "color": "#666",
        "font_style": "italic"
    }))
    browse_section.add(selected_display)

    def on_file_selected(file_path, file_content):
        selected_display._dom_element.innerHTML = ""

        # File path
        selected_display.add(P(
            f"📄 {file_path}",
            style={
                "margin": "0 0 10px 0",
                "color": "#333",
                "font_weight": "bold",
                "font_size": "1.1em"
            }
        ))

        # File size
        size = len(file_content) if file_content else 0
        selected_display.add(P(
            f"Size: {_format_size(size)}",
            style={"margin": "0 0 10px 0", "color": "#666"}
        ))

        # File type
        file_type = "Text" if isinstance(file_content, str) else "Binary"
        selected_display.add(P(
            f"Type: {file_type}",
            style={"margin": "0 0 10px 0", "color": "#666"}
        ))

        # Preview for text files
        if isinstance(file_content, str) and len(file_content) > 0:
            preview = file_content[:200] if len(file_content) > 200 else file_content
            preview_text = preview + "..." if len(file_content) > 200 else preview

            selected_display.add(P("Preview:", style={
                "margin": "10px 0 5px 0",
                "color": "#666",
                "font_weight": "bold"
            }))
            selected_display.add(Div(
                preview_text,
                style={
                    "padding": "10px",
                    "background": "#fff",
                    "border": "1px solid #ddd",
                    "border_radius": "4px",
                    "font_family": "monospace",
                    "font_size": "0.85em",
                    "color": "#333",
                    "white_space": "pre-wrap",
                    "overflow": "auto",
                    "max_height": "150px"
                }
            ))

    # File selector
    file_list = FileSelect(
        on_select=on_file_selected,
        height='400px'
    )
    browse_section.add(file_list)

    layout.add(browse_section)
    page.add(layout)

    # Statistics section
    stats_section = Div(style={
        "background": "#fff",
        "padding": "20px",
        "border_radius": "8px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
        "margin_bottom": "20px"
    })
    stats_section.add(H2("File System Statistics", style={"color": "#444", "margin_top": "0"}))

    stats_display = Div()
    stats_section.add(stats_display)

    def update_stats():
        stats_display._dom_element.innerHTML = ""

        # Calculate statistics
        total_files = 0
        total_size = 0
        file_types = {}

        def count_items(directory, path=[]):
            nonlocal total_files, total_size
            for name, item in directory.children.items():
                if item.type == 'file':
                    total_files += 1
                    if item.content:
                        size = len(item.content)
                        total_size += size

                    # Count file type
                    ext = '.' + name.split('.')[-1] if '.' in name else 'no extension'
                    file_types[ext] = file_types.get(ext, 0) + 1
                elif item.type == 'directory':
                    count_items(item, path + [name])

        count_items(fs.root)

        # Display stats
        stats_grid = Div(style={
            "display": "grid",
            "grid_template_columns": "repeat(auto-fit, minmax(200px, 1fr))",
            "gap": "15px"
        })

        # Total files stat
        stat_card = Div(style={
            "padding": "15px",
            "background": "#e3f2fd",
            "border_radius": "4px"
        })
        stat_card.add(P("Total Files", style={"margin": "0 0 5px 0", "color": "#666", "font_size": "0.9em"}))
        stat_card.add(P(str(total_files), style={"margin": "0", "color": "#2196f3", "font_size": "2em", "font_weight": "bold"}))
        stats_grid.add(stat_card)

        # Total size stat
        stat_card = Div(style={
            "padding": "15px",
            "background": "#e8f5e9",
            "border_radius": "4px"
        })
        stat_card.add(P("Total Size", style={"margin": "0 0 5px 0", "color": "#666", "font_size": "0.9em"}))
        stat_card.add(P(_format_size(total_size), style={"margin": "0", "color": "#4caf50", "font_size": "2em", "font_weight": "bold"}))
        stats_grid.add(stat_card)

        # File types stat
        stat_card = Div(style={
            "padding": "15px",
            "background": "#fff3e0",
            "border_radius": "4px"
        })
        stat_card.add(P("File Types", style={"margin": "0 0 5px 0", "color": "#666", "font_size": "0.9em"}))
        stat_card.add(P(str(len(file_types)), style={"margin": "0", "color": "#ff9800", "font_size": "2em", "font_weight": "bold"}))
        stats_grid.add(stat_card)

        stats_display.add(stats_grid)

        # File type breakdown
        if file_types:
            breakdown = Div(style={"margin_top": "20px"})
            breakdown.add(H3("File Type Breakdown", style={"color": "#555", "font_size": "1em", "margin": "0 0 10px 0"}))

            type_list = Div(style={
                "display": "flex",
                "flex_wrap": "wrap",
                "gap": "10px"
            })

            for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
                badge = Div(
                    f"{ext}: {count}",
                    style={
                        "padding": "5px 10px",
                        "background": "#f5f5f5",
                        "border": "1px solid #ddd",
                        "border_radius": "4px",
                        "font_size": "0.9em",
                        "color": "#333"
                    }
                )
                type_list.add(badge)

            breakdown.add(type_list)
            stats_display.add(breakdown)

    # Initial stats update
    update_stats()

    # Refresh stats button
    refresh_btn = Button("🔄 Refresh Statistics", style={
        "padding": "8px 16px",
        "background_color": "#2196f3",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "margin_top": "15px"
    })
    refresh_btn.on_click(lambda e: update_stats())
    stats_section.add(refresh_btn)

    page.add(stats_section)

    # Add page to DOM
    DOM.add(page)

    print("✅ File Manager Demo loaded!")


def _ensure_directories(fs):
    """Ensure required directories exist."""
    fs.navigate_to([])

    dirs = ['maps', 'documents', 'data']
    for dir_name in dirs:
        if dir_name not in fs.current_directory.children:
            try:
                fs.create_directory(dir_name)
            except:
                pass


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
