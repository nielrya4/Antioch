# Antioch

**Build interactive web applications entirely in Python**

Antioch is a Python library that lets you create rich, interactive web applications that run entirely in the browser using [Pyodide](https://pyodide.org/) (Python compiled to WebAssembly). Write modern web apps in pure Python without touching JavaScript.

## Features

### Core Capabilities
- **Pure Python Development** - Write complete web applications without JavaScript
- **Direct DOM Manipulation** - Pythonic API for browser DOM with method chaining
- **Rich Component Library** - 28+ ready-to-use UI components (modals, windows, forms, charts, maps)
- **Virtual Filesystem** - In-browser file system with automatic persistence
- **Cloud Synchronization** - Google Drive integration with conflict resolution and offline support
- **Canvas Graphics** - Interactive canvas-based components for games and visualizations
- **Zero Backend** - Generates self-contained static HTML that runs client-side

### Component Library (Macros)
- **Interactive**: Counter, Slider, Dropdown, Pagination
- **Layout**: Modal, Window Manager, Tabs, Accordion
- **Data Visualization**: DataTable, Charts (Chart.js), Maps (Leaflet)
- **Forms**: Form builder with validators (Email, MinLength, Required, Custom)
- **Filesystem**: File selector, upload, download
- **Navigation**: Multi-level toolbar with nested menus
- **Feedback**: Alerts, toasts, progress bars
- **Code Editing**: Syntax-highlighted code viewer/editor (CodeMirror)
- **Canvas**: Button, interactive widgets for custom rendering

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nielrya4/Antioch.git
cd antioch

# Download Pyodide runtime (required - ~420MB)
# Option 1: Use the download script (recommended)
python download_pyodide

# Option 2: Manual download
wget https://github.com/pyodide/pyodide/releases/download/0.24.1/pyodide-0.24.1.tar.bz2
tar -xjf pyodide-0.24.1.tar.bz2
mv pyodide pyodide/
```

### Hello World

Create a simple application in `scripts/main.py`:

```python
from antioch import DOM, Div, H1, Button

def main():
    # Create elements
    container = Div()
    title = H1("Hello, Antioch!")
    button = Button("Click Me")

    # Add styling
    title.style.color = "#2196F3"
    button.style.padding = "10px 20px"

    # Add event handler
    button.on_click(lambda e: print("Button clicked!"))

    # Add to page
    container.add(title, button)
    DOM.add(container)

if __name__ == "__main__":
    main()
```

### Build and Run

```bash
# Build the static website
python build.py

# Serve locally (choose any method)
python -m http.server -d output 8000
# or
cd output && python -m http.server

# Open browser to http://localhost:8000
```

## Examples

The project includes 20+ comprehensive examples in `scripts/examples/`:

- **example.py** - Basic usage and DOM manipulation
- **macro_showcase.py** - Component library demonstrations
- **cloud_sync_demo.py** - Google Drive integration
- **window_manager_demo.py** - Draggable, resizable windows
- **data_table_demo.py** - Interactive data tables
- **chart_demo.py** - Data visualization with Chart.js
- **map_demo.py** - Interactive maps with Leaflet
- **form_demo.py** - Form validation and handling
- **canvas_demo.py** - Canvas-based graphics
- **code_block_demo.py** - Syntax-highlighted code editor
- And many more...

To run an example, modify `scripts/main.py` to import and run it, then rebuild:

```python
from examples.macro_showcase import main

if __name__ == "__main__":
    main()
```

## Documentation

- **[Cloud Sync Implementation Guide](CLOUD_SYNC_IMPLEMENTATION.md)** - Complete guide to Google Drive integration
- **[Toolbar Usage Guide](TOOLBAR_USAGE.md)** - Multi-level menu system documentation
- **[Core Module README](antioch/core/README.md)** - Filesystem and storage backend details
- **[Canvas Macros Guide](antioch/macros/canvas_macros/README.md)** - Canvas component documentation

## Architecture

```
antioch/
├── elements.py           # Core DOM elements (Div, Button, Input, Canvas, etc.)
├── dom.py                # DOM manipulation helper
├── core/                 # Core modules
│   ├── filesystem.py     # Virtual filesystem with observers
│   ├── storage.py        # Storage backends (localStorage, memory)
│   ├── async_storage.py  # Async backends (Google Drive)
│   └── sync_queue.py     # Cloud sync with conflict resolution
├── macros/               # UI component library (28 components)
│   ├── base.py           # Base Macro class
│   ├── modal.py          # Modal dialogs
│   ├── window.py         # Draggable windows
│   ├── data_table.py     # Interactive tables
│   ├── chart.py          # Chart.js integration
│   ├── map.py            # Leaflet map integration
│   ├── form.py           # Form builder with validation
│   └── ...               # And 20+ more components
└── lib/                  # External library loading utilities

scripts/
├── examples/             # 20+ demonstration scripts
├── tutorials/            # Learning materials
└── main.py               # Entry point for your app

build.py                  # Build script
environment.py            # Build environment setup
```

## API Overview

### Creating Elements

```python
from antioch import Div, H1, Button, Input, Canvas

# Create with content
div = Div("Hello World")
heading = H1("Title")

# Method chaining for styling
button = Button("Submit").style.update({
    "background_color": "#4CAF50",
    "color": "white",
    "padding": "10px 20px"
})

# Event handling
input_field = Input()
input_field.on_input(lambda e: print(f"Value: {e.target.value}"))
```

### DOM Manipulation

```python
from antioch import DOM

# Add elements to page
DOM.add(div)                    # Add to body
DOM.add(div, "#container")      # Add to specific selector

# Find elements
element = DOM.find(".my-class")
elements = DOM.find_all("button")

# Remove and clear
DOM.remove(element)
DOM.clear()                     # Clear entire page
```

### Using Macros

```python
from antioch.macros import Modal, DataTable, Toolbar

# Create modal
modal = Modal(title="Settings", closable=True)
modal.set_content(Div("Modal content here"))
modal.show()

# Create data table
table = DataTable(
    columns=["Name", "Email", "Role"],
    data=[
        ["Alice", "alice@example.com", "Admin"],
        ["Bob", "bob@example.com", "User"]
    ]
)
DOM.add(table.element)

# Create toolbar with nested menus
toolbar = Toolbar([
    {
        "label": "File",
        "items": [
            {"label": "New", "action": lambda: print("New")},
            {"label": "Open", "action": lambda: print("Open")},
            {"separator": True},
            {"label": "Exit", "action": lambda: print("Exit")}
        ]
    }
])
DOM.add(toolbar.element)
```

### Virtual Filesystem

```python
from antioch.core import get_filesystem, LocalStorageBackend

# Initialize filesystem
backend = LocalStorageBackend()
fs = get_filesystem(backend)

# File operations
fs.create_file("notes.txt", "Hello World")
content = fs.read_file("notes.txt")
fs.create_directory("documents")
fs.navigate_to("/documents")

# Observe changes
def on_change(event_type, path, item):
    print(f"File {event_type}: {path}")

fs.add_observer(on_change)
```

### Cloud Sync

```python
from antioch.core import GoogleDriveBackend, SyncQueue, AsyncLocalStorageBackend

# Setup backends
local = AsyncLocalStorageBackend()
drive = GoogleDriveBackend(client_id="your-client-id.apps.googleusercontent.com")

# Create sync queue
sync_queue = SyncQueue(local, drive, debounce_ms=2000)

# Sync UI components
from antioch.macros import SyncStatusIndicator, StorageSettingsPanel

status = SyncStatusIndicator(sync_queue, show_details=True)
settings = StorageSettingsPanel(fs, sync_queue)

DOM.add(status.element)
DOM.add(settings.element)
```

## Build Configuration

Customize packages in `build.py`:

```python
# Pyodide packages (from Pyodide's package index)
PYODIDE_PACKAGES = [
    'micropip',
    'numpy',      # If you need numerical computing
    'pandas',     # If you need data analysis
]

# PyPI packages (installed via micropip)
PYPI_PACKAGES = [
    'requests',   # If you need HTTP requests
    # Add other pure Python packages
]
```

## Browser Compatibility

Antioch works in any modern browser that supports WebAssembly:
- Chrome/Edge 89+
- Firefox 89+
- Safari 14.1+
- Opera 75+

## Performance Considerations

- First load includes ~420MB Pyodide runtime (cached by browser)
- Subsequent loads are instant (served from cache)
- Python execution is near-native speed thanks to WebAssembly
- DOM operations are direct browser API calls (no JavaScript overhead)

## Use Cases

- **Interactive Dashboards** - Data visualization and monitoring
- **Educational Tools** - Python tutorials and interactive learning
- **Browser-Based IDEs** - Code editors and REPLs
- **Games** - 2D games using canvas components
- **Data Analysis Tools** - Pandas-powered web apps
- **Prototyping** - Rapid UI development without backend setup

## Development Workflow

1. Write your application in `scripts/main.py` or create new scripts
2. Import Antioch components and build your UI
3. Run `python build.py` to generate `output/index.html`
4. Serve the output folder with any HTTP server
5. Deploy by copying `output/` to any web hosting (GitHub Pages, Netlify, etc.)

## Deployment

The generated `output/index.html` and folder is completely self-contained:

```bash
# Deploy to GitHub Pages
cp -r output/* docs/
git add docs/
git commit -m "Deploy to GitHub Pages"
git push

# Deploy to any static host
# Just upload the output/ folder contents
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Stats

- **Core Library**: ~2,100 lines of Python
- **Component Library**: 29 reusable macros
- **Examples**: 20+ demonstration scripts
- **Documentation**: 5 comprehensive guides
- **Zero Dependencies**: (except Pyodide runtime)

## Credits

Built with [Pyodide](https://pyodide.org/) - Python for the browser powered by WebAssembly.

External library integrations:
- [Chart.js](https://www.chartjs.org/) for charts
- [Leaflet](https://leafletjs.com/) for maps
- [CodeMirror](https://codemirror.net/) for code editing

---

**Start building Python web apps today - no JavaScript required!**