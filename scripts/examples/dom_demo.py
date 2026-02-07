from antioch import Div, P, H1, Button, DOM
import main as main_page
def create_dom_demo():
    """Demonstrate DOM helper functionality."""
    
    # Create a demo section
    demo = Div(style={
        "padding": "20px",
        "margin": "20px 0",
        "background_color": "#e8f4f8",
        "border_radius": "8px",
        "border": "2px solid #4a90e2"
    })
    
    demo.add(
        H1("DOM Helper Demo", style={"color": "#2c5aa0", "margin_bottom": "15px"}),
        P("This demonstrates the DOM.add() helper method!"),
        P("No more append_to(js.document.body) - just DOM.add(element)")
    )
    
    # Create an interactive button that manipulates the DOM
    dom_button = Button("Clear Page & Add New Content", style={
        "background_color": "#e74c3c",
        "color": "white",
        "border": "none",
        "padding": "12px 20px",
        "border_radius": "6px",
        "cursor": "pointer",
        "margin_top": "10px"
    })
    
    # Event that demonstrates DOM manipulation
    dom_button.on_click(lambda e: demonstrate_dom_operations())

    demo.add(dom_button)
    return demo

def go_back_to_main():
    """Navigate back to main page without reloading."""
    DOM.clear()
    main_page.main()
    print("✓ Returned to main page!")

def demonstrate_dom_operations():
    """Show off DOM helper operations."""
    # Clear the page
    DOM.clear()

    # Back button for the cleared page
    back_btn = Button("← Back to Main Page", style={
        "background_color": "white",
        "color": "#667eea",
        "border": "none",
        "padding": "12px 24px",
        "border_radius": "6px",
        "cursor": "pointer",
        "margin_top": "20px",
        "margin_right": "10px",
        "font_weight": "bold"
    })
    back_btn.on_click(lambda e: go_back_to_main())

    # Add new content
    new_content = Div(style={
        "text_align": "center",
        "padding": "50px",
        "background": "linear-gradient(45deg, #667eea, #764ba2)",
        "color": "white",
        "min_height": "300px"
    }).add(
        H1("🎉 DOM Cleared & Rebuilt!", style={"margin_bottom": "20px"}),
        P("The entire page was cleared with DOM.clear()"),
        P("Then this content was added with DOM.add()"),
        back_btn,
        Button("Refresh to Start Over",
               onclick="location.reload()",
               style={
                   "background_color": "white",
                   "color": "#667eea",
                   "border": "none",
                   "padding": "12px 24px",
                   "border_radius": "6px",
                   "cursor": "pointer",
                   "margin_top": "20px",
                   "font_weight": "bold"
               })
    )

    DOM.add(new_content)
    print("✓ DOM operations demo executed!")

def main():
    """Show DOM helper in action."""
    demo = create_dom_demo()
    DOM.add(demo)
    
    # Also show that we can add multiple elements
    info = P("DOM.add() makes adding elements to the document super simple!", 
             style={
                 "background_color": "#fff3cd",
                 "border": "1px solid #ffeaa7",
                 "padding": "15px",
                 "border_radius": "6px",
                 "margin": "10px 0",
                 "color": "#856404"
             })
    DOM.add(info)
    print("✓ DOM helper demo loaded!")

if __name__ == "__main__":
    main()