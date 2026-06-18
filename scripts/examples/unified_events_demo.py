"""
Unified Event System Demo

Demonstrates the new unified event system with decorator-based subscriptions.
Shows how to use Events with macros, elements, and global events.
"""
from antioch import *
from antioch.macros import Modal, Counter, Dropdown


def main():
    DOM.add(
        H1("Unified Event System Demo"),
        P("Demonstrating the new Event system with @when decorator and direct subscriptions."),
        Hr()
    )

    # ========== Demo 1: Modal Events with @when Decorator ==========
    DOM.add(
        H2("1. Modal Events with @when Decorator"),
        P("The @when decorator provides a clean way to handle events.")
    )

    # Create a modal with events
    modal = Modal(
        title="Event Demo Modal",
        content=P("This modal demonstrates the unified event system!"),
        show_footer=True
    )

    # Add modal to page (hidden initially)
    DOM.add(modal.element)

    # Events are already created by Modal.__init__
    # Available: modalopen_event.events.open, modal.events.close, modalconfirm_event.events.confirm, modalcancel_event.events.cancel

    # Status display
    event_log = Div(style={
        "padding": "10px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "margin-top": "10px",
        "min-height": "100px",
        "font-family": "monospace",
        "font-size": "12px"
    })
    event_log.add(P("Event log:", style={"font-weight": "bold", "margin": "0 0 5px 0"}))

    def log_event(message):
        """Helper to log events to the display."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_line = Div(f"[{timestamp}] {message}", style={"margin": "2px 0"})
        event_log.add(log_line)

    # Subscribe to modal events using @when decorator
    @when(modalopen_event.events.open)
    def handle_modal_open(sender, *args):
        log_event(f"Modal opened (via @when decorator)")

    @when(modal.events.close)
    def handle_modal_close(sender, *args):
        log_event(f"Modal closed (via @when decorator)")

    @when(modalconfirm_event.events.confirm)
    def handle_modal_confirm(sender, *args):
        log_event(f"Modal confirmed! (via @when decorator)")

    # Also subscribe using direct method (works alongside @when)
    modalopen_event.events.open.subscribe(lambda sender, *args: log_event("Modal opened (via direct subscribe)"))

    # Button to open modal
    open_modal_btn = Button("Open Modal", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    open_modal_btn.on_click(lambda e: modalopen.events.open())

    DOM.add(open_modal_btn, event_log, Hr(style={"margin": "30px 0"}))

    # ========== Demo 2: Counter Events ==========
    DOM.add(
        H2("2. Counter Events"),
        P("Counter with change events using the unified system.")
    )

    counter = Counter(initial_value=0)

    # Create change event
    counter.change_event = counter._create_event('change')

    counter_status = P("Counter value: 0", style={
        "padding": "10px",
        "background-color": "#e3f2fd",
        "border-radius": "4px",
        "margin-top": "10px"
    })

    # Subscribe using @when
    @when(counter.change_event)
    def handle_counter_change(sender, new_value, old_value):
        counter_status.set_text(
            f"Counter changed from {old_value} to {new_value} (via @when)"
        )

    DOM.add(counter.element, counter_status, Hr(style={"margin": "30px 0"}))

    # ========== Demo 3: Dropdown Events ==========
    DOM.add(
        H2("3. Dropdown Events"),
        P("Dropdown with multiple event types.")
    )

    dropdown_options = [
        {"value": "python", "label": "Python"},
        {"value": "javascript", "label": "JavaScript"},
        {"value": "rust", "label": "Rust"},
        {"value": "go", "label": "Go"}
    ]

    dropdown = Dropdown(
        options=dropdown_options,
        placeholder="Select a language..."
    )

    # Create events
    dropdown.change_event = dropdown._create_event('change')
    dropdown.open_event = dropdown._create_event('open')
    dropdown.close_event = dropdown._create_event('close')

    dropdown_status = P("No selection", style={
        "padding": "10px",
        "background-color": "#f3e5f5",
        "border-radius": "4px",
        "margin-top": "10px"
    })

    # Subscribe to multiple events
    @when(dropdown.change_event)
    def handle_dropdown_change(sender, selected):
        if selected:
            dropdown_status.set_text(f"Selected: {selected['label']} ({selected['value']})")
        else:
            dropdown_status.set_text("No selection")

    @when(dropdown.open_event)
    def handle_dropdown_open(sender, *args):
        print("Dropdown opened")

    @when(dropdown.close_event)
    def handle_dropdown_close(sender, *args):
        print("Dropdown closed")

    DOM.add(dropdown.element, dropdown_status, Hr(style={"margin": "30px 0"}))

    # ========== Demo 4: EventGroup - Multiple Events at Once ==========
    DOM.add(
        H2("4. EventGroup - Subscribe to Multiple Events"),
        P("EventGroup lets you subscribe one handler to multiple events at once.")
    )

    # Create another modal
    modal2 = Modal(
        title="EventGroup Demo",
        content=P("This demonstrates EventGroup functionality."),
        show_footer=True
    )
    DOM.add(modal2.element)

    # Events are already created by Modal.__init__

    # Create an EventGroup
    all_modal_events = EventGroup([
        modalopen_event.events.open,
        modalclose_event.events.close,
        modalconfirm_event.events.confirm,
        modalcancel_event.events.cancel
    ])

    event_group_log = Div(style={
        "padding": "10px",
        "background-color": "#fff3cd",
        "border-radius": "4px",
        "margin-top": "10px",
        "min-height": "60px",
        "font-family": "monospace",
        "font-size": "12px"
    })

    # Subscribe to all events at once using decorator
    @all_modal_events
    def handle_any_modal_event(sender, *args):
        event_name = "unknown"
        if sender._events:
            for name, event in sender._events.items():
                # Check which event fired by comparing args
                event_name = name
        event_group_log.add(Div(f"Modal event fired: {event_name}", style={"margin": "2px 0"}))

    open_modal2_btn = Button("Open EventGroup Modal", style={
        "padding": "10px 20px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    open_modal2_btn.on_click(lambda e: modalopen.events.open())

    DOM.add(open_modal2_btn, event_group_log, Hr(style={"margin": "30px 0"}))

    # ========== Demo 5: Global Events ==========
    DOM.add(
        H2("5. Global Events"),
        P("Application-wide events using DOM global events.")
    )

    global_event_log = Div(style={
        "padding": "10px",
        "background-color": "#d1ecf1",
        "border-radius": "4px",
        "margin-top": "10px",
        "font-family": "monospace",
        "font-size": "12px"
    })

    # Subscribe to global app events
    @when(DOM.events.app_ready)
    def on_app_ready(sender, *args):
        global_event_log.add(Div("✓ Application is ready!", style={"color": "green", "margin": "2px 0"}))

    @when(DOM.events.app_error)
    def on_app_error(sender, error_msg):
        global_event_log.add(Div(f"✗ Error: {error_msg}", style={"color": "red", "margin": "2px 0"}))

    # Buttons to trigger global events
    trigger_ready_btn = Button("Trigger App Ready", style={
        "padding": "8px 16px",
        "background-color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })
    trigger_ready_btn.on_click(lambda e: DOM.events.app_ready.fire())

    trigger_error_btn = Button("Trigger App Error", style={
        "padding": "8px 16px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    trigger_error_btn.on_click(lambda e: DOM.events.app_error.fire("Simulated error"))

    DOM.add(
        Div(trigger_ready_btn, trigger_error_btn),
        global_event_log,
        Hr(style={"margin": "30px 0"})
    )

    # ========== Summary ==========
    DOM.add(
        H2("Unified Event System Benefits"),
        Ul(
            Li(Strong("Decorator syntax:"), " Use @when(event) for clean, declarative event handling"),
            Li(Strong("Consistent signature:"), " All handlers receive (sender, *args, **kwargs)"),
            Li(Strong("Works everywhere:"), " Same pattern for elements, macros, and global events"),
            Li(Strong("Direct subscription:"), " event.subscribe(handler) for programmatic usage"),
            Li(Strong("EventGroup:"), " Subscribe to multiple events with one handler"),
            Li(Strong("Backwards compatible:"), " Works alongside existing on() and on_click() methods"),
            Li(Strong("Type safety:"), " Event objects are first-class, can be passed around and typed")
        ),

        H3("Usage Pattern"),
        Pre(Code("""# In macro __init__:
self.close_event = self._create_event('close')

# Subscribe with decorator:
@when(modal.events.close)
def handle_close(sender, args):
    print("Modal closed")

# Or direct subscription:
modal.events.close.subscribe(handle_close)

# Fire the event:
self._fire_event('close', some_data)
""", style={"background-color": "#f5f5f5", "padding": "10px", "border-radius": "4px"}))
    )


if __name__ == "__main__":
    main()
