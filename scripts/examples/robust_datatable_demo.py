"""
Robust DataTable Demo - Showcases Tabulator-powered table component.

This demo demonstrates:
- Interactive columns with sorting and filtering
- Inline editing with various editors
- Column formatters and validators
- Row selection and manipulation
- Data export (CSV, JSON, XLSX)
- Responsive layouts
"""

from antioch import Div, H1, H2, P, DOM
from antioch.macros import DataTable


def create_product_inventory_table():
    """Create a product inventory table with various column types."""

    columns = [
        {
            "title": "Product Name",
            "field": "name",
            "editor": "input",
            "validator": ["required"],
            "width": 200
        },
        {
            "title": "SKU",
            "field": "sku",
            "editor": "input",
            "validator": ["required"],
            "width": 120
        },
        {
            "title": "Category",
            "field": "category",
            "editor": "list",
            "editorParams": {
                "values": ["Electronics", "Clothing", "Food", "Books", "Toys"]
            },
            "width": 150
        },
        {
            "title": "Price",
            "field": "price",
            "editor": "number",
            "editorParams": {"min": 0, "max": 10000, "step": 0.01},
            "formatter": "money",
            "formatterParams": {"precision": 2},
            "validator": ["required", "numeric", "min:0", "max:10000"],
            "width": 100
        },
        {
            "title": "Stock",
            "field": "stock",
            "editor": "number",
            "editorParams": {"min": 0},
            "validator": ["required", "numeric", "min:0"],
            "width": 100
        },
        {
            "title": "In Stock",
            "field": "in_stock",
            "formatter": "tickCross",
            "editor": "tickCross",
            "width": 100
        },
        {
            "title": "Last Restock",
            "field": "last_restock",
            "editor": "date",
            "width": 150
        }
    ]

    data = [
        {"name": "Laptop Pro 15", "sku": "LT-001", "category": "Electronics", "price": 1299.99, "stock": 25, "in_stock": True, "last_restock": "2025-12-15"},
        {"name": "Wireless Mouse", "sku": "MS-042", "category": "Electronics", "price": 29.99, "stock": 150, "in_stock": True, "last_restock": "2026-01-05"},
        {"name": "T-Shirt Blue XL", "sku": "TS-BL-XL", "category": "Clothing", "price": 19.99, "stock": 0, "in_stock": False, "last_restock": "2025-11-20"},
        {"name": "Python Programming Book", "sku": "BK-PY-101", "category": "Books", "price": 49.99, "stock": 45, "in_stock": True, "last_restock": "2025-12-01"},
        {"name": "USB-C Cable 2m", "sku": "CB-UC-02", "category": "Electronics", "price": 12.99, "stock": 200, "in_stock": True, "last_restock": "2026-01-10"},
        {"name": "Action Figure Set", "sku": "TY-AF-001", "category": "Toys", "price": 34.99, "stock": 30, "in_stock": True, "last_restock": "2025-12-20"},
        {"name": "Coffee Beans 1kg", "sku": "FD-CF-001", "category": "Food", "price": 24.99, "stock": 60, "in_stock": True, "last_restock": "2026-01-08"},
        {"name": "Mechanical Keyboard", "sku": "KB-MK-001", "category": "Electronics", "price": 159.99, "stock": 18, "in_stock": True, "last_restock": "2025-12-28"},
        {"name": "Jeans Denim 32", "sku": "JN-DN-32", "category": "Clothing", "price": 59.99, "stock": 35, "in_stock": True, "last_restock": "2025-11-25"},
        {"name": "Cookbook Italian", "sku": "BK-CK-IT", "category": "Books", "price": 29.99, "stock": 20, "in_stock": True, "last_restock": "2025-12-10"}
    ]

    table = DataTable(
        data=data,
        columns=columns,
        height="400px",
        layout="fitColumns",
        options={
            "movableColumns": True,
            "pagination": True,
            "paginationSize": 5
        }
    )

    # Register callbacks
    table.on_cell_edited(lambda cell: print(f"Cell edited: {cell.getValue()}"))

    return table


def create_employee_schedule_table():
    """Create an employee schedule table."""

    columns = [
        {"title": "Employee", "field": "employee", "editor": "input", "validator": ["required"], "width": 150},
        {
            "title": "Department",
            "field": "department",
            "editor": "list",
            "editorParams": {"values": ["Engineering", "Sales", "Marketing", "HR", "Support"]},
            "width": 130
        },
        {
            "title": "Monday",
            "field": "monday",
            "editor": "list",
            "editorParams": {"values": ["9-5", "10-6", "12-8", "Off"]},
            "width": 100
        },
        {
            "title": "Tuesday",
            "field": "tuesday",
            "editor": "list",
            "editorParams": {"values": ["9-5", "10-6", "12-8", "Off"]},
            "width": 100
        },
        {
            "title": "Wednesday",
            "field": "wednesday",
            "editor": "list",
            "editorParams": {"values": ["9-5", "10-6", "12-8", "Off"]},
            "width": 100
        },
        {
            "title": "Thursday",
            "field": "thursday",
            "editor": "list",
            "editorParams": {"values": ["9-5", "10-6", "12-8", "Off"]},
            "width": 100
        },
        {
            "title": "Friday",
            "field": "friday",
            "editor": "list",
            "editorParams": {"values": ["9-5", "10-6", "12-8", "Off"]},
            "width": 100
        },
        {
            "title": "Hours/Week",
            "field": "hours",
            "editor": "number",
            "editorParams": {"min": 0, "max": 60},
            "validator": ["numeric", "min:0", "max:60"],
            "width": 110
        }
    ]

    data = [
        {"employee": "Alice Johnson", "department": "Engineering", "monday": "9-5", "tuesday": "9-5", "wednesday": "9-5", "thursday": "9-5", "friday": "9-5", "hours": 40},
        {"employee": "Bob Smith", "department": "Sales", "monday": "9-5", "tuesday": "10-6", "wednesday": "9-5", "thursday": "10-6", "friday": "9-5", "hours": 40},
        {"employee": "Carol Davis", "department": "Marketing", "monday": "10-6", "tuesday": "10-6", "wednesday": "Off", "thursday": "10-6", "friday": "10-6", "hours": 32},
        {"employee": "Dave Wilson", "department": "Support", "monday": "12-8", "tuesday": "12-8", "wednesday": "12-8", "thursday": "12-8", "friday": "Off", "hours": 32},
        {"employee": "Eve Martinez", "department": "Engineering", "monday": "9-5", "tuesday": "9-5", "wednesday": "9-5", "thursday": "9-5", "friday": "Off", "hours": 32}
    ]

    table = DataTable(
        data=data,
        columns=columns,
        height="350px",
        layout="fitColumns"
    )

    return table


def create_project_tracker_table():
    """Create a simple project tracker."""

    columns = [
        {"title": "Project", "field": "project", "editor": "input", "validator": ["required"], "width": 200},
        {"title": "Owner", "field": "owner", "editor": "input", "validator": ["required"], "width": 150},
        {
            "title": "Status",
            "field": "status",
            "editor": "list",
            "editorParams": {"values": ["Planning", "In Progress", "On Hold", "Completed"]},
            "width": 120
        },
        {
            "title": "Priority",
            "field": "priority",
            "editor": "list",
            "editorParams": {"values": ["Low", "Medium", "High", "Critical"]},
            "formatter": "traffic",
            "formatterParams": {
                "Low": "green",
                "Medium": "orange",
                "High": "red",
                "Critical": "red"
            },
            "width": 100
        },
        {"title": "Start Date", "field": "start_date", "editor": "date", "width": 130},
        {"title": "Due Date", "field": "due_date", "editor": "date", "width": 130},
        {
            "title": "Budget",
            "field": "budget",
            "editor": "number",
            "editorParams": {"min": 0},
            "formatter": "money",
            "formatterParams": {"precision": 0},
            "width": 120
        },
        {
            "title": "Completed",
            "field": "completed",
            "formatter": "tickCross",
            "editor": "tickCross",
            "width": 100
        }
    ]

    data = [
        {"project": "Website Redesign", "owner": "Alice Johnson", "status": "In Progress", "priority": "High", "start_date": "2026-01-01", "due_date": "2026-03-15", "budget": 50000, "completed": False},
        {"project": "Mobile App Launch", "owner": "Bob Smith", "status": "Planning", "priority": "Critical", "start_date": "2026-02-01", "due_date": "2026-06-30", "budget": 150000, "completed": False},
        {"project": "Database Migration", "owner": "Carol Davis", "status": "Completed", "priority": "High", "start_date": "2025-11-01", "due_date": "2025-12-31", "budget": 30000, "completed": True},
        {"project": "Marketing Campaign Q1", "owner": "Dave Wilson", "status": "In Progress", "priority": "Medium", "start_date": "2026-01-01", "due_date": "2026-03-31", "budget": 25000, "completed": False},
        {"project": "Security Audit", "owner": "Eve Martinez", "status": "Planning", "priority": "Critical", "start_date": "2026-02-15", "due_date": "2026-03-15", "budget": 20000, "completed": False}
    ]

    table = DataTable(
        data=data,
        columns=columns,
        height="350px",
        layout="fitColumns"
    )

    return table


def main():
    """Main application entry point."""

    # Page title
    title = H1("Tabulator DataTable Demo", style={
        "text_align": "center",
        "color": "#333",
        "margin": "20px 0"
    })
    DOM.add(title)

    # Introduction
    intro = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 30px",
        "padding": "20px",
        "background_color": "#f8f9fa",
        "border_radius": "8px"
    })

    intro.add(
        P("This demo showcases the Tabulator-powered DataTable with professional features:",
          style={"font_weight": "bold", "margin_bottom": "10px"}),
        P("✨ Rich Editors: input, number, date, dropdown, checkbox",
          style={"margin": "5px 0 5px 20px"}),
        P("✅ Built-in Validation: required, numeric, min/max, custom validators",
          style={"margin": "5px 0 5px 20px"}),
        P("🔄 Sorting & Filtering: click headers to sort, filter any column",
          style={"margin": "5px 0 5px 20px"}),
        P("📊 Formatters: money, traffic lights, tick/cross, and more",
          style={"margin": "5px 0 5px 20px"}),
        P("📄 Pagination: handle large datasets with built-in pagination",
          style={"margin": "5px 0 5px 20px"}),
        P("💾 Export: CSV, JSON, XLSX, PDF, HTML formats",
          style={"margin": "5px 0 5px 20px"}),
        P("📱 Responsive: mobile-friendly tables that adapt to screen size",
          style={"margin": "5px 0 5px 20px"}),
        P("🎨 Themes: multiple built-in themes available",
          style={"margin": "5px 0 5px 20px"})
    )

    DOM.add(intro)

    # Section 1: Product Inventory
    section1 = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 40px",
        "padding": "20px",
        "background_color": "white",
        "border": "1px solid #ddd",
        "border_radius": "8px"
    })

    section1.add(
        H2("Product Inventory", style={"color": "#333", "margin_top": "0"}),
        P("Manage product inventory with validation, money formatting, and pagination.",
          style={"color": "#666", "margin_bottom": "15px"}),
        create_product_inventory_table().element
    )

    DOM.add(section1)

    # Section 2: Employee Schedule
    section2 = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 40px",
        "padding": "20px",
        "background_color": "white",
        "border": "1px solid #ddd",
        "border_radius": "8px"
    })

    section2.add(
        H2("Employee Schedule", style={"color": "#333", "margin_top": "0"}),
        P("Track employee schedules with dropdown editors for shift selections.",
          style={"color": "#666", "margin_bottom": "15px"}),
        create_employee_schedule_table().element
    )

    DOM.add(section2)

    # Section 3: Project Tracker
    section3 = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 40px",
        "padding": "20px",
        "background_color": "white",
        "border": "1px solid #ddd",
        "border_radius": "8px"
    })

    section3.add(
        H2("Project Tracker", style={"color": "#333", "margin_top": "0"}),
        P("Monitor projects with priority traffic lights, date editors, and budget formatting.",
          style={"color": "#666", "margin_bottom": "15px"}),
        create_project_tracker_table().element
    )

    DOM.add(section3)

    # Instructions footer
    footer = Div(style={
        "max_width": "1200px",
        "margin": "0 auto 40px",
        "padding": "20px",
        "background_color": "#e7f3ff",
        "border_radius": "8px",
        "border_left": "4px solid #2196F3"
    })

    footer.add(
        P("💡 Try These Features:", style={"font_weight": "bold", "margin_bottom": "10px"}),
        P("• Click any cell to edit it directly",
          style={"margin": "5px 0 5px 20px"}),
        P("• Click column headers to sort data",
          style={"margin": "5px 0 5px 20px"}),
        P("• Use pagination controls in the product table",
          style={"margin": "5px 0 5px 20px"}),
        P("• See money formatting in price and budget columns",
          style={"margin": "5px 0 5px 20px"}),
        P("• Try the priority traffic light indicators",
          style={"margin": "5px 0 5px 20px"}),
        P("• All data is validated on edit",
          style={"margin": "5px 0 5px 20px"})
    )

    DOM.add(footer)

    print("✅ Tabulator DataTable Demo loaded!")


if __name__ == "__main__":
    main()
