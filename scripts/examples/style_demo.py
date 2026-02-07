from antioch import Div, P, H2, Button, DOM

def create_style_demo():
    """Demonstrate both dot notation and dictionary assignment for styles."""
    demo_section = Div()
    demo_section.add(H2("Style Assignment Demo"))
    
    # Example 1: Constructor style parameter
    button1 = Button("Constructor Styled", style={
        "background_color": "#e74c3c",
        "color": "white",
        "border": "none",
        "padding": "12px 24px",
        "border_radius": "8px",
        "cursor": "pointer",
        "margin": "10px",
        "font_size": "16px",
        "transition": "all 0.3s ease"
    })
    
    # Example 2: Mixed - dictionary then dot notation
    button2 = Button("Mixed Styling")
    button2.style = {
        "background_color": "#3498db",
        "color": "white",
        "border": "none",
        "padding": "12px 24px"
    }
    # Then modify with dot notation
    button2.style.border_radius = "8px"
    button2.style.cursor = "pointer" 
    button2.style.margin = "10px"
    button2.style.transition = "all 0.3s ease"
    
    # Example 3: Update method
    button3 = Button("Updated Styling")
    button3.style.update({
        "background_color": "#9b59b6",
        "color": "white",
        "border": "none",
        "padding": "12px 24px",
        "border_radius": "8px",
        "cursor": "pointer",
        "margin": "10px"
    })
    
    # Example 4: Dot notation only
    button4 = Button("Dot Notation")
    button4.style.background_color = "#f39c12"
    button4.style.color = "white"
    button4.style.border = "none"
    button4.style.padding = "12px 24px"
    button4.style.border_radius = "8px"
    button4.style.cursor = "pointer"
    button4.style.margin = "10px"
    
    # Container styling with dictionary
    demo_section.style = {
        "margin_top": "30px",
        "padding": "30px",
        "background_color": "#f8f9fa",
        "border_radius": "12px",
        "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    }
    
    # Add descriptions
    descriptions = [
        P("1. Constructor parameter: Button(style={...})"),
        P("2. Mixed: Dictionary + dot notation"),
        P("3. Update method: button.style.update({...})"),
        P("4. Traditional dot notation")
    ]
    
    for desc in descriptions:
        desc.style = {
            "font_size": "14px",
            "color": "#666",
            "margin": "5px 10px"
        }
    
    demo_section.add(
        descriptions[0], button1,
        descriptions[1], button2, 
        descriptions[2], button3,
        descriptions[3], button4
    )
    
    return demo_section

def create_chained_demo():
    """Demonstrate the exact syntax requested by user."""
    # Example exactly as requested: Div(style={"color": "black"}).add(P("asdfasdfasdf", style={"color": "white"}))
    chained_example = Div(style={"color": "black", "background_color": "#333", "padding": "20px", "border_radius": "8px"}).add(
        H2("Chained Style Demo", style={"color": "yellow", "margin_bottom": "10px"}),
        P("This text is white on a black background", style={"color": "white", "font_size": "18px"}),
        P("Multiple styled elements in one chain!", style={"color": "lightblue", "font_style": "italic"})
    )
    
    return chained_example

def main():
    # Create and append the demos using DOM.add()
    style_demo = create_style_demo()
    chained_demo = create_chained_demo()
    
    DOM.add(style_demo)
    chained_demo.style.margin_top = "30px"
    DOM.add(chained_demo)
    
    print("✓ Style assignment demo loaded!")
    print("✓ Chained styling demo loaded!")

if __name__ == "__main__":
    main()
