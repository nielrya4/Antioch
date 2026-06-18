"""
Event Combination Demo

Demonstrates:
1. Pre-registered events on all elements (no create_event needed!)
2. Event combination with | operator
"""
from antioch import *


def main():
    DOM.add(
        H1("Event Combination Demo"),
        P("All elements now have pre-registered events, and you can combine them with ", Code("|"), " operator!")
    )

    # ========== Demo 1: Pre-registered Events ==========
    DOM.add(
        Hr(style={"margin": "20px 0"}),
        H2("1. Pre-registered Events"),
        P("All elements automatically have common events. No need to call ", Code("create_event()"), "!")
    )

    # Create buttons - events are already registered!
    btn1 = Button("Button 1", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })

    btn2 = Button("Button 2", style={
        "padding": "10px 20px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })

    btn3 = Button("Button 3", style={
        "padding": "10px 20px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })

    log1 = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "60px"
    })
    log1.add(P("Event log:", style={"margin": "0 0 5px 0", "font-weight": "bold"}))

    # Events are already registered - just use them!
    @when(btn1.events.click)
    def on_btn1_click(sender, dom_event):
        log1.add(Div("Button 1 clicked!", style={"color": "#007bff", "margin": "2px 0"}))

    @when(btn2.events.click)
    def on_btn2_click(sender, dom_event):
        log1.add(Div("Button 2 clicked!", style={"color": "#28a745", "margin": "2px 0"}))

    @when(btn3.events.click)
    def on_btn3_click(sender, dom_event):
        log1.add(Div("Button 3 clicked!", style={"color": "#dc3545", "margin": "2px 0"}))

    DOM.add(
        Div(btn1, btn2, btn3),
        log1,
        P("Notice: No ", Code("button.create_event('click')"), " needed! Events are auto-registered.", style={
            "margin-top": "10px",
            "padding": "10px",
            "background-color": "#d1ecf1",
            "border-radius": "4px"
        })
    )

    # ========== Demo 2: Combine Events with | Operator ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("2. Combine Events with | Operator"),
        P("Use ", Code("event1 | event2 | event3"), " to subscribe one handler to multiple events!")
    )

    # Create more buttons
    red_btn = Button("Red", style={
        "padding": "10px 20px",
        "background-color": "#dc3545",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })

    green_btn = Button("Green", style={
        "padding": "10px 20px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })

    blue_btn = Button("Blue", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })

    log2 = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#fff3cd",
        "border-radius": "4px",
        "min-height": "60px"
    })
    log2.add(P("Unified handler log:", style={"margin": "0 0 5px 0", "font-weight": "bold"}))

    # One handler for all three buttons using | operator!
    @when(red_btn.events.click | green_btn.events.click | blue_btn.events.click)
    def handle_any_color_click(sender, dom_event):
        button_text = sender._dom_element.textContent
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log2.add(Div(
            f"[{timestamp}] {button_text} button clicked!",
            style={"margin": "2px 0", "color": "#856404"}
        ))

    DOM.add(
        Div(red_btn, green_btn, blue_btn),
        log2,
        Pre(Code("""@when(red_btn.events.click | green_btn.events.click | blue_btn.events.click)
def handle_any_color_click(sender, dom_event):
    print(f"{sender} clicked!")
""", style={
            "background-color": "#f5f5f5",
            "padding": "12px",
            "border-radius": "4px",
            "margin-top": "10px",
            "font-size": "13px"
        }))
    )

    # ========== Demo 3: Input Events ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("3. Input Events (Pre-registered)"),
        P("Input elements have ", Code("input"), " and ", Code("change"), " events pre-registered.")
    )

    input1 = Input("text", style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px",
        "width": "200px",
        "margin-right": "10px"
    })
    input1.set_attribute("placeholder", "Type here...")

    input2 = Input("text", style={
        "padding": "10px",
        "border": "1px solid #ddd",
        "border-radius": "4px",
        "width": "200px"
    })
    input2.set_attribute("placeholder", "Or here...")

    input_log = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#e3f2fd",
        "border-radius": "4px"
    })
    input_log.add(P("Both inputs monitored:", style={"margin": "0"}))

    # Monitor both inputs with one handler
    @when(input1.events.input | input2.events.input)
    def on_any_input(sender, dom_event):
        value = dom_event.target.value
        which = "first" if sender == input1 else "second"
        input_log.clear()
        input_log.add(P(f"Typing in {which} input: '{value}'", style={"margin": "0"}))

    DOM.add(
        Div(input1, input2),
        input_log
    )

    # ========== Demo 4: Mouse Events ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("4. Mouse Events (Pre-registered)"),
        P("All mouse events are pre-registered: ", Code("mouseenter"), ", ", Code("mouseleave"), ", etc.")
    )

    hover_box1 = Div("Hover Box 1", style={
        "display": "inline-block",
        "padding": "40px",
        "background-color": "#f0f0f0",
        "border": "2px solid #ddd",
        "border-radius": "4px",
        "margin-right": "20px",
        "cursor": "pointer",
        "transition": "all 0.3s"
    })

    hover_box2 = Div("Hover Box 2", style={
        "display": "inline-block",
        "padding": "40px",
        "background-color": "#f0f0f0",
        "border": "2px solid #ddd",
        "border-radius": "4px",
        "cursor": "pointer",
        "transition": "all 0.3s"
    })

    # Handle hover for both boxes with one handler
    @when(hover_box1.events.mouseenter | hover_box2.events.mouseenter)
    def on_mouse_enter(sender, dom_event):
        sender.style.background_color = "#007bff"
        sender.style.color = "white"
        sender.style.transform = "scale(1.05)"

    @when(hover_box1.events.mouseleave | hover_box2.events.mouseleave)
    def on_mouse_leave(sender, dom_event):
        sender.style.background_color = "#f0f0f0"
        sender.style.color = "black"
        sender.style.transform = "scale(1)"

    DOM.add(Div(hover_box1, hover_box2))

    # ========== Demo 5: Combining Modal Events ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("5. Combining Macro Events"),
        P("Works with macro events too!")
    )

    from antioch.macros import Modal

    modal1 = Modal(title="Modal 1", content=P("First modal"))
    modal2 = Modal(title="Modal 2", content=P("Second modal"))

    DOM.add(modal1.element, modal2.element)

    modal_log = Div(style={
        "margin-top": "15px",
        "padding": "10px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "min-height": "60px"
    })
    modal_log.add(P("Modal events:", style={"margin": "0 0 5px 0", "font-weight": "bold"}))

    # Watch both modals with one handler
    @when(modal1.events.open | modal2.events.open)
    def on_any_modal_open(sender):
        title = sender._get_state('title')
        modal_log.add(Div(f"✓ {title} opened", style={"color": "#28a745", "margin": "2px 0"}))

    @when(modal1.events.close | modal2.events.close)
    def on_any_modal_close(sender):
        title = sender._get_state('title')
        modal_log.add(Div(f"✗ {title} closed", style={"color": "#dc3545", "margin": "2px 0"}))

    open_modal1_btn = Button("Open Modal 1", style={
        "padding": "10px 20px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-right": "10px"
    })
    open_modal1_btn.on_click(lambda e: modal1.open())

    open_modal2_btn = Button("Open Modal 2", style={
        "padding": "10px 20px",
        "background-color": "#28a745",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer"
    })
    open_modal2_btn.on_click(lambda e: modal2.open())

    DOM.add(
        Div(open_modal1_btn, open_modal2_btn),
        modal_log,
        Pre(Code("""@when(modal1.events.open | modal2.events.open)
def on_any_modal_open(sender):
    print(f"{sender} opened!")
""", style={
            "background-color": "#f5f5f5",
            "padding": "12px",
            "border-radius": "4px",
            "margin-top": "10px",
            "font-size": "13px"
        }))
    )

    # ========== Summary ==========
    DOM.add(
        Hr(style={"margin": "30px 0"}),
        H2("Summary"),
        Ul(
            Li(Strong("Pre-registered events:"), " All elements have common events ready to use"),
            Li(Strong("Element-specific:"), " Input, Form, etc. have their specific events pre-registered"),
            Li(Strong("Combine with | :"), " Use ", Code("event1 | event2 | event3"), " for multi-event handlers"),
            Li(Strong("Works everywhere:"), " Elements, Macros, DOM - all use the same pattern"),
            Li(Strong("No boilerplate:"), " Just use ", Code("element.events.click"), " directly!")
        ),

        H3("Available Events on All Elements"),
        P("Pre-registered on every element:"),
        Ul(
            Li(Code("click"), ", ", Code("dblclick")),
            Li(Code("mouseenter"), ", ", Code("mouseleave"), ", ", Code("mousedown"), ", ", Code("mouseup"), ", ", Code("mousemove")),
            Li(Code("focus"), ", ", Code("blur")),
            Li(Code("keydown"), ", ", Code("keyup"), ", ", Code("keypress"))
        ),

        H3("Element-Specific Events"),
        Ul(
            Li(Strong("Input/Textarea:"), " ", Code("input"), ", ", Code("change")),
            Li(Strong("Select:"), " ", Code("change")),
            Li(Strong("Form:"), " ", Code("submit"), ", ", Code("reset")),
            Li(Strong("Img:"), " ", Code("load"), ", ", Code("error")),
            Li(Strong("Video/Audio:"), " ", Code("play"), ", ", Code("pause"), ", ", Code("ended"), ", ", Code("timeupdate"))
        )
    )


if __name__ == "__main__":
    main()
