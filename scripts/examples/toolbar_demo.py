"""
Toolbar Demo - Demonstrating the Toolbar macro with nested menus.
Shows how to create a horizontal menu bar with dropdowns and submenus.
"""

from antioch import DOM, Div, H1, H2, P
from antioch.macros import Toolbar, Alert


class ToolbarDemo:
    """Demo application showing toolbar usage."""

    def __init__(self):
        # Create a message display area
        self.message_display = Alert("Welcome! Try the menu options above.", alert_type="info")

        # Create the toolbar
        self.toolbar = self._create_toolbar()

    def _create_toolbar(self):
        """Create the toolbar with menu structure."""
        # Define menu structure
        menu_structure = {
            "File": {
                "New": lambda: self.show_message("Creating new file..."),
                "Open": lambda: self.show_message("Opening file..."),
                "Save": {
                    "Save": lambda: self.show_message("Saving file..."),
                    "Save As": lambda: self.show_message("Save As dialog opened"),
                    "Save All": lambda: self.show_message("Saving all files...")
                },
                "Recent Files": {
                    "Today": {
                        "document.txt": lambda: self.show_message("Opening document.txt"),
                        "project.py": lambda: self.show_message("Opening project.py")
                    },
                    "Yesterday": {
                        "notes.md": lambda: self.show_message("Opening notes.md"),
                        "data.csv": lambda: self.show_message("Opening data.csv")
                    },
                    "This Week": lambda: self.show_message("Showing this week's files...")
                },
                "Exit": lambda: self.show_message("Exiting application...")
            },
            "Edit": {
                "Undo": lambda: self.show_message("Undo last action"),
                "Redo": lambda: self.show_message("Redo last action"),
                "Cut": lambda: self.show_message("Cut selection"),
                "Copy": lambda: self.show_message("Copy selection"),
                "Paste": lambda: self.show_message("Paste from clipboard"),
                "Find": {
                    "Find": lambda: self.show_message("Find dialog opened"),
                    "Find Next": lambda: self.show_message("Finding next occurrence"),
                    "Replace": lambda: self.show_message("Replace dialog opened"),
                    "Find in Files": lambda: self.show_message("Find in files...")
                }
            },
            "View": {
                "Zoom In": lambda: self.show_message("Zooming in..."),
                "Zoom Out": lambda: self.show_message("Zooming out..."),
                "Reset Zoom": lambda: self.show_message("Resetting zoom to 100%"),
                "Layout": {
                    "Sidebar": lambda: self.show_message("Toggling sidebar"),
                    "Panel": lambda: self.show_message("Toggling panel"),
                    "Fullscreen": lambda: self.show_message("Entering fullscreen mode")
                },
                "Theme": {
                    "Light": lambda: self.show_message("Switched to light theme"),
                    "Dark": lambda: self.show_message("Switched to dark theme"),
                    "Custom": {
                        "Blue": lambda: self.show_message("Switched to blue theme"),
                        "Green": lambda: self.show_message("Switched to green theme"),
                        "Purple": lambda: self.show_message("Switched to purple theme"),
                        "Import Theme": {
                            "From File": lambda: self.show_message("Importing theme from file..."),
                            "From URL": lambda: self.show_message("Importing theme from URL...")
                        }
                    },
                    "Auto": lambda: self.show_message("Using system theme")
                }
            },
            "Tools": {
                "Settings": lambda: self.show_message("Opening settings..."),
                "Extensions": lambda: self.show_message("Managing extensions..."),
                "Command Palette": lambda: self.show_message("Opening command palette...")
            },
            "Help": {
                "Documentation": lambda: self.show_message("Opening documentation..."),
                "Keyboard Shortcuts": lambda: self.show_message("Showing keyboard shortcuts"),
                "About": lambda: self.show_message("About this application")
            }
        }

        # Create toolbar with custom styling
        toolbar = Toolbar(
            menu_structure=menu_structure,
            toolbar_style={
                "background_color": "#1e272e",
                "box_shadow": "0 2px 6px rgba(0,0,0,0.2)"
            }
        )

        # Register callbacks
        toolbar.on_menu_click(lambda toolbar, menu_label:
            print(f"Menu opened: {menu_label}"))

        toolbar.on_item_click(lambda toolbar, item_label, callback:
            print(f"Item clicked: {item_label}")
        )

        return toolbar

    def show_message(self, message: str):
        """Update the message display."""
        self.message_display.set_message(message)
        self.message_display.show()
        print(f"Action: {message}")

    def get_elements(self):
        """Get the toolbar and message display elements."""
        return self.toolbar.element, self.message_display.element


def main():
    """Create and display the toolbar demo."""
    # Create main container
    container = Div(style={
        "font_family": "Arial, sans-serif"
    })

    # Title section
    title_section = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "background_color": "#ffffff"
    })

    title = H1("Toolbar Demo", style={
        "text_align": "center",
        "color": "#2c3e50",
        "margin_bottom": "10px"
    })

    subtitle = H2("Horizontal Menu Bar with Nested Dropdowns", style={
        "text_align": "center",
        "color": "#7f8c8d",
        "font_size": "18px",
        "font_weight": "normal",
        "margin_bottom": "20px"
    })

    title_section.add(title, subtitle)

    # Description
    description = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 20px auto",
        "padding": "0 20px"
    })

    desc_box = Div(style={
        "background_color": "#ecf0f1",
        "padding": "15px",
        "border_radius": "6px",
        "margin_bottom": "20px"
    })

    desc_box.add(
        P("✨ Features:", style={"font_weight": "bold", "margin": "0 0 10px 0"}),
        P("• Spans the full width of its container", style={"margin": "5px 0"}),
        P("• Supports unlimited nesting depth (menus within menus within menus...)", style={"margin": "5px 0"}),
        P("• Clean, professional appearance with hover effects", style={"margin": "5px 0"}),
        P("• Click outside or press Escape to close menus", style={"margin": "5px 0"}),
        P("• Fully customizable styles and callbacks", style={"margin": "5px 0"})
    )

    description.add(desc_box)

    # Create demo
    demo = ToolbarDemo()
    toolbar_element, message_element = demo.get_elements()

    # Content area
    content_area = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "min_height": "400px"
    })

    instructions = Div(style={
        "background_color": "#fff",
        "padding": "20px",
        "border_radius": "6px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
        "margin_bottom": "20px"
    })

    instructions.add(
        P("Instructions:", style={"font_weight": "bold", "margin": "0 0 10px 0"}),
        P("1. Click on any menu item (File, Edit, View, Tools, Help) to see dropdown options", style={"margin": "5px 0"}),
        P("2. Hover over items with arrows (▸) to reveal nested submenus", style={"margin": "5px 0"}),
        P("3. Click any menu item to execute its action and see the result below", style={"margin": "5px 0"}),
        P("4. Try 'Recent Files' under 'File' for 3-level deep nesting", style={"margin": "5px 0"}),
        P("5. Try 'Theme > Custom > Import Theme' under 'View' for 4-level deep nesting!", style={"margin": "5px 0"})
    )

    content_area.add(instructions, message_element)

    # Add everything to the page
    container.add(toolbar_element, title_section, description, content_area)

    # Add to DOM
    DOM.add(container)


# Run when explicitly called from main.py
