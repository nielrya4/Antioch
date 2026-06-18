"""
Interactive Components Demo

Showcases three production-ready interactive components:
- ChartJS (Chart.js wrapper using JSLibraryMacro)
- CodeBlock (CodeMirror wrapper using JSLibraryMacro)
- DataTable (Native implementation using pure Antioch elements)

Demonstrates both the JSLibraryMacro pattern for wrapping JavaScript libraries
and native component development using Antioch's built-in elements.
"""
from antioch import *
from antioch.macros import ChartJS, CodeBlock, DataTable


def main():
    DOM.add(
        H1("Interactive Components Showcase"),
        P("Demonstrating three production-ready components: ChartJS and CodeBlock (JSLibraryMacro wrappers) and DataTable (native Antioch implementation)."),
        Hr()
    )

    # ========== Demo 1: ChartJS ==========
    DOM.add(
        H2("1. ChartJS - Interactive Charts"),
        P("Chart.js wrapper with automatic dependency loading and state management.")
    )

    # Create chart configuration
    chart_config = {
        'type': 'bar',
        'data': {
            'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            'datasets': [{
                'label': 'Color Votes',
                'data': [12, 19, 3, 5, 2, 3],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                'borderWidth': 2
            }]
        },
        'options': {
            'responsive': True,
            'plugins': {
                'title': {
                    'display': True,
                    'text': 'Favorite Colors Survey',
                    'font': {'size': 16}
                },
                'legend': {
                    'display': True,
                    'position': 'top'
                }
            },
            'scales': {
                'y': {
                    'beginAtZero': True
                }
            }
        }
    }

    chart = ChartJS(config=chart_config, width=700, height=400)
    DOM.add(chart.element)

    # Add interactive controls
    def randomize_data(e):
        import random
        new_data = {
            'labels': chart_config['data']['labels'],
            'datasets': [{
                **chart_config['data']['datasets'][0],
                'data': [random.randint(1, 25) for _ in range(6)]
            }]
        }
        chart.update_data(new_data)

    def change_to_line(e):
        chart.set_type('line')

    def change_to_bar(e):
        chart.set_type('bar')

    controls = Div(style={"margin-top": "15px"})
    controls.add(
        Button("Randomize Data", style=button_style()).on_click(randomize_data),
        Button("Line Chart", style=button_style(margin_left="10px")).on_click(change_to_line),
        Button("Bar Chart", style=button_style(margin_left="10px")).on_click(change_to_bar)
    )
    DOM.add(controls)

    DOM.add(Hr(style={"margin": "30px 0"}))

    # ========== Demo 2: CodeBlock ==========
    DOM.add(
        H2("2. CodeBlock - Syntax Highlighted Editor"),
        P("CodeMirror wrapper with syntax highlighting, themes, and optional editing.")
    )

    # Example Python code
    python_code = """def fibonacci(n):
    \"\"\"Calculate the nth Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Generate first 10 Fibonacci numbers
fibs = [fibonacci(i) for i in range(10)]
print(f"First 10 Fibonacci numbers: {fibs}")
"""

    code_editor = CodeBlock(
        content=python_code,
        language="python",
        editable=True,
        theme="monokai",
        line_numbers=True,
        height="300px"
    )
    DOM.add(code_editor.element)

    # Theme switcher
    theme_controls = Div(style={"margin-top": "15px"})

    def set_theme_monokai(e):
        code_editor.set_theme("monokai")

    def set_theme_dracula(e):
        code_editor.set_theme("dracula")

    def set_theme_default(e):
        code_editor.set_theme("default")

    def switch_to_javascript(e):
        js_code = """// Async function example
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
}"""
        code_editor.set_value(js_code)
        code_editor.set_language("javascript")

    theme_controls.add(
        Button("Monokai Theme", style=button_style()).on_click(set_theme_monokai),
        Button("Dracula Theme", style=button_style(margin_left="10px")).on_click(set_theme_dracula),
        Button("Default Theme", style=button_style(margin_left="10px")).on_click(set_theme_default),
        Button("Switch to JavaScript", style=button_style(margin_left="20px")).on_click(switch_to_javascript)
    )
    DOM.add(theme_controls)

    # Show changes
    change_display = P(
        "Edit the code above to see real-time updates.",
        style={
            "margin-top": "10px",
            "padding": "10px",
            "background-color": "#f0f0f0",
            "border-radius": "4px",
            "font-family": "monospace"
        }
    )
    DOM.add(change_display)

    def on_code_change(macro, new_code):
        line_count = len(new_code.split('\n'))
        char_count = len(new_code)
        change_display.set_text(f"Lines: {line_count} | Characters: {char_count}")

    code_editor.on_change(on_code_change)

    DOM.add(Hr(style={"margin": "30px 0"}))

    # ========== Demo 3: DataTable ==========
    DOM.add(
        H2("3. DataTable - Interactive Data Grid"),
        P("Native Antioch component built with pure Python. Features inline editing, row operations, and CSV/JSON export with built-in controls.")
    )

    # Sample data
    table_data = [
        {"id": 1, "name": "Alice Johnson", "age": 28, "city": "New York", "salary": 75000},
        {"id": 2, "name": "Bob Smith", "age": 34, "city": "San Francisco", "salary": 92000},
        {"id": 3, "name": "Carol White", "age": 25, "city": "Chicago", "salary": 68000},
        {"id": 4, "name": "David Brown", "age": 42, "city": "Boston", "salary": 85000},
        {"id": 5, "name": "Eve Davis", "age": 31, "city": "Seattle", "salary": 79000},
        {"id": 6, "name": "Frank Miller", "age": 29, "city": "Austin", "salary": 71000},
        {"id": 7, "name": "Grace Lee", "age": 37, "city": "Denver", "salary": 88000},
    ]

    # Column definitions
    columns = [
        {"title": "ID", "field": "id", "width": 80},
        {"title": "Name", "field": "name", "editor": "input"},
        {"title": "Age", "field": "age", "editor": "number"},
        {"title": "City", "field": "city", "editor": "input"},
        {"title": "Salary", "field": "salary", "editor": "number", "formatter": "money"}
    ]

    data_table = DataTable(
        data=table_data,
        columns=columns,
        height="350px",
        editable=True
    )
    DOM.add(data_table.element)

    # Status display for row clicks
    table_status = P(
        f"Table loaded with {len(table_data)} rows. Click cells to edit, click rows to select. Use built-in controls below the table to add/delete rows or export data.",
        style={
            "margin-top": "10px",
            "padding": "10px",
            "background-color": "#e8f4f8",
            "border-radius": "4px",
            "border-left": "4px solid #2196F3"
        }
    )
    DOM.add(table_status)

    # Row click handler
    def on_row_click(macro, row_data):
        if row_data:
            table_status.set_text(
                f"Selected: {row_data['name']} | Age: {row_data['age']} | Salary: ${row_data['salary']:,}"
            )

    data_table.on_row_click(on_row_click)

    DOM.add(Hr(style={"margin": "30px 0"}))

    # ========== Summary ==========
    DOM.add(
        H2("Component Architecture"),
        P("This demo showcases two different approaches to building interactive components:"),

        H3("JSLibraryMacro-Based Components"),
        P(Strong("ChartJS"), " and ", Strong("CodeBlock"), " use the JSLibraryMacro pattern to wrap existing JavaScript libraries:"),
        Ul(
            Li(Strong("Automatic dependency loading"), " - Scripts and stylesheets loaded on-demand"),
            Li(Strong("Initialization lifecycle"), " - Retry logic and ready callbacks built-in"),
            Li(Strong("Proxy management"), " - Automatic creation and cleanup prevents GC issues"),
            Li(Strong("State management"), " - Consistent patterns for managing component state"),
            Li(Strong("Python ↔ JS conversion"), " - Easy data exchange with ", Code("_to_js()"), " helper"),
            Li(Strong("Cleanup"), " - Proper resource cleanup on ", Code("destroy()"))
        ),

        H3("Native Antioch Components"),
        P(Strong("DataTable"), " is built entirely with native Antioch elements (Table, Tr, Td, Input, Button):"),
        Ul(
            Li(Strong("No external dependencies"), " - Fully self-contained with no JS library requirements"),
            Li(Strong("Direct event handling"), " - Python event handlers directly on DOM elements"),
            Li(Strong("Built-in controls"), " - Add/delete rows, CSV/JSON export included"),
            Li(Strong("Inline editing"), " - Editable cells with real-time data updates"),
            Li(Strong("Full customization"), " - Complete control over styling and behavior")
        ),

        P(
            "See ",
            Code("antioch/macros/js_library.py"),
            " for the JSLibraryMacro base class and ",
            Code("antioch/macros/datatable.py"),
            " for an example of a native implementation."
        )
    )


def button_style(margin_left="0px"):
    """Helper for consistent button styling."""
    return {
        "padding": "8px 16px",
        "background-color": "#007bff",
        "color": "white",
        "border": "none",
        "border-radius": "4px",
        "cursor": "pointer",
        "margin-left": margin_left,
        "font-size": "14px"
    }


if __name__ == "__main__":
    main()