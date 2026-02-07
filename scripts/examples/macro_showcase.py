"""
Macro Showcase - Demonstrates all the new built-in macros in Antioch.
This example showcases the expanded macro library with interactive components.
"""

from antioch import Div, H1, H2, Hr, P, Button, DOM
from antioch.macros import (
    ProgressBar, Alert, Accordion, AccordionPanel, Pagination,
    Dropdown, DropdownItem, Toast, ToastManager, Slider,
    show_toast, info_toast, success_toast, warning_toast, error_toast, clear_all_toasts
)

def create_showcase():
    """Create a comprehensive showcase of all new macros."""
    
    # Define common button style
    button_style = {
        "padding": "8px 16px",
        "margin": "0 5px",
        "border": "1px solid #007bff",
        "background_color": "#007bff",
        "color": "white",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px",
        "transition": "all 0.2s ease"
    }
    
    # Main container
    container = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })
    
    # Title
    title = H1("Antioch Macro Showcase", style={
        "text_align": "center",
        "color": "#333",
        "margin_bottom": "30px"
    })
    container.add(title)
    
    # Progress Bar Section
    container.add(H2("Progress Bar Examples"))
    
    # Basic progress bar
    progress1 = ProgressBar(initial_progress=75, width="400px")
    container.add(P("Basic Progress Bar (75%):"))
    container.add(progress1.element)
    
    # Animated striped progress bar
    progress2 = ProgressBar(
        initial_progress=45, 
        width="400px", 
        color="#28a745",
        animate=True,
        striped=True
    )
    container.add(P("Animated Striped Progress Bar:"))
    container.add(progress2.element)
    
    # Progress control buttons
    progress_controls = Div(style={"margin": "10px 0"})
    
    increase_btn = Button("Increase (+10)", style=button_style)
    decrease_btn = Button("Decrease (-10)", style=button_style)
    reset_btn = Button("Reset", style=button_style)
    
    increase_btn.on_click(lambda e: progress1.increment(10))
    decrease_btn.on_click(lambda e: progress1.decrement(10))
    reset_btn.on_click(lambda e: progress1.set_progress(0))
    
    progress_controls.add(increase_btn, decrease_btn, reset_btn)
    container.add(progress_controls)
    
    container.add(Hr())
    
    # Alert Section
    container.add(H2("Alert Examples"))
    
    # Different alert types
    info_alert = Alert("This is an info alert with useful information.", "info")
    success_alert = Alert("Success! Your action was completed.", "success")
    warning_alert = Alert("Warning: Please check your input.", "warning")
    error_alert = Alert("Error: Something went wrong.", "error", auto_dismiss=True, dismiss_delay=3000)
    
    container.add(info_alert.element)
    container.add(success_alert.element)
    container.add(warning_alert.element)
    container.add(error_alert.element)
    
    container.add(Hr())
    
    # Accordion Section
    container.add(H2("Accordion Example"))
    
    panels = [
        {"title": "What is Antioch?", "content": "Antioch is a Python DOM library that runs in browsers via Pyodide, enabling full-stack Python development."},
        {"title": "How do macros work?", "content": "Macros are reusable UI components with built-in state management, event handling, and styling."},
        {"title": "Can I create custom macros?", "content": "Yes! Inherit from the Macro base class to create your own reusable components with safe multi-instance support."}
    ]
    
    accordion = Accordion(panels=panels, allow_multiple=True, default_expanded=[0])
    container.add(accordion.element)
    
    container.add(Hr())
    
    # Pagination Section
    container.add(H2("Pagination Example"))
    container.add(P("Navigate through 250 items (25 items per page):"))
    
    pagination = Pagination(total_items=250, items_per_page=25, current_page=1)
    
    # Page info display
    page_info = Div(style={"margin": "10px 0", "padding": "10px", "background": "#f8f9fa", "border_radius": "4px"})
    
    def update_page_info():
        data = pagination.get_page_data_range()
        page_info.set_text(f"Showing items {data['start_item']}-{data['end_item']} of {data['total_items']}")
    
    pagination.on_page_change(lambda pagination, page, old_page: update_page_info())
    update_page_info()  # Initial update
    
    container.add(pagination.element)
    container.add(page_info)
    
    container.add(Hr())
    
    # Dropdown Section
    container.add(H2("Dropdown Examples"))
    
    # Simple dropdown
    simple_items = ["Option 1", "Option 2", "Option 3", "Option 4"]
    simple_dropdown = Dropdown(items=simple_items, placeholder="Choose an option")
    
    container.add(P("Simple Dropdown:"))
    container.add(simple_dropdown.element)
    
    # Multi-select searchable dropdown
    multi_items = [
        DropdownItem("JavaScript", "js"),
        DropdownItem("Python", "py"),
        DropdownItem("TypeScript", "ts"),
        DropdownItem("Rust", "rust"),
        DropdownItem("Go", "go"),
        DropdownItem("Java", "java")
    ]
    
    multi_dropdown = Dropdown(
        items=multi_items,
        placeholder="Select programming languages",
        searchable=True,
        multi_select=True
    )
    
    container.add(P("Multi-select Searchable Dropdown:"))
    container.add(multi_dropdown.element)
    
    # Selection display
    selection_display = Div(style={"margin": "10px 0", "padding": "10px", "background": "#e7f3ff"})
    
    def update_selection():
        if simple_dropdown.selected_value:
            simple_text = f"Simple: {simple_dropdown.selected_value}"
        else:
            simple_text = "Simple: None selected"
            
        multi_text = f"Multi: {', '.join(multi_dropdown.selected_values) if multi_dropdown.selected_values else 'None selected'}"
        selection_display.set_text(f"{simple_text} | {multi_text}")
    
    simple_dropdown.on_change(lambda *args: update_selection())
    multi_dropdown.on_change(lambda *args: update_selection())
    update_selection()  # Initial update
    
    container.add(selection_display)
    
    container.add(Hr())
    
    # Toast Section
    container.add(H2("Toast Notification Examples"))
    
    toast_controls = Div(style={"display": "flex", "gap": "10px", "flex_wrap": "wrap"})
    
    info_btn = Button("Show Info Toast", style=button_style)
    success_btn = Button("Show Success Toast", style=button_style) 
    warning_btn = Button("Show Warning Toast", style=button_style)
    error_btn = Button("Show Error Toast", style=button_style)
    clear_btn = Button("Clear All Toasts", style=button_style)
    
    info_btn.on_click(lambda e: info_toast("This is an informational message!"))
    success_btn.on_click(lambda e: success_toast("Operation completed successfully!"))
    warning_btn.on_click(lambda e: warning_toast("Please review your settings."))
    error_btn.on_click(lambda e: error_toast("An error occurred while processing."))
    clear_btn.on_click(lambda e: clear_all_toasts())
    
    toast_controls.add(info_btn, success_btn, warning_btn, error_btn, clear_btn)
    container.add(toast_controls)
    
    container.add(Hr())
    
    # Slider Section
    container.add(H2("Slider Examples"))
    
    # Volume slider
    volume_slider = Slider(
        min_value=0,
        max_value=100,
        initial_value=70,
        label="Volume Control",
        show_value=True,
        show_ticks=True
    )
    
    container.add(volume_slider.element)
    
    # Temperature slider
    temp_slider = Slider(
        min_value=-20,
        max_value=50,
        initial_value=22,
        step=0.5,
        label="Temperature (°C)",
        show_value=True,
        show_min_max=True
    )
    
    container.add(temp_slider.element)
    
    # Slider value display
    slider_display = Div(style={"margin": "10px 0", "padding": "10px", "background": "#f0f8ff"})
    
    def update_slider_display():
        slider_display.set_text(f"Volume: {volume_slider.value}% | Temperature: {temp_slider.value}°C")
    
    volume_slider.on_input(lambda slider, value, old_value: update_slider_display())
    temp_slider.on_input(lambda slider, value, old_value: update_slider_display())
    update_slider_display()  # Initial update
    
    container.add(slider_display)
    
    # Slider controls
    slider_controls = Div(style={"display": "flex", "gap": "10px", "margin": "10px 0"})
    
    vol_up = Button("Vol +10", style=button_style)
    vol_down = Button("Vol -10", style=button_style)
    temp_up = Button("Temp +5", style=button_style)
    temp_down = Button("Temp -5", style=button_style)
    
    vol_up.on_click(lambda e: volume_slider.increment(10))
    vol_down.on_click(lambda e: volume_slider.decrement(10))
    temp_up.on_click(lambda e: temp_slider.increment(5))
    temp_down.on_click(lambda e: temp_slider.decrement(5))
    
    slider_controls.add(vol_up, vol_down, temp_up, temp_down)
    container.add(slider_controls)
    
    # Footer
    footer = Div(style={
        "margin_top": "50px",
        "padding": "20px",
        "text_align": "center",
        "background": "#f8f9fa",
        "border_radius": "6px"
    })
    footer.add(P("🎉 Antioch Macro Showcase - Interactive UI components built with Python! 🎉"))
    container.add(footer)
    
    return container

def main():
    """Main application entry point."""
    # Create and add the showcase
    showcase = create_showcase()
    DOM.add(showcase)
    print("🚀 Antioch Macro Showcase loaded!")

if __name__ == "__main__":
    main()