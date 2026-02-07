"""
CanvasMacro base class - Foundation for canvas-based interactive components.

Provides common functionality for creating reusable, interactive components
that live within a WebCanvas instead of the DOM.
"""
import uuid
from typing import Dict, Any, List, Callable, Optional, Tuple


class CanvasMacro:
    """
    Base class for canvas-based interactive components.

    Similar to the regular Macro class but designed for canvas drawing.
    Provides:
    - Unique ID generation
    - Position and size management
    - State management
    - Callback system
    - Mouse interaction helpers
    - Drawing abstraction

    To create a canvas macro, inherit from this class and implement:
    - draw(canvas): Draw the component on the canvas
    - Optional: handle_mouse_down(x, y), handle_mouse_move(x, y), etc.
    """

    def __init__(self, x: float, y: float, width: float, height: float,
                 macro_type: str = "canvas_macro", **kwargs):
        """
        Initialize base canvas macro functionality.

        Args:
            x: X position on canvas
            y: Y position on canvas
            width: Component width
            height: Component height
            macro_type: Type identifier for this macro
            **kwargs: Additional arguments (passed to subclasses)
        """
        # Generate unique ID for this instance
        self._id = f"{macro_type}_{str(uuid.uuid4())[:8]}"
        self._macro_type = macro_type

        # Position and size
        self._x = x
        self._y = y
        self._width = width
        self._height = height

        # Visibility and interaction
        self._visible = True
        self._enabled = True

        # State management
        self._state: Dict[str, Any] = {}
        self._destroyed = False

        # Callback management
        self._callbacks: Dict[str, List[Callable]] = {}

        # Mouse state (for handling hover, etc.)
        self._mouse_over = False
        self._mouse_down = False

        # Store constructor kwargs for subclass access
        self._kwargs = kwargs

    # ========== Properties ==========

    @property
    def id(self) -> str:
        """Get the unique ID for this macro instance."""
        return self._id

    @property
    def x(self) -> float:
        """Get X position."""
        return self._x

    @x.setter
    def x(self, value: float):
        """Set X position."""
        self._x = value
        self._trigger_callbacks('position_change', self._x, self._y)

    @property
    def y(self) -> float:
        """Get Y position."""
        return self._y

    @y.setter
    def y(self, value: float):
        """Set Y position."""
        self._y = value
        self._trigger_callbacks('position_change', self._x, self._y)

    @property
    def width(self) -> float:
        """Get width."""
        return self._width

    @width.setter
    def width(self, value: float):
        """Set width."""
        self._width = value
        self._trigger_callbacks('size_change', self._width, self._height)

    @property
    def height(self) -> float:
        """Get height."""
        return self._height

    @height.setter
    def height(self, value: float):
        """Set height."""
        self._height = value
        self._trigger_callbacks('size_change', self._width, self._height)

    @property
    def visible(self) -> bool:
        """Get visibility state."""
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        """Set visibility state."""
        old_visible = self._visible
        self._visible = value
        if old_visible != value:
            event = 'show' if value else 'hide'
            self._trigger_callbacks(event)

    @property
    def enabled(self) -> bool:
        """Get enabled state."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        """Set enabled state."""
        old_enabled = self._enabled
        self._enabled = value
        if old_enabled != value:
            self._trigger_callbacks('enabled_change', value)

    @property
    def state(self) -> Dict[str, Any]:
        """Get the current state dictionary (copy)."""
        return self._state.copy()

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Get component bounds as (x, y, width, height)."""
        return (self._x, self._y, self._width, self._height)

    # ========== Position and Hit Testing ==========

    def set_position(self, x: float, y: float) -> 'CanvasMacro':
        """
        Set position of this component.

        Args:
            x: New X position
            y: New Y position

        Returns:
            Self for method chaining
        """
        self._x = x
        self._y = y
        self._trigger_callbacks('position_change', x, y)
        return self

    def set_size(self, width: float, height: float) -> 'CanvasMacro':
        """
        Set size of this component.

        Args:
            width: New width
            height: New height

        Returns:
            Self for method chaining
        """
        self._width = width
        self._height = height
        self._trigger_callbacks('size_change', width, height)
        return self

    def contains_point(self, x: float, y: float) -> bool:
        """
        Check if a point is within this component's bounds.

        Args:
            x: X coordinate to test
            y: Y coordinate to test

        Returns:
            True if point is inside component
        """
        return (self._x <= x <= self._x + self._width and
                self._y <= y <= self._y + self._height)

    def get_local_coords(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert canvas coordinates to local component coordinates.

        Args:
            x: Canvas X coordinate
            y: Canvas Y coordinate

        Returns:
            Tuple of (local_x, local_y) relative to component origin
        """
        return (x - self._x, y - self._y)

    # ========== State Management ==========

    def _set_state(self, **kwargs) -> 'CanvasMacro':
        """
        Update state values and trigger state change callbacks.

        Args:
            **kwargs: State key-value pairs to update

        Returns:
            Self for method chaining
        """
        old_state = self._state.copy()
        self._state.update(kwargs)

        # Trigger state change callbacks
        self._trigger_callbacks('state_change', old_state, self._state)
        return self

    def _get_state(self, key: str, default: Any = None) -> Any:
        """
        Get a state value.

        Args:
            key: State key to retrieve
            default: Default value if key not found

        Returns:
            State value or default
        """
        return self._state.get(key, default)

    # ========== Callback System ==========

    def _add_callback_type(self, event_type: str):
        """
        Add a new callback type for this macro.

        Args:
            event_type: Name of the event type (e.g., 'click', 'hover')
        """
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []

    def _trigger_callbacks(self, event_type: str, *args, **kwargs):
        """
        Trigger all callbacks for a specific event type.

        Args:
            event_type: Type of event to trigger
            *args: Arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
        """
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(self, *args, **kwargs)
                except Exception as e:
                    print(f"CanvasMacro {self._id} callback error ({event_type}): {e}")

    def on(self, event_type: str, callback: Callable) -> 'CanvasMacro':
        """
        Register a callback for an event type.

        Args:
            event_type: Type of event to listen for
            callback: Function to call when event occurs

        Returns:
            Self for method chaining

        Example:
            button.on('click', lambda btn: print("Clicked!"))
        """
        self._add_callback_type(event_type)
        self._callbacks[event_type].append(callback)
        return self

    def off(self, event_type: str, callback: Optional[Callable] = None) -> 'CanvasMacro':
        """
        Remove callbacks for an event type.

        Args:
            event_type: Event type to remove callbacks from
            callback: Specific callback to remove, or None to remove all

        Returns:
            Self for method chaining
        """
        if event_type in self._callbacks:
            if callback is None:
                self._callbacks[event_type].clear()
            else:
                try:
                    self._callbacks[event_type].remove(callback)
                except ValueError:
                    pass
        return self

    # ========== Mouse Event Handling ==========

    def handle_mouse_down(self, x: float, y: float) -> bool:
        """
        Handle mouse down event.

        Args:
            x: Canvas X coordinate
            y: Canvas Y coordinate

        Returns:
            True if event was handled (stops propagation)
        """
        if not self._visible or not self._enabled:
            return False

        if self.contains_point(x, y):
            self._mouse_down = True
            local_x, local_y = self.get_local_coords(x, y)
            self._trigger_callbacks('mouse_down', local_x, local_y)
            return True
        return False

    def handle_mouse_up(self, x: float, y: float) -> bool:
        """
        Handle mouse up event.

        Args:
            x: Canvas X coordinate
            y: Canvas Y coordinate

        Returns:
            True if event was handled
        """
        if not self._visible or not self._enabled:
            return False

        was_down = self._mouse_down
        self._mouse_down = False

        if self.contains_point(x, y):
            local_x, local_y = self.get_local_coords(x, y)
            self._trigger_callbacks('mouse_up', local_x, local_y)

            # Trigger click if mouse was pressed on this component
            if was_down:
                self._trigger_callbacks('click', local_x, local_y)
            return True
        return False

    def handle_mouse_move(self, x: float, y: float) -> bool:
        """
        Handle mouse move event.

        Args:
            x: Canvas X coordinate
            y: Canvas Y coordinate

        Returns:
            True if event was handled
        """
        if not self._visible or not self._enabled:
            return False

        is_over = self.contains_point(x, y)

        # Check for hover state changes
        if is_over != self._mouse_over:
            self._mouse_over = is_over
            if is_over:
                self._trigger_callbacks('mouse_enter')
            else:
                self._trigger_callbacks('mouse_leave')

        if is_over:
            local_x, local_y = self.get_local_coords(x, y)
            self._trigger_callbacks('mouse_move', local_x, local_y)
            return True
        return False

    # ========== Drawing ==========

    def draw(self, canvas):
        """
        Draw this component on the canvas.
        Must be implemented by subclasses.

        Args:
            canvas: WebCanvas instance to draw on
        """
        raise NotImplementedError("Subclasses must implement draw()")

    # ========== Lifecycle ==========

    def show(self) -> 'CanvasMacro':
        """Show this component."""
        self.visible = True
        return self

    def hide(self) -> 'CanvasMacro':
        """Hide this component."""
        self.visible = False
        return self

    def toggle(self) -> 'CanvasMacro':
        """Toggle visibility of this component."""
        self.visible = not self.visible
        return self

    def enable(self) -> 'CanvasMacro':
        """Enable this component."""
        self.enabled = True
        return self

    def disable(self) -> 'CanvasMacro':
        """Disable this component."""
        self.enabled = False
        return self

    def destroy(self):
        """Destroy this component and clean up resources."""
        self._destroyed = True
        self._callbacks.clear()
        self._state.clear()
        self._trigger_callbacks('destroy')

    # ========== Utility Methods ==========

    def __repr__(self) -> str:
        """String representation of this component."""
        return (f"<{self.__class__.__name__} id={self._id} "
                f"pos=({self._x}, {self._y}) "
                f"size=({self._width}, {self._height})>")
