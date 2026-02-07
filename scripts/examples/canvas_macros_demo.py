"""
Canvas Macros Demo - Demonstrating reusable canvas components.

Shows how to use CanvasMacro base class and canvas components
like CanvasButton within a WebCanvas.
"""

import js
from pyodide.ffi import create_proxy
from antioch import DOM, Div, H1, H2, P
from antioch.macros import WebCanvas
from antioch.macros.canvas_macros import CanvasButton


class CanvasMacrosDemo:
    """Demo application showing canvas macro usage."""

    def __init__(self):
        # Create canvas
        self.canvas = WebCanvas(
            width=800,
            height=600,
            background="#ecf0f1"
        )

        # List of canvas macros
        self.components = []

        # Message display
        self.message = "Click buttons or hover over them!"
        self.message_timer = 0

        # Setup canvas macros
        self._setup_components()

        # Setup mouse handlers
        self._setup_mouse_handlers()

    def _setup_components(self):
        """Create canvas macro components."""
        # Button 1 - Basic button
        btn1 = CanvasButton(
            x=50, y=50, width=150, height=50,
            text="Click Me!",
            bg_color="#3498db",
            hover_color="#2980b9"
        )
        btn1.on_click(lambda btn, x, y: self.show_message("Button 1 clicked!"))
        btn1.on('mouse_enter', lambda btn: self.show_message("Hovering Button 1"))
        self.components.append(btn1)

        # Button 2 - Success style
        btn2 = CanvasButton(
            x=220, y=50, width=150, height=50,
            text="Success",
            bg_color="#2ecc71",
            hover_color="#27ae60"
        )
        btn2.on_click(lambda btn, x, y: self.show_message("Success button clicked!"))
        self.components.append(btn2)

        # Button 3 - Warning style
        btn3 = CanvasButton(
            x=390, y=50, width=150, height=50,
            text="Warning",
            bg_color="#f39c12",
            hover_color="#e67e22"
        )
        btn3.on_click(lambda btn, x, y: self.show_message("Warning button clicked!"))
        self.components.append(btn3)

        # Button 4 - Danger style
        btn4 = CanvasButton(
            x=560, y=50, width=150, height=50,
            text="Danger",
            bg_color="#e74c3c",
            hover_color="#c0392b"
        )
        btn4.on_click(lambda btn, x, y: self.show_message("Danger button clicked!"))
        self.components.append(btn4)

        # Button 5 - Large button
        btn5 = CanvasButton(
            x=50, y=130, width=300, height=80,
            text="Large Button",
            bg_color="#9b59b6",
            hover_color="#8e44ad",
            font="bold 24px Arial",
            border_radius=10
        )
        btn5.on_click(lambda btn, x, y: self.show_message("Large button clicked!"))
        self.components.append(btn5)

        # Button 6 - Toggle enabled/disabled
        btn6 = CanvasButton(
            x=370, y=130, width=200, height=80,
            text="Toggle Others",
            bg_color="#34495e",
            hover_color="#2c3e50",
            font="bold 20px Arial"
        )

        def toggle_others(btn, x, y):
            for comp in self.components:
                if comp != btn6:
                    comp.enabled = not comp.enabled
            state = "disabled" if not btn1.enabled else "enabled"
            self.show_message(f"Other buttons {state}!")

        btn6.on_click(toggle_others)
        self.components.append(btn6)

        # Button 7 - Small buttons
        for i in range(5):
            btn = CanvasButton(
                x=50 + i * 90, y=240, width=80, height=40,
                text=f"Btn {i+1}",
                bg_color="#16a085",
                hover_color="#1abc9c",
                font="14px Arial",
                border_radius=3
            )
            btn.on_click(lambda b, x, y, idx=i: self.show_message(f"Small button {idx+1} clicked!"))
            self.components.append(btn)

        # Button 8 - Hide/Show demo
        hidden_btn = CanvasButton(
            x=50, y=310, width=150, height=50,
            text="Hidden Target",
            bg_color="#7f8c8d",
            hover_color="#95a5a6"
        )
        hidden_btn.on_click(lambda btn, x, y: self.show_message("Hidden button clicked!"))
        self.components.append(hidden_btn)

        toggle_vis_btn = CanvasButton(
            x=220, y=310, width=150, height=50,
            text="Toggle Hidden",
            bg_color="#2c3e50",
            hover_color="#34495e"
        )
        toggle_vis_btn.on_click(lambda btn, x, y: self.toggle_button(hidden_btn))
        self.components.append(toggle_vis_btn)

        # Button 9 - Dynamic text change
        counter_btn = CanvasButton(
            x=50, y=390, width=200, height=60,
            text="Click Count: 0",
            bg_color="#d35400",
            hover_color="#e67e22",
            font="16px Arial"
        )
        counter_btn._click_count = 0

        def increment_counter(btn, x, y):
            btn._click_count += 1
            btn.set_text(f"Click Count: {btn._click_count}")
            self.show_message(f"Clicked {btn._click_count} times!")

        counter_btn.on_click(increment_counter)
        self.components.append(counter_btn)

        # Info display area
        self.info_area = {
            'x': 50,
            'y': 480,
            'width': 700,
            'height': 100
        }

    def _setup_mouse_handlers(self):
        """Setup canvas mouse event handlers."""
        canvas_element = self.canvas._get_element('canvas')

        def get_mouse_pos(event):
            rect = canvas_element._dom_element.getBoundingClientRect()
            return event.clientX - rect.left, event.clientY - rect.top

        def on_mousedown(event):
            x, y = get_mouse_pos(event)
            # Propagate to components (in reverse order for proper z-index)
            for comp in reversed(self.components):
                if comp.handle_mouse_down(x, y):
                    break  # Stop propagation if handled

        def on_mouseup(event):
            x, y = get_mouse_pos(event)
            for comp in reversed(self.components):
                comp.handle_mouse_up(x, y)

        def on_mousemove(event):
            x, y = get_mouse_pos(event)
            for comp in self.components:
                comp.handle_mouse_move(x, y)

        canvas_element.on_mousedown(on_mousedown)
        canvas_element.on_mouseup(on_mouseup)
        canvas_element.on('mousemove', on_mousemove)

    def show_message(self, message: str):
        """Display a temporary message."""
        self.message = message
        self.message_timer = 120  # Show for ~2 seconds at 60fps

    def toggle_button(self, button):
        """Toggle button visibility."""
        button.toggle()
        state = "shown" if button.visible else "hidden"
        self.show_message(f"Button {state}!")

    def draw(self):
        """Draw all components."""
        # Clear canvas
        self.canvas.clear("#ecf0f1")

        # Draw title
        self.canvas.text(
            "Canvas Macros Demo - Interactive Canvas Components",
            400, 20,
            fill="#2c3e50",
            font="bold 20px Arial",
            align="center"
        )

        # Draw all components
        for comp in self.components:
            comp.draw(self.canvas)

        # Draw info area
        info = self.info_area
        self.canvas.rect(
            info['x'], info['y'], info['width'], info['height'],
            fill="#ffffff",
            stroke="#bdc3c7",
            line_width=2
        )

        # Draw message
        if self.message_timer > 0:
            self.canvas.text(
                self.message,
                info['x'] + info['width'] / 2,
                info['y'] + 30,
                fill="#2c3e50",
                font="18px Arial",
                align="center"
            )
            self.message_timer -= 1

        # Draw instructions
        self.canvas.text(
            "Hover over buttons to see effects. Click to interact!",
            info['x'] + info['width'] / 2,
            info['y'] + 65,
            fill="#7f8c8d",
            font="14px Arial",
            align="center"
        )

    def game_loop(self):
        """Main animation loop."""
        self.draw()

        # Continue animation
        js.requestAnimationFrame(
            create_proxy(lambda t: self.game_loop())
        )

    def get_element(self):
        """Get the canvas element."""
        return self.canvas.element


def main():
    """Create and display the canvas macros demo."""
    container = Div(style={
        "max_width": "850px",
        "margin": "20px auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif",
        "background_color": "#ffffff",
        "border_radius": "8px",
        "box_shadow": "0 2px 8px rgba(0,0,0,0.1)"
    })

    # Title
    title = H1("Canvas Macros Demo", style={
        "text_align": "center",
        "color": "#2c3e50",
        "margin_bottom": "10px"
    })

    subtitle = H2("Reusable Interactive Canvas Components", style={
        "text_align": "center",
        "color": "#7f8c8d",
        "font_size": "18px",
        "font_weight": "normal",
        "margin_bottom": "20px"
    })

    # Description
    description = Div(style={
        "background_color": "#ecf0f1",
        "padding": "15px",
        "border_radius": "6px",
        "margin_bottom": "20px"
    })

    description.add(
        P("✨ Features:", style={"font_weight": "bold", "margin": "0 0 10px 0"}),
        P("• CanvasMacro base class for building reusable components", style={"margin": "5px 0"}),
        P("• Built-in mouse interaction handling (click, hover, move)", style={"margin": "5px 0"}),
        P("• State management and callback system", style={"margin": "5px 0"}),
        P("• Position, size, visibility, and enabled state", style={"margin": "5px 0"}),
        P("• Example: CanvasButton with hover effects and click detection", style={"margin": "5px 0"})
    )

    # Create demo
    demo = CanvasMacrosDemo()

    # Add everything to container
    container.add(title, subtitle, description, demo.get_element())

    # Add to DOM
    DOM.add(container)

    # Start the animation loop
    demo.game_loop()


# Run when explicitly called from main.py
# (Don't run on import, only when main() is called)
