"""
Example showing how to use JSLibraryMacro to wrap a JavaScript library.

This demonstrates the refactored ChartJS implementation using the new base class.
"""
from .js_library import JSLibraryMacro
from ..elements import Canvas


class ChartJSRefactored(JSLibraryMacro):
    """
    Chart.js wrapper using JSLibraryMacro base class.

    Compare this with the original chartjs.py to see the simplification.
    """

    def __init__(self, config, width=600, height=400, container_style=None, **kwargs):
        """
        Initialize Chart.js component.

        Args:
            config: Chart.js configuration object (Python dict)
            width: Canvas width in pixels
            height: Canvas height in pixels
            container_style: Custom container styles
            **kwargs: Additional arguments (passed to JSLibraryMacro)
        """
        # Validate config
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")
        if 'type' not in config:
            raise ValueError("config must include 'type' (e.g., 'bar', 'line', 'pie')")

        # Initialize base class
        super().__init__(macro_type="chartjs", **kwargs)

        # Set up state
        self._set_state(
            config=config,
            width=width,
            height=height
        )

        # Store styles
        default_container_style = {
            "width": str(width) + "px" if isinstance(width, int) else width,
            "height": str(height) + "px" if isinstance(height, int) else height,
            "position": "relative"
        }
        self._container_style = self._merge_styles(default_container_style, container_style)

        # Add custom callback types
        self._add_callback_type('click')
        self._add_callback_type('hover')

        # Initialize (creates DOM and optionally JS instance)
        self._init_macro()

    # ========== Required Overrides ==========

    def _get_library_dependencies(self):
        """Specify Chart.js library files to load."""
        return {
            'scripts': ['antioch/lib/vendor/chart.min.js'],
            'stylesheets': []
        }

    def _get_library_global_name(self):
        """Chart.js exposes the 'Chart' global."""
        return 'Chart'

    def _create_elements(self):
        """Create the canvas element for Chart.js."""
        # Create container
        container = self._register_element(
            'container',
            self._create_container(self._container_style)
        )

        # Create canvas
        canvas = self._register_element('canvas', Canvas(
            width=self._get_state('width'),
            height=self._get_state('height'),
            style={"display": "block"}
        ))

        container.add(canvas)
        return container

    def _create_js_instance(self):
        """Create the Chart.js instance."""
        import js

        canvas = self._get_element('canvas')
        config = self._to_js(self._get_state('config'))

        # Create Chart.js instance
        chart = js.Chart.new(canvas._dom_element, config)

        # Add event listeners if needed
        # (Chart.js uses plugins for click/hover, but this shows the pattern)

        return chart

    def _cleanup_js_instance(self):
        """Clean up Chart.js instance (called automatically on destroy)."""
        js_instance = self._get_state('js_instance')
        if js_instance:
            js_instance.destroy()

    # ========== Public API Methods ==========

    def update(self, new_data=None):
        """
        Update the chart with new data.

        Args:
            new_data: New dataset to display (optional)

        Returns:
            Self for method chaining
        """
        self.ensure_initialized()

        if new_data:
            config = self._get_state('config')
            config['data'] = new_data
            self._set_state(config=config)

            # Update the JS instance
            self.js_instance.data = self._to_js(new_data)

        self.js_instance.update()
        return self

    def set_type(self, chart_type):
        """
        Change the chart type.

        Args:
            chart_type: New chart type ('bar', 'line', 'pie', etc.)

        Returns:
            Self for method chaining
        """
        self.ensure_initialized()

        config = self._get_state('config')
        config['type'] = chart_type
        self._set_state(config=config)

        self.js_instance.config.type = chart_type
        self.js_instance.update()
        return self


# ========== Comparison with Original ==========

"""
BEFORE (original chartjs.py):
- 300+ lines of code
- Manual dependency loading
- Manual initialization retry logic
- Manual proxy tracking (or missing it!)
- Duplicated patterns across wrappers

AFTER (using JSLibraryMacro):
- ~120 lines of code
- Automatic dependency loading
- Automatic initialization with retries
- Automatic proxy management
- Consistent pattern across all wrappers

WHAT YOU GET FOR FREE:
✅ .ensure_initialized() - safe lazy initialization
✅ .js_instance - access to underlying Chart.js object
✅ .on_ready() - callback when library is ready
✅ .on_error() - callback for initialization errors
✅ ._to_js() - clean Python → JS conversion
✅ ._add_js_event_listener() - automatic proxy management
✅ Automatic cleanup on destroy()
✅ Standardized lifecycle hooks
✅ Consistent API across all JS library wrappers
"""