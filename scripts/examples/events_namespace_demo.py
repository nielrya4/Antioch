"""
Events Namespace Demo

Demonstrates the clean event.events namespace for accessing events.
No more naming collisions with methods!
"""
from antioch import *
from antioch.macros import Modal


def main():
    DOM.add(
        H1("Events Namespace Demo"),
        P("Events are now accessed via ", Code("modal.events.open"), ", ", Code("DOM.events.app_ready"), ", etc.")
    )

    # Create a modal
    modal = Modal(
        title="Events Demo",
        content=P("Events are accessed through the .events namespace!"),
        show_footer=True
    )
    DOM.add(modal.element)

    # Event log
    log_div = Div(style={
        "margin-top": "20px",
        "padding": "15px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "150px"
    })
    log_div.add(H3("Event Log:", style={"margin": "0 0 10px 0"}))

    def log(msg, color="#333"):
        log_div.add(Div(f"• {msg}", style={"color": color, "margin": "3px 0"}))

    DOM.add(log_div)

    # ========== Subscribe using @when ==========

    @when(modal.events.open)
    def on_open(sender):
        log("Modal opened!", "#28a745")

    @when(modal.events.close)
    def on_close(sender):
        log("Modal closed!", "#dc3545")

    @when(modal.events.confirm)
    def on_confirm(sender):
        log("Confirmed!", "#007bff")

    @when(modal.events.cancel)
    def on_cancel(sender):
        log("Cancelled!", "#6c757d")

    # ========== Global DOM Events ==========

    @when(DOM.events.app_ready)
    def on_app_ready(sender):
        log("DOM: App ready!", "#ffc107")

    @when(DOM.events.app_error)
    def on_app_error(sender, msg):
        log(f"DOM: Error - {msg}", "#dc3545")

    # ========== Buttons ==========

    open_btn = Button("Open Modal", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    open_btn.on_click(lambda e: modal.open())  # Method call - no collision!

    trigger_ready_btn = Button("Trigger DOM.events.app_ready", style={
        "padding": "10px 20px",
        "background-color": "#ffc107",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-left": "10px"
    })
    trigger_ready_btn.on_click(lambda e: DOM.events.app_ready.fire())

    trigger_error_btn = Button("Trigger DOM.events.app_error", style={
        "padding": "10px 20px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-left": "10px"
    })
    trigger_error_btn.on_click(lambda e: DOM.events.app_error.fire("Test error"))

    clear_btn = Button("Clear Log", style={
        "padding": "10px 20px",
        "background-color": "#6c757d",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-left": "10px"
    })
    clear_btn.on_click(lambda e: (
        log_div.clear(),
        log_div.add(H3("Event Log:", style={"margin": "0 0 10px 0"}))
    ))

    DOM.add(Div(open_btn, trigger_ready_btn, trigger_error_btn, clear_btn, style={"margin-top": "15px"}))

    # ========== Show the benefits ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Benefits of .events Namespace"),
        Ul(
            Li(Strong("No naming collisions:"), " ", Code("modal.open()"), " is a method, ", Code("modal.events.open"), " is an event"),
            Li(Strong("Clear semantics:"), " It's obvious you're accessing an event"),
            Li(Strong("Discoverable:"), " See all events with ", Code("modal.events.keys()")),
            Li(Strong("Consistent:"), " Same pattern for macros, elements, and DOM"),
            Li(Strong("Dictionary access:"), " Can use ", Code("modal.events['open']"), " if needed")
        ),

        H3("Usage Examples"),
        Pre(Code("""# Subscribe to macro events
@when(modal.events.open)
def on_open(sender):
    print("Opened!")

# Subscribe to global DOM events
@when(DOM.events.app_ready)
def on_ready(sender):
    print("Ready!")

# Call methods without collision
modal.open()  # Method call
modal.events.open  # Event object

# Access with dictionary syntax
modal.events['close'].subscribe(handler)

# List all available events
print(list(modal.events.keys()))
""", style={
            "background-color": "#f5f5f5",
            "padding": "12px",
            "border-radius": "4px",
            "font-family": "monospace",
            "font-size": "13px"
        })),

        H3("Creating Events in Your Macros"),
        Pre(Code("""class MyMacro(Macro):
    def __init__(self):
        super().__init__()

        # Create events - accessed via self.events.click, etc.
        self._create_event('click')
        self._create_event('change')
        self._create_event('submit')

        self._init_macro()

    def _some_method(self):
        # Fire events
        self._fire_event('click', click_data)
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
