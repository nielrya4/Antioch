"""
Chart.js wrapper macro for Antioch framework.
Provides full access to Chart.js API with Python convenience.
"""
import js
from .js_library import JSLibraryMacro
from ..elements import Canvas


class ChartJS(JSLibraryMacro):
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
        DOM.add(chart.element)
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
            **kwargs: Additional JSLibraryMacro arguments
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

        # Default container style
        default_container_style = {
            "width": str(width) + "px" if isinstance(width, int) else width,
            "height": str(height) + "px" if isinstance(height, int) else height,
            "position": "relative"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Create unified Events for decorator usage
        self._create_event('click')
        self._create_event('hover')

        # Initialize macro
        self._init_macro()

    # ========== Required JSLibraryMacro Methods ==========

    def _get_library_dependencies(self):
        """Specify Chart.js library to load."""
        return {
            'scripts': ['antioch/lib/vendor/chart.min.js'],
            'stylesheets': []
        }

    def _get_library_global_name(self):
        """Chart.js exposes the 'Chart' global."""
        return 'Chart'

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
        return container

    def _create_js_instance(self):
        """Create Chart.js instance."""
        canvas = self._get_element('canvas')
        config = self._to_js(self._get_state('config'))

        # Create Chart.js instance
        return js.Chart.new(canvas._dom_element, config)

    def _cleanup_js_instance(self):
        """Clean up Chart.js instance."""
        if self.js_instance:
            self.js_instance.destroy()

    # ========== Public API Methods ==========

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
        self.ensure_initialized()

        if config:
            # Update config in state
            self._set_state(config=config)
            js_config = self._to_js(config)

            # Update chart data and options
            if hasattr(js_config, 'data'):
                self.js_instance.data = js_config.data
            if hasattr(js_config, 'options'):
                self.js_instance.options = js_config.options
            if hasattr(js_config, 'type'):
                self.js_instance.config.type = js_config.type

        # Trigger Chart.js update
        self.js_instance.update(mode)
        return self

    def update_data(self, new_data):
        """
        Update only the chart data.

        Args:
            new_data: New data object for the chart

        Returns:
            Self for method chaining
        """
        self.ensure_initialized()

        config = self._get_state('config')
        config['data'] = new_data
        self._set_state(config=config)

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

    # ========== Convenience Properties ==========

    @property
    def chart(self):
        """
        Access native Chart.js instance for advanced usage.

        Returns:
            JavaScript Chart.js object or None if not initialized
        """
        return self.js_instance

    @property
    def is_ready(self):
        """Check if chart is initialized."""
        return self.is_initialized

    @property
    def config(self):
        """Get current chart configuration."""
        return self._get_state('config')