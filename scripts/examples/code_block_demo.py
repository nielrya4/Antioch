#!/usr/bin/env python3
"""
CodeBlock Macro Demo

Demonstrates the syntax-highlighted code viewer/editor component.
Shows various languages, themes, and editable/readonly modes.
"""

from antioch import DOM, Div, H1, H2, H3, P, Button, Hr
from antioch.macros import CodeBlock, Tabs, Tab
import js

# Sample code for different languages
PYTHON_CODE = '''def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result

# Example usage
fib_sequence = fibonacci(10)
print(f"First 10 Fibonacci numbers: {fib_sequence}")
'''

JAVASCRIPT_CODE = '''// Async/await example with error handling
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        return null;
    }
}

// Usage
fetchUserData(123).then(user => console.log(user));
'''

HTML_CODE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antioch Demo</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to Antioch!</h1>
        <p>Build web apps in Python.</p>
    </div>
    <script src="app.js"></script>
</body>
</html>
'''

CSS_CODE = '''/* Modern CSS with Grid and Flexbox */
.card {
    display: flex;
    flex-direction: column;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
    .card { padding: 16px; }
}
'''

JSON_CODE = '''{
  "name": "antioch",
  "version": "1.0.0",
  "description": "Build web apps in Python",
  "features": [
    "Pure Python",
    "DOM manipulation",
    "Rich components",
    "Virtual filesystem"
  ],
  "dependencies": {
    "pyodide": ">=0.24.0"
  },
  "license": "MIT"
}
'''


def main():
    """Main demo function."""
    # Create main container
    container = Div()
    container.style.padding = "20px"
    container.style.max_width = "1200px"
    container.style.margin = "0 auto"
    container.style.font_family = "Arial, sans-serif"

    # Title
    title = H1("CodeBlock Macro Demo")
    title.style.color = "#333"
    title.style.margin_bottom = "10px"

    desc = P(
        "Syntax-highlighted code viewer and editor powered by CodeMirror. "
        "Supports 20+ languages, multiple themes, and read-only or editable modes."
    )
    desc.style.color = "#666"
    desc.style.margin_bottom = "30px"

    container.add(title, desc)

    # Section 1: Basic readonly code blocks
    section1 = create_readonly_section()
    container.add(section1, Hr())

    # Section 2: Editable code blocks with themes
    section2 = create_editable_section()
    container.add(section2, Hr())

    # Section 3: Interactive demo
    section3 = create_interactive_section()
    container.add(section3)

    # Add to DOM
    DOM.add(container)


def create_readonly_section():
    """Create section showing readonly code blocks."""
    section = Div()
    section.style.margin_bottom = "40px"

    heading = H2("Read-Only Code Viewers")
    heading.style.color = "#333"
    heading.style.margin_bottom = "20px"
    section.add(heading)

    # Create tabs for different languages
    tabs = Tabs()

    # Python tab
    python_code = CodeBlock(
        content=PYTHON_CODE,
        language="python",
        editable=False,
        line_numbers=True,
        height="300px",
        lazy_init=True  # Initialize when tab becomes active
    )
    tabs.add_tab(Tab("Python", python_code))

    # JavaScript tab
    js_code = CodeBlock(
        content=JAVASCRIPT_CODE,
        language="javascript",
        editable=False,
        line_numbers=True,
        height="300px",
        lazy_init=True
    )
    tabs.add_tab(Tab("JavaScript", js_code))

    # HTML tab
    html_code = CodeBlock(
        content=HTML_CODE,
        language="html",
        editable=False,
        line_numbers=True,
        height="300px",
        lazy_init=True
    )
    tabs.add_tab(Tab("HTML", html_code))

    # CSS tab
    css_code = CodeBlock(
        content=CSS_CODE,
        language="css",
        editable=False,
        line_numbers=True,
        height="300px",
        lazy_init=True
    )
    tabs.add_tab(Tab("CSS", css_code))

    # JSON tab
    json_code = CodeBlock(
        content=JSON_CODE,
        language="json",
        editable=False,
        line_numbers=True,
        height="300px",
        lazy_init=True
    )
    tabs.add_tab(Tab("JSON", json_code))

    section.add(tabs.element)
    return section


def create_editable_section():
    """Create section showing editable code blocks with themes."""
    section = Div()
    section.style.margin_bottom = "40px"

    heading = H2("Editable Code Editors with Themes")
    heading.style.color = "#333"
    heading.style.margin_bottom = "20px"
    section.add(heading)

    desc = P(
        "Try editing the code below. The editors use different CodeMirror themes "
        "and support live editing with change detection."
    )
    desc.style.color = "#666"
    desc.style.margin_bottom = "20px"
    section.add(desc)

    # Create grid for themes
    grid = Div()
    grid.style.display = "grid"
    grid.style.grid_template_columns = "repeat(auto-fit, minmax(500px, 1fr))"
    grid.style.gap = "20px"

    # Default theme
    default_container = Div()
    default_title = H3("Default Theme")
    default_title.style.margin = "0 0 10px 0"
    default_title.style.color = "#555"
    default_editor = CodeBlock(
        content=PYTHON_CODE,
        language="python",
        editable=True,
        theme="default",
        height="250px"
    )
    default_editor.on_change(lambda editor, content: print(f"Default editor changed: {len(content)} chars"))
    default_container.add(default_title, default_editor.element)
    grid.add(default_container)

    # Monokai theme
    monokai_container = Div()
    monokai_title = H3("Monokai Theme")
    monokai_title.style.margin = "0 0 10px 0"
    monokai_title.style.color = "#555"
    monokai_editor = CodeBlock(
        content=JAVASCRIPT_CODE,
        language="javascript",
        editable=True,
        theme="monokai",
        height="250px"
    )
    monokai_editor.on_change(lambda editor, content: print(f"Monokai editor changed: {len(content)} chars"))
    monokai_container.add(monokai_title, monokai_editor.element)
    grid.add(monokai_container)

    # Dracula theme
    dracula_container = Div()
    dracula_title = H3("Dracula Theme")
    dracula_title.style.margin = "0 0 10px 0"
    dracula_title.style.color = "#555"
    dracula_editor = CodeBlock(
        content=CSS_CODE,
        language="css",
        editable=True,
        theme="dracula",
        height="250px"
    )
    dracula_editor.on_change(lambda editor, content: print(f"Dracula editor changed: {len(content)} chars"))
    dracula_container.add(dracula_title, dracula_editor.element)
    grid.add(dracula_container)

    # Material theme
    material_container = Div()
    material_title = H3("Material Theme")
    material_title.style.margin = "0 0 10px 0"
    material_title.style.color = "#555"
    material_editor = CodeBlock(
        content=HTML_CODE,
        language="html",
        editable=True,
        theme="material",
        height="250px"
    )
    material_editor.on_change(lambda editor, content: print(f"Material editor changed: {len(content)} chars"))
    material_container.add(material_title, material_editor.element)
    grid.add(material_container)

    section.add(grid)
    return section


def create_interactive_section():
    """Create interactive demo with controls."""
    section = Div()
    section.style.margin_bottom = "40px"

    heading = H2("Interactive Demo")
    heading.style.color = "#333"
    heading.style.margin_bottom = "20px"
    section.add(heading)

    desc = P(
        "Try the controls below to dynamically change the editor properties."
    )
    desc.style.color = "#666"
    desc.style.margin_bottom = "20px"
    section.add(desc)

    # Create editor
    editor = CodeBlock(
        content=PYTHON_CODE,
        language="python",
        editable=True,
        theme="default",
        height="350px"
    )

    # Control buttons
    controls = Div()
    controls.style.margin_bottom = "15px"
    controls.style.display = "flex"
    controls.style.gap = "10px"
    controls.style.flex_wrap = "wrap"

    # Toggle editable
    toggle_edit_btn = create_button("Toggle Editable")
    toggle_edit_btn.on_click(lambda e: toggle_editable(editor))
    controls.add(toggle_edit_btn)

    # Change language buttons
    lang_python_btn = create_button("Python")
    lang_python_btn.on_click(lambda e: editor.set_language("python"))
    controls.add(lang_python_btn)

    lang_js_btn = create_button("JavaScript")
    lang_js_btn.on_click(lambda e: editor.set_language("javascript"))
    controls.add(lang_js_btn)

    lang_html_btn = create_button("HTML")
    lang_html_btn.on_click(lambda e: editor.set_language("html"))
    controls.add(lang_html_btn)

    # Theme buttons
    theme_default_btn = create_button("Default Theme")
    theme_default_btn.on_click(lambda e: editor.set_theme("default"))
    controls.add(theme_default_btn)

    theme_monokai_btn = create_button("Monokai Theme")
    theme_monokai_btn.on_click(lambda e: editor.set_theme("monokai"))
    controls.add(theme_monokai_btn)

    theme_dracula_btn = create_button("Dracula Theme")
    theme_dracula_btn.on_click(lambda e: editor.set_theme("dracula"))
    controls.add(theme_dracula_btn)

    # Get content button
    get_content_btn = create_button("Get Content", "#4CAF50")
    get_content_btn.on_click(lambda e: show_content(editor))
    controls.add(get_content_btn)

    section.add(controls, editor.element)

    # Output area
    output = Div()
    output.set_attribute("id", "output_area")
    output.style.margin_top = "15px"
    output.style.padding = "15px"
    output.style.background_color = "#f5f5f5"
    output.style.border_radius = "4px"
    output.style.min_height = "50px"
    output.style.font_family = "monospace"
    output.style.white_space = "pre_wrap"
    section.add(output)

    return section


def create_button(text, bg_color="#2196F3"):
    """Helper to create styled button."""
    btn = Button(text)
    btn.style.padding = "8px 16px"
    btn.style.background_color = bg_color
    btn.style.color = "white"
    btn.style.border = "none"
    btn.style.border_radius = "4px"
    btn.style.cursor = "pointer"
    btn.style.font_size = "14px"
    return btn


def toggle_editable(editor):
    """Toggle editor editable state."""
    current = editor._get_state('editable')
    editor.set_editable(not current)
    print(f"Editor is now {'editable' if not current else 'read-only'}")


def show_content(editor):
    """Display current editor content."""
    import js
    content = editor.get_content()
    output = js.document.getElementById("output_area")
    if output:
        output.textContent = f"Current content ({len(content)} characters):\n\n{content[:500]}..."


if __name__ == "__main__":
    main()