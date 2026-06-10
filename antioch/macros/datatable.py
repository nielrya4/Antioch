"""
DataTable macro - Interactive table component with inline editing.

Built with native Antioch elements for clean, warning-free operation.
Supports inline editing, row operations, and data export.
"""
import js
from .base import Macro
from ..elements import Div, Table, Th, Tr, Td, Input, Button, Span


class DataTable(Macro):
    """
    Native data table component with inline editing capabilities.

    Usage:
        table = DataTable(
            data=[
                {"name": "Alice", "age": 30, "city": "NYC"},
                {"name": "Bob", "age": 25, "city": "SF"}
            ],
            columns=[
                {"title": "Name", "field": "name"},
                {"title": "Age", "field": "age"},
                {"title": "City", "field": "city"}
            ],
            editable=True,
            height="400px"
        )
    """

    def __init__(self, data=None, columns=None, editable=True,
                 height="400px", show_row_numbers=True,
                 container_style=None, **kwargs):
        """
        Initialize DataTable.

        Args:
            data: List of dictionaries representing table rows
            columns: List of column definitions with 'title' and 'field' keys
            editable: Whether cells are editable (default: True)
            height: Table height (CSS string)
            show_row_numbers: Show row number column (default: True)
            container_style: Custom container styles
            **kwargs: Additional Macro arguments
        """
        # Initialize base class
        super().__init__(macro_type="datatable", **kwargs)

        # Process columns
        if columns is None:
            columns = []
        self._column_fields = [col.get('field', f'col_{i}') for i, col in enumerate(columns)]

        # Process data
        if data is None:
            data = []
        processed_data = self._process_data(data)

        # Set up state
        self._set_state(
            data=processed_data,
            columns=columns,
            editable=editable,
            height=height,
            show_row_numbers=show_row_numbers
        )

        # Default container style
        default_container_style = {
            "width": "100%",
            "max-width": "100%",
            "overflow": "auto",
            "border": "1px solid #ddd",
            "border-radius": "4px",
            "background-color": "white"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Create unified Events for decorator usage
        self._create_event('cell_change')
        self._create_event('row_add')
        self._create_event('row_delete')
        self._create_event('data_change')
        self._create_event('rowClick')

        # Initialize macro
        self._init_macro()

    def _process_data(self, data):
        """Convert data to list of lists format."""
        if not data:
            return []

        # Convert list of dicts to list of lists
        if isinstance(data[0], dict):
            return [[row.get(field, "") for field in self._column_fields] for row in data]

        # Already list of lists
        return [list(row) for row in data]

    def _create_elements(self):
        """Create the table UI elements."""
        # Container
        container = self._create_container(self._container_style)

        # Table wrapper with fixed height
        table_wrapper = Div(style={
            "height": self._get_state('height'),
            "overflow-y": "auto",
            "overflow-x": "auto"
        })

        # Table
        table = self._register_element('table', Table(style={
            "width": "100%",
            "border-collapse": "collapse",
            "font-family": "Arial, sans-serif",
            "font-size": "14px"
        }))

        # Create header
        self._create_header(table)

        # Create body
        self._create_body(table)

        table_wrapper.add(table)

        # Controls
        controls = self._create_controls()

        container.add(table_wrapper, controls)
        return container

    def _create_header(self, table):
        """Create table header."""
        columns = self._get_state('columns')
        show_row_numbers = self._get_state('show_row_numbers')

        header_row = Tr()

        # Row number column
        if show_row_numbers:
            header_row.add(Th("#", style={
                "background-color": "#f8f9fa",
                "border": "1px solid #ddd",
                "padding": "8px",
                "font-weight": "bold",
                "text-align": "center",
                "width": "50px",
                "position": "sticky",
                "top": "0",
                "z-index": "10"
            }))

        # Data columns
        for col in columns:
            th = Th(col.get('title', ''), style={
                "background-color": "#f8f9fa",
                "border": "1px solid #ddd",
                "padding": "8px",
                "font-weight": "bold",
                "text-align": "left",
                "min-width": "100px",
                "position": "sticky",
                "top": "0",
                "z-index": "10"
            })
            header_row.add(th)

        # Actions column
        header_row.add(Th("Actions", style={
            "background-color": "#f8f9fa",
            "border": "1px solid #ddd",
            "padding": "8px",
            "font-weight": "bold",
            "text-align": "center",
            "width": "80px",
            "position": "sticky",
            "top": "0",
            "z-index": "10"
        }))

        table.add(header_row)

    def _create_body(self, table):
        """Create table body with data rows."""
        data = self._get_state('data')
        show_row_numbers = self._get_state('show_row_numbers')
        editable = self._get_state('editable')

        for row_idx, row_data in enumerate(data):
            tr = Tr()
            tr.set_attribute("data-row-index", str(row_idx))

            # Add click handler for entire row
            tr.on_click(self._create_proxy(lambda e, idx=row_idx: self._handle_row_click(idx)))

            # Row number
            if show_row_numbers:
                tr.add(Td(str(row_idx + 1), style={
                    "border": "1px solid #ddd",
                    "padding": "8px",
                    "text-align": "center",
                    "background-color": "#f8f9fa",
                    "font-weight": "bold"
                }))

            # Data cells
            for col_idx, cell_value in enumerate(row_data):
                td = self._create_cell(row_idx, col_idx, cell_value, editable)
                tr.add(td)

            # Actions cell
            actions_td = Td(style={
                "border": "1px solid #ddd",
                "padding": "4px",
                "text-align": "center"
            })

            delete_btn = Button("×", style={
                "background-color": "#dc3545",
                "color": "white",
                "border": "none",
                "border-radius": "3px",
                "padding": "4px 8px",
                "cursor": "pointer",
                "font-size": "16px",
                "font-weight": "bold"
            })
            delete_btn.on_click(self._create_proxy(lambda e, idx=row_idx: self._delete_row_handler(e, idx)))
            actions_td.add(delete_btn)
            tr.add(actions_td)

            table.add(tr)

    def _create_cell(self, row_idx, col_idx, value, editable):
        """Create a table cell with optional editing."""
        td = Td(style={
            "border": "1px solid #ddd",
            "padding": "0",
            "position": "relative"
        })

        if editable:
            input_elem = Input("text", style={
                "width": "100%",
                "border": "none",
                "padding": "8px",
                "background": "transparent",
                "font-family": "inherit",
                "font-size": "inherit"
            })
            input_elem.value = str(value) if value is not None else ""
            input_elem.set_attribute("data-row", str(row_idx))
            input_elem.set_attribute("data-col", str(col_idx))

            # Handle cell changes with proxies
            input_elem.on_blur(self._create_proxy(self._handle_cell_change))
            input_elem.on_keydown(self._create_proxy(self._handle_cell_keypress))

            td.add(input_elem)
        else:
            td.add(Span(str(value) if value is not None else "", style={
                "padding": "8px",
                "display": "block"
            }))

        return td

    def _handle_row_click(self, row_idx):
        """Handle row click."""
        data = self._get_state('data')
        if row_idx < len(data):
            row_data = self._get_row_as_dict(row_idx)
            self._fire_event('rowClick', row_data)

    def _handle_cell_change(self, event):
        """Handle cell value change."""
        input_elem = event.target
        row_idx = int(input_elem.getAttribute("data-row"))
        col_idx = int(input_elem.getAttribute("data-col"))
        new_value = input_elem.value

        # Update data
        data = self._get_state('data')
        if row_idx < len(data) and col_idx < len(data[row_idx]):
            old_value = data[row_idx][col_idx]
            data[row_idx][col_idx] = new_value
            self._set_state(data=data)

            # Trigger callbacks
            self._fire_event('cell_change', self, row_idx, col_idx, new_value, old_value)
            self._fire_event('data_change', self, self.get_data())

    def _handle_cell_keypress(self, event):
        """Handle keypress in cell (Enter to confirm)."""
        if event.key == "Enter":
            event.target.blur()

    def _delete_row_handler(self, event, row_idx):
        """Handle delete button click."""
        # Stop propagation to prevent row click
        event.stopPropagation()
        self.delete_row(row_idx)

    def _create_controls(self):
        """Create table controls."""
        controls = Div(style={
            "padding": "10px",
            "border-top": "1px solid #ddd",
            "background-color": "#f8f9fa",
            "display": "flex",
            "gap": "10px",
            "align-items": "center"
        })

        add_row_btn = Button("Add Row", style={
            "background-color": "#007bff",
            "color": "white",
            "border": "none",
            "padding": "6px 12px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px"
        })
        add_row_btn.on_click(self._create_proxy(lambda e: self.add_row()))

        clear_btn = Button("Clear Data", style={
            "background-color": "#6c757d",
            "color": "white",
            "border": "none",
            "padding": "6px 12px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px"
        })
        clear_btn.on_click(self._create_proxy(lambda e: self.clear_data()))

        export_csv_btn = Button("Export CSV", style={
            "background-color": "#28a745",
            "color": "white",
            "border": "none",
            "padding": "6px 12px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px"
        })
        export_csv_btn.on_click(self._create_proxy(lambda e: self.download("csv", "data")))

        export_json_btn = Button("Export JSON", style={
            "background-color": "#17a2b8",
            "color": "white",
            "border": "none",
            "padding": "6px 12px",
            "border-radius": "4px",
            "cursor": "pointer",
            "font-size": "14px"
        })
        export_json_btn.on_click(self._create_proxy(lambda e: self.download("json", "data")))

        controls.add(add_row_btn, clear_btn, export_csv_btn, export_json_btn)
        return controls

    # ========== Public API Methods ==========

    def add_row(self, data=None, position="bottom"):
        """
        Add a new row to the table.

        Args:
            data: Row data dict or list (None for empty row)
            position: "top" or "bottom"

        Returns:
            Self for method chaining
        """
        current_data = self._get_state('data')

        if data is None:
            new_row = [""] * len(self._column_fields)
        elif isinstance(data, dict):
            new_row = [data.get(field, "") for field in self._column_fields]
        else:
            new_row = list(data)

        # Ensure correct length
        while len(new_row) < len(self._column_fields):
            new_row.append("")

        if position == "top":
            current_data.insert(0, new_row)
        else:
            current_data.append(new_row)

        self._set_state(data=current_data)
        self._rebuild_table()

        self._fire_event('row_add', self, new_row)
        self._trigger_callbacks('data_change', self, self.get_data())
        return self

    def delete_row(self, row_index):
        """
        Delete a row by index.

        Args:
            row_index: Index of row to delete

        Returns:
            Self for method chaining
        """
        current_data = self._get_state('data')
        if 0 <= row_index < len(current_data):
            deleted_row = current_data.pop(row_index)
            self._set_state(data=current_data)
            self._rebuild_table()

            self._fire_event('row_delete', self, row_index, deleted_row)
            self._fire_event('data_change', self, self.get_data())
        return self

    def set_data(self, data):
        """
        Set table data.

        Args:
            data: List of dictionaries or list of lists

        Returns:
            Self for method chaining
        """
        processed_data = self._process_data(data)
        self._set_state(data=processed_data)
        self._rebuild_table()

        self._trigger_callbacks('data_change', self, self.get_data())
        return self

    def get_data(self, format="dict"):
        """
        Get current table data.

        Args:
            format: "dict" or "list"

        Returns:
            List of data in specified format
        """
        data = self._get_state('data')

        if format == "dict":
            return [dict(zip(self._column_fields, row)) for row in data]
        else:
            return [list(row) for row in data]

    def clear_data(self):
        """Clear all table data."""
        self._set_state(data=[])
        self._rebuild_table()
        self._trigger_callbacks('data_change', self, self.get_data())
        return self

    def download(self, format="csv", filename="data"):
        """
        Download table data.

        Args:
            format: "csv" or "json"
            filename: Output filename (without extension)

        Returns:
            Self for method chaining
        """
        data = self.get_data(format="dict")

        if format == "csv":
            self._download_csv(data, filename)
        elif format == "json":
            self._download_json(data, filename)

        return self

    def _download_csv(self, data, filename):
        """Download data as CSV."""
        if not data:
            return

        # Create CSV content
        columns = self._get_state('columns')
        headers = [col.get('title', '') for col in columns]
        csv_lines = [','.join(f'"{h}"' for h in headers)]

        for row in data:
            values = [str(row.get(field, '')) for field in self._column_fields]
            csv_lines.append(','.join(f'"{v}"' for v in values))

        csv_content = '\n'.join(csv_lines)

        # Trigger download
        self._trigger_download(csv_content, f"{filename}.csv", "text/csv")

    def _download_json(self, data, filename):
        """Download data as JSON."""
        import json
        json_content = json.dumps(data, indent=2)
        self._trigger_download(json_content, f"{filename}.json", "application/json")

    def _trigger_download(self, content, filename, mime_type):
        """Trigger browser download."""
        blob = js.Blob.new([content], {"type": mime_type})
        url = js.URL.createObjectURL(blob)

        a = js.document.createElement("a")
        a.href = url
        a.download = filename
        js.document.body.appendChild(a)
        a.click()
        js.document.body.removeChild(a)
        js.URL.revokeObjectURL(url)

    def _rebuild_table(self):
        """Rebuild the entire table body."""
        table = self._get_element('table')

        # Remove all rows except header (first row)
        while table._dom_element.children.length > 1:
            table._dom_element.removeChild(table._dom_element.children[1])

        # Recreate body
        self._create_body(table)

    def _get_row_as_dict(self, row_idx):
        """Get row data as dictionary."""
        data = self._get_state('data')
        if row_idx < len(data):
            return dict(zip(self._column_fields, data[row_idx]))
        return {}

    # ========== Callback Helpers ==========

    def on_row_click(self, callback):
        """Register callback for row clicks."""
        return self.on('rowClick', callback)

    def on_cell_change(self, callback):
        """Register callback for cell changes."""
        return self.on('cell_change', callback)

    def on_row_add(self, callback):
        """Register callback for row additions."""
        return self.on('row_add', callback)

    def on_row_delete(self, callback):
        """Register callback for row deletions."""
        return self.on('row_delete', callback)

    def on_data_change(self, callback):
        """Register callback for any data changes."""
        return self.on('data_change', callback)

    # ========== Convenience Properties ==========

    @property
    def is_ready(self):
        """Check if table is ready (always true for native table)."""
        return True


# For backward compatibility
Column = dict
ColumnType = None

__all__ = ['DataTable', 'Column', 'ColumnType']
