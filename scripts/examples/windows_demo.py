"""
Windows Demo - Showcase the Window and WindowManager macros.

Demonstrates a complete desktop-like windowing system with draggable,
resizable windows, taskbar, and window management features.
"""
from antioch import Div, H1, H2, P, Button, DOM
from antioch.macros import WindowManager, Counter, DataTable


def main():
    """Initialize and run the windows demo."""
    print("🚀 Starting Windows Demo...")

    # Create the window manager
    wm = WindowManager(show_taskbar=True)

    # Add the window manager to the DOM
    DOM.add(wm.element)

    # Create some demo windows

    # Window 1: Welcome window
    welcome_content = Div()
    welcome_content.add(
        H1("Welcome to Antioch Windows!", style={
            "color": "#667eea",
            "margin_top": "0"
        }),
        P("This demo showcases the Window and WindowManager components."),
        P("Features:"),
        Div(style={"margin_left": "20px"}).add(
            P("• Drag windows by their title bar"),
            P("• Resize windows from edges and corners"),
            P("• Minimize windows to the taskbar"),
            P("• Maximize windows to full screen"),
            P("• Close windows with the × button")
        ),
        P("Try creating more windows using the buttons below!", style={
            "margin_top": "20px",
            "font_weight": "bold"
        })
    )

    welcome_window = wm.create_window(
        title="Welcome to Windows",
        content=welcome_content,
        x=100,
        y=80,
        width=500,
        height=400
    )

    # Window 2: Counter demo
    counter_content = Div()
    counter_content.add(
        H2("Interactive Counter", style={"margin_top": "0"}),
        P("This window contains a Counter macro:"),
        Counter(initial_value=5, min_value=0, max_value=20)
    )

    counter_window = wm.create_window(
        title="Counter Demo",
        content=counter_content,
        x=650,
        y=100,
        width=350,
        height=250
    )

    # Window 3: DataTable demo
    table_content = Div()
    table_content.add(
        H2("Data Table", style={"margin_top": "0"}),
        P("A simple data table in a window:")
    )

    # Create sample data
    data = [
        {"name": "Alice", "age": 30, "city": "New York"},
        {"name": "Bob", "age": 25, "city": "San Francisco"},
        {"name": "Carol", "age": 35, "city": "Chicago"},
        {"name": "David", "age": 28, "city": "Boston"}
    ]

    columns = [
        {"title": "Name", "field": "name", "width": 120},
        {"title": "Age", "field": "age", "width": 80},
        {"title": "City", "field": "city", "width": 150}
    ]

    table = DataTable(
        data=data,
        columns=columns,
        height="200px",
        layout="fitData"
    )

    table_content.add(table.element)

    table_window = wm.create_window(
        title="Data Table Example",
        content=table_content,
        x=250,
        y=250,
        width=450,
        height=350
    )

    # Control panel for creating more windows
    control_panel = Div(style={
        "position": "fixed",
        "bottom": "20px",
        "right": "20px",
        "background": "white",
        "border": "2px solid #667eea",
        "border_radius": "8px",
        "padding": "15px",
        "box_shadow": "0 4px 12px rgba(0,0,0,0.2)",
        "z_index": "10001"
    })

    control_panel.add(
        H2("Create Windows", style={
            "margin": "0 0 10px 0",
            "font_size": "16px",
            "color": "#667eea"
        })
    )

    # Button to create a simple window
    def create_simple_window():
        content = Div().add(
            H2("Simple Window", style={"color": "#667eea"}),
            P(f"This is window #{len(wm.get_all_windows())}"),
            P("You can drag, resize, minimize, maximize, and close this window.")
        )
        wm.create_window(
            title=f"Window #{len(wm.get_all_windows())}",
            content=content,
            width=400,
            height=250
        )

    simple_btn = Button("Create Simple Window", style={
        "display": "block",
        "width": "100%",
        "margin_bottom": "8px",
        "padding": "8px 12px",
        "background": "#667eea",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_weight": "500"
    })
    simple_btn.on_click(lambda e: create_simple_window())

    # Button to create a counter window
    def create_counter_window():
        content = Div().add(
            H2("Counter Window", style={"color": "#667eea"}),
            Counter(initial_value=0, min_value=-10, max_value=100)
        )
        wm.create_window(
            title="Counter",
            content=content,
            width=300,
            height=200
        )

    counter_btn = Button("Create Counter Window", style={
        "display": "block",
        "width": "100%",
        "margin_bottom": "8px",
        "padding": "8px 12px",
        "background": "#28a745",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_weight": "500"
    })
    counter_btn.on_click(lambda e: create_counter_window())

    # Info text
    info = P("Tip: Try minimizing windows to see the taskbar!", style={
        "font_size": "12px",
        "color": "#666",
        "margin": "10px 0 0 0"
    })

    control_panel.add(simple_btn, counter_btn, info)
    DOM.add(control_panel)

    print("✅ Windows Demo loaded!")
    print(f"Created {len(wm.get_all_windows())} initial windows")


if __name__ == "__main__":
    main()
