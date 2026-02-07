"""
Chart.js wrapper macro for Antioch framework.
Provides full access to Chart.js API with Python convenience.
"""
import js
from pyodide.ffi import create_proxy, to_js
from .base import Macro
from ..elements import Div, Canvas
from ..lib.loader import inject_script

# Ensure Chart.js is loaded when this module is imported
inject_script('antioch/lib/vendor/chart.min.js')


class ChartJS(Macro):
    """
    Chart.js wrapper component.

    Provides full access to Chart.js API while handling initialization,
    lifecycle, and Python-JavaScript interop.

    Usage:
        # Native Chart.js config
        config = {
            'type': 'bar',
            'data': {
                'labels': ['Red', 'Blue', 'Yellow'],
                'datasets': [{
                    'label': 'My Dataset',
                    'data': [12, 19, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)'
                    ]
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {'position': 'top'},
                    'title': {'display': True, 'text': 'Chart Title'}
                }
            }
        }

        chart = ChartJS(config, width=600, height=400)
        DOM.add(chart)
    """

    def __init__(self, config, width=600, height=400, container_style=None, **kwargs):
        """
        Initialize Chart.js component.

        Args:
            config: Chart.js configuration object (Python dict)
                   See: https://www.chartjs.org/docs/latest/configuration/
            width: Canvas width in pixels (or CSS string like "100%")
            height: Canvas height in pixels (or CSS string)
            container_style: Custom container styles
            **kwargs: Additional Macro base class arguments
        """
        super().__init__(macro_type="chartjs", **kwargs)

        # Validate config
        if not isinstance(config, dict):
            raise ValueError("config must be a dictionary")
        if 'type' not in config:
            raise ValueError("config must include 'type' (e.g., 'bar', 'line', 'pie')")

        # Set up state
        self._set_state(
            config=config,
            width=width,
            height=height,
            chart_instance=None,
            initialized=False,
            init_retry_count=0
        )

        # Default container style
        default_container_style = {
            "width": str(width) + "px" if isinstance(width, int) else width,
            "height": str(height) + "px" if isinstance(height, int) else height,
            "position": "relative"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Callback types
        self._add_callback_type('ready')
        self._add_callback_type('click')
        self._add_callback_type('hover')

        # Initialize macro
        self._init_macro()

    def _create_elements(self):
        """Create canvas element and container."""
        # Create container
        container = self._register_element('container',
                                          self._create_container(self._container_style))

        # Create canvas element
        width = self._get_state('width')
        height = self._get_state('height')

        canvas = self._register_element('canvas', Canvas(
            style={"display": "block", "width": "100%", "height": "100%"}
        ))

        # Set canvas dimensions as attributes (required for Chart.js)
        if isinstance(width, int):
            canvas.set_attribute("width", str(width))
        if isinstance(height, int):
            canvas.set_attribute("height", str(height))

        canvas.set_attribute("id", f"canvas_{self._id}")

        container.add(canvas)

        # Initialize Chart.js after DOM ready
        init_proxy = create_proxy(lambda: self._initialize_chart())
        js.setTimeout(init_proxy, 100)

        return container

    def _initialize_chart(self):
        """Initialize Chart.js instance with retry mechanism."""
        if self._get_state('initialized'):
            return

        retry_count = self._get_state('init_retry_count')
        if retry_count > 50:  # Max 50 retries (5 seconds)
            print(f"Chart.js initialization failed after {retry_count} attempts")
            print("Make sure Chart.js is loaded in the HTML page")
            return

        try:
            # Check if Chart.js is loaded
            if not hasattr(js, 'Chart') or not js.Chart:
                # Not loaded yet, retry
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_chart())
                js.setTimeout(init_proxy, 100)
                return

            canvas = self._get_element('canvas')
            if not canvas or not canvas._dom_element:
                # Canvas not ready
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_chart())
                js.setTimeout(init_proxy, 100)
                return

            # Convert Python config to JavaScript object
            config = self._get_state('config')
            js_config = to_js(config, dict_converter=js.Object.fromEntries)

            # Create Chart.js instance
            chart_instance = js.Chart.new(canvas._dom_element, js_config)

            # Store instance
            self._set_state(chart_instance=chart_instance, initialized=True)

            # Trigger ready callback
            self._trigger_callbacks('ready', self)

        except Exception as e:
            print(f"Chart.js initialization error: {e}")
            # Retry with longer delay on error
            self._set_state(init_retry_count=retry_count + 1)
            init_proxy = create_proxy(lambda: self._initialize_chart())
            js.setTimeout(init_proxy, 200)

    def update(self, config=None, mode='default'):
        """
        Update chart with new configuration.

        Args:
            config: New Chart.js config (optional, uses current if None)
            mode: Update mode ('default', 'resize', 'reset', 'none')
                  See: https://www.chartjs.org/docs/latest/developers/updates.html

        Returns:
            Self for method chaining
        """
        chart = self._get_state('chart_instance')
        if not chart:
            print("Chart not initialized yet")
            return self

        if config:
            # Update config in state
            self._set_state(config=config)
            js_config = to_js(config, dict_converter=js.Object.fromEntries)

            # Update chart data and options
            if hasattr(js_config, 'data'):
                chart.data = js_config.data
            if hasattr(js_config, 'options'):
                chart.options = js_config.options
            if hasattr(js_config, 'type'):
                chart.config.type = js_config.type

        # Trigger Chart.js update
        chart.update(mode)
        return self

    def destroy(self):
        """Destroy chart instance and clean up."""
        chart = self._get_state('chart_instance')
        if chart:
            chart.destroy()
            self._set_state(chart_instance=None, initialized=False)

        super().destroy()

    def on_ready(self, callback):
        """
        Register callback for when chart is ready.

        Args:
            callback: Function to call when chart is initialized

        Returns:
            Self for method chaining
        """
        return self.on('ready', callback)

    @property
    def chart(self):
        """
        Access native Chart.js instance for advanced usage.

        Returns:
            JavaScript Chart.js object or None if not initialized
        """
        return self._get_state('chart_instance')

    @property
    def is_ready(self):
        """Check if chart is initialized."""
        return self._get_state('initialized')

    @property
    def config(self):
        """Get current chart configuration."""
        return self._get_state('config')

