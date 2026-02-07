"""
Macros Demo - Showcases all Antioch macro components.
Demonstrates safe multiple instance usage and component features.
"""
from antioch import Div, H1, H2, P, Button, DOM

# Import macros from antioch.macros package
from antioch.macros import Counter, Modal, Form, FormField, RequiredValidator, EmailValidator, MinLengthValidator, Tabs, Tab


def create_counter_demo():
    """Demonstrate Counter macro with multiple instances."""
    section = Div(style={
        "margin": "20px 0",
        "padding": "20px",
        "border": "1px solid #ddd",
        "border_radius": "8px",
        "background_color": "#f8f9fa"
    })
    
    section.add(H2("Counter Components"))
    section.add(P("Multiple counter instances working independently:"))
    
    # Basic counter
    basic_counter = Counter(initial_value=5, label="Basic Counter")
    basic_counter.on_change(lambda counter, new_value, old_value: print(f"Basic counter changed to: {new_value}"))
    section.add(basic_counter.element)
    
    # Limited counter
    limited_counter = Counter(
        initial_value=0, 
        min_value=0, 
        max_value=10, 
        label="Limited (0-10)",
        button_style={"background_color": "#28a745"}
    )
    limited_counter.on_change(lambda counter, new_value, old_value: print(f"Limited counter: {new_value}"))
    section.add(limited_counter.element)
    
    # Step counter
    step_counter = Counter(
        initial_value=0,
        step=5,
        label="Step by 5",
        button_style={"background_color": "#ffc107", "color": "#000"}
    )
    step_counter.on_change(lambda counter, new_value, old_value: print(f"Step counter: {new_value}"))
    section.add(step_counter.element)
    
    return section


def create_modal_demo():
    """Demonstrate Modal macro with multiple instances."""
    section = Div(style={
        "margin": "20px 0",
        "padding": "20px", 
        "border": "1px solid #ddd",
        "border_radius": "8px",
        "background_color": "#f8f9fa"
    })
    
    section.add(H2("Modal Components"))
    section.add(P("Click buttons to open different modal types:"))
    
    # Button container
    button_container = Div(style={"margin": "10px 0"})
    
    # Basic modal
    basic_modal = Modal("Basic Modal", "This is a simple modal dialog.")
    basic_modal.on_open(lambda modal: print("Basic modal opened"))
    basic_modal.on_close(lambda modal: print("Basic modal closed"))
    
    basic_btn = Button("Open Basic Modal", style={
        "background_color": "#007bff",
        "color": "white",
        "border": "none",
        "padding": "10px 15px",
        "border_radius": "4px",
        "margin": "5px",
        "cursor": "pointer"
    })
    basic_btn.on_click(lambda e: basic_modal.show())
    button_container.add(basic_btn)
    
    # Confirm modal with buttons
    confirm_modal = Modal("Confirm Action", "Are you sure you want to proceed?")
    confirm_modal.add_confirm_cancel_buttons()
    confirm_modal.on_confirm(lambda modal: print("User confirmed action"))
    confirm_modal.on_cancel(lambda modal: print("User cancelled action"))
    
    confirm_btn = Button("Open Confirm Modal", style={
        "background_color": "#28a745",
        "color": "white",
        "border": "none",
        "padding": "10px 15px",
        "border_radius": "4px",
        "margin": "5px",
        "cursor": "pointer"
    })
    confirm_btn.on_click(lambda e: confirm_modal.show())
    button_container.add(confirm_btn)
    
    # Custom content modal
    custom_modal = Modal("Custom Content", closable=True)
    from antioch import Ul, Li, A
    custom_content = Div().add(
        P("This modal has custom content:"),
        Ul().add(
            Li("Interactive elements"),
            Li("Rich formatting"),
            Li(A("External links", href="https://example.com", target="_blank"))
        )
    )
    custom_modal.set_content(custom_content)
    
    custom_btn = Button("Open Custom Modal", style={
        "background_color": "#6f42c1",
        "color": "white", 
        "border": "none",
        "padding": "10px 15px",
        "border_radius": "4px",
        "margin": "5px",
        "cursor": "pointer"
    })
    custom_btn.on_click(lambda e: custom_modal.show())
    button_container.add(custom_btn)
    
    section.add(button_container)
    
    # Add modals to DOM (they start hidden)
    DOM.add(basic_modal.element)
    DOM.add(confirm_modal.element)
    DOM.add(custom_modal.element)
    
    return section


def create_form_demo():
    """Demonstrate Form macro with validation."""
    section = Div(style={
        "margin": "20px 0",
        "padding": "20px",
        "border": "1px solid #ddd", 
        "border_radius": "8px",
        "background_color": "#f8f9fa"
    })
    
    section.add(H2("Form Component"))
    section.add(P("Form with validation and multiple field types:"))
    
    # Create form fields
    fields = [
        FormField(
            "name",
            label="Full Name",
            placeholder="Enter your full name",
            required=True,
            validators=[MinLengthValidator(2, "Name must be at least 2 characters")]
        ),
        FormField(
            "email", 
            field_type="email",
            label="Email Address",
            placeholder="your@email.com",
            required=True,
            validators=[EmailValidator()]
        ),
        FormField(
            "age",
            field_type="number",
            label="Age",
            placeholder="25",
            min="18",
            max="120"
        ),
        FormField(
            "message",
            field_type="textarea",
            label="Message",
            placeholder="Tell us about yourself...",
            rows="4"
        )
    ]
    
    # Create form
    form = Form(fields, submit_text="Submit Form", show_reset=True)
    
    # Form callbacks
    form.on_submit(lambda f, data: handle_form_submit(data))
    form.on_reset(lambda f: print("Form was reset"))
    form.on_change(lambda f, name, value, field: print(f"Field '{name}' changed to: '{value}'"))
    
    section.add(form.element)
    
    return section


def handle_form_submit(data):
    """Handle form submission."""
    print("Form submitted with data:", data)
    
    # Show a modal with the submitted data
    result_modal = Modal("Form Submitted", closable=True)
    
    content = Div().add(
        P("Your form was submitted successfully!"),
        P(f"Name: {data.get('name', 'N/A')}"),
        P(f"Email: {data.get('email', 'N/A')}"),
        P(f"Age: {data.get('age', 'N/A')}"),
        P(f"Message: {data.get('message', 'N/A')}")
    )
    
    result_modal.set_content(content)
    DOM.add(result_modal.element)
    result_modal.show()


def create_tabs_demo():
    """Demonstrate Tabs macro with dynamic content."""
    section = Div(style={
        "margin": "20px 0",
        "padding": "20px",
        "border": "1px solid #ddd",
        "border_radius": "8px", 
        "background_color": "#f8f9fa"
    })
    
    section.add(H2("Tabs Component"))
    section.add(P("Tabbed interface with dynamic content management:"))
    
    # Create tabs
    tabs = [
        Tab("Overview", P("This is the overview tab with basic information.")),
        Tab("Features", create_features_content()),
        Tab("Settings", create_settings_content()),
        Tab("About", P("Learn more about Antioch macros and their capabilities."))
    ]
    
    # Create tabs component
    tabs_component = Tabs(tabs, active_tab=0)
    tabs_component.on_change(lambda tabs, new_tab, old_id: 
                            print(f"Switched to tab: {new_tab.title}"))
    
    section.add(tabs_component.element)
    
    # Add control buttons
    controls = Div(style={"margin_top": "15px"})
    
    add_tab_btn = Button("Add Dynamic Tab", style={
        "background_color": "#17a2b8",
        "color": "white",
        "border": "none", 
        "padding": "8px 12px",
        "border_radius": "4px",
        "margin": "5px",
        "cursor": "pointer"
    })
    
    def add_dynamic_tab(e):
        import time
        tab_count = len(tabs_component.tabs) + 1
        new_tab = Tab(
            f"Dynamic {tab_count}",
            P(f"This is a dynamically added tab created at {time.strftime('%H:%M:%S')}")
        )
        tabs_component.add_tab(new_tab)
        tabs_component.set_active_tab(new_tab.tab_id)
    
    add_tab_btn.on_click(add_dynamic_tab)
    controls.add(add_tab_btn)
    
    section.add(controls)
    
    return section


def create_features_content():
    """Create content for features tab."""
    from antioch import Ul, Li
    
    return Div().add(
        P("Key features of Antioch macros:"),
        Ul().add(
            Li("🔒 Safe multi-instance support"),
            Li("🎨 Customizable styling"),
            Li("📱 Event-driven architecture"),
            Li("✅ Built-in validation"),
            Li("🔄 State management"),
            Li("🧩 Modular design")
        )
    )


def create_settings_content():
    """Create content for settings tab with interactive elements."""
    content = Div()
    
    content.add(P("Configure your preferences:"))
    
    # Theme counter
    theme_counter = Counter(
        initial_value=1,
        min_value=1,
        max_value=3, 
        label="Theme",
        button_style={"background_color": "#6c757d"}
    )
    
    def update_theme(counter, new_value, old_value):
        themes = {1: "Light", 2: "Dark", 3: "Auto"}
        print(f"Theme changed to: {themes.get(new_value, 'Unknown')}")
    
    theme_counter.on_change(update_theme)
    content.add(theme_counter.element)
    
    return content


def main():
    """Main demo function."""
    # Page title
    title = H1("Antioch Macros Demo", style={
        "text_align": "center",
        "color": "#333",
        "margin_bottom": "30px"
    })
    DOM.add(title)
    
    # Introduction
    intro = P(
        "This demo showcases reusable UI components built with Antioch. "
        "All components use unique identifiers and safe event handling, "
        "allowing multiple instances to coexist without conflicts.",
        style={
            "max_width": "800px",
            "margin": "0 auto 30px",
            "text_align": "center",
            "font_size": "16px",
            "color": "#666"
        }
    )
    DOM.add(intro)
    
    # Create demo sections
    counter_demo = create_counter_demo()
    modal_demo = create_modal_demo()
    form_demo = create_form_demo()
    tabs_demo = create_tabs_demo()
    
    # Add all demos to page
    DOM.add(counter_demo)
    DOM.add(modal_demo) 
    DOM.add(form_demo)
    DOM.add(tabs_demo)
    
    print("✅ Antioch Macros Demo loaded!")


if __name__ == "__main__":
    main()