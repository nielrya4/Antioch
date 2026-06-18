"""
Element Events Demo

Demonstrates the .events namespace for Elements and DOM.
Shows how to create and subscribe to custom events on elements.
"""
from antioch import *


def main():
    DOM.add(
        H1("Element & DOM Events Demo"),
        P("Elements can have custom events accessed via ", Code("element.events"), " namespace.")
    )

    # ========== Example 1: Button with Custom Event ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("1. Button with Custom Events"),
        P("Create unified events on elements that work with @when decorator.")
    )

    button = Button("Click Me!", style={
        "padding": "12px 24px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "font-size": "16px"
    })

    # Create a unified event that auto-wires to DOM click
    button.create_event('click')

    click_log = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "80px"
    })
    click_log.add(P("Click the button above:", style={"margin": "0 0 5px 0", "font-weight": "bold"}))

    # Subscribe using @when decorator
    @when(button.events.click)
    def on_button_click(sender, dom_event):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        click_log.add(Div(f"[{timestamp}] Button clicked!", style={
            "color": "#28a745",
            "margin": "2px 0"
        }))

    DOM.add(button, click_log)

    # ========== Example 2: Input with Change Event ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("2. Input with Change Events"),
        P("Track input changes with unified events.")
    )

    input_field = Input("text", style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px",
        "font-size": "14px",
        "width": "300px"
    })
    input_field.set_attribute("placeholder", "Type something...")

    # Create change and input events
    input_field.create_event('input')
    input_field.create_event('change')
    input_field.create_event('focus')
    input_field.create_event('blur')

    input_status = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#e3f2fd",
        "border-radius": "4px"
    })
    input_status.add(P("Status: Waiting for input...", style={"margin": "0"}))

    @when(input_field.events.input)
    def on_input(sender, dom_event):
        value = dom_event.target.value
        input_status.clear()
        input_status.add(P(f"Typing: '{value}' ({len(value)} chars)", style={"margin": "0"}))

    @when(input_field.events.change)
    def on_change(sender, dom_event):
        value = dom_event.target.value
        input_status.clear()
        input_status.add(P(f"Changed to: '{value}'", style={"margin": "0", "color": "#1976d2"}))

    @when(input_field.events.focus)
    def on_focus(sender, dom_event):
        input_field.style.border_color = "#2196f3"

    @when(input_field.events.blur)
    def on_blur(sender, dom_event):
        input_field.style.border_color = "#ddd"

    DOM.add(input_field, input_status)

    # ========== Example 3: Custom Non-DOM Event ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("3. Custom Non-DOM Events"),
        P("Create custom events not tied to DOM events.")
    )

    counter_div = Div(style={
        "padding": "20px",
        "background-color": "#fff3cd",
        "border-radius": "4px",
        "text-align": "center"
    })

    counter_value = H2("Count: 0", style={"margin": "0"})
    counter_div.add(counter_value)

    # Create a custom event (not auto-wired to DOM)
    counter_div.create_event('threshold_reached', auto_wire=False)
    counter_div.create_event('reset', auto_wire=False)

    count = [0]  # Use list for closure

    def increment():
        count[0] += 1
        counter_value.set_text(f"Count: {count[0]}")

        # Fire custom event when threshold reached
        if count[0] == 10:
            counter_div.events.threshold_reached.fire(count[0])

    def reset():
        count[0] = 0
        counter_value.set_text(f"Count: {count[0]}")
        counter_div.events.reset.fire()

    inc_btn = Button("+1", style={
        "padding": "10px 20px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin": "10px 5px 0 5px"
    })
    inc_btn.on_click(lambda e: increment())

    reset_btn = Button("Reset", style={
        "padding": "10px 20px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin": "10px 5px 0 5px"
    })
    reset_btn.on_click(lambda e: reset())

    counter_div.add(inc_btn, reset_btn)

    custom_event_log = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "60px"
    })

    @when(counter_div.events.threshold_reached)
    def on_threshold(sender, value):
        custom_event_log.add(Div(
            f"🎉 Threshold reached! Count = {value}",
            style={"color": "#ff6b6b", "font-weight": "bold", "margin": "2px 0"}
        ))

    @when(counter_div.events.reset)
    def on_reset(sender):
        custom_event_log.add(Div(
            "Counter reset",
            style={"color": "#6c757d", "margin": "2px 0"}
        ))

    DOM.add(counter_div, custom_event_log)

    # ========== Example 4: Global DOM Events ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("4. Global DOM Events"),
        P("Application-wide events via ", Code("DOM.events"))
    )

    global_log = Div(style={
        "padding": "10px",
        "background-color": "#d1ecf1",
        "border-radius": "4px",
        "min-height": "80px"
    })
    global_log.add(P("Global event log:", style={"margin": "0 0 5px 0", "font-weight": "bold"}))

    @when(DOM.events.app_ready)
    def on_app_ready(sender):
        global_log.add(Div("✓ App ready event fired", style={"color": "#28a745", "margin": "2px 0"}))

    @when(DOM.events.app_error)
    def on_app_error(sender, message):
        global_log.add(Div(f"✗ App error: {message}", style={"color": "#dc3545", "margin": "2px 0"}))

    # Custom global events
    DOM.events.register('user_action')

    @when(DOM.events.user_action)
    def on_user_action(sender, action):
        global_log.add(Div(f"→ User action: {action}", style={"color": "#007bff", "margin": "2px 0"}))

    ready_btn = Button("Fire DOM.events.app_ready", style={
        "padding": "8px 16px",
        "background-color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })
    ready_btn.on_click(lambda e: DOM.events.app_ready.fire())

    error_btn = Button("Fire DOM.events.app_error", style={
        "padding": "8px 16px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })
    error_btn.on_click(lambda e: DOM.events.app_error.fire("Test error message"))

    action_btn = Button("Fire DOM.events.user_action", style={
        "padding": "8px 16px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    action_btn.on_click(lambda e: DOM.events.user_action.fire("custom action"))

    DOM.add(
        Div(ready_btn, error_btn, action_btn, style={"margin-bottom": "10px"}),
        global_log
    )

    # ========== Summary ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Summary"),
        Ul(
            Li(Strong("Elements: "), Code("element.create_event('click')"), " creates ", Code("element.events.click")),
            Li(Strong("Macros: "), Code("modal.events.open"), " accessed via .events namespace"),
            Li(Strong("DOM: "), Code("DOM.events.app_ready"), " for global events"),
            Li(Strong("Auto-wire: "), "DOM events automatically fire unified events"),
            Li(Strong("Custom events: "), "Use ", Code("auto_wire=False"), " for non-DOM events"),
            Li(Strong("@when decorator: "), "Works everywhere with .events namespace")
        ),

        H3("Code Pattern"),
        Pre(Code("""# Elements
button = Button("Click")
button.create_event('click')  # Auto-wires to DOM

@when(button.events.click)
def on_click(sender, dom_event):
    print("Clicked!")

# DOM global events
@when(DOM.events.app_ready)
def on_ready(sender):
    print("Ready!")

DOM.events.app_ready.fire()
""", style={
            "background-color": "#f5f5f5",
            "padding": "12px",
            "border-radius": "4px",
            "font-family": "monospace",
            "font-size": "13px"
        }))
    )


if __name__ == "__main__":
    main()
