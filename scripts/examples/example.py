from antioch import Div, P, H1, H2, Button, Input, Span, DOM

def create_welcome_div():
    welcome_div = Div().add(
        H1("Welcome to Antioch!"),
        P("A Python library for seamless DOM manipulation"),
        P("Built for real-time interactivity with js.document")
    )
    
    welcome_div.style.display = "block"
    welcome_div.style.background_color = "#f0f8ff"
    welcome_div.style.padding = "20px"
    welcome_div.style.border_radius = "8px"
    welcome_div.style.margin = "20px auto"
    welcome_div.style.max_width = "600px"
    welcome_div.style.box_shadow = "0 4px 6px rgba(0, 0, 0, 0.1)"
    
    return welcome_div

def create_event_demo():
    """Demonstrate the new handle() method for multiple event handling."""
    demo_section = Div()
    demo_section.add(H2("Event Handling Demo"))
    
    # Counter for button clicks
    counter = {"value": 0}
    
    # Interactive button with multiple events
    button = Button("Interactive Button")
    button.style.background_color = "#28a745"
    button.style.color = "white"
    button.style.border = "none"
    button.style.padding = "12px 20px"
    button.style.border_radius = "6px"
    button.style.cursor = "pointer"
    button.style.margin = "10px 5px"
    button.style.transition = "all 0.3s ease"
    
    # Status display
    status = Span("Ready...")
    status.style.margin_left = "10px"
    status.style.font_weight = "bold"
    
    # Use the new handle() method for multiple events
    button.handle({
        "click": lambda e: handle_click(counter, button, status),
        "mouseenter": lambda e: handle_hover_in(button, status),
        "mouseleave": lambda e: handle_hover_out(button, status),
        "mousedown": lambda e: handle_mouse_down(button),
        "mouseup": lambda e: handle_mouse_up(button)
    })
    
    # Input field with real-time handling
    text_input = Input("text")
    text_input.set_attribute("placeholder", "Type something...")
    text_input.style.padding = "8px 12px"
    text_input.style.border = "2px solid #ddd"
    text_input.style.border_radius = "4px"
    text_input.style.margin = "10px 5px"
    text_input.style.width = "200px"
    
    output_text = P("Your text will appear here...")
    output_text.style.font_style = "italic"
    output_text.style.color = "#666"
    output_text.style.background_color = "#f9f9f9"
    output_text.style.padding = "10px"
    output_text.style.border_radius = "4px"
    output_text.style.margin_top = "10px"
    
    # Real-time input handling
    text_input.handle({
        "input": lambda e: handle_input(e, output_text),
        "focus": lambda e: handle_focus_in(text_input),
        "blur": lambda e: handle_focus_out(text_input)
    })
    
    demo_section.add(
        P("This button handles multiple events:"),
        Div().add(button, status),
        P("This input field responds in real-time:"),
        text_input,
        output_text
    )
    
    return demo_section

def handle_click(counter, button, status):
    counter["value"] += 1
    count = counter["value"]
    button.set_text(f"Clicked {count} time{'s' if count != 1 else ''}!")
    status.set_text("👆 Clicked!")
    status.style.color = "#007bff"
    
    if count == 5:
        status.set_text("🎉 You found the secret!")
        status.style.color = "#ff6347"

def handle_hover_in(button, status):
    button.style.background_color = "#34ce57"
    button.style.transform = "scale(1.05)"
    status.set_text("🖱️ Hovering")
    status.style.color = "#28a745"

def handle_hover_out(button, status):
    button.style.background_color = "#28a745"
    button.style.transform = "scale(1)"
    status.set_text("Ready...")
    status.style.color = "#333"

def handle_mouse_down(button):
    button.style.transform = "scale(0.95)"

def handle_mouse_up(button):
    button.style.transform = "scale(1.05)"

def handle_input(event, output):
    value = event.target.value
    if value.strip():
        output.set_text(f"You typed: '{value}'")
        output.style.color = "#333"
        output.style.background_color = "#e8f5e8"
    else:
        output.set_text("Your text will appear here...")
        output.style.color = "#666"
        output.style.background_color = "#f9f9f9"

def handle_focus_in(input_element):
    input_element.style.border_color = "#007bff"
    input_element.style.box_shadow = "0 0 0 2px rgba(0,123,255,.25)"

def handle_focus_out(input_element):
    input_element.style.border_color = "#ddd"
    input_element.style.box_shadow = "none"

def main():
    # Create main container
    main_container = Div()
    main_container.style.font_family = "Arial, sans-serif"
    
    # Add welcome section
    welcome_section = create_welcome_div()
    
    # Add event demo section
    event_demo = create_event_demo()
    event_demo.style.margin_top = "30px"
    event_demo.style.padding = "20px"
    event_demo.style.background_color = "#ffffff"
    event_demo.style.border_radius = "8px"
    event_demo.style.box_shadow = "0 2px 4px rgba(0, 0, 0, 0.1)"
    
    main_container.add(welcome_section, event_demo)
    DOM.add(main_container)
    
    print("✓ Antioch event handling demo loaded!")

if __name__ == "__main__":
    main()