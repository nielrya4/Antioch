#!/usr/bin/env python3
"""
Download Link Demo - Demonstrates the DownloadLink macro

Shows how to create download links from:
- External URLs
- In-memory data strings
- Files in the Virtual File System (VFS)
"""

from antioch import DOM
from antioch.elements import Div, H1, H2, P, Hr
from antioch.macros import DownloadLink
from antioch.core.filesystem import get_filesystem


def create_demo():
    """Create the download link demonstration."""

    # Main container
    container = Div(style={
        "max_width": "800px",
        "margin": "40px auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Title
    container.add(
        H1("DownloadLink Demo", style={"color": "#333", "margin_bottom": "10px"}),
        P("Demonstrates downloading from URLs, data strings, and VFS files",
          style={"color": "#666", "margin_bottom": "30px"})
    )

    # Section 1: Download from URL
    container.add(
        H2("1. Download from URL", style={"color": "#007bff", "margin_top": "20px"}),
        P("Download a file from an external URL:"),
        DownloadLink(
            href="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            filename="sample.pdf",
            text="Download Sample PDF from URL"
        ).element,
        Hr(style={"margin": "30px 0"})
    )

    # Section 2: Download from data string
    container.add(
        H2("2. Download from Data String", style={"color": "#007bff"}),
        P("Download generated content from a data string:"),
        DownloadLink(
            data="Hello from Antioch!\n\nThis is a test file generated in memory.",
            mimetype="text/plain",
            filename="hello.txt",
            text="Download Generated Text File"
        ).element,
        Hr(style={"margin": "30px 0"})
    )

    # Section 3: Download from VFS
    # First, create some files in the VFS
    vfs = get_filesystem()

    # Create a sample JSON file in the data directory
    vfs.navigate_to(['data'])
    vfs.create_file('config.json', '{\n  "app": "Antioch",\n  "version": "1.0.0",\n  "features": ["VFS", "Macros", "Download"]\n}')

    # Create a sample text file in documents
    vfs.navigate_to(['documents'])
    vfs.create_file('notes.txt', 'Meeting Notes\n\nDate: 2024-01-15\nTopic: Download functionality\n\nImplemented DownloadLink macro with VFS support.')

    # Return to root
    vfs.navigate_to([])

    container.add(
        H2("3. Download from Virtual File System", style={"color": "#007bff"}),
        P("Download files stored in the browser's Virtual File System:"),
        Div(
            DownloadLink(
                vfs_path="/data/config.json",
                mimetype="application/json",
                filename="config.json",
                text="Download config.json from VFS"
            ).element,
            style={"margin_bottom": "10px"}
        ),
        Div(
            DownloadLink(
                vfs_path="/documents/notes.txt",
                mimetype="text/plain",
                filename="notes.txt",
                text="Download notes.txt from VFS"
            ).element,
            style={"margin_bottom": "10px"}
        ),
        Div(
            DownloadLink(
                vfs_path="/documents/README.txt",
                mimetype="text/plain",
                filename="README.txt",
                text="Download README.txt from VFS"
            ).element,
            style={"margin_bottom": "10px"}
        ),
        Hr(style={"margin": "30px 0"})
    )

    # Section 4: Custom styled link
    container.add(
        H2("4. Custom Styled Download Link", style={"color": "#007bff"}),
        P("Download link with custom styling:"),
        DownloadLink(
            data="This file was downloaded using a custom-styled link!",
            mimetype="text/plain",
            filename="custom.txt",
            text="🎨 Custom Styled Download",
            link_style={
                "background_color": "#28a745",
                "color": "white",
                "padding": "12px 24px",
                "border": "none",
                "border_radius": "8px",
                "font_size": "16px",
                "font_weight": "bold",
                "text_decoration": "none",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
            }
        ).element,
        Hr(style={"margin": "30px 0"})
    )

    # Section 5: Dynamic update demo
    container.add(
        H2("5. Dynamic Update Example", style={"color": "#007bff"}),
        P("This link can be updated dynamically (check console for example code):"),
    )

    # Create a link that can be updated
    dynamic_link = DownloadLink(
        data="Initial content",
        mimetype="text/plain",
        filename="dynamic.txt",
        text="Download Dynamic Content"
    )

    container.add(dynamic_link.element)

    # Example of updating the link (in console you can do):
    # dynamic_link.update_text("New Link Text")
    # dynamic_link.update_source(data="Updated content!")
    # dynamic_link.update_filename("new_filename.txt")

    # Add to DOM
    DOM.add(container)

    # Info message
    container.add(
        P("Note: External URL downloads may not work due to CORS restrictions. "
          "The data string and VFS downloads will work perfectly!",
          style={
              "margin_top": "30px",
              "padding": "15px",
              "background_color": "#fff3cd",
              "border": "1px solid #ffc107",
              "border_radius": "4px",
              "color": "#856404"
          })
    )


# Run the demo
create_demo()