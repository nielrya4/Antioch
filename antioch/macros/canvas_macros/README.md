# Canvas Macros

Reusable interactive components for WebCanvas.

## Overview

Canvas Macros provide a way to create reusable, interactive components that live within a WebCanvas instead of the DOM. They're similar to regular Antioch Macros but designed specifically for canvas-based applications.

## Features

- **Position & Size Management**: Easy positioning and sizing with properties
- **Mouse Interaction**: Built-in handling for click, hover, move events
- **State Management**: Internal state dictionary with change callbacks
- **Callback System**: Event-driven architecture for component interaction
- **Visibility & Enabled State**: Show/hide and enable/disable functionality
- **Hit Testing**: Automatic bounds checking for mouse events
- **Lifecycle Management**: Clean initialization and destruction

## Base Class: CanvasMacro

All canvas components inherit from `CanvasMacro`:

```python
from antioch.macros.canvas_macros import CanvasMacro

class MyComponent(CanvasMacro):
    def __init__(self, x, y, width, height, **kwargs):
        super().__init__(x, y, width, height, macro_type="my_component", **kwargs)

        # Initialize state
        self._set_state(
            color="#ff0000",
            label="Hello"
        )

        # Register callback types
        self._add_callback_type('click')

    def draw(self, canvas):
        """Draw the component."""
        if not self._visible:
            return

        # Draw your component
        color = self._get_state('color')
        canvas.rect(self._x, self._y, self._width, self._height, fill=color)

        label = self._get_state('label')
        canvas.text(label, self._x + self._width/2, self._y + self._height/2,
                   fill="#fff", align="center", baseline="middle")
```

## Using Canvas Macros

### 1. Create Components

```python
from antioch.macros.canvas_macros import CanvasButton

# Create a button
button = CanvasButton(
    x=50, y=50, width=150, height=50,
    text="Click Me!",
    bg_color="#3498db",
    hover_color="#2980b9"
)

# Register callbacks
button.on_click(lambda btn: print("Button clicked!"))
button.on('mouse_enter', lambda btn: print("Mouse over button"))
```

### 2. Setup Canvas and Mouse Handlers

```python
from antioch.macros import WebCanvas

canvas = WebCanvas(width=800, height=600)
components = [button]  # List of your components

# Setup mouse event propagation
canvas_element = canvas._get_element('canvas')

def get_mouse_pos(event):
    rect = canvas_element._dom_element.getBoundingClientRect()
    return event.clientX - rect.left, event.clientY - rect.top

def on_mousedown(event):
    x, y = get_mouse_pos(event)
    for comp in reversed(components):  # Reverse for z-index
        if comp.handle_mouse_down(x, y):
            break  # Stop propagation

def on_mouseup(event):
    x, y = get_mouse_pos(event)
    for comp in components:
        comp.handle_mouse_up(x, y)

def on_mousemove(event):
    x, y = get_mouse_pos(event)
    for comp in components:
        comp.handle_mouse_move(x, y)

canvas_element.on_mousedown(on_mousedown)
canvas_element.on_mouseup(on_mouseup)
canvas_element.on('mousemove', on_mousemove)
```

### 3. Draw in Animation Loop

```python
import js
from pyodide.ffi import create_proxy

def game_loop():
    canvas.clear("#ffffff")

    # Draw all components
    for comp in components:
        comp.draw(canvas)

    js.requestAnimationFrame(create_proxy(lambda t: game_loop()))

game_loop()
```

## Available Components

### CanvasButton

A clickable button with hover effects.

```python
from antioch.macros.canvas_macros import CanvasButton

button = CanvasButton(
    x=100, y=100, width=200, height=60,
    text="My Button",
    bg_color="#3498db",      # Normal background
    hover_color="#2980b9",   # Hover background
    text_color="#ffffff",    # Text color
    font="18px Arial",       # Font
    border_radius=5          # Corner radius
)

button.on_click(lambda btn: print("Clicked!"))
```

## Properties

### Position and Size
- `x`, `y` - Position (read/write)
- `width`, `height` - Dimensions (read/write)
- `bounds` - Tuple of (x, y, width, height) (read-only)

### State
- `visible` - Show/hide component (read/write)
- `enabled` - Enable/disable interaction (read/write)
- `state` - State dictionary copy (read-only)

### Methods
- `set_position(x, y)` - Set position
- `set_size(width, height)` - Set size
- `contains_point(x, y)` - Check if point is inside bounds
- `get_local_coords(x, y)` - Convert canvas coords to local coords
- `show()` / `hide()` / `toggle()` - Visibility control
- `enable()` / `disable()` - Interaction control

## Events

Canvas macros support these events:

- `click` - Component clicked
- `mouse_down` - Mouse button pressed on component
- `mouse_up` - Mouse button released on component
- `mouse_move` - Mouse moved over component
- `mouse_enter` - Mouse entered component bounds
- `mouse_leave` - Mouse left component bounds
- `position_change` - Position changed
- `size_change` - Size changed
- `enabled_change` - Enabled state changed
- `show` / `hide` - Visibility changed
- `state_change` - Internal state changed

## Creating Custom Components

Extend `CanvasMacro` and implement the `draw()` method:

```python
class MySlider(CanvasMacro):
    def __init__(self, x, y, width, height, min_val=0, max_val=100, **kwargs):
        super().__init__(x, y, width, height, macro_type="slider", **kwargs)

        self._set_state(
            value=min_val,
            min_val=min_val,
            max_val=max_val,
            dragging=False
        )

        self._add_callback_type('change')

    def draw(self, canvas):
        if not self._visible:
            return

        # Draw track
        canvas.rect(self._x, self._y + self._height/2 - 2,
                   self._width, 4, fill="#ddd")

        # Draw thumb
        value = self._get_state('value')
        min_val = self._get_state('min_val')
        max_val = self._get_state('max_val')

        ratio = (value - min_val) / (max_val - min_val)
        thumb_x = self._x + ratio * self._width

        thumb_color = "#2980b9" if self._mouse_over else "#3498db"
        canvas.circle(thumb_x, self._y + self._height/2, 8, fill=thumb_color)

    def handle_mouse_down(self, x, y):
        if super().handle_mouse_down(x, y):
            self._set_state(dragging=True)
            self._update_value_from_mouse(x)
            return True
        return False

    def handle_mouse_move(self, x, y):
        super().handle_mouse_move(x, y)
        if self._get_state('dragging'):
            self._update_value_from_mouse(x)

    def handle_mouse_up(self, x, y):
        self._set_state(dragging=False)
        return super().handle_mouse_up(x, y)

    def _update_value_from_mouse(self, x):
        ratio = (x - self._x) / self._width
        ratio = max(0, min(1, ratio))  # Clamp to 0-1

        min_val = self._get_state('min_val')
        max_val = self._get_state('max_val')
        new_value = min_val + ratio * (max_val - min_val)

        old_value = self._get_state('value')
        self._set_state(value=new_value)
        self._trigger_callbacks('change', new_value, old_value)
```

## Examples

See `scripts/canvas_macros_demo.py` for a complete working example with multiple interactive buttons.

## Best Practices

1. **Always check visibility**: Start `draw()` with visibility check
2. **Use state management**: Store component data in `_state` dict
3. **Trigger callbacks**: Notify listeners of important events
4. **Handle z-order**: Process mouse events in reverse order for proper layering
5. **Clean up**: Call `destroy()` when removing components
6. **Return self**: Enable method chaining in public methods
