"""
@when Decorator Demo

Simple demonstration of the new @when decorator for event handling.
Shows how to use Events with the decorator pattern.
"""
from antioch import *
from antioch.macros import Modal


def main():
    DOM.add(
        H1("@when Decorator Demo"),
        P("This demonstrates the new unified event system with decorator-based event handling.")
    )

    # Create a modal
    modal = Modal(
        title="Decorator Demo Modal",
        content=P("Click the buttons below to see different events fire!"),
        show_footer=True
    )

    DOM.add(modal.element)

    # Event log display
    event_log = Div(style={
        "margin-top": "20px",
        "padding": "15px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "border-left": "4px solid #007bff",
        "min-height": "150px"
    })
    event_log.add(H3("Event Log:", style={"margin": "0 0 10px 0", "font-size": "16px"}))

    DOM.add(event_log)

    def log_event(message, color="#6c757d"):
        """Helper to log events."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        event_log.add(
            Div(f"[{timestamp}] {message}", style={
                "margin": "3px 0",
                "color": color,
                "font-family": "monospace",
                "font-size": "13px"
            })
        )

    # ========== Event Subscriptions using @when ==========

    @when(modalopen_event.events.open)
    def on_modal_open(sender):
        log_event("✓ Modal opened", "#28a745")

    @when(modal.events.close)
    def on_modal_close(sender):
        log_event("✓ Modal closed", "#dc3545")

    @when(modalconfirm_event.events.confirm)
    def on_modal_confirm(sender):
        log_event("✓ Confirm clicked", "#007bff")

    @when(modalcancel.events.cancel)
    def on_modal_cancel(sender):
        log_event("✓ Cancel clicked", "#ffc107")

    # You can also have multiple handlers for the same event!
    @when(modalopen_event.events.open)
    def another_open_handler(sender):
        log_event("  (Second handler also notified)", "#6c757d")

    # Button to open modal
    open_btn = Button("Open Modal", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "font-size": "14px"
    })
    open_btn.on_click(lambda e: modalopen.events.open())

    # Clear log button
    clear_btn = Button("Clear Log", style={
        "padding": "10px 20px",
        "background-color": "#6c757d",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "font-size": "14px",
        "margin-left": "10px"
    })
    clear_btn.on_click(lambda e: (
        event_log.clear(),
        event_log.add(H3("Event Log:", style={"margin": "0 0 10px 0", "font-size": "16px"}))
    ))

    DOM.add(
        Div(open_btn, clear_btn, style={"margin-top": "15px"}),
        Hr(style={"margin": "30px 0"})
    )

    # ========== Show the code ==========
    DOM.add(
        H2("How It Works"),
        P("The ", Code("@when"), " decorator lets you subscribe to events declaratively:"),

        Pre(Code("""# Create events (done in Modal.__init__)
modalopen.events.open = modal_create_event.events._create('open')
modal.events.close = modal_create_event.events._create('close')
modalconfirm.events.confirm = modal_create_event.events._create('confirm')

# Subscribe using @when decorator
@when(modalopen_event.events.open)
def on_modal_open(sender):
    print(f"Modal {sender} opened!")

@when(modal.events.close)
def on_modal_close(sender):
    print("Modal closed!")

# You can have multiple handlers for one event
@when(modalopen_event.events.open)
def another_handler(sender):
    print("This also runs when modal opens")

# Fire the event (done internally by modalopen.events.open())
modalopen.events.open()  # Triggers all @when handlers + old .on() handlers
""", style={
            "background-color": "#282c34",
            "color": "#abb2bf",
            "padding": "15px",
            "border-radius": "4px",
            "font-family": "monospace",
            "font-size": "13px",
            "overflow-x": "auto"
        })),

        H3("Benefits"),
        Ul(
            Li(Strong("Declarative:"), " Event handling is clear and readable"),
            Li(Strong("Flexible:"), " Use @when or .subscribe() or .on() - they all work together"),
            Li(Strong("Multiple handlers:"), " Many functions can respond to the same event"),
            Li(Strong("Type-safe:"), " Event objects can be typed and passed around"),
            Li(Strong("Backwards compatible:"), " Works with existing .on() and .on_click() code")
        ),

        H3("Event Signature"),
        P("All event handlers receive the sender (owner) as the first argument:"),
        Pre(Code("""@when(modal.events.close)
def handle_close(sender, *args, **kwargs):
    # sender is the modal instance
    # args are event-specific arguments
    print(f"Closed: {sender.id}")
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
