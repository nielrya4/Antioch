"""
Data Visualization App - A comprehensive spreadsheet and charting application.
Demonstrates advanced macro usage with DataTable and Chart components.
"""
from antioch import Div, H1, H2, P, Button, Select, Option, DOM
from antioch.macros import DataTable, ChartJS as Chart, Tabs, Tab, Modal


class DataVizApp:
    """Main data visualization application class."""
    
    def __init__(self):
        self.data_table = None
        self.chart = None
        self.tabs = None
        self.sample_datasets = self._get_sample_datasets()
        self.setup_ui()
    
    def _get_sample_datasets(self):
        """Get sample datasets for the app."""
        return {
            "sales": {
                "name": "Monthly Sales Data",
                "columns": [
                    {"title": "Month", "field": "month", "editor": "input", "width": 150},
                    {"title": "Revenue", "field": "revenue", "editor": "number", "formatter": "money", "width": 150},
                    {"title": "Units Sold", "field": "units", "editor": "number", "width": 150},
                    {"title": "Profit", "field": "profit", "editor": "number", "formatter": "money", "width": 150}
                ],
                "data": [
                    {"month": "January", "revenue": 45000, "units": 120, "profit": 12000},
                    {"month": "February", "revenue": 52000, "units": 135, "profit": 14500},
                    {"month": "March", "revenue": 38000, "units": 95, "profit": 9500},
                    {"month": "April", "revenue": 61000, "units": 165, "profit": 18500},
                    {"month": "May", "revenue": 55000, "units": 140, "profit": 16000},
                    {"month": "June", "revenue": 67000, "units": 180, "profit": 21000}
                ]
            },
            "performance": {
                "name": "Team Performance Metrics",
                "columns": [
                    {"title": "Month", "field": "month", "editor": "input"},
                    {"title": "Revenue", "field": "revenue", "editor": "number", "formatter": "money"},
                    {"title": "Units Sold", "field": "units", "editor": "number"},
                    {"title": "Profit", "field": "profit", "editor": "number", "formatter": "money"}
                ],
                "data": [
                    {"month": "Alice", "revenue": 28, "units": 9.2, "profit": 85},
                    {"month": "Bob", "revenue": 32, "units": 8.7, "profit": 92},
                    {"month": "Carol", "revenue": 25, "units": 9.5, "profit": 88},
                    {"month": "David", "revenue": 30, "units": 8.9, "profit": 90},
                    {"month": "Eve", "revenue": 27, "units": 9.1, "profit": 87}
                ]
            },
            "budget": {
                "name": "Department Budget Allocation",
                "columns": [
                    {"title": "Month", "field": "month", "editor": "input"},
                    {"title": "Revenue", "field": "revenue", "editor": "number", "formatter": "money"},
                    {"title": "Units Sold", "field": "units", "editor": "number"},
                    {"title": "Profit", "field": "profit", "editor": "number", "formatter": "money"}
                ],
                "data": [
                    {"month": "Engineering", "revenue": 120000, "units": 130000, "profit": 125000},
                    {"month": "Marketing", "revenue": 80000, "units": 95000, "profit": 90000},
                    {"month": "Sales", "revenue": 60000, "units": 70000, "profit": 75000},
                    {"month": "HR", "revenue": 40000, "units": 45000, "profit": 42000},
                    {"month": "Operations", "revenue": 95000, "units": 100000, "profit": 105000}
                ]
            }
        }
    
    def setup_ui(self):
        """Set up the main application UI."""
        # Create main container
        main_container = Div(style={
            "max_width": "1200px",
            "margin": "0 auto",
            "padding": "20px",
            "font_family": "Arial, sans-serif"
        })
        
        # App header
        header = self._create_header()
        
        # Create tabs for different sections
        self.tabs = Tabs(
            tabs=[
                Tab("Data Editor", self._create_data_editor_tab()),
                Tab("Visualizations", self._create_charts_tab()),
                Tab("Sample Data", self._create_samples_tab())
            ],
            container_style={
                "width": "100%"
            },
            content_style={
                "max_width": "100%",
                "overflow": "auto"
            }
        )
        
        main_container.add(header, self.tabs.element)
        DOM.add(main_container)

        # Initialize column selector with default data
        self._update_column_selector()
    
    def _create_header(self):
        """Create application header."""
        header = Div(style={
            "text_align": "center",
            "margin_bottom": "30px",
            "padding": "20px",
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "color": "white",
            "border_radius": "10px",
            "box_shadow": "0 4px 6px rgba(0,0,0,0.1)"
        })
        
        title = H1("📊 Data Visualization Studio", style={
            "margin": "0 0 10px 0",
            "font_size": "28px",
            "font_weight": "bold"
        })
        
        subtitle = P("Create spreadsheets, visualize data, and build interactive charts", style={
            "margin": "0",
            "font_size": "16px",
            "opacity": "0.9"
        })
        
        header.add(title, subtitle)
        return header
    
    def _create_data_editor_tab(self):
        """Create the data editor tab content."""
        container = Div(style={
            "padding": "20px",
            "max_width": "100%",
            "overflow": "hidden"
        })
        
        # Section header
        header = Div(style={"margin_bottom": "20px"})
        header.add(H2("📝 Data Editor", style={"margin": "0 0 10px 0"}))
        header.add(P("Edit your data in the spreadsheet below. Changes will automatically update the charts.", 
                    style={"color": "#666", "margin": "0"}))
        
        # Data table controls
        controls = Div(style={
            "display": "flex",
            "gap": "10px",
            "margin_bottom": "15px",
            "align_items": "center"
        })
        
        # Add sample data button
        load_sample_btn = Button("Load Sample Data", style={
            "background_color": "#28a745",
            "color": "white",
            "border": "none",
            "padding": "8px 16px",
            "border_radius": "4px",
            "cursor": "pointer"
        })
        load_sample_btn.on_click(lambda e: self._show_sample_selector())
        
        # Clear data button
        clear_btn = Button("Clear All", style={
            "background_color": "#dc3545",
            "color": "white",
            "border": "none",
            "padding": "8px 16px",
            "border_radius": "4px",
            "cursor": "pointer"
        })
        clear_btn.on_click(lambda e: self._clear_data())
        
        # Export button
        export_btn = Button("Export Data", style={
            "background_color": "#6c757d",
            "color": "white",
            "border": "none",
            "padding": "8px 16px",
            "border_radius": "4px",
            "cursor": "pointer"
        })
        export_btn.on_click(lambda e: self._export_data())
        
        controls.add(load_sample_btn, clear_btn, export_btn)

        # Create data table with sales data by default
        default_dataset = self.sample_datasets["sales"]
        self.data_table = DataTable(
            data=default_dataset["data"],
            columns=default_dataset["columns"],
            height="500px",
            layout="fitData",
            container_style={
                "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
            }
        )

        # Connect data table changes to chart updates
        self.data_table.on_cell_edited(lambda cell: self._update_charts())

        container.add(header, controls, self.data_table.element)
        return container
    
    def _create_charts_tab(self):
        """Create the charts visualization tab."""
        container = Div(style={"padding": "20px"})
        
        # Section header
        header = Div(style={"margin_bottom": "20px"})
        header.add(H2("📈 Data Visualizations", style={"margin": "0 0 10px 0"}))
        header.add(P("Interactive charts that automatically update when you modify the data.", 
                    style={"color": "#666", "margin": "0"}))
        
        # Chart controls
        controls = Div(style={
            "display": "flex",
            "gap": "15px",
            "margin_bottom": "20px",
            "align_items": "center",
            "padding": "15px",
            "background_color": "#f8f9fa",
            "border_radius": "8px"
        })
        
        controls.add(P("Data Column:", style={"margin": "0", "font_weight": "bold"}))
        
        # Column selector
        self.column_select = Select(style={
            "padding": "5px 10px",
            "border": "1px solid #ddd",
            "border_radius": "4px",
            "min_width": "150px"
        })
        self.column_select.on_change(lambda e: self._update_charts())
        
        controls.add(self.column_select)
        
        # Create chart with Chart.js
        self.chart = Chart(
            config={
                'type': 'bar',
                'data': {
                    'labels': [],
                    'datasets': [{
                        'label': 'Data Visualization',
                        'data': [],
                        'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'responsive': True,
                    'maintainAspectRatio': False,
                    'plugins': {
                        'title': {
                            'display': True,
                            'text': 'Data Visualization',
                            'font': {
                                'size': 16
                            }
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
            },
            width=700,
            height=400
        )
        
        container.add(header, controls, self.chart.element)
        return container
    
    def _create_samples_tab(self):
        """Create the sample data tab."""
        container = Div(style={"padding": "20px"})
        
        # Section header
        header = Div(style={"margin_bottom": "20px"})
        header.add(H2("🎯 Sample Datasets", style={"margin": "0 0 10px 0"}))
        header.add(P("Choose from pre-made datasets to get started quickly.", 
                    style={"color": "#666", "margin": "0"}))
        
        # Sample dataset buttons
        for key, dataset in self.sample_datasets.items():
            sample_card = Div(style={
                "border": "1px solid #ddd",
                "border_radius": "8px",
                "padding": "20px",
                "margin_bottom": "15px",
                "background_color": "#fff",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.05)"
            })
            
            sample_card.add(H2(dataset["name"], style={
                "margin": "0 0 10px 0",
                "color": "#333",
                "font_size": "18px"
            }))
            
            # Show column info
            columns_text = ", ".join([col["title"] for col in dataset["columns"]])
            sample_card.add(P(f"Columns: {columns_text}", style={
                "color": "#666",
                "margin": "0 0 10px 0",
                "font_size": "14px"
            }))
            
            sample_card.add(P(f"{len(dataset['data'])} rows of sample data", style={
                "color": "#999",
                "margin": "0 0 15px 0",
                "font_size": "12px"
            }))
            
            load_btn = Button("Load This Dataset", style={
                "background_color": "#007bff",
                "color": "white",
                "border": "none",
                "padding": "10px 20px",
                "border_radius": "5px",
                "cursor": "pointer",
                "font_weight": "bold"
            })
            load_btn.on_click(lambda e, dataset_key=key: self._load_sample_dataset(dataset_key))
            
            sample_card.add(load_btn)
            container.add(sample_card)
        
        return container
    
    def _load_sample_dataset(self, dataset_key):
        """Load a sample dataset into the data table."""
        if dataset_key not in self.sample_datasets:
            return

        dataset = self.sample_datasets[dataset_key]

        if self.data_table:
            # Just update data, not columns (to avoid expansion issues)
            # Note: This only works if datasets have same fields as sales
            self.data_table.set_data(dataset["data"])

        # Switch to data editor tab
        if self.tabs:
            self.tabs.set_active_tab(self.tabs.tabs[0].tab_id)  # First tab

        print(f"✅ Loaded sample dataset: {dataset['name']}")
    
    def _update_column_selector(self):
        """Update the column selector with current table columns."""
        if not self.column_select or not self.data_table:
            return

        columns = self.data_table._get_state('columns')

        # Clear existing options
        self.column_select._dom_element.innerHTML = ""

        # Add default option
        default_option = Option("Select a column...", value="")
        self.column_select.add(default_option)

        # Add column options
        for i, col in enumerate(columns):
            col_title = col.get('title', f'Column {i+1}')
            col_field = col.get('field', '')
            option = Option(f"{col_title}", value=col_field)
            self.column_select.add(option)
    
    def _update_charts(self):
        """Update charts with current data table data."""
        if not self.data_table or not self.chart or not self.column_select:
            return

        selected_field = self.column_select.value
        if not selected_field or selected_field == "":
            # Show empty chart
            config = self.chart.config.copy()
            config['data']['labels'] = []
            config['data']['datasets'][0]['data'] = []
            self.chart.update(config)
            return

        try:
            # Get all data from table
            table_data = self.data_table.get_data()

            if not table_data:
                return

            columns = self.data_table._get_state('columns')

            # Find the selected column info
            selected_col_title = None
            for col in columns:
                if col.get('field') == selected_field:
                    selected_col_title = col.get('title', selected_field)
                    break

            # Extract data for selected field
            chart_data = []
            for row in table_data:
                val = row.get(selected_field)
                # Convert to number if possible
                if val is not None:
                    try:
                        chart_data.append(float(val))
                    except (ValueError, TypeError):
                        chart_data.append(val)
                else:
                    chart_data.append(None)

            # Get labels from first column field if available
            if columns:
                first_field = columns[0].get('field')
                labels = [str(row.get(first_field, f"Row {i+1}")) for i, row in enumerate(table_data)]

                # If first column looks numeric, use row numbers instead
                try:
                    if all(isinstance(row.get(first_field), (int, float)) for row in table_data):
                        labels = [f"Row {i+1}" for i in range(len(table_data))]
                except:
                    pass
            else:
                labels = [f"Row {i+1}" for i in range(len(table_data))]

            # Filter out None values and corresponding labels
            filtered_data = []
            filtered_labels = []
            for data_val, label in zip(chart_data, labels):
                if data_val is not None:
                    filtered_data.append(data_val)
                    filtered_labels.append(str(label))

            # Update chart with Chart.js API
            chart_title = f"{selected_col_title} Visualization" if selected_col_title else "Data Visualization"

            # Get current config and update it
            config = self.chart.config.copy()
            config['data']['labels'] = filtered_labels
            config['data']['datasets'][0]['data'] = filtered_data
            config['data']['datasets'][0]['label'] = chart_title
            config['options']['plugins']['title']['text'] = chart_title

            self.chart.update(config)

        except Exception as e:
            print(f"Error updating chart: {e}")
    
    def _show_sample_selector(self):
        """Show modal with sample dataset options."""
        modal_content = Div()
        
        modal_content.add(P("Choose a sample dataset to load:", style={
            "margin_bottom": "15px",
            "font_weight": "bold"
        }))
        
        for key, dataset in self.sample_datasets.items():
            btn = Button(dataset["name"], style={
                "display": "block",
                "width": "100%",
                "margin_bottom": "10px",
                "padding": "12px",
                "background_color": "#f8f9fa",
                "border": "1px solid #ddd",
                "border_radius": "4px",
                "cursor": "pointer",
                "text_align": "left"
            })
            btn.on_click(lambda e, dk=key: self._load_and_close_modal(dk))
            modal_content.add(btn)
        
        self.sample_modal = Modal("Load Sample Data", modal_content)
        DOM.add(self.sample_modal.element)
        self.sample_modal.show()
    
    def _load_and_close_modal(self, dataset_key):
        """Load dataset and close modal."""
        self._load_sample_dataset(dataset_key)
        if hasattr(self, 'sample_modal'):
            self.sample_modal.close()
    
    def _clear_data(self):
        """Clear all data from the table."""
        if self.data_table:
            self.data_table.clear_data()
        print("🗑️ Data cleared")
    
    def _export_data(self):
        """Export current data (simulation)."""
        if not self.data_table:
            return

        data = self.data_table.get_data()
        print("📤 Export data (simulation):")
        print("Data would be exported as:")
        for i, row in enumerate(data[:3]):  # Show first 3 rows
            print(f"  Row {i+1}: {row}")
        if len(data) > 3:
            print(f"  ... and {len(data) - 3} more rows")

        # Could also use Tabulator's built-in download
        # self.data_table.download("csv", "dataviz_export")


def main():
    """Initialize and run the data visualization app."""
    print("🚀 Starting Data Visualization Studio...")
    app = DataVizApp()
    print("✅ Data Visualization Studio loaded!")


if __name__ == "__main__":
    main()