"""
Window and WindowManager macros - Draggable, resizable windows with taskbar.

Provides a complete windowing system similar to desktop operating systems,
with features like window snapping, minimize/maximize/close, and a taskbar.
"""
from .base import Macro
from ..elements import Div, Button, Span
from pyodide.ffi import create_proxy
import js


class Window(Macro):
    """Individual draggable, resizable window."""

    def __init__(self, title="Window", content=None, x=100, y=100,
                 width=600, height=400, minimized=False, maximized=False,
                 resizable=True, container_style=None, **kwargs):
        """
        Initialize a window.

        Args:
            title: Window title text
            content: Content to display (Element or HTML string)
            x, y: Initial position
            width, height: Initial size
            minimized: Start minimized
            maximized: Start maximized
            resizable: Whether window can be resized
            container_style: Custom styles for window container
        """
        super().__init__(macro_type="window", **kwargs)

        # Set up window state
        self._set_state(
            title=title,
            content=content or "",
            x=x,
            y=y,
            width=width,
            height=height,
            minimized=minimized,
            maximized=maximized,
            resizable=resizable,
            z_index=1000,
            is_dragging=False,
            is_resizing=False,
            resize_direction=None,
            saved_state=None  # For restore from min/max
        )

        # Add callback types
        self._add_callback_type('close')
        self._add_callback_type('minimize')
        self._add_callback_type('maximize')
        self._add_callback_type('restore')
        self._add_callback_type('focus')

        # Default container style
        default_container_style = {
            "position": "absolute",
            "background": "white",
            "border": "1px solid #ccc",
            "border_radius": "8px",
            "box_shadow": "0 4px 20px rgba(0,0,0,0.3)",
            "display": "flex",
            "flex_direction": "column",
            "min_width": "200px",
            "min_height": "100px",
            "user_select": "none"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Initialize macro
        self._init_macro()

    def _get_window_style(self):
        """Get computed style dict for window positioning."""
        visibility = "hidden" if self._get_state('minimized') else "visible"
        return {
            **self._container_style,
            "left": f"{self._get_state('x')}px",
            "top": f"{self._get_state('y')}px",
            "width": f"{self._get_state('width')}px",
            "height": f"{self._get_state('height')}px",
            "z_index": str(self._get_state('z_index')),
            "visibility": visibility
        }

    def _create_elements(self):
        """Create the window DOM structure."""
        # Main window container
        window_div = Div(
            id=self._id,
            class_="antioch-window",
            style=self._get_window_style()
        )

        # Title bar
        titlebar = Div(
            class_="antioch-window-titlebar",
            data_macro_id=self._id,
            data_action="drag"
        )
        titlebar.style.update({
            "background": "linear-gradient(to bottom, #f0f0f0, #e0e0e0)",
            "border_bottom": "1px solid #ccc",
            "border_radius": "7px 7px 0 0",
            "padding": "8px 12px",
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "cursor": "move",
            "user_select": "none",
            "font_size": "14px"
        })

        # Title text
        title_span = Span(class_="antioch-window-title")
        title_span.add(self._get_state('title'))
        title_span.style.update({
            "font_weight": "500",
            "flex": "1",
            "white_space": "nowrap",
            "overflow": "hidden",
            "text_overflow": "ellipsis"
        })

        # Window controls
        controls = Div(class_="antioch-window-controls")
        controls.style.update({
            "display": "flex",
            "gap": "4px"
        })

        # Minimize button
        min_btn = Button("−", class_="antioch-window-btn antioch-minimize-btn",
                        data_macro_id=self._id, data_action="minimize")
        min_btn.style.update(self._get_button_style())

        # Maximize button
        max_btn = Button("□", class_="antioch-window-btn antioch-maximize-btn",
                        data_macro_id=self._id, data_action="maximize")
        max_btn.style.update(self._get_button_style())

        # Close button
        close_btn = Button("×", class_="antioch-window-btn antioch-close-btn",
                          data_macro_id=self._id, data_action="close")
        close_btn.style.update(self._get_button_style())

        controls.add(min_btn, max_btn, close_btn)
        titlebar.add(title_span, controls)

        # Content area
        content_div = Div(class_="antioch-window-content",
                         data_macro_id=self._id)
        content_div.style.update({
            "flex": "1",
            "padding": "12px",
            "overflow": "auto"
        })

        content = self._get_state('content')
        if content:
            content_div.add(content)

        window_div.add(titlebar, content_div)

        # Add resize handles if resizable
        if self._get_state('resizable'):
            for direction in ['n', 's', 'e', 'w', 'ne', 'nw', 'se', 'sw']:
                handle = Div(
                    class_=f"antioch-resize-handle antioch-resize-{direction}",
                    data_macro_id=self._id,
                    data_action="resize",
                    data_direction=direction
                )
                handle.style.update(self._get_resize_handle_style(direction))
                window_div.add(handle)

        return window_div

    def _get_button_style(self):
        """Get style for window control buttons."""
        return {
            "width": "18px",
            "height": "18px",
            "border": "1px solid #999",
            "border_radius": "50%",
            "background": "linear-gradient(to bottom, #fff, #f0f0f0)",
            "cursor": "pointer",
            "font_size": "12px",
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "line_height": "1",
            "padding": "0",
            "margin": "0"
        }

    def _get_resize_handle_style(self, direction):
        """Get style for resize handles based on direction."""
        base = {
            "position": "absolute",
            "background": "transparent"
        }

        styles = {
            'n': {"top": "-3px", "left": "3px", "right": "3px", "height": "6px", "cursor": "n-resize"},
            's': {"bottom": "-3px", "left": "3px", "right": "3px", "height": "6px", "cursor": "s-resize"},
            'e': {"right": "-3px", "top": "3px", "bottom": "3px", "width": "6px", "cursor": "e-resize"},
            'w': {"left": "-3px", "top": "3px", "bottom": "3px", "width": "6px", "cursor": "w-resize"},
            'ne': {"top": "-3px", "right": "-3px", "width": "6px", "height": "6px", "cursor": "ne-resize"},
            'nw': {"top": "-3px", "left": "-3px", "width": "6px", "height": "6px", "cursor": "nw-resize"},
            'se': {"bottom": "-3px", "right": "-3px", "width": "6px", "height": "6px", "cursor": "se-resize"},
            'sw': {"bottom": "-3px", "left": "-3px", "width": "6px", "height": "6px", "cursor": "sw-resize"}
        }

        return {**base, **styles.get(direction, {})}

    def set_content(self, content):
        """Update window content."""
        self._set_state(content=content)

        # Update DOM if initialized
        if self._root_element:
            content_el = self._root_element._dom_element.querySelector('.antioch-window-content')
            if content_el:
                content_el.innerHTML = ""
                if hasattr(content, '_root_element'):
                    content_el.appendChild(content._dom_element)
                else:
                    content_el.innerHTML = str(content)

        return self

    def set_title(self, title):
        """Update window title."""
        self._set_state(title=title)

        # Update DOM if initialized
        if self._root_element:
            title_el = self._root_element._dom_element.querySelector('.antioch-window-title')
            if title_el:
                title_el.textContent = title

        return self

    def focus(self):
        """Bring window to front."""
        # This will be handled by WindowManager
        self._trigger_callbacks('focus')
        return self

    def minimize(self):
        """Minimize the window."""
        if not self._get_state('minimized'):
            # Save current state
            self._set_state(
                saved_state={
                    'x': self._get_state('x'),
                    'y': self._get_state('y'),
                    'width': self._get_state('width'),
                    'height': self._get_state('height'),
                    'maximized': self._get_state('maximized')
                },
                minimized=True
            )

            # Update visibility
            if self._root_element:
                self._root_element._dom_element.style.visibility = "hidden"

            self._trigger_callbacks('minimize')

        return self

    def maximize(self):
        """Maximize the window."""
        if not self._get_state('maximized'):
            # Save current state
            self._set_state(
                saved_state={
                    'x': self._get_state('x'),
                    'y': self._get_state('y'),
                    'width': self._get_state('width'),
                    'height': self._get_state('height'),
                    'minimized': self._get_state('minimized')
                },
                maximized=True,
                x=0,
                y=40,  # Below taskbar
                width=js.window.innerWidth,
                height=js.window.innerHeight - 40
            )

            # Update DOM
            self._update_position_and_size()
            self._trigger_callbacks('maximize')

        return self

    def restore(self):
        """Restore from minimized or maximized state."""
        saved = self._get_state('saved_state')
        if saved:
            self._set_state(
                x=saved['x'],
                y=saved['y'],
                width=saved['width'],
                height=saved['height'],
                minimized=False,
                maximized=False,
                saved_state=None
            )

            # Update DOM
            if self._root_element:
                self._root_element._dom_element.style.visibility = "visible"
            self._update_position_and_size()
            self._trigger_callbacks('restore')

        return self

    def close(self):
        """Close the window."""
        self._trigger_callbacks('close')
        return self

    def _update_position_and_size(self):
        """Update DOM element position and size from state."""
        if self._root_element:
            self._root_element._dom_element.style.left = f"{self._get_state('x')}px"
            self._root_element._dom_element.style.top = f"{self._get_state('y')}px"
            self._root_element._dom_element.style.width = f"{self._get_state('width')}px"
            self._root_element._dom_element.style.height = f"{self._get_state('height')}px"
            self._root_element._dom_element.style.zIndex = str(self._get_state('z_index'))