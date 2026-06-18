"""
Event Patterns - Quick Reference

Shows all the different ways to handle events in Antioch.
"""
from antioch import *
from antioch.macros import Modal


def main():
    DOM.add(
        H1("Event Patterns Quick Reference"),
        P("Three ways to handle events in Antioch, all working together.")
    )

    # ========== Create a Modal ==========
    modal = Modal(
        title="Event Demo",
        content=P("This modal demonstrates all event patterns."),
        show_footer=True
    )
    DOM.add(modal.element)

    # Status display
    status = Div(style={
        "margin-top": "20px",
        "padding": "15px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "100px"
    })
    status.add(H3("Event Log:", style={"margin": "0 0 10px 0"}))

    def log(msg, color="#333"):
        status.add(Div(f"• {msg}", style={"color": color, "margin": "3px 0"}))

    DOM.add(status)

    # ========== Pattern 1: @when Decorator (NEW!) ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Pattern 1: @when Decorator (Recommended)"),
        P("Clean, declarative event handling:")
    )

    @when(modal.events.open)
    def on_open_decorator(sender):
        log("@when decorator: Modal opened", "#28a745")

    @when(modal.events.close)
    def on_close_decorator(sender):
        log("@when decorator: Modal closed", "#dc3545")

    @when(modalconfirm_event.events.confirm)
    def on_confirm_decorator(sender):
        log("@when decorator: Confirmed!", "#007bff")

    DOM.add(
        Pre(Code("""@when(modal.events.open)
def on_open(sender):
    print("Modal opened!")
""", style={
            "background-color": "#f5f5f5",
            "padding": "10px",
            "border-radius": "4px",
            "font-size": "13px"
        }))
    )

    # ========== Pattern 2: Direct Event Subscription ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Pattern 2: Direct Event Subscription"),
        P("Programmatic subscription:")
    )

    def on_open_direct(sender):
        log("Direct subscribe: Modal opened", "#17a2b8")

    modalopen_event.events.open.subscribe(on_open_direct)

    DOM.add(
        Pre(Code("""def on_open(sender):
    print("Modal opened!")

modalopen_event.events.open.subscribe(on_open)
""", style={
            "background-color": "#f5f5f5",
            "padding": "10px",
            "border-radius": "4px",
            "font-size": "13px"
        }))
    )

    # ========== Pattern 3: Traditional .on() Method ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Pattern 3: Traditional .on() Method"),
        P("Backwards compatible callback registration:")
    )

    def on_open_traditional(sender):
        log("Traditional .on(): Modal opened", "#6c757d")

    modal.on('open', on_open_traditional)

    DOM.add(
        Pre(Code("""def on_open(sender):
    print("Modal opened!")

modal.on('open', on_open)
# Or the convenience method:
modal.on_open(on_open)
""", style={
            "background-color": "#f5f5f5",
            "padding": "10px",
            "border-radius": "4px",
            "font-size": "13px"
        }))
    )

    # ========== Global DOM Events ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Global DOM Events"),
        P("Application-wide events via the DOM object:")
    )

    @when(DOM.events.app_ready)
    def on_app_ready(sender):
        log("DOM event: App is ready!", "#ffc107")

    @when(DOM.events.app_error)
    def on_app_error(sender, error_msg):
        log(f"DOM event: Error - {error_msg}", "#dc3545")

    trigger_ready = Button("Trigger DOM.events.app_ready", style={
        "padding": "8px 16px",
        "background-color": "#ffc107",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })
    trigger_ready.on_click(lambda e: DOM.events.app_ready.fire())

    trigger_error = Button("Trigger DOM.events.app_error", style={
        "padding": "8px 16px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    trigger_error.on_click(lambda e: DOM.events.app_error.fire("Test error"))

    DOM.add(
        Div(trigger_ready, trigger_error, style={"margin-top": "10px"}),
        Pre(Code("""@when(DOM.events.app_ready)
def on_ready(sender):
    print("App ready!")

@when(DOM.events.app_error)
def on_error(sender, msg):
    print(f"Error: {msg}")

# Fire events
DOM.events.app_ready.fire()
DOM.events.app_error.fire("Something failed")
""", style={
            "background-color": "#f5f5f5",
            "padding": "10px",
            "border-radius": "4px",
            "font-size": "13px",
            "margin-top": "10px"
        }))
    )

    # ========== All Together ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("All Patterns Working Together"),
        P("When you open the modal, all three handlers fire! They all work together seamlessly.")
    )

    # Button to trigger modal
    open_btn = Button("Open Modal (Triggers All Handlers)", style={
        "padding": "12px 24px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "font-size": "16px"
    })
    open_btn.on_click(lambda e: modalopen.events.open())

    clear_btn = Button("Clear Log", style={
        "padding": "12px 24px",
        "background-color": "#6c757d",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "font-size": "16px",
        "margin-left": "10px"
    })
    clear_btn.on_click(lambda e: (
        status.clear(),
        status.add(H3("Event Log:", style={"margin": "0 0 10px 0"}))
    ))

    DOM.add(Div(open_btn, clear_btn))

    # ========== Summary ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Which Pattern to Use?"),
        Ul(
            Li(Strong("Use @when"), " for most cases - it's clean and declarative"),
            Li(Strong("Use .subscribe()"), " when you need programmatic control"),
            Li(Strong("Use .on()"), " when working with existing code or for backwards compatibility"),
            Li(Strong("Mix them!"), " All three patterns work together seamlessly")
        ),

        H3("Key Points"),
        Ul(
            Li("All handlers receive ", Code("(sender, *args, **kwargs)"), " signature"),
            Li("Multiple handlers can subscribe to the same event"),
            Li("Events are first-class objects you can pass around"),
            Li("Global events live on ", Code("DOM"), " object"),
            Li("Fully backwards compatible with existing code")
        )
    )


if __name__ == "__main__":
    main()
