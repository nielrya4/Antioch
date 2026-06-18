# JavaScript Library Wrapper Guide

This guide explains how to create Python wrappers for JavaScript libraries using the `JSLibraryMacro` base class.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Required Methods](#required-methods)
4. [Optional Methods](#optional-methods)
5. [Built-in Features](#built-in-features)
6. [Complete Example](#complete-example)
7. [Best Practices](#best-practices)

---

## Overview

The `JSLibraryMacro` base class provides a standardized pattern for wrapping JavaScript libraries in Antioch. It handles the boilerplate of:

- Loading scripts and stylesheets
- Managing initialization lifecycle
- Creating and cleaning up JS instances
- Managing Pyodide proxies
- Converting Python objects to JavaScript

## Quick Start

**Minimal wrapper in 4 steps:**

```python
from antioch.macros.js_library import JSLibraryMacro
from antioch.elements import Div

class MyLibrary(JSLibraryMacro):
    def __init__(self, config, **kwargs):
        super().__init__(macro_type="mylibrary", **kwargs)
        self._set_state(config=config)
        self._init_macro()

    # 1. Specify what to load
    def _get_library_dependencies(self):
        return {
            'scripts': ['path/to/library.js'],
            'stylesheets': ['path/to/library.css']
        }

    # 2. Specify the global JS object name
    def _get_library_global_name(self):
        return 'MyLib'  # The global like window.MyLib

    # 3. Create the DOM structure
    def _create_elements(self):
        container = self._create_container()
        # Add your elements here
        return container

    # 4. Create the JS instance
    def _create_js_instance(self):
        import js
        config = self._to_js(self._get_state('config'))
        return js.MyLib.new(config)
```

That's it! You now have a working wrapper with automatic initialization, cleanup, and proxy management.

---

## Required Methods

### `_get_library_dependencies() -> Dict[str, List[str]]`

Return scripts and stylesheets to load.

```python
def _get_library_dependencies(self):
    return {
        'scripts': [
            'antioch/lib/vendor/library.min.js',
            'https://cdn.example.com/plugin.js'  # CDN URLs work too
        ],
        'stylesheets': [
            'antioch/lib/vendor/library.css'
        ]
    }
```

**Note:** Dependencies are loaded in order. Stylesheets load before scripts.

### `_get_library_global_name() -> Optional[str]`

Return the global JavaScript object name.

```python
def _get_library_global_name(self):
    return 'Chart'  # For Chart.js
    # return 'L'    # For Leaflet
    # return 'CodeMirror'  # For CodeMirror
    # return None  # If library doesn't expose a global
```

This is used to check if the library loaded successfully.

### `_create_elements() -> Element`

Create the DOM structure (same as regular Macros).

```python
def _create_elements(self):
    container = self._create_container({
        "width": "600px",
        "height": "400px"
    })

    canvas = self._register_element('canvas', Canvas())
    container.add(canvas)

    return container
```

### `_create_js_instance() -> Any`

Create and return the JavaScript library instance.

```python
def _create_js_instance(self):
    import js

    # Get DOM element
    canvas = self._get_element('canvas')

    # Convert Python config to JS
    config = self._to_js(self._get_state('config'))

    # Create the JS instance
    chart = js.Chart.new(canvas._dom_element, config)

    # Optionally add event listeners
    self._add_js_event_listener(chart, 'click', self._handle_click)

    return chart
```

---

## Optional Methods

### `_cleanup_js_instance() -> None`

Custom cleanup logic when the macro is destroyed.

```python
def _cleanup_js_instance(self):
    js_instance = self._get_state('js_instance')
    if js_instance:
        # Custom cleanup
        js_instance.destroy()
        # Or js_instance.remove(), js_instance.dispose(), etc.
```

**Default behavior:** Tries common methods (`destroy()`, `remove()`, `dispose()`) automatically.

### `_add_js_event_listener()` and `_remove_js_event_listener()`

Override if your library uses a non-standard event API.

```python
def _add_js_event_listener(self, js_object, event_type, handler):
    # Default tries .on() or .addEventListener()
    # Override if your library uses something else
    proxy = self._create_proxy(handler)
    js_object.someCustomMethod(event_type, proxy)
    # Don't forget to track for cleanup!
```

---

## Built-in Features

### Properties

**`.js_instance`** - Access the underlying JS object:
```python
chart = ChartJS(config)
chart.ensure_initialized()
chart.js_instance.update()  # Call Chart.js methods directly
```

**`.is_initialized`** - Check if ready:
```python
if chart.is_initialized:
    chart.js_instance.resize()
```

### Methods

**`.ensure_initialized()`** - Guarantee initialization:
```python
chart = ChartJS(config, lazy_init=True)
# ... later ...
chart.ensure_initialized()  # Safe to call multiple times
```

**`._to_js(obj)`** - Convert Python → JavaScript:
```python
data = {'labels': ['A', 'B'], 'values': [1, 2]}
js_data = self._to_js(data)  # Clean JS object
```

**`._add_js_event_listener(js_obj, event, handler)`** - Add JS events with auto-proxy:
```python
self._add_js_event_listener(
    self.js_instance,
    'click',
    lambda e: print("Clicked!")
)
# Proxy created, stored, and cleaned up automatically!
```

### Lifecycle Callbacks

**`.on_library_loaded(callback)`** - When dependencies load:
```python
chart.on_library_loaded(lambda macro: print("Chart.js loaded!"))
```

**`.on_ready(callback)`** - When JS instance is created:
```python
chart.on_ready(lambda macro: print("Chart ready!"))
```

**`.on_error(callback)`** - If initialization fails:
```python
chart.on_error(lambda macro, msg: print(f"Error: {msg}"))
```

---

## Complete Example

Here's a complete wrapper for a hypothetical charting library:

```python
from antioch.macros.js_library import JSLibraryMacro
from antioch.elements import Canvas, Div, Button

class SuperChart(JSLibraryMacro):
    """Wrapper for SuperChart.js library."""

    def __init__(self, data, chart_type='bar', width=600, height=400, **kwargs):
        """Initialize SuperChart component."""
        super().__init__(macro_type="superchart", **kwargs)

        # Store configuration in state
        self._set_state(
            data=data,
            chart_type=chart_type,
            width=width,
            height=height
        )

        # Add custom callback types
        self._add_callback_type('data_click')

        # Initialize
        self._init_macro()

    # ========== Required Overrides ==========

    def _get_library_dependencies(self):
        return {
            'scripts': ['antioch/lib/vendor/superchart.min.js'],
            'stylesheets': ['antioch/lib/vendor/superchart.css']
        }

    def _get_library_global_name(self):
        return 'SuperChart'

    def _create_elements(self):
        # Container
        container = self._create_container({
            "width": f"{self._get_state('width')}px",
            "height": f"{self._get_state('height')}px"
        })

        # Canvas for chart
        canvas = self._register_element('canvas', Canvas(
            width=self._get_state('width'),
            height=self._get_state('height')
        ))

        # Control button
        refresh_btn = self._register_element('refresh_btn',
            Button("Refresh", style={"margin-top": "10px"})
        )
        refresh_btn.on_click(lambda e: self.refresh())

        container.add(canvas, refresh_btn)
        return container

    def _create_js_instance(self):
        import js

        canvas = self._get_element('canvas')

        # Build configuration
        config = {
            'type': self._get_state('chart_type'),
            'data': self._get_state('data'),
            'canvas': canvas._dom_element
        }

        # Create JS instance
        chart = js.SuperChart.new(self._to_js(config))

        # Add event listener with automatic proxy management
        self._add_js_event_listener(
            chart,
            'dataClick',
            self._handle_data_click
        )

        return chart

    def _cleanup_js_instance(self):
        """Custom cleanup (optional)."""
        js_instance = self._get_state('js_instance')
        if js_instance:
            js_instance.destroy()

    # ========== Public API ==========

    def update_data(self, new_data):
        """Update chart with new data."""
        self.ensure_initialized()

        self._set_state(data=new_data)
        self.js_instance.setData(self._to_js(new_data))
        self.js_instance.render()
        return self

    def set_type(self, chart_type):
        """Change chart type."""
        self.ensure_initialized()

        self._set_state(chart_type=chart_type)
        self.js_instance.setType(chart_type)
        return self

    def refresh(self):
        """Refresh the chart."""
        self.ensure_initialized()
        self.js_instance.render()
        return self

    # ========== Event Handlers ==========

    def _handle_data_click(self, event):
        """Handle clicks on data points."""
        # Extract data from JS event
        index = event.dataIndex
        value = event.dataValue

        # Trigger Python callback
        self._trigger_callbacks('data_click', index, value)

    def on_data_click(self, callback):
        """Register callback for data point clicks."""
        return self.on('data_click', callback)


# ========== Usage ==========

if __name__ == "__main__":
    from antioch import DOM

    # Create chart
    chart = SuperChart(
        data={'labels': ['A', 'B', 'C'], 'values': [10, 20, 15]},
        chart_type='bar',
        width=800,
        height=400
    )

    # Add event listener
    chart.on_data_click(lambda macro, idx, val:
        print(f"Clicked: {idx} = {val}")
    )

    # Add to page
    DOM.add(chart.element)

    # Update later
    chart.update_data({'labels': ['X', 'Y', 'Z'], 'values': [30, 40, 35]})
```

---

## Best Practices

### 1. **Validate Configuration Early**

```python
def __init__(self, config, **kwargs):
    if not isinstance(config, dict):
        raise ValueError("config must be a dictionary")
    if 'required_field' not in config:
        raise ValueError("config missing required_field")

    super().__init__(...)
```

### 2. **Use State for Everything**

```python
# Store all configuration in state
self._set_state(
    width=width,
    height=height,
    options=options
)

# Access via _get_state()
width = self._get_state('width')
```

### 3. **Always Call `ensure_initialized()` in Public Methods**

```python
def update(self, new_data):
    self.ensure_initialized()  # ← Important!
    self.js_instance.update(self._to_js(new_data))
```

### 4. **Use `_add_js_event_listener()` for JS Events**

```python
# ✅ Good - automatic proxy management
self._add_js_event_listener(chart, 'click', self._handle_click)

# ❌ Bad - manual proxy creation
proxy = create_proxy(self._handle_click)
chart.on('click', proxy)  # Will leak!
```

### 5. **Expose Both Python API and JS Instance**

```python
# Python convenience methods
def set_color(self, color):
    self.js_instance.setOption('color', color)
    return self

# But also allow direct access
@property
def js_instance(self):
    return self._get_state('js_instance')

# Users can choose:
chart.set_color('red')  # Python API
chart.js_instance.setOption('color', 'red')  # Direct JS
```

### 6. **Handle Lazy Initialization**

```python
def __init__(self, config, lazy_init=False, **kwargs):
    super().__init__(macro_type="...", lazy_init=lazy_init, **kwargs)
    # ...
    self._init_macro()

# Users can control when JS initializes
chart = MyChart(config, lazy_init=True)  # Just DOM, no JS yet
# ... later ...
chart.ensure_initialized()  # Now create JS instance
```

### 7. **Add Typed Callback Methods**

```python
# Don't just expose .on('event')
def on_click(self, callback):
    """Register click callback.

    Args:
        callback: Function(macro, event) called on click
    """
    return self.on('click', callback)

# Better developer experience!
chart.on_click(lambda m, e: print("Clicked!"))
```

---

## Summary

**What you write:**
- 4 required methods (~30 lines)
- Public API methods for your library
- Event handlers (optional)

**What you get for free:**
- Dependency loading
- Initialization lifecycle
- Retry logic
- Proxy management
- Python ↔ JS conversion
- Automatic cleanup
- Error handling
- Standard callbacks

**Result:** Clean, consistent, maintainable JavaScript library wrappers!