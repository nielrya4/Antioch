"""
DataTable macro - Interactive table component powered by Tabulator.

Provides powerful spreadsheet-like tables with:
- Sorting, filtering, and pagination
- Inline editing
- Row selection
- Column formatting
- Data export (CSV, JSON, etc.)
- And much more from Tabulator

Documentation: https://tabulator.info/docs/6.2
"""
import js
from pyodide.ffi import create_proxy, to_js
from .base import Macro
from ..elements import Div
from ..lib.loader import inject_script, inject_stylesheet

# Ensure Tabulator is loaded when this module is imported
inject_stylesheet('antioch/lib/vendor/tabulator.min.css')
inject_script('antioch/lib/vendor/tabulator.min.js')


class DataTable(Macro):
    """
    DataTable macro powered by Tabulator.

    Usage:
        table = DataTable(
            data=[
                {"name": "Alice", "age": 30, "city": "NYC"},
                {"name": "Bob", "age": 25, "city": "SF"}
            ],
            columns=[
                {"title": "Name", "field": "name", "editor": "input"},
                {"title": "Age", "field": "age", "editor": "number"},
                {"title": "City", "field": "city"}
            ],
            height="400px",
            layout="fitColumns"
        )

        # Access native Tabulator for advanced features
        table.tabulator.setData(new_data)
    """

    def __init__(self, data=None, columns=None, options=None,
                 height="400px", layout="fitData", container_style=None, **kwargs):
        """
        Initialize DataTable with Tabulator.

        Args:
            data: List of dictionaries representing table rows
            columns: List of column definitions (Tabulator format)
                    See: https://tabulator.info/docs/6.2/columns
            options: Additional Tabulator options dict
            height: Table height (CSS string or pixels)
            layout: Column layout mode ("fitData", "fitColumns", "fitDataFill", etc.)
            container_style: Custom container styles
            **kwargs: Additional Macro base class arguments
        """
        super().__init__(macro_type="datatable", **kwargs)

        # Set up state
        self._set_state(
            data=data or [],
            columns=columns or [],
            options=options or {},
            height=height,
            layout=layout,
            table_instance=None,
            initialized=False,
            init_retry_count=0
        )

        # Default container style
        default_container_style = {
            "width": "100%",
            "max_width": "100%",
            "position": "relative",
            "overflow": "auto"
        }

        self._container_style = self._merge_styles(default_container_style, container_style)

        # Callback types
        self._add_callback_type('ready')
        self._add_callback_type('rowClick')
        self._add_callback_type('cellEdited')
        self._add_callback_type('dataChanged')

        # Initialize macro
        self._init_macro()

    def _create_elements(self):
        """Create table container element."""
        # Create container div
        container = self._register_element('container',
                                          self._create_container(self._container_style))

        # Initialize Tabulator after DOM ready
        init_proxy = create_proxy(lambda: self._initialize_table())
        js.setTimeout(init_proxy, 100)

        return container

    def _initialize_table(self):
        """Initialize Tabulator instance with retry mechanism."""
        if self._get_state('initialized'):
            return

        retry_count = self._get_state('init_retry_count')
        if retry_count > 50:  # Max 50 retries (5 seconds)
            print(f"Tabulator initialization failed after {retry_count} attempts")
            print("Make sure Tabulator is loaded")
            return

        try:
            # Check if Tabulator is loaded
            if not hasattr(js, 'Tabulator') or not js.Tabulator:
                # Not loaded yet, retry
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_table())
                js.setTimeout(init_proxy, 100)
                return

            container = self._get_element('container')
            if not container or not container._dom_element:
                # Container not ready
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_table())
                js.setTimeout(init_proxy, 100)
                return

            # Build Tabulator configuration
            config = {
                'data': self._get_state('data'),
                'columns': self._get_state('columns'),
                'height': self._get_state('height'),
                'layout': self._get_state('layout')
            }

            # Merge with additional options
            config.update(self._get_state('options'))

            # Convert Python config to JavaScript object
            js_config = to_js(config, dict_converter=js.Object.fromEntries)

            # Create Tabulator instance
            table_instance = js.Tabulator.new(container._dom_element, js_config)

            # Store instance
            self._set_state(table_instance=table_instance, initialized=True)

            # Trigger ready callback
            self._trigger_callbacks('ready', self)

        except Exception as e:
            print(f"Tabulator initialization error: {e}")
            # Retry with longer delay on error
            self._set_state(init_retry_count=retry_count + 1)
            init_proxy = create_proxy(lambda: self._initialize_table())
            js.setTimeout(init_proxy, 200)

    def set_columns(self, columns):
        """
        Set table columns.

        Args:
            columns: List of column definitions (Tabulator format)

        Returns:
            Self for method chaining
        """
        self._set_state(columns=columns)

        table = self._get_state('table_instance')
        if table:
            table.setColumns(to_js(columns))

        return self

    def set_data(self, data):
        """
        Set table data.

        Args:
            data: List of dictionaries representing rows

        Returns:
            Self for method chaining
        """
        self._set_state(data=data)

        table = self._get_state('table_instance')
        if table:
            table.setData(to_js(data))

        return self

    def get_data(self):
        """
        Get current table data.

        Returns:
            List of row data dictionaries
        """
        table = self._get_state('table_instance')
        if table:
            # Convert JS array to Python list
            js_data = table.getData()
            return js_data.to_py()
        return self._get_state('data')

    def clear_data(self):
        """Clear all table data."""
        table = self._get_state('table_instance')
        if table:
            table.clearData()
        self._set_state(data=[])
        return self

    def add_row(self, data, position=None, index=None):
        """
        Add a row to the table.

        Args:
            data: Row data dictionary
            position: "top" or "bottom" (default: bottom)
            index: Specific index to insert at

        Returns:
            Self for method chaining
        """
        table = self._get_state('table_instance')
        if table:
            js_data = to_js(data)
            if position:
                table.addRow(js_data, position)
            elif index is not None:
                table.addRow(js_data, index)
            else:
                table.addRow(js_data)
        return self

    def delete_row(self, row_index):
        """
        Delete a row by index.

        Args:
            row_index: Index of row to delete

        Returns:
            Self for method chaining
        """
        table = self._get_state('table_instance')
        if table:
            rows = table.getRows()
            if 0 <= row_index < rows.length:
                rows[row_index].delete()
        return self

    def update_row(self, row_index, data):
        """
        Update a row by index.

        Args:
            row_index: Index of row to update
            data: New row data dictionary

        Returns:
            Self for method chaining
        """
        table = self._get_state('table_instance')
        if table:
            rows = table.getRows()
            if 0 <= row_index < rows.length:
                rows[row_index].update(to_js(data))
        return self

    def download(self, format="csv", filename="data"):
        """
        Download table data.

        Args:
            format: "csv", "json", "xlsx", "pdf", "html"
            filename: Output filename (without extension)

        Returns:
            Self for method chaining
        """
        table = self._get_state('table_instance')
        if table:
            table.download(format, f"{filename}.{format}")
        return self

    def on_ready(self, callback):
        """
        Register callback for when table is ready.

        Args:
            callback: Function to call when table is initialized

        Returns:
            Self for method chaining
        """
        return self.on('ready', callback)

    def on_row_click(self, callback):
        """
        Register callback for row clicks.

        Args:
            callback: Function to call with (row_data, row_component)

        Returns:
            Self for method chaining
        """
        def wrapped_callback(e, row):
            row_data = row.getData().to_py() if row else None
            callback(row_data, row)

        table = self._get_state('table_instance')
        if table:
            table.on("rowClick", create_proxy(wrapped_callback))

        return self

    def on_cell_edited(self, callback):
        """
        Register callback for cell edits.

        Args:
            callback: Function to call with (cell_component)

        Returns:
            Self for method chaining
        """
        table = self._get_state('table_instance')
        if table:
            table.on("cellEdited", create_proxy(callback))

        return self

    def destroy(self):
        """Destroy table instance and clean up."""
        table = self._get_state('table_instance')
        if table:
            table.destroy()
            self._set_state(table_instance=None, initialized=False)

        super().destroy()

    @property
    def tabulator(self):
        """
        Access native Tabulator instance for advanced usage.

        Returns:
            JavaScript Tabulator object or None if not initialized
        """
        return self._get_state('table_instance')

    @property
    def is_ready(self):
        """Check if table is initialized."""
        return self._get_state('initialized')


# For backward compatibility and convenience
Column = dict  # Columns are now just dictionaries
ColumnType = None  # Not needed with Tabulator

__all__ = ['DataTable', 'Column', 'ColumnType']
