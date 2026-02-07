"""
WindowManager - Manages all windows, taskbar, and windowing system.
"""
from .base import Macro
from .window import Window
from ..elements import Div, Button, Span
from pyodide.ffi import create_proxy
import js


class WindowManager(Macro):
    """Manages all windows in the application."""

    def __init__(self, show_taskbar=True, container_style=None, **kwargs):
        """
        Initialize window manager.

        Args:
            show_taskbar: Whether to show the taskbar
            container_style: Custom styles for main container
        """
        super().__init__(macro_type="window_manager", **kwargs)

        # Set up state
        self._set_state(
            show_taskbar=show_taskbar,
            windows={},  # window_id -> Window instance
            active_window_id=None,
            next_z_index=1000,
            window_counter=0,
            drag_state=None,  # Current drag info
            resize_state=None,  # Current resize info
            minimized_windows=set()  # IDs of minimized windows
        )

        # Default container style
        default_container_style = {
            "position": "fixed",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
            "pointer_events": "none",
            "z_index": "999"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Initialize macro
        self._init_macro()

        # Setup global event handlers after initialization
        self._setup_global_handlers()

    def _create_elements(self):
        """Create the window manager container."""
        container = Div(
            id=self._id,
            class_="antioch-window-manager",
            style=self._container_style
        )

        # Add taskbar if enabled
        if self._get_state('show_taskbar'):
            taskbar = self._create_taskbar()
            taskbar.style.update({"pointer_events": "auto"})
            container.add(taskbar)

        return container

    def _create_taskbar(self):
        """Create the taskbar element."""
        taskbar = Div(
            id=f"{self._id}-taskbar",
            class_="antioch-taskbar"
        )
        taskbar.style.update({
            "position": "fixed",
            "top": "0",
            "left": "0",
            "right": "0",
            "height": "40px",
            "background": "linear-gradient(to bottom, #f0f0f0, #d0d0d0)",
            "border_bottom": "1px solid #999",
            "display": "flex",
            "align_items": "center",
            "padding": "0 10px",
            "gap": "10px",
            "z_index": "10000"
        })

        return taskbar

    def _setup_global_handlers(self):
        """Setup global mouse event handlers for drag and resize."""

        def handle_mouse_down(event):
            target = event.target
            macro_id = target.getAttribute('data-macro-id')
            action = target.getAttribute('data-action')

            if not macro_id:
                # Check parent elements
                parent = target.parentElement
                while parent and not macro_id:
                    macro_id = parent.getAttribute('data-macro-id')
                    if macro_id:
                        action = parent.getAttribute('data-action')
                        target = parent
                    parent = parent.parentElement

            if not macro_id:
                return

            # Find the window
            window = self._find_window_by_macro_id(macro_id)
            if not window:
                return

            # Handle different actions
            if action == "close":
                self.close_window(macro_id)
            elif action == "minimize":
                window.minimize()
                self._add_to_taskbar(window)
            elif action == "maximize":
                if window._get_state('maximized'):
                    window.restore()
                else:
                    window.maximize()
            elif action == "drag":
                if not window._get_state('maximized'):
                    self._start_drag(window, event)
                window.focus()
                self._set_active_window(macro_id)
            elif action == "resize":
                direction = target.getAttribute('data-direction')
                self._start_resize(window, event, direction)

            # Focus window on any click
            window.focus()
            self._set_active_window(macro_id)

        def handle_mouse_move(event):
            drag = self._get_state('drag_state')
            resize = self._get_state('resize_state')

            if drag:
                self._update_drag(event)
            elif resize:
                self._update_resize(event)

        def handle_mouse_up(event):
            self._set_state(drag_state=None, resize_state=None)

        # Create proxies and attach
        self._mouse_down_proxy = create_proxy(handle_mouse_down)
        self._mouse_move_proxy = create_proxy(handle_mouse_move)
        self._mouse_up_proxy = create_proxy(handle_mouse_up)

        js.document.addEventListener('mousedown', self._mouse_down_proxy)
        js.document.addEventListener('mousemove', self._mouse_move_proxy)
        js.document.addEventListener('mouseup', self._mouse_up_proxy)

    def _find_window_by_macro_id(self, macro_id):
        """Find a window by its macro ID."""
        windows = self._get_state('windows')
        for window in windows.values():
            if window._id == macro_id:
                return window
        return None

    def create_window(self, title="Window", content=None, **options):
        """
        Create a new window.

        Args:
            title: Window title
            content: Window content
            **options: Additional Window options (x, y, width, height, etc.)

        Returns:
            Window instance
        """
        # Generate window ID
        counter = self._get_state('window_counter') + 1
        self._set_state(window_counter=counter)
        window_id = f"window-{counter}"

        # Set default position with cascade
        cascade_offset = (counter - 1) * 30
        options.setdefault('x', 50 + cascade_offset)
        options.setdefault('y', 50 + cascade_offset)
        options.setdefault('z_index', self._get_next_z_index())

        # Create window
        window = Window(title=title, content=content, **options)

        # Setup window callbacks
        window.on('close', lambda w: self.close_window(window._id))
        window.on('minimize', lambda w: self._add_to_taskbar(window))
        window.on('restore', lambda w: self._remove_from_taskbar(window._id))
        window.on('focus', lambda w: self._set_active_window(window._id))

        # Add to state
        windows = self._get_state('windows')
        windows[window_id] = window
        self._set_state(windows=windows)

        # Add to DOM
        if self._root_element:
            # Append window element to container
            window_el = window._root_element
            if window_el:
                window_el.style.update({"pointer_events": "auto"})
                self._root_element.add(window_el)

        # Focus the new window
        window.focus()
        self._set_active_window(window._id)

        return window

    def close_window(self, window_id):
        """Close a window by ID or macro_id."""
        windows = self._get_state('windows')

        # Find window (by window_id or macro_id)
        window = None
        key_to_remove = None
        for wid, win in windows.items():
            if wid == window_id or win._id == window_id:
                window = win
                key_to_remove = wid
                break

        if window:
            # Remove from taskbar if minimized
            self._remove_from_taskbar(window._id)

            # Remove DOM element
            if window._root_element:
                window._root_element._dom_element.remove()

            # Remove from windows dict
            del windows[key_to_remove]
            self._set_state(windows=windows)

            # Update active window
            if self._get_state('active_window_id') == window._id:
                self._set_state(active_window_id=None)
                # Focus next available window
                if windows:
                    next_window = list(windows.values())[0]
                    next_window.focus()
                    self._set_active_window(next_window._id)

    def _get_next_z_index(self):
        """Get next available z-index."""
        z_index = self._get_state('next_z_index') + 1
        self._set_state(next_z_index=z_index)
        return z_index

    def _set_active_window(self, macro_id):
        """Set the active window."""
        self._set_state(active_window_id=macro_id)

        # Update z-index and visual style
        windows = self._get_state('windows')
        for window in windows.values():
            if window._id == macro_id:
                # Bring to front
                z_index = self._get_next_z_index()
                window._set_state(z_index=z_index)
                if window._root_element:
                    window._root_element._dom_element.style.zIndex = str(z_index)
                    window._root_element._dom_element.classList.add('active')
            else:
                if window._root_element:
                    window._root_element._dom_element.classList.remove('active')

    def _start_drag(self, window, event):
        """Start dragging a window."""
        self._set_state(drag_state={
            'window': window,
            'start_x': event.clientX,
            'start_y': event.clientY,
            'window_start_x': window._get_state('x'),
            'window_start_y': window._get_state('y')
        })

    def _update_drag(self, event):
        """Update window position during drag."""
        drag = self._get_state('drag_state')
        if not drag:
            return

        window = drag['window']
        dx = event.clientX - drag['start_x']
        dy = event.clientY - drag['start_y']

        new_x = max(0, drag['window_start_x'] + dx)
        new_y = max(40, drag['window_start_y'] + dy)  # Can't go above taskbar

        # Keep window on screen
        max_x = js.window.innerWidth - 100
        max_y = js.window.innerHeight - 100

        new_x = min(new_x, max_x)
        new_y = min(new_y, max_y)

        window._set_state(x=new_x, y=new_y)
        window._update_position_and_size()

    def _start_resize(self, window, event, direction):
        """Start resizing a window."""
        self._set_state(resize_state={
            'window': window,
            'direction': direction,
            'start_x': event.clientX,
            'start_y': event.clientY,
            'window_start_x': window._get_state('x'),
            'window_start_y': window._get_state('y'),
            'window_start_width': window._get_state('width'),
            'window_start_height': window._get_state('height')
        })

    def _update_resize(self, event):
        """Update window size during resize."""
        resize = self._get_state('resize_state')
        if not resize:
            return

        window = resize['window']
        direction = resize['direction']
        dx = event.clientX - resize['start_x']
        dy = event.clientY - resize['start_y']

        new_width = resize['window_start_width']
        new_height = resize['window_start_height']
        new_x = resize['window_start_x']
        new_y = resize['window_start_y']

        # Update dimensions based on resize direction
        if 'e' in direction:  # East (right)
            new_width = max(200, resize['window_start_width'] + dx)
        if 'w' in direction:  # West (left)
            new_width = max(200, resize['window_start_width'] - dx)
            new_x = resize['window_start_x'] + dx
        if 's' in direction:  # South (bottom)
            new_height = max(100, resize['window_start_height'] + dy)
        if 'n' in direction:  # North (top)
            new_height = max(100, resize['window_start_height'] - dy)
            new_y = max(40, resize['window_start_y'] + dy)

        # Apply constraints
        new_x = max(0, new_x)
        new_y = max(40, new_y)

        window._set_state(x=new_x, y=new_y, width=new_width, height=new_height)
        window._update_position_and_size()

    def _add_to_taskbar(self, window):
        """Add a minimized window to the taskbar."""
        macro_id = window._id

        # Track minimized window
        minimized = self._get_state('minimized_windows')
        if macro_id in minimized:
            return
        minimized.add(macro_id)
        self._set_state(minimized_windows=minimized)

        # Create taskbar item
        taskbar_dom = self._root_element._dom_element.querySelector(f"#{self._id}-taskbar")
        if not taskbar_dom:
            return

        item = Div(
            id=f"taskbar-item-{macro_id}",
            class_="antioch-taskbar-item"
        )
        item.style.update({
            "background": "linear-gradient(to bottom, #fff, #e8e8e8)",
            "border": "1px solid #999",
            "border_radius": "4px",
            "padding": "4px 8px",
            "display": "flex",
            "align_items": "center",
            "gap": "6px",
            "cursor": "pointer",
            "max_width": "200px",
            "font_size": "12px"
        })

        icon = Span(class_="antioch-taskbar-icon")
        icon.add("🗔")

        title = Span(class_="antioch-taskbar-title")
        title.add(window._get_state('title'))
        title.style.update({
            "white_space": "nowrap",
            "overflow": "hidden",
            "text_overflow": "ellipsis",
            "flex": "1"
        })

        item.add(icon, title)

        # Add click handler to restore
        def handle_restore(event):
            window.restore()
            self._remove_from_taskbar(macro_id)

        item._dom_element.addEventListener('click', create_proxy(handle_restore))

        # Append to taskbar
        taskbar_dom.appendChild(item._dom_element)

    def _remove_from_taskbar(self, macro_id):
        """Remove a window from the taskbar."""
        minimized = self._get_state('minimized_windows')
        if macro_id in minimized:
            minimized.remove(macro_id)
            self._set_state(minimized_windows=minimized)

        # Remove DOM element
        if self._root_element:
            item = self._root_element._dom_element.querySelector(f"#taskbar-item-{macro_id}")
            if item:
                item.remove()

    def get_window(self, window_id):
        """Get a window by ID."""
        windows = self._get_state('windows')
        return windows.get(window_id)

    def get_all_windows(self):
        """Get all windows."""
        return list(self._get_state('windows').values())