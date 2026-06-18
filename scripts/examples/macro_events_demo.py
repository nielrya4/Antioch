"""
Macro Events Demo

Demonstrates the unified event system across multiple macros:
1. All macros now have .events namespace
2. @when decorator syntax works with all macros
3. Event combination with | operator
4. Full backwards compatibility maintained
"""
from antioch import *
from antioch.macros import (
    Modal, Alert, Toast, Counter, ProgressBar, Slider,
    Tabs, Tab, Accordion, AccordionPanel, Dropdown, DropdownItem,
    Form, FormField
)


def main():
    DOM.add(
        H1("Macro Events Demo"),
        P("Showcasing the unified event system across all macros with @when decorator and event combination.")
    )

    # ========== Event Log ==========
    event_log = Div(style={
        "position": "fixed",
        "top": "10px",
        "right": "10px",
        "width": "300px",
        "max-height": "400px",
        "overflow": "auto",
        "background-color": "#f8f9fa",
        "border": "1px solid #ddd",
        "border-radius": "4px",
        "padding": "10px",
        "font-size": "12px",
        "z-index": "9999"
    })
    event_log.add(H3("Event Log", style={"margin": "0 0 10px 0", "font-size": "14px"}))

    def log_event(message, color="#333"):
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        event_log.add(Div(
            f"[{timestamp}] {message}",
            style={"color": color, "margin": "2px 0", "padding": "2px", "font-size": "11px"}
        ))
        # Auto-scroll to bottom
        event_log._dom_element.scrollTop = event_log._dom_element.scrollHeight

    DOM.add(event_log)

    # ========== Modal Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("1. Modal Events"),
        P("Modal with open/close events using @when decorator")
    )

    modal = Modal(
        title="Demo Modal",
        content=P("This modal demonstrates the unified event system!")
    )
    DOM.add(modal.element)

    @when(modal.events.open)
    def handle_modal_open(sender):
        log_event("✓ Modal opened", "#28a745")

    @when(modal.events.close)
    def handle_modal_close(sender):
        log_event("✗ Modal closed", "#dc3545")

    open_modal_btn = Button("Open Modal", style={
        "padding": "8px 16px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    # open_modal_btn.on_click(lambda e: modal.open())
    DOM.add(open_modal_btn)
    @when(open_modal_btn.events.click)
    def _(sender, *args):
        modal.open()

    # ========== Alert Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("2. Alert Events"),
        P("Alert with dismiss/show events")
    )

    alert = Alert("This is an informational alert!", alert_type="info")

    @when(alert.events.dismiss)
    def handle_alert_dismiss(sender):
        log_event("Alert dismissed", "#17a2b8")

    @when(alert.events.show)
    def handle_alert_show(sender):
        log_event("Alert shown", "#17a2b8")

    DOM.add(
        alert.element,
        Button("Show Alert Again", style={
            "padding": "8px 16px",
            "background-color": "#17a2b8",
            "color": "white",
            "border": "none",
            "border-radius": "4px",
            "cursor": "pointer",
            "margin-top": "10px"
        }).on_click(lambda e: alert.show())
    )

    # ========== Counter with Event Combination ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("3. Counter Events (Event Combination)"),
        P("Multiple counters with ONE combined event handler using | operator")
    )

    counter1 = Counter(initial_value=0, label="Counter 1")
    counter2 = Counter(initial_value=10, label="Counter 2")
    counter3 = Counter(initial_value=20, label="Counter 3")

    # Single handler for all three counters using | operator!
    @when(counter1.events.change | counter2.events.change | counter3.events.change)
    def handle_any_counter_change(sender, new_value, old_value):
        label = sender._get_state('label')
        log_event(f"{label}: {old_value} → {new_value}", "#ffc107")

    DOM.add(
        Div(counter1.element, counter2.element, counter3.element, style={
            "display": "flex",
            "gap": "20px",
            "flex-wrap": "wrap"
        })
    )

    # ========== ProgressBar Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("4. ProgressBar Events"),
        P("ProgressBar with progress_change and complete events")
    )

    progress = ProgressBar(initial_progress=0, max_progress=100)

    @when(progress.events.progress_change)
    def handle_progress_change(sender, new_value, old_value):
        log_event(f"Progress: {new_value}%", "#28a745")

    @when(progress.events.complete)
    def handle_progress_complete(sender, value):
        log_event(f"✓ Progress completed at {value}%!", "#28a745")

    progress_btn = Button("Increment Progress (+10%)", style={
        "padding": "8px 16px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-top": "10px"
    })
    progress_btn.on_click(lambda e: progress.set_progress(min(progress.progress + 10, 100)))

    DOM.add(progress.element, progress_btn)

    # ========== Slider Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("5. Slider Events"),
        P("Slider with input (continuous) and change (final) events")
    )

    slider = Slider(min_value=0, max_value=100, initial_value=50, label="Volume")

    @when(slider.events.input)
    def handle_slider_input(sender, new_value, old_value):
        log_event(f"Slider dragging: {new_value}", "#6c757d")

    @when(slider.events.change)
    def handle_slider_change(sender, new_value, old_value):
        log_event(f"Slider released at: {new_value}", "#007bff")

    DOM.add(slider.element)

    # ========== Tabs Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("6. Tabs Events"),
        P("Tabs with change event when switching tabs")
    )

    tabs = Tabs(tabs=[
        Tab("Tab 1", content=P("Content for tab 1")),
        Tab("Tab 2", content=P("Content for tab 2")),
        Tab("Tab 3", content=P("Content for tab 3"))
    ])

    @when(tabs.events.change)
    def handle_tab_change(sender, tab, old_id):
        log_event(f"Switched to: {tab.title}", "#6f42c1")

    DOM.add(tabs.element)

    # ========== Accordion Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("7. Accordion Events"),
        P("Accordion with expand/collapse events")
    )

    accordion = Accordion(panels=[
        AccordionPanel("Section 1", P("Content for section 1")),
        AccordionPanel("Section 2", P("Content for section 2")),
        AccordionPanel("Section 3", P("Content for section 3"))
    ])

    @when(accordion.events.panel_expand)
    def handle_panel_expand(sender, panel):
        log_event(f"Expanded: {panel.title}", "#20c997")

    @when(accordion.events.panel_collapse)
    def handle_panel_collapse(sender, panel):
        log_event(f"Collapsed: {panel.title}", "#fd7e14")

    DOM.add(accordion.element)

    # ========== Dropdown Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("8. Dropdown Events"),
        P("Dropdown with select, open, and close events")
    )

    dropdown = Dropdown(
        items=["Apple", "Banana", "Cherry", "Date", "Elderberry"],
        placeholder="Select a fruit"
    )

    @when(dropdown.events.select)
    def handle_dropdown_select(sender, value, item):
        log_event(f"Selected: {value}", "#e83e8c")

    @when(dropdown.events.open)
    def handle_dropdown_open(sender):
        log_event("Dropdown opened", "#6c757d")

    @when(dropdown.events.close)
    def handle_dropdown_close(sender):
        log_event("Dropdown closed", "#6c757d")

    DOM.add(dropdown.element)

    # ========== Form Demo ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("9. Form Events"),
        P("Form with submit and change events")
    )

    form = Form(
        fields=[
            FormField("name", label="Name", placeholder="Enter your name", required=True),
            FormField("email", field_type="email", label="Email", placeholder="your@email.com", required=True)
        ],
        submit_text="Submit Form"
    )

    @when(form.events.submit)
    def handle_form_submit(sender, data):
        log_event(f"Form submitted: {data}", "#28a745")

    @when(form.events.change)
    def handle_form_change(sender, field_name, field_value, field):
        log_event(f"Field changed: {field_name} = '{field_value}'", "#17a2b8")

    DOM.add(form.element)

    # ========== Summary ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Summary"),
        P("This demo showcases:"),
        Ul(
            Li(Strong("@when decorator:"), " Clean, declarative event subscription"),
            Li(Strong("Event combination:"), " Use ", Code("event1 | event2 | event3"), " for multi-event handlers"),
            Li(Strong("Unified .events namespace:"), " All macros use ", Code("macro.events.event_name")),
            Li(Strong("Type safety:"), " Events are discoverable and well-documented"),
            Li(Strong("Backwards compatible:"), " Old ", Code(".on()"), " methods still work")
        ),
        P("All events are logged in the Event Log panel (top-right corner).", style={
            "padding": "10px",
            "background-color": "#d1ecf1",
            "border-radius": "4px",
            "margin-top": "20px"
        })
    )


if __name__ == "__main__":
    main()
