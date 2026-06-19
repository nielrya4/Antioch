# Antioch

**Build interactive web applications entirely in Python - no JavaScript required**

Antioch is a modern Python framework for building rich, interactive web applications that run entirely in the browser using [Pyodide](https://pyodide.org/) (Python compiled to WebAssembly). Write complete web applications in pure Python with a clean, intuitive API.

## Table of Contents

- [What is Antioch?](#what-is-antioch)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Themes](#themes)
- [Event System](#event-system)
- [Element Tree & DOM Manipulation](#element-tree--dom-manipulation)
- [CLI Reference](#cli-reference)
- [Configuration](#configuration)
- [Component Library (Macros)](#component-library-macros)
- [Virtual Filesystem](#virtual-filesystem)
- [Build Process](#build-process)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Advanced Topics](#advanced-topics)
- [Architecture](#architecture)
- [Deployment](#deployment)

---

## What is Antioch?

Antioch is a **client-side Python web framework** that lets you build modern web applications without writing any JavaScript. Instead of running Python on a server, Antioch applications run entirely in the browser using WebAssembly.

### Key Features

- **Pure Python Development** - Write complete web applications in Python (no HTML, CSS, or JavaScript required)
- **Modern Event System** - Unified event handling with decorators and event combination (`|` operator)
- **Direct DOM Manipulation** - Pythonic API for creating and manipulating HTML elements
- **Rich Component Library** - 28+ pre-built UI components (modals, windows, forms, charts, maps, etc.)
- **Virtual Filesystem** - In-browser file system with automatic persistence via localStorage
- **Cloud Synchronization** - Google Drive integration for data sync across devices
- **Zero Backend Required** - Generates self-contained static HTML that runs client-side
- **Professional CLI** - Command-line tools for project scaffolding, building, and development
- **Full Python Ecosystem** - Use NumPy, Pandas, and other pure-Python packages via micropip

### What Can You Build?

- Interactive dashboards and data visualizations
- Browser-based IDEs and code editors
- Educational tools and interactive tutorials
- 2D games using canvas components
- Data analysis applications with Pandas
- Form-based applications with validation
- Scientific computing tools
- Rapid UI prototypes

---

## How It Works

### The Technology Stack

1. **Pyodide** - Python interpreter compiled to WebAssembly that runs in the browser
2. **Antioch Framework** - Python library providing DOM manipulation, event handling, and UI components
3. **Build System** - CLI that bundles your Python code with Pyodide into a single HTML file
4. **Browser** - Any modern browser with WebAssembly support executes your Python code

### Execution Flow

```
Your Python Code (scripts/main.py)
         ↓
Antioch CLI (antioch build)
         ↓
Static HTML + Embedded Python (output/index.html)
         ↓
Browser loads HTML
         ↓
Pyodide initializes (Python runtime in WebAssembly)
         ↓
Your Python code executes
         ↓
Antioch manipulates DOM, handles events
         ↓
Interactive web application running!
```

### Why No Server Needed?

Traditional Python web frameworks (Django, Flask) run Python on a server and send HTML to the browser. Antioch runs Python **in the browser itself** via WebAssembly, so there's no need for a backend server. This means:

- **Zero hosting costs** - Deploy to any static host (GitHub Pages, Netlify, S3, etc.)
- **Instant deployment** - Just upload HTML files
- **No backend complexity** - No databases, APIs, or server configuration
- **Works offline** - Applications continue running without internet
- **Enhanced privacy** - All data stays in the user's browser

---

## Installation

### Option 1: Portable Installer (Recommended)

The installer is a single 7.9MB file that includes everything you need:

```bash
# Download and run installer
curl -sSL https://github.com/nielrya4/antioch/releases/latest/download/antioch-installer.sh | bash

# Or download manually and install
wget https://github.com/nielrya4/antioch/releases/latest/download/antioch-installer.sh
bash antioch-installer.sh

# System-wide installation (requires sudo)
sudo bash antioch-installer.sh --system
```

This installs the `antioch` command to your PATH (~/.local/bin or /usr/local/bin).

### Option 2: From Source

```bash
# Clone repository
git clone https://github.com/ryanmccauley/antioch.git
cd antioch

# Use development CLI
./build_installer/antioch-cli env

# Or install CLI with pip
pip install -e .
```

### Verify Installation

```bash
antioch --help
```

You should see the Antioch CLI help message.

---

## Quick Start

### 1. Create a New Project

```bash
# Create project directory
mkdir my-antioch-app
cd my-antioch-app

# Initialize project (creates scripts/, assets/, antioch.toml, antioch/)
antioch env
```

This creates:
- `scripts/main.py` - Your application entry point (with working counter example)
- `assets/styles.css` - Custom CSS styles
- `antioch.toml` - Project configuration
- `antioch/` - The Antioch framework library

### 2. Edit Your Application

Open `scripts/main.py` and replace with:

```python
"""
My First Antioch Application
"""
from antioch import *

def main():
    # Create a title
    DOM.add(
        H1("Welcome to My App!", style={
            "color": "#2196F3",
            "text-align": "center"
        })
    )

    # Create a counter
    count = 0
    display = H2(f"Count: {count}", style={"text-align": "center"})
    DOM.add(display)

    # Create buttons
    btn_container = Div(style={
        "text-align": "center",
        "margin-top": "20px"
    })

    increment_btn = Button("Increment", style={
        "padding": "10px 20px",
        "margin": "5px",
        "font-size": "16px",
        "cursor": "pointer",
        "background-color": "#4CAF50",
        "color": "white",
        "border": "none",
        "border-radius": "4px"
    })

    decrement_btn = Button("Decrement", style={
        "padding": "10px 20px",
        "margin": "5px",
        "font-size": "16px",
        "cursor": "pointer",
        "background-color": "#f44336",
        "color": "white",
        "border": "none",
        "border-radius": "4px"
    })

    btn_container.add(increment_btn, decrement_btn)
    DOM.add(btn_container)

    # Add event handlers using @when decorator
    @when(increment_btn.events.click)
    def handle_increment(sender, event):
        nonlocal count
        count += 1
        display.set_text(f"Count: {count}")

    @when(decrement_btn.events.click)
    def handle_decrement(sender, event):
        nonlocal count
        count -= 1
        display.set_text(f"Count: {count}")

if __name__ == "__main__":
    main()
```

### 3. Build Your Application

```bash
antioch build
```

This creates `output/index.html` and copies all necessary files to `output/`.

### 4. Run Development Server

```bash
antioch run
```

This starts a local server at http://localhost:8000 and opens your browser automatically.

### 5. Deploy

The `output/` directory contains everything needed. Just upload it to any static host:

```bash
# Deploy to GitHub Pages
cp -r output/* docs/
git add docs/
git commit -m "Deploy app"
git push

# Or use Netlify, Vercel, S3, etc.
```

---

## Core Concepts

### Elements

Elements are Python objects representing HTML DOM nodes. Antioch provides classes for all standard HTML elements:

```python
from antioch import Div, H1, P, Button, Input, Img, Canvas, Table, Tr, Td

# Create elements
heading = H1("Hello World")
paragraph = P("This is a paragraph")
button = Button("Click Me")
text_input = Input(type="text", placeholder="Enter name...")
image = Img(src="photo.jpg", alt="Photo")

# Elements can contain other elements
container = Div(
    H1("My App"),
    P("Welcome to my application"),
    Button("Get Started")
)
```

### Element Styling

Every element has a `.style` property for CSS styling:

```python
# Method 1: Dictionary update
button.style.update({
    "background-color": "#4CAF50",
    "color": "white",
    "padding": "10px 20px",
    "border": "none",
    "border-radius": "4px"
})

# Method 2: Pass style dict to constructor
button = Button("Click", style={
    "background-color": "#4CAF50",
    "color": "white"
})

# Method 3: Direct property access (Python-style names)
button.style.background_color = "#4CAF50"
button.style.color = "white"

# Method 4: Chain multiple styles
button.style.set("background-color", "#4CAF50") \
           .set("color", "white") \
           .set("padding", "10px 20px")
```

### Element Attributes

Set HTML attributes on elements:

```python
input_field = Input()
input_field.set_attribute("type", "email")
input_field.set_attribute("placeholder", "Enter email...")
input_field.set_attribute("required", True)

# Or pass in constructor
input_field = Input(
    type="email",
    placeholder="Enter email...",
    required=True
)

# Get attributes
value = input_field.get_attribute("value")

# Check if attribute exists
if input_field.has_attribute("required"):
    print("Field is required")
```

### Element Properties

Access common element properties:

```python
# Text content
heading.set_text("New Title")
text = heading.get_text()

# HTML content
div.set_html("<strong>Bold text</strong>")
html = div.get_html()

# Value (for inputs)
input_field.set_value("Default text")
value = input_field.get_value()

# Classes
button.add_class("btn", "btn-primary")
button.remove_class("btn-primary")
button.toggle_class("active")
has_class = button.has_class("btn")
```

---

## Themes

Antioch includes a theming system that provides consistent color palettes and styling across your application. Themes affect macros, components, and provide a `COLORS` dictionary for custom styling.

### Using Themes

Apply a theme at the start of your application:

```python
from antioch.themes import set_theme, COLORS
import js

def main():
    # Set the theme
    set_theme("basalt")

    # Apply theme background color to page
    js.document.body.style.backgroundColor = COLORS['background']

    # Use theme colors in your components
    button = Button("Click Me", style={
        "background-color": COLORS['primary'],
        "color": COLORS['text']
    })
```

### Available Themes

Antioch includes several built-in themes with distinct color palettes:

**basalt** - Dark theme with cool grays and blue accents
```python
set_theme("basalt")
# Background: Dark gray (#1e1e1e)
# Primary: Blue (#4a9eff)
# Text: Light gray
```

**rhyolite** - Light theme with warm earth tones
```python
set_theme("rhyolite")
# Background: Light beige
# Primary: Rust orange
# Text: Dark brown
```

**quartzite** - Light theme with cool blue-gray tones
```python
set_theme("quartzite")
# Background: Off-white (#f5f5f5)
# Primary: Teal blue
# Text: Charcoal
```

**marble** - Clean, minimal light theme
```python
set_theme("marble")
# Background: White
# Primary: Navy blue
# Text: Black
```

**jasper** - Vibrant theme with bold colors
```python
set_theme("jasper")
# Background: Deep purple
# Primary: Orange
# Text: White
```

**diorite** - Balanced dark theme with green accents
```python
set_theme("diorite")
# Background: Dark slate
# Primary: Emerald green
# Text: Off-white
```

### Theme Colors Dictionary

After setting a theme, the `COLORS` dictionary contains the active theme's colors:

```python
from antioch.themes import set_theme, COLORS

set_theme("basalt")

# Available color keys:
COLORS['background']     # Main background color
COLORS['foreground']     # Foreground/surface color
COLORS['primary']        # Primary accent color
COLORS['secondary']      # Secondary accent color
COLORS['text']           # Main text color
COLORS['text_secondary'] # Secondary text color
COLORS['border']         # Border color
COLORS['hover']          # Hover state color
COLORS['success']        # Success/positive color
COLORS['warning']        # Warning color
COLORS['error']          # Error/danger color
COLORS['info']           # Info color

# Use in element styles
card = Div(style={
    "background-color": COLORS['foreground'],
    "border": f"1px solid {COLORS['border']}",
    "color": COLORS['text'],
    "padding": "20px"
})
```

### Themed Components

All macro components automatically use the active theme's colors:

```python
from antioch.macros import Modal, Alert, Button
from antioch.themes import set_theme

set_theme("basalt")

# Components use theme colors automatically
modal = Modal(title="Themed Modal")
alert = Alert(message="Success!", alert_type="success")
button = Button("Themed Button")

# The components will use basalt theme colors
```

### Creating Custom Themes

You can create custom themes by defining a color dictionary:

```python
from antioch.themes import register_theme, set_theme

# Define custom theme
custom_theme = {
    'background': '#2d2d2d',
    'foreground': '#3a3a3a',
    'primary': '#ff6b6b',
    'secondary': '#4ecdc4',
    'text': '#ffffff',
    'text_secondary': '#b0b0b0',
    'border': '#4a4a4a',
    'hover': '#ff8787',
    'success': '#51cf66',
    'warning': '#ffd43b',
    'error': '#ff6b6b',
    'info': '#339af0'
}

# Register and use custom theme
register_theme("custom", custom_theme)
set_theme("custom")
```

### Switching Themes Dynamically

You can change themes at runtime:

```python
from antioch.themes import set_theme, COLORS
import js

current_theme = "basalt"

def toggle_theme():
    global current_theme
    current_theme = "marble" if current_theme == "basalt" else "basalt"
    set_theme(current_theme)

    # Update page background
    js.document.body.style.backgroundColor = COLORS['background']

    # Rebuild UI components to apply new theme
    rebuild_ui()

toggle_btn = Button("Toggle Theme")
toggle_btn.on_click(lambda e: toggle_theme())
```

---

## Event System

Antioch provides a **unified event system** that works across all elements with a consistent API.

### The @when Decorator (Recommended)

The modern way to handle events:

```python
from antioch import *

button = Button("Click Me")
DOM.add(button)

# Handle click events
@when(button.events.click)
def handle_click(sender, event):
    print(f"Button clicked! Sender: {sender}")
    print(f"Mouse position: ({event.clientX}, {event.clientY})")

# Handle input events
text_input = Input(type="text")
DOM.add(text_input)

@when(text_input.events.input)
def handle_input(sender, event):
    print(f"Input value changed: {sender.get_value()}")
```

### Event Combination with | Operator

Respond to multiple events with a single handler:

```python
button1 = Button("Button 1")
button2 = Button("Button 2")
button3 = Button("Button 3")

# Handle clicks on any of the three buttons
@when(button1.events.click | button2.events.click | button3.events.click)
def handle_any_button(sender, event):
    print(f"{sender.get_text()} was clicked!")
```

### Traditional Event Handlers

You can also use traditional callback-style handlers:

```python
def on_click(event):
    print("Button clicked!")

button.on_click(on_click)

# Lambda for simple cases
button.on_click(lambda e: print("Clicked!"))
```

### Available Events

Every element provides these events through `.events`:

- **Mouse Events**: `click`, `dblclick`, `mousedown`, `mouseup`, `mouseenter`, `mouseleave`, `mousemove`, `mouseover`, `mouseout`
- **Keyboard Events**: `keydown`, `keyup`, `keypress`
- **Form Events**: `input`, `change`, `submit`, `focus`, `blur`
- **Drag Events**: `drag`, `dragstart`, `dragend`, `dragover`, `dragenter`, `dragleave`, `drop`
- **Touch Events**: `touchstart`, `touchmove`, `touchend`, `touchcancel`
- **Other**: `scroll`, `resize`, `load`, `error`

### Event Object Properties

Event handlers receive an event object with useful properties:

```python
@when(element.events.click)
def handle(sender, event):
    # Mouse position
    x, y = event.clientX, event.clientY

    # Keyboard keys
    key = event.key
    ctrl_pressed = event.ctrlKey
    shift_pressed = event.shiftKey
    alt_pressed = event.altKey

    # Form values
    value = event.target.value

    # Prevent default behavior
    event.preventDefault()

    # Stop event propagation
    event.stopPropagation()
```

### Programmatic Event Firing

You can trigger events programmatically:

```python
# Fire an event
button.events.click.fire(event_object)

# Fire without event object (defensive handlers should check for None)
button.events.click.fire(None)
```

### Event Namespaces

Events are organized in namespaces for different element types:

```python
# All elements have basic events
button.events.click
button.events.mouseenter

# Canvas elements have canvas-specific events
canvas.events.canvas_click
canvas.events.canvas_mousemove

# Macro components have custom events
modal.events.opened
modal.events.closed
```

---

## Element Tree & DOM Manipulation

### Parent-Child Relationships

Elements form a tree structure. Every element (except the root) has a parent and can have children:

```python
# Create a hierarchy
container = Div()
header = H1("Title")
content = P("Content")

# Add children
container.add(header, content)

# Access parent
print(header.parent)  # Returns container

# Access children
for child in container.children:
    print(child)

# Navigation
sibling = header.next_sibling()
previous = content.previous_sibling()

# Find ancestors
ancestor = content.find_parent_by_tag("div")
```

### Adding Elements to the Page

Use the `DOM` utility to add elements to the document:

```python
from antioch import DOM

# Add to document body
DOM.add(element)

# Add to specific parent by selector
DOM.add(element, "#container")
DOM.add(element, ".sidebar")

# Add multiple elements
DOM.add(heading, paragraph, button)

# Add to element reference
container = Div()
DOM.add(container)
container.add(H1("Title"), P("Content"))
```

### Finding Elements

```python
from antioch import DOM

# Find single element
element = DOM.find("#my-id")
element = DOM.find(".my-class")
element = DOM.find("button")

# Find all matching elements
buttons = DOM.find_all("button")
items = DOM.find_all(".list-item")

# Find within an element
container = Div()
container.add(Button("Click"))
button = container.find("button")
all_buttons = container.find_all("button")
```

### Removing Elements

```python
# Remove specific element
DOM.remove(element)

# Remove by selector
DOM.remove("#old-element")

# Clear all children
container.clear()

# Clear entire page
DOM.clear()

# Remove element from its parent
element.remove()
```

### Element Manipulation Methods

```python
# Add children
container.add(child1, child2, child3)

# Insert at position
container.insert(0, first_child)  # Insert at beginning
container.insert(2, middle_child)  # Insert at index

# Replace child
container.replace_child(old_child, new_child)

# Remove child
container.remove_child(child)

# Clone element
clone = element.clone(deep=True)  # Deep clone with all children
shallow_clone = element.clone(deep=False)  # Clone without children
```

---

## CLI Reference

The Antioch CLI provides commands for managing projects:

### antioch env

Initialize a new Antioch project with starter files.

```bash
antioch env
```

Creates:
- `scripts/main.py` - Application entry point with counter example
- `assets/styles.css` - Custom CSS file
- `antioch.toml` - Project configuration
- `antioch/` - Antioch framework library

### antioch build

Build the project to the output directory.

```bash
antioch build
```

This:
1. Reads `antioch.toml` configuration
2. Copies `antioch/` library to `output/antioch/`
3. Copies `scripts/` directory to `output/scripts/`
4. Copies `assets/` directory to `output/assets/`
5. Generates `output/index.html` with Pyodide loader
6. Embeds package dependencies from config

### antioch run

Start a local development server.

```bash
antioch run                # Start on default port (8000)
antioch run --port 3000    # Custom port
antioch run --no-open      # Don't auto-open browser
```

Serves the `output/` directory and opens your browser automatically (unless `--no-open`).

### antioch install

Add a Python package to your project dependencies.

```bash
antioch install numpy           # Add numpy
antioch install pandas matplotlib  # Add multiple packages
```

This adds the package to `antioch.toml` under `[dependencies]` → `pypi_packages`. The packages will be automatically installed via micropip when your app runs.

### antioch update

Update your installed Antioch framework to the latest version from GitHub.

```bash
antioch update                  # Update to latest from master branch
antioch update --branch dev     # Update from a specific branch
antioch update --ssh            # Use SSH instead of HTTPS (requires SSH key setup)
```

This command:
1. Creates a backup of your current Antioch installation
2. Clones the latest version from GitHub
3. Replaces the framework library in `~/.antioch/antioch/`
4. Keeps your CLI, build tools, and projects unchanged

**What gets updated:**
- Antioch framework library (`antioch/` directory)
- All themes and macros
- Core functionality improvements

**What stays unchanged:**
- Your CLI and build tools
- Your projects and configurations
- Project-specific `antioch/` directories (you'll need to run `antioch build` to use the updated framework)

After updating, rebuild your projects to use the new framework:

```bash
cd your-project
antioch build
```

### antioch --help

Show detailed help:

```bash
antioch --help              # Main help
antioch env --help          # Help for specific command
antioch build --help
antioch run --help
antioch install --help
```

---

## Configuration

Projects are configured via `antioch.toml` in the project root.

### Full Configuration Example

```toml
[project]
name = "my-antioch-app"
version = "0.1.0"
entry_point = "scripts/main.py"

[build]
output_dir = "output"
scripts_dir = "scripts"
pyodide_source = "cdn"        # Options: "local" or "cdn"
pyodide_version = "0.29.3"    # Used when pyodide_source = "cdn"

[dependencies]
# Pyodide built-in packages to load
pyodide_packages = [
    "micropip",
]

# PyPI packages to install via micropip
pypi_packages = [
    "numpy",
    "pandas",
    "matplotlib",
]

# Local packages (paths relative to project root)
local_packages = []

[server]
host = "localhost"
port = 8000
auto_open = true              # Automatically open browser when running
```

### Configuration Sections

#### [project]

- `name` - Project name
- `version` - Project version
- `entry_point` - Main Python file to execute (default: `scripts/main.py`)

#### [build]

- `output_dir` - Where to output build files (default: `output`)
- `scripts_dir` - Where Python scripts are located (default: `scripts`)
- `pyodide_source` - How to load Pyodide:
  - `"cdn"` - Load from CDN (recommended - 8MB builds, always up-to-date)
  - `"local"` - Bundle Pyodide locally (~300MB builds, works offline)
- `pyodide_version` - Pyodide version when using CDN (e.g., `"0.29.3"`)

#### [dependencies]

- `pyodide_packages` - Packages from Pyodide's package index (faster, pre-compiled)
  - Examples: `"micropip"`, `"numpy"`, `"pandas"`, `"scipy"`, `"scikit-learn"`
  - See full list: https://pyodide.org/en/stable/usage/packages-in-pyodide.html

- `pypi_packages` - Pure Python packages from PyPI (installed via micropip)
  - Must be pure Python (no C extensions unless available in Pyodide)
  - Add with: `antioch install <package>`

- `local_packages` - Paths to local Python packages to include

#### [server]

- `host` - Development server host (default: `localhost`)
- `port` - Development server port (default: `8000`)
- `auto_open` - Auto-open browser when starting server (default: `true`)

---

## Component Library (Macros)

Antioch includes 28+ pre-built UI components called "Macros". Each macro is a reusable component with its own API.

### Interactive Components

```python
from antioch.macros import Counter, Slider, Dropdown, Pagination

# Counter with increment/decrement
counter = Counter(initial_value=0, min_value=0, max_value=100)
DOM.add(counter.element)

# Slider
slider = Slider(min_val=0, max_val=100, initial_val=50, step=1)
slider.on_change(lambda value: print(f"Slider: {value}"))
DOM.add(slider.element)

# Dropdown
dropdown = Dropdown(
    options=["Option 1", "Option 2", "Option 3"],
    selected="Option 1"
)
dropdown.on_select(lambda option: print(f"Selected: {option}"))
DOM.add(dropdown.element)

# Pagination
pagination = Pagination(total_pages=10, current_page=1)
pagination.on_page_change(lambda page: print(f"Page: {page}"))
DOM.add(pagination.element)
```

### Layout Components

```python
from antioch.macros import Modal, WindowManager, Tabs, Accordion

# Modal dialog
modal = Modal(title="Settings", closable=True, width="500px")
modal.set_content(Div("Modal content here"))
modal.show()
modal.hide()

# Window Manager (draggable, resizable windows)
wm = WindowManager()
DOM.add(wm.element)

window = wm.create_window(
    title="My Window",
    width=400,
    height=300,
    x=100,
    y=100
)
window.set_content(Div("Window content"))

# Tabs
tabs = Tabs(tabs_data=[
    {"title": "Tab 1", "content": Div("Content 1")},
    {"title": "Tab 2", "content": Div("Content 2")},
    {"title": "Tab 3", "content": Div("Content 3")}
])
DOM.add(tabs.element)

# Accordion
accordion = Accordion(sections=[
    {"title": "Section 1", "content": Div("Content 1")},
    {"title": "Section 2", "content": Div("Content 2")}
])
DOM.add(accordion.element)
```

### Data Display Components

```python
from antioch.macros import DataTable, Chart, Map

# Data Table
table = DataTable(
    columns=["Name", "Email", "Role"],
    data=[
        ["Alice", "alice@example.com", "Admin"],
        ["Bob", "bob@example.com", "User"],
        ["Charlie", "charlie@example.com", "User"]
    ],
    sortable=True,
    filterable=True,
    row_actions=[
        {"label": "Edit", "callback": lambda row: print(f"Edit {row}")},
        {"label": "Delete", "callback": lambda row: print(f"Delete {row}")}
    ]
)
DOM.add(table.element)

# Chart (Chart.js integration)
chart = Chart(
    chart_type="line",
    data={
        "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
        "datasets": [{
            "label": "Sales",
            "data": [12, 19, 3, 5, 2]
        }]
    },
    options={"responsive": True}
)
DOM.add(chart.element)

# Map (Leaflet integration)
map_component = Map(
    center=[51.505, -0.09],
    zoom=13,
    height="400px"
)
map_component.add_marker([51.5, -0.09], popup="Hello World!")
DOM.add(map_component.element)
```

### Form Components

```python
from antioch.macros import Form, EmailValidator, MinLengthValidator, RequiredValidator

# Form with validation
form = Form()

# Add fields with validators
form.add_field(
    "email",
    Input(type="email", placeholder="Email"),
    validators=[RequiredValidator(), EmailValidator()]
)

form.add_field(
    "password",
    Input(type="password", placeholder="Password"),
    validators=[RequiredValidator(), MinLengthValidator(8)]
)

# Add submit handler
def handle_submit(data):
    print(f"Form data: {data}")
    # data = {"email": "...", "password": "..."}

form.on_submit(handle_submit)

DOM.add(form.element)
```

### Feedback Components

```python
from antioch.macros import Alert, Toast, ProgressBar

# Alert
alert = Alert(message="Operation successful!", alert_type="success", dismissible=True)
DOM.add(alert.element)

# Toast notification
toast = Toast(message="File saved!", duration=3000, position="top-right")
toast.show()

# Progress Bar
progress = ProgressBar(initial_value=0, max_value=100, show_percentage=True)
DOM.add(progress.element)

# Update progress
progress.set_value(50)
progress.set_value(100)
```

### Filesystem Components

```python
from antioch.macros import FileSelector, FileUpload, FileDownload

# File selector (virtual filesystem)
selector = FileSelector(filesystem=fs, on_select=lambda path: print(f"Selected: {path}"))
DOM.add(selector.element)

# File upload (from user's computer)
uploader = FileUpload(
    accept=".txt,.py",
    on_upload=lambda filename, content: print(f"Uploaded {filename}")
)
DOM.add(uploader.element)

# File download (to user's computer)
download = FileDownload(filename="data.txt", content="Hello World")
DOM.add(download.element)
```

### Navigation Components

```python
from antioch.macros import Toolbar

# Multi-level toolbar
toolbar = Toolbar(items=[
    {
        "label": "File",
        "items": [
            {"label": "New", "action": lambda: print("New file")},
            {"label": "Open", "action": lambda: print("Open file")},
            {"separator": True},
            {"label": "Save", "action": lambda: print("Save file")},
            {
                "label": "Export",
                "items": [  # Nested submenu
                    {"label": "As PDF", "action": lambda: print("Export PDF")},
                    {"label": "As HTML", "action": lambda: print("Export HTML")}
                ]
            }
        ]
    },
    {
        "label": "Edit",
        "items": [
            {"label": "Cut", "action": lambda: print("Cut")},
            {"label": "Copy", "action": lambda: print("Copy")},
            {"label": "Paste", "action": lambda: print("Paste")}
        ]
    }
])
DOM.add(toolbar.element)
```

### Code Editing Components

```python
from antioch.macros import CodeBlock

# Syntax-highlighted code viewer/editor (CodeMirror)
code_editor = CodeBlock(
    code='def hello():\n    print("Hello, World!")',
    language="python",
    theme="monokai",
    line_numbers=True,
    read_only=False
)

# Get edited code
code = code_editor.get_code()

# Set new code
code_editor.set_code('print("New code")')

DOM.add(code_editor.element)
```

---

## Virtual Filesystem

Antioch provides an in-browser virtual filesystem with automatic persistence.

### Basic Usage

```python
from antioch.core import get_filesystem, LocalStorageBackend

# Initialize filesystem
backend = LocalStorageBackend()  # Persists to browser's localStorage
fs = get_filesystem(backend)

# Create files
fs.create_file("notes.txt", "My notes content")
fs.create_file("data.json", '{"key": "value"}')

# Read files
content = fs.read_file("notes.txt")

# Update files
fs.update_file("notes.txt", "Updated content")

# Delete files
fs.delete_file("notes.txt")

# Create directories
fs.create_directory("documents")
fs.create_directory("documents/2024")

# Navigate filesystem
fs.navigate_to("/documents")
fs.navigate_to("..")  # Go up one level
fs.navigate_to("/")   # Go to root

# List current directory
items = fs.list_current_directory()
for item in items:
    print(f"{item.name} ({'dir' if item.is_directory else 'file'})")

# Get current path
current_path = fs.current_directory_path()
```

### File System Observers

Watch for filesystem changes:

```python
def on_change(event_type, path, item):
    """
    event_type: "created", "updated", "deleted", "navigated"
    path: Full path of affected item
    item: FileSystemItem object (or None for navigation)
    """
    print(f"{event_type}: {path}")

    if event_type == "created":
        print(f"New item: {item.name}")
    elif event_type == "updated":
        print(f"Updated: {item.name}")
    elif event_type == "deleted":
        print(f"Deleted: {path}")
    elif event_type == "navigated":
        print(f"Navigated to: {path}")

# Add observer
fs.add_observer(on_change)

# Remove observer
fs.remove_observer(on_change)
```

### Storage Backends

Antioch supports multiple storage backends:

#### LocalStorageBackend (Default)

Persists data to browser's localStorage (survives page reloads):

```python
from antioch.core import LocalStorageBackend

backend = LocalStorageBackend()
fs = get_filesystem(backend)
```

#### MemoryBackend

In-memory only (data lost on page reload):

```python
from antioch.core import MemoryBackend

backend = MemoryBackend()
fs = get_filesystem(backend)
```

#### AsyncLocalStorageBackend

Async wrapper around localStorage (for cloud sync):

```python
from antioch.core import AsyncLocalStorageBackend

backend = AsyncLocalStorageBackend()
# Used with SyncQueue for cloud synchronization
```

---

## Build Process

### What Happens During Build?

When you run `antioch build`:

1. **Read Configuration** - Parse `antioch.toml`
2. **Copy Antioch Library** - Copy `antioch/` to `output/antioch/`
3. **Copy Scripts** - Copy `scripts/` to `output/scripts/`
4. **Copy Assets** - Copy `assets/` to `output/assets/`
5. **Generate HTML** - Create `output/index.html` with:
   - Pyodide loader (CDN or local)
   - Package installation code (micropip)
   - Python execution environment
   - Your application entry point

### Generated HTML Structure

The `output/index.html` file contains:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Antioch App</title>
    <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
    <div id="loading">Loading Python runtime...</div>

    <!-- Pyodide loader script -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.29.3/full/pyodide.js"></script>

    <script>
        async function main() {
            // Initialize Pyodide
            let pyodide = await loadPyodide();

            // Install packages via micropip
            await pyodide.loadPackage("micropip");
            const micropip = pyodide.pyimport("micropip");
            await micropip.install(["numpy", "pandas"]);

            // Mount virtual filesystem
            pyodide.FS.mkdirTree('/scripts');
            pyodide.FS.mkdirTree('/antioch');

            // Load your Python code
            await pyodide.runPythonAsync(`
                import sys
                sys.path.insert(0, '/scripts')
                sys.path.insert(0, '/')

                from scripts.main import main
                main()
            `);

            document.getElementById('loading').style.display = 'none';
        }

        main();
    </script>
</body>
</html>
```

### Build Customization

Edit `antioch.toml` to customize the build:

```toml
[build]
output_dir = "dist"           # Change output directory
scripts_dir = "src"            # Change scripts directory
pyodide_source = "local"       # Bundle Pyodide locally
pyodide_version = "0.29.3"

[project]
entry_point = "src/app.py"    # Change entry point
```

---

## API Reference

### DOM Utility

```python
from antioch import DOM

# Add elements
DOM.add(element)                    # Add to body
DOM.add(element, selector)          # Add to selector
DOM.add(el1, el2, el3)              # Add multiple

# Find elements
element = DOM.find(selector)        # Find first match
elements = DOM.find_all(selector)   # Find all matches

# Remove elements
DOM.remove(element)                 # Remove element
DOM.remove(selector)                # Remove by selector

# Clear
DOM.clear()                         # Clear entire document body
```

### Element Classes

All HTML elements are available as classes:

```python
from antioch import (
    # Structure
    Div, Span, Article, Section, Header, Footer, Nav, Main, Aside,

    # Text
    H1, H2, H3, H4, H5, H6, P, Strong, Em, Small, Mark, Del, Ins, Sub, Sup,

    # Lists
    Ul, Ol, Li, Dl, Dt, Dd,

    # Tables
    Table, Thead, Tbody, Tfoot, Tr, Th, Td, Caption,

    # Forms
    Form, Input, Textarea, Button, Select, Option, Label, Fieldset, Legend,

    # Media
    Img, Video, Audio, Source, Canvas, Svg,

    # Interactive
    A, Details, Summary, Dialog,

    # Semantic
    Time, Progress, Meter, Output
)
```

### Element Methods

All elements inherit these methods:

```python
# Content
element.set_text(text)              # Set text content
element.get_text()                  # Get text content
element.set_html(html)              # Set HTML content
element.get_html()                  # Get HTML content
element.set_value(value)            # Set value (inputs)
element.get_value()                 # Get value (inputs)

# Attributes
element.set_attribute(name, value)
element.get_attribute(name)
element.remove_attribute(name)
element.has_attribute(name)

# Classes
element.add_class(*classes)
element.remove_class(*classes)
element.toggle_class(class_name)
element.has_class(class_name)

# Styling
element.style.set(property, value)
element.style.update(dict)
element.style[property] = value

# Tree manipulation
element.add(*children)
element.insert(index, child)
element.remove_child(child)
element.replace_child(old, new)
element.clear()
element.remove()

# Tree navigation
element.parent
element.children
element.first_child()
element.last_child()
element.next_sibling()
element.previous_sibling()
element.find(selector)
element.find_all(selector)
element.find_parent_by_tag(tag)

# Events
element.on_click(handler)
element.on_input(handler)
# ... (all event types)

# Clone
element.clone(deep=True)

# Visibility
element.show()
element.hide()
element.is_visible()
```

### Event Handler Signatures

```python
# Traditional event handlers
def handler(event):
    """
    event: Browser event object with properties like:
        - target: The element that triggered the event
        - clientX, clientY: Mouse coordinates
        - key, ctrlKey, shiftKey, altKey: Keyboard info
        - preventDefault(): Prevent default browser behavior
        - stopPropagation(): Stop event bubbling
    """
    pass

element.on_click(handler)

# @when decorator handlers
@when(element.events.click)
def handler(sender, event):
    """
    sender: The element that triggered the event
    event: Browser event object (same as above)
    """
    pass
```

---

## Examples

The project includes 20+ comprehensive examples in `scripts/examples/`:

### Basic Examples

- **element_events_demo.py** - Basic event handling
- **event_combination_demo.py** - Event combination with `|` operator
- **event_patterns.py** - Common event patterns
- **events_namespace_demo.py** - Event namespaces
- **parent_children_demo.py** - Element tree navigation
- **when_decorator_demo.py** - Using @when decorator
- **unified_events_demo.py** - Unified event system

### Component Examples

- **macro_showcase.py** - All macro components
- **macro_events_demo.py** - Macro event handling
- **window_manager_demo.py** - Draggable windows
- **data_table_demo.py** - Interactive data tables
- **chart_demo.py** - Charts and visualizations
- **map_demo.py** - Interactive maps
- **form_demo.py** - Forms with validation
- **canvas_demo.py** - Canvas graphics
- **code_block_demo.py** - Code editor

### Advanced Examples

- **cloud_sync_demo.py** - Google Drive synchronization
- **js_library_wrapper_demo.py** - Wrapping JavaScript libraries
- **user_input_modal.py** - Custom modal dialogs

### Running Examples

```bash
# Copy example to main.py
cp scripts/examples/macro_showcase.py scripts/main.py

# Or import in main.py
cat > scripts/main.py << 'EOF'
from examples.macro_showcase import main

if __name__ == "__main__":
    main()
EOF

# Build and run
antioch build
antioch run
```

---

## Advanced Topics

### Custom Macros

Create your own reusable components:

```python
from antioch.macros import Macro
from antioch import Div, H3, P, Button

class CustomCard(Macro):
    def __init__(self, title, content, on_action=None):
        super().__init__()
        self.title = title
        self.content = content
        self.on_action = on_action
        self._build()

    def _build(self):
        """Build the component UI"""
        self.element = Div(style={
            "border": "1px solid #ddd",
            "border-radius": "8px",
            "padding": "20px",
            "margin": "10px"
        })

        title_el = H3(self.title, style={"margin-top": "0"})
        content_el = P(self.content)
        action_btn = Button("Action", style={
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "padding": "8px 16px",
            "border-radius": "4px"
        })

        if self.on_action:
            action_btn.on_click(lambda e: self.on_action())

        self.element.add(title_el, content_el, action_btn)

# Use custom macro
card = CustomCard(
    title="My Card",
    content="This is a custom reusable component!",
    on_action=lambda: print("Action clicked!")
)
DOM.add(card.element)
```

### Wrapping JavaScript Libraries

Use JavaScript libraries from Python:

```python
from antioch import Div, Script
from antioch.lib import LibraryLoader

# Load external library
loader = LibraryLoader()
loader.load_script("https://cdn.example.com/library.js")

# Wait for library to load, then use it
import js

# Access JavaScript objects
js_object = js.SomeLibrary.create({
    "option1": "value1",
    "option2": "value2"
})

# Call JavaScript functions
result = js.someFunction("argument")

# Pass Python functions to JavaScript
def python_callback(data):
    print(f"Called from JS: {data}")

js_object.onEvent(python_callback)
```

### Cloud Synchronization

Sync filesystem to Google Drive:

```python
from antioch.core import (
    get_filesystem,
    AsyncLocalStorageBackend,
    GoogleDriveBackend,
    SyncQueue
)

# Setup backends
local_backend = AsyncLocalStorageBackend()
drive_backend = GoogleDriveBackend(
    client_id="your-client-id.apps.googleusercontent.com"
)

# Create filesystem with local backend
fs = get_filesystem(local_backend)

# Create sync queue
sync_queue = SyncQueue(
    local_backend,
    drive_backend,
    debounce_ms=2000  # Wait 2 seconds before syncing changes
)

# Initialize sync
await sync_queue.initialize()

# UI components for sync status
from antioch.macros import SyncStatusIndicator, StorageSettingsPanel

status_indicator = SyncStatusIndicator(sync_queue, show_details=True)
settings_panel = StorageSettingsPanel(fs, sync_queue)

DOM.add(status_indicator.element)
DOM.add(settings_panel.element)

# Now all filesystem changes automatically sync to Google Drive!
fs.create_file("synced.txt", "This will sync to Drive")
```

### Canvas Graphics

Create interactive canvas-based components:

```python
from antioch import Canvas
from antioch.macros.canvas_macros import CanvasButton

# Create canvas
canvas = Canvas(width=800, height=600, style={
    "border": "1px solid black"
})
DOM.add(canvas)

# Get 2D context
ctx = canvas.get_context("2d")

# Draw shapes
ctx.fillStyle = "#FF0000"
ctx.fillRect(10, 10, 100, 100)

ctx.strokeStyle = "#0000FF"
ctx.lineWidth = 2
ctx.strokeRect(150, 10, 100, 100)

# Draw circles
ctx.beginPath()
ctx.arc(200, 300, 50, 0, 2 * 3.14159)
ctx.fillStyle = "#00FF00"
ctx.fill()

# Canvas events
@when(canvas.events.canvas_click)
def handle_canvas_click(sender, event):
    x, y = event.canvas_x, event.canvas_y
    print(f"Canvas clicked at ({x}, {y})")

    # Draw circle where clicked
    ctx.beginPath()
    ctx.arc(x, y, 10, 0, 2 * 3.14159)
    ctx.fillStyle = "#FF00FF"
    ctx.fill()

# Canvas buttons
button = CanvasButton(
    canvas=canvas,
    x=50,
    y=450,
    width=120,
    height=40,
    label="Click Me",
    on_click=lambda: print("Canvas button clicked!")
)
```

### State Management

For complex applications, consider a state management pattern:

```python
class AppState:
    """Centralized application state"""
    def __init__(self):
        self.user = None
        self.items = []
        self.observers = []

    def set_user(self, user):
        self.user = user
        self._notify("user_changed", user)

    def add_item(self, item):
        self.items.append(item)
        self._notify("item_added", item)

    def remove_item(self, item):
        self.items.remove(item)
        self._notify("item_removed", item)

    def observe(self, callback):
        """Register observer for state changes"""
        self.observers.append(callback)

    def _notify(self, event_type, data):
        """Notify all observers of state change"""
        for callback in self.observers:
            callback(event_type, data)

# Create global state
state = AppState()

# Components observe state
def on_state_change(event_type, data):
    if event_type == "user_changed":
        update_ui_for_user(data)
    elif event_type == "item_added":
        add_item_to_ui(data)
    elif event_type == "item_removed":
        remove_item_from_ui(data)

state.observe(on_state_change)

# Update state from anywhere
state.set_user({"name": "Alice", "email": "alice@example.com"})
state.add_item({"id": 1, "title": "Task 1"})
```

---

## Architecture

### Project Structure

```
my-antioch-project/
├── antioch/                    # Antioch framework (copied by antioch env)
│   ├── __init__.py
│   ├── elements.py             # Element classes
│   ├── dom.py                  # DOM utilities
│   ├── event_manager.py        # Event system
│   ├── core/                   # Core modules
│   │   ├── filesystem.py
│   │   ├── storage.py
│   │   ├── async_storage.py
│   │   └── sync_queue.py
│   ├── macros/                 # UI components
│   │   ├── base.py
│   │   ├── modal.py
│   │   ├── window.py
│   │   ├── data_table.py
│   │   ├── chart.py
│   │   ├── form.py
│   │   └── ...
│   └── lib/                    # Library utilities
│       └── library_loader.py
├── scripts/                    # Your application code
│   ├── main.py                 # Entry point
│   └── examples/               # Example scripts
├── assets/                     # Static assets
│   ├── styles.css              # Custom CSS
│   └── images/                 # Images
├── output/                     # Build output (generated)
│   ├── index.html              # Generated HTML
│   ├── antioch/                # Copied framework
│   ├── scripts/                # Copied scripts
│   └── assets/                 # Copied assets
└── antioch.toml                # Project configuration
```

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser                           │
│  ┌───────────────────────────────────────────────┐  │
│  │              Your Antioch App                 │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │         scripts/main.py                 │  │  │
│  │  │  - Your application logic               │  │  │
│  │  │  - Event handlers                       │  │  │
│  │  │  - UI components                        │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  │                    ↓                          │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │        Antioch Framework                │  │  │
│  │  │  - Element classes (Div, Button, etc)   │  │  │
│  │  │  - Event system (@when, .events)        │  │  │
│  │  │  - DOM utilities                        │  │  │
│  │  │  - Macros (Modal, Table, Chart, etc)    │  │  │
│  │  │  - Virtual filesystem                   │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  │                    ↓                          │  │
│  │  ┌─────────────────────────────────────────┐  │  │
│  │  │         Pyodide Runtime                 │  │  │
│  │  │  - CPython interpreter                  │  │  │
│  │  │  - JavaScript bridge                    │  │  │
│  │  │  - Package management (micropip)        │  │  │
│  │  │  - Virtual filesystem (FS)              │  │  │
│  │  └─────────────────────────────────────────┘  │  │
│  │                    ↓                          │  │
│  └───────────────────────────────────────────────┘  │
│                     ↓                               │
│  ┌───────────────────────────────────────────────┐  │
│  │          Browser APIs                         │  │
│  │  - DOM manipulation                           │  │
│  │  - Event handling                             │  │
│  │  - localStorage                               │  │
│  │  - Fetch API                                  │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Event Flow

```
User clicks button in browser
         ↓
Browser triggers DOM event
         ↓
Pyodide intercepts event (JavaScript → Python bridge)
         ↓
Antioch EventManager receives event
         ↓
EventManager notifies subscribed handlers
         ↓
@when decorated handler executes
         ↓
Handler modifies element (e.g., element.set_text())
         ↓
Antioch calls Pyodide's JavaScript bridge
         ↓
DOM is updated in browser
         ↓
User sees updated UI
```

---

## Deployment

### Static Hosting

Since Antioch apps are pure static files, deploy to any static host:

#### GitHub Pages

```bash
# Build
antioch build

# Copy to docs/ (GitHub Pages source)
cp -r output/* docs/

# Commit and push
git add docs/
git commit -m "Deploy to GitHub Pages"
git push

# Enable GitHub Pages in repo settings → Pages → Source: docs/
```

#### Netlify

```bash
# Build
antioch build

# Deploy via Netlify CLI
npm install -g netlify-cli
netlify deploy --dir=output --prod

# Or drag-and-drop output/ folder to Netlify web UI
```

#### Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod output/
```

#### AWS S3

```bash
# Build
antioch build

# Upload to S3
aws s3 sync output/ s3://your-bucket-name/ --acl public-read

# Enable static website hosting in S3 bucket settings
```

### CDN vs Local Pyodide

**CDN (Recommended for production):**
- Small build size (~8MB)
- Fast global delivery
- Automatic updates
- Browser caching across sites

```toml
[build]
pyodide_source = "cdn"
pyodide_version = "0.29.3"
```

**Local (For offline or custom builds):**
- Large build size (~300MB)
- Works offline
- Specific Pyodide version
- No external dependencies

```toml
[build]
pyodide_source = "local"
```

### Performance Optimization

**First Load:**
- ~300-420MB Pyodide download (one-time, cached by browser)
- ~2-5 seconds initialization time

**Subsequent Loads:**
- Instant (served from cache)
- ~100ms app initialization

**Optimization Tips:**
1. Use CDN Pyodide for smaller builds
2. Minimize package dependencies
3. Lazy-load large components
4. Use browser caching headers
5. Compress assets (gzip/brotli)

---

## Browser Compatibility

Antioch works in any modern browser with WebAssembly support:

| Browser | Minimum Version |
|---------|----------------|
| Chrome  | 89+            |
| Firefox | 89+            |
| Safari  | 14.1+          |
| Edge    | 89+            |
| Opera   | 75+            |

**Note:** Internet Explorer is not supported (no WebAssembly).

---

## Frequently Asked Questions

### Can I use NumPy/Pandas/etc?

Yes! Use `antioch install <package>` to add packages:

```bash
antioch install numpy pandas matplotlib
```

Most pure-Python packages work. Packages with C extensions must be available in Pyodide's package index.

### Can I make API calls?

Yes! Use `fetch` or `requests`:

```python
import js

# Using JavaScript fetch
response = await js.fetch("https://api.example.com/data")
data = await response.json()

# Or use requests (if installed)
import requests
response = requests.get("https://api.example.com/data")
data = response.json()
```

### How do I persist data?

Use the virtual filesystem with LocalStorageBackend:

```python
from antioch.core import get_filesystem, LocalStorageBackend

fs = get_filesystem(LocalStorageBackend())
fs.create_file("data.json", '{"saved": true}')
# Data persists across page reloads
```

### Can I access the browser's DOM directly?

Yes, via Pyodide's `js` module:

```python
import js

# Access window object
js.window.alert("Hello!")

# Access document
js.document.title = "New Title"

# But Antioch's API is recommended for consistency
```

### How big are the builds?

- **CDN builds**: ~8MB (just your code + config)
- **Local builds**: ~300MB (includes Pyodide runtime)

The browser caches Pyodide, so users only download it once.

### Can I use async/await?

Yes! Pyodide fully supports async Python:

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "Data loaded"

async def main():
    data = await fetch_data()
    print(data)

asyncio.create_task(main())
```

### What about SEO?

Since Antioch apps run client-side JavaScript (WebAssembly), search engines may have difficulty indexing content. For SEO-critical sites, consider:

1. Server-side rendering (SSR) with pre-rendered static pages
2. Using Antioch for admin panels/dashboards (not public pages)
3. Providing meta tags and structured data in HTML

### Can I integrate with existing JavaScript?

Yes! See the "Wrapping JavaScript Libraries" section in Advanced Topics.

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Report bugs and request features via [GitHub Issues](https://github.com/ryanmccauley/antioch/issues).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Credits

**Antioch** is built with:
- [Pyodide](https://pyodide.org/) - Python for the browser (WebAssembly)
- [CPython](https://www.python.org/) - Python interpreter

**External library integrations:**
- [Chart.js](https://www.chartjs.org/) - Charts and graphs
- [Leaflet](https://leafletjs.com/) - Interactive maps
- [CodeMirror](https://codemirror.net/) - Code editing

---

## Support

- **Documentation**: This README + inline examples
- **Examples**: `scripts/examples/` directory (20+ demos)
- **Issues**: [GitHub Issues](https://github.com/ryanmccauley/antioch/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ryanmccauley/antioch/discussions)

---

**Start building Python web apps today - no JavaScript, no backend, just Python!**

```bash
antioch env
antioch build
antioch run
```