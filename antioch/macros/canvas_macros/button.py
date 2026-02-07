"""
CanvasButton - A simple button component for WebCanvas.

Example of a canvas macro component.
"""
from typing import Optional
from .base import CanvasMacro


class CanvasButton(CanvasMacro):
    """
    A clickable button component for canvas.

    Features:
    - Text label
    - Hover effects
    - Click detection
    - Customizable colors
    """

    def __init__(self, x: float, y: float, width: float, height: float,
                 text: str = "Button",
                 bg_color: str = "#3498db",
                 hover_color: str = "#2980b9",
                 text_color: str = "#ffffff",
                 font: str = "16px Arial",
                 border_radius: float = 5,
                 **kwargs):
        """
        Initialize a canvas button.

        Args:
            x: X position
            y: Y position
            width: Button width
            height: Button height
            text: Button label text
            bg_color: Background color
            hover_color: Background color on hover
            text_color: Text color
            font: Font specification
            border_radius: Corner radius for rounded corners
            **kwargs: Additional arguments passed to CanvasMacro
        """
        super().__init__(x, y, width, height, macro_type="canvas_button", **kwargs)

        # Button properties
        self._set_state(
            text=text,
            bg_color=bg_color,
            hover_color=hover_color,
            text_color=text_color,
            font=font,
            border_radius=border_radius
        )

        # Register callback types
        self._add_callback_type('click')
        self._add_callback_type('mouse_enter')
        self._add_callback_type('mouse_leave')

    def draw(self, canvas):
        """Draw the button on the canvas."""
        if not self._visible:
            return

        # Get current colors based on state
        bg = self._get_state('hover_color') if self._mouse_over else self._get_state('bg_color')

        # Draw button background (rounded rectangle)
        radius = self._get_state('border_radius')
        if radius > 0:
            # Draw rounded rectangle using path
            canvas.save()
            canvas.begin_path()

            # Top-left corner
            canvas.move_to(self._x + radius, self._y)

            # Top edge and top-right corner
            canvas.line_to(self._x + self._width - radius, self._y)
            canvas.arc_to(
                self._x + self._width, self._y,
                self._x + self._width, self._y + radius,
                radius
            )

            # Right edge and bottom-right corner
            canvas.line_to(self._x + self._width, self._y + self._height - radius)
            canvas.arc_to(
                self._x + self._width, self._y + self._height,
                self._x + self._width - radius, self._y + self._height,
                radius
            )

            # Bottom edge and bottom-left corner
            canvas.line_to(self._x + radius, self._y + self._height)
            canvas.arc_to(
                self._x, self._y + self._height,
                self._x, self._y + self._height - radius,
                radius
            )

            # Left edge and top-left corner
            canvas.line_to(self._x, self._y + radius)
            canvas.arc_to(
                self._x, self._y,
                self._x + radius, self._y,
                radius
            )

            canvas.close_path()
            canvas.fill(bg)
            canvas.restore()
        else:
            # Simple rectangle
            canvas.rect(self._x, self._y, self._width, self._height, fill=bg)

        # Draw text centered
        text = self._get_state('text')
        text_color = self._get_state('text_color')
        font = self._get_state('font')

        canvas.text(
            text,
            self._x + self._width / 2,
            self._y + self._height / 2,
            fill=text_color,
            font=font,
            align="center",
            baseline="middle"
        )

        # Draw disabled overlay if not enabled
        if not self._enabled:
            canvas.rect(
                self._x, self._y, self._width, self._height,
                fill="rgba(128, 128, 128, 0.5)"
            )

    def set_text(self, text: str) -> 'CanvasButton':
        """
        Set button text.

        Args:
            text: New button text

        Returns:
            Self for method chaining
        """
        self._set_state(text=text)
        return self

    def on_click(self, callback) -> 'CanvasButton':
        """
        Register a click callback.

        Args:
            callback: Function to call on click

        Returns:
            Self for method chaining

        Example:
            button.on_click(lambda btn: print("Button clicked!"))
        """
        return self.on('click', callback)
