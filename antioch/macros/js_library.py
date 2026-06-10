"""
Base class for JavaScript library wrappers.

Provides a standardized pattern for creating Python wrappers around JavaScript libraries
with automatic resource loading, initialization lifecycle, and cleanup.
"""
import js
from typing import Dict, List, Any, Optional, Callable
from pyodide.ffi import to_js, create_proxy
from .base import Macro
from ..lib.loader import inject_script, inject_script_async, inject_stylesheet, is_global_defined


class JSLibraryMacro(Macro):
    """
    Base class for macros that wrap JavaScript libraries.

    Provides:
    - Automatic script/stylesheet loading
    - Standardized initialization lifecycle
    - JS instance management and cleanup
    - Proxy management for JS callbacks
    - Python dict → JS object conversion helpers

    Subclasses should override:
    - _get_library_dependencies() - Return list of scripts/stylesheets to load
    - _get_library_global_name() - Return the global JS object name (e.g., 'Chart', 'L')
    - _create_js_instance() - Create and return the JS library instance
    - _create_elements() - Create the DOM structure (as usual)

    Example:
        class ChartJS(JSLibraryMacro):
            def _get_library_dependencies(self):
                return {
                    'scripts': ['antioch/lib/vendor/chart.min.js'],
                    'stylesheets': []
                }

            def _get_library_global_name(self):
                return 'Chart'

            def _create_js_instance(self):
                canvas = self._get_element('canvas')
                config = to_js(self._get_state('config'))
                return js.Chart.new(canvas._dom_element, config)
    """

    def __init__(self, macro_type: str = "jslibrary", lazy_init: bool = False, **kwargs):
        """
        Initialize JS library macro.

        Args:
            macro_type: Type identifier for this macro
            lazy_init: If True, delay JS instance creation until ensure_initialized()
            **kwargs: Additional arguments passed to base Macro
        """
        super().__init__(macro_type=macro_type, **kwargs)

        # JS library state
        self._set_state(
            js_instance=None,
            initialized=False,
            init_retry_count=0,
            max_init_retries=10,
            lazy_init=lazy_init
        )

        # Track JS event listeners for cleanup (list of tuples since JsProxy isn't hashable)
        self._js_event_listeners: List[tuple[Any, str, Any]] = []  # [(js_object, event_type, proxy), ...]

        # Create unified Events for decorator usage
        self._create_event('library_loaded')
        self._create_event('ready')
        self._create_event('error')

    def _get_library_dependencies(self) -> Dict[str, List[str]]:
        """
        Return the library dependencies to load.

        Returns:
            Dictionary with 'scripts' and 'stylesheets' lists:
            {
                'scripts': ['path/to/script.js', ...],
                'stylesheets': ['path/to/style.css', ...]
            }

        Override this in subclasses.
        """
        return {'scripts': [], 'stylesheets': []}

    def _get_library_global_name(self) -> Optional[str]:
        """
        Return the global JavaScript object name for this library.

        Returns:
            Name of global JS object (e.g., 'Chart', 'L', 'CodeMirror')
            or None if the library doesn't expose a global

        Override this in subclasses.
        """
        return None

    def _load_dependencies(self) -> None:
        """Load all script and stylesheet dependencies."""
        import asyncio

        deps = self._get_library_dependencies()

        # Load stylesheets first (synchronously is fine)
        for stylesheet in deps.get('stylesheets', []):
            inject_stylesheet(stylesheet)

        # Load scripts sequentially to maintain order
        scripts = deps.get('scripts', [])
        if scripts:
            # Set loading flag
            self._set_state(scripts_loading=True)

            # Start async task to load scripts sequentially
            async def load_scripts_sequential():
                try:
                    for script in scripts:
                        await inject_script_async(script)
                finally:
                    self._set_state(scripts_loading=False)

            # Schedule the task
            asyncio.ensure_future(load_scripts_sequential())
        else:
            self._set_state(scripts_loading=False)

    def _is_library_loaded(self) -> bool:
        """
        Check if the JavaScript library is loaded and ready.

        Returns:
            True if library is available, False otherwise
        """
        global_name = self._get_library_global_name()
        if global_name:
            return is_global_defined(global_name)
        # If no global name specified, assume library is loaded
        return True

    def _create_js_instance(self) -> Any:
        """
        Create and return the JavaScript library instance.

        This is called after dependencies are loaded and DOM is ready.
        Subclasses MUST override this method.

        Returns:
            The JavaScript library instance

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _create_js_instance()"
        )

    def _init_macro(self):
        """
        Initialize the macro (overrides base class).

        Loads dependencies and creates DOM structure.
        JS instance creation is deferred until dependencies are ready.
        """
        # Load dependencies
        self._load_dependencies()

        # Create DOM elements
        self._root_element = self._create_elements()
        if not self._root_element:
            raise ValueError("_create_elements() must return a root element")

        # Initialize JS instance (unless lazy)
        if not self._get_state('lazy_init'):
            self.ensure_initialized()

    def ensure_initialized(self) -> bool:
        """
        Ensure the JavaScript library instance is created and ready.

        This can be called multiple times safely - it only initializes once.
        Returns immediately if already initialized, otherwise attempts to initialize.

        Returns:
            True if initialized successfully, False if library not ready yet

        Raises:
            RuntimeError: If max retries exceeded or library unavailable
        """
        if self._get_state('initialized'):
            return True

        # Check if library is loaded
        if not self._is_library_loaded():
            retry_count = self._get_state('init_retry_count')
            max_retries = self._get_state('max_init_retries')

            if retry_count >= max_retries:
                error_msg = f"Library not available after {max_retries} retries"
                self._fire_event('error', error_msg)
                raise RuntimeError(error_msg)

            # Schedule retry
            self._set_state(init_retry_count=retry_count + 1)
            retry_proxy = self._create_proxy(lambda: self.ensure_initialized())
            import js
            js.setTimeout(retry_proxy, 100)
            return False

        # Library is loaded, create instance
        try:
            js_instance = self._create_js_instance()
            self._set_state(js_instance=js_instance, initialized=True)
            self._fire_event('library_loaded')
            self._fire_event('ready')
            return True

        except Exception as e:
            error_msg = f"Failed to initialize JS library: {e}"
            self._trigger_callbacks('error', error_msg)
            raise RuntimeError(error_msg) from e

    def _to_js(self, obj: Any, **kwargs) -> Any:
        """
        Convert Python object to JavaScript object.

        Helper method that wraps pyodide.ffi.to_js with common defaults.

        Args:
            obj: Python object to convert (dict, list, etc.)
            **kwargs: Additional arguments for to_js()

        Returns:
            JavaScript equivalent object
        """
        # Default to dict_converter for cleaner JS objects
        kwargs.setdefault('dict_converter', js.Object.fromEntries)
        return to_js(obj, **kwargs)

    def _add_js_event_listener(self, js_object: Any, event_type: str, handler: Callable) -> None:
        """
        Add a JS event listener with automatic proxy management.

        The proxy is automatically stored and will be cleaned up when the macro is destroyed.

        Args:
            js_object: JavaScript object to attach listener to (e.g., map instance, chart instance)
            event_type: Event type string (e.g., 'click', 'change')
            handler: Python function to handle the event

        Example:
            self._add_js_event_listener(self.js_instance, 'click', self._handle_click)
        """
        # Create proxy
        proxy = self._create_proxy(handler)

        # Store for cleanup (as tuple: js_object, event_type, proxy)
        self._js_event_listeners.append((js_object, event_type, proxy))

        # Add the listener
        # Most JS libraries use .on() or .addEventListener()
        if hasattr(js_object, 'on'):
            js_object.on(event_type, proxy)
        elif hasattr(js_object, 'addEventListener'):
            js_object.addEventListener(event_type, proxy)
        else:
            raise ValueError(
                f"JS object does not have .on() or .addEventListener() method. "
                f"You may need to override _add_js_event_listener() for this library."
            )

    def _remove_js_event_listener(self, js_object: Any, event_type: str, proxy: Any) -> None:
        """
        Remove a JS event listener.

        Args:
            js_object: JavaScript object the listener is attached to
            event_type: Event type string
            proxy: The proxy object to remove
        """
        # Remove the listener
        if hasattr(js_object, 'off'):
            js_object.off(event_type, proxy)
        elif hasattr(js_object, 'removeEventListener'):
            js_object.removeEventListener(event_type, proxy)

        # Remove from tracking (find and remove the matching tuple)
        self._js_event_listeners = [
            (obj, et, p) for obj, et, p in self._js_event_listeners
            if not (obj == js_object and et == event_type and p == proxy)
        ]

    def _cleanup_js_instance(self) -> None:
        """
        Clean up the JavaScript library instance.

        Override this to add custom cleanup logic (e.g., chart.destroy(), map.remove()).
        This is called automatically in destroy().
        """
        js_instance = self._get_state('js_instance')
        if js_instance:
            # Try common cleanup methods
            if hasattr(js_instance, 'destroy'):
                js_instance.destroy()
            elif hasattr(js_instance, 'remove'):
                js_instance.remove()
            elif hasattr(js_instance, 'dispose'):
                js_instance.dispose()

    def destroy(self):
        """
        Destroy the macro and clean up resources.

        Overrides base class to add JS library cleanup.
        """
        if self._destroyed:
            return

        # Remove all JS event listeners
        for js_object, event_type, proxy in list(self._js_event_listeners):
            self._remove_js_event_listener(js_object, event_type, proxy)
        self._js_event_listeners.clear()

        # Clean up JS instance
        if self._get_state('initialized'):
            self._cleanup_js_instance()

        # Call base class destroy
        super().destroy()

    @property
    def js_instance(self) -> Any:
        """
        Get the underlying JavaScript library instance.

        Returns:
            The JS instance, or None if not initialized

        Example:
            chart = ChartJS(config)
            chart.ensure_initialized()
            # Access the Chart.js instance directly
            chart.js_instance.update()
        """
        return self._get_state('js_instance')

    @property
    def is_initialized(self) -> bool:
        """Check if the JS library instance is initialized."""
        return self._get_state('initialized')

    def on_library_loaded(self, callback: Callable) -> 'JSLibraryMacro':
        """
        Register callback for when library dependencies are loaded.

        Args:
            callback: Function to call when library is ready

        Returns:
            Self for method chaining
        """
        return self.on('library_loaded', callback)

    def on_ready(self, callback: Callable) -> 'JSLibraryMacro':
        """
        Register callback for when JS instance is created and ready.

        Args:
            callback: Function to call when instance is ready

        Returns:
            Self for method chaining
        """
        return self.on('ready', callback)

    def on_error(self, callback: Callable) -> 'JSLibraryMacro':
        """
        Register callback for initialization errors.

        Args:
            callback: Function to call on error (receives error message)

        Returns:
            Self for method chaining
        """
        return self.on('error', callback)