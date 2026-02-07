"""
Chart.js Demo - Comprehensive demonstration of Chart.js integration in Antioch.

This demo showcases all major Chart.js chart types and features:
- Bar charts
- Line charts
- Pie and Doughnut charts
- Radar charts
- Polar Area charts
- Scatter charts
- Bubble charts
- Mixed chart types
- Dynamic updates
- Custom styling
"""
from antioch import *
from antioch.macros import ChartJS as Chart


def main():
    """Create comprehensive Chart.js demonstration."""

    # Page header
    DOM.add(
        Div(
            H1("📊 Chart.js Integration Demo", style={"color": "#333", "margin_bottom": "10px"}),
            P("Interactive charting powered by Chart.js and Python",
              style={"color": "#666", "margin_bottom": "30px"}),
            style={"text_align": "center", "padding": "20px"}
        )
    )

    # Create demo sections
    create_bar_chart_demo()
    create_line_chart_demo()
    create_pie_doughnut_demo()
    create_radar_chart_demo()
    create_polar_area_demo()
    create_scatter_bubble_demo()
    create_mixed_chart_demo()
    create_dynamic_update_demo()


def create_bar_chart_demo():
    """Bar chart demonstration."""
    section = create_section(
        "📊 Bar Chart",
        "Basic bar chart with custom colors and labels"
    )

    chart = Chart(
        config={
            'type': 'bar',
            'data': {
                'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                'datasets': [{
                    'label': 'Votes',
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)',
                        'rgba(255, 159, 64, 0.5)'
                    ],
                    'borderColor': [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Color Preferences Survey'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        },
        width=800,
        height=400
    )

    section.add(chart.element)
    DOM.add(section)


def create_line_chart_demo():
    """Line chart demonstration."""
    section = create_section(
        "📈 Line Chart",
        "Multi-dataset line chart with tension and fill"
    )

    chart = Chart(
        config={
            'type': 'line',
            'data': {
                'labels': ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
                'datasets': [
                    {
                        'label': 'Dataset 1',
                        'data': [65, 59, 80, 81, 56, 55, 40],
                        'fill': False,
                        'borderColor': 'rgb(75, 192, 192)',
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'tension': 0.1
                    },
                    {
                        'label': 'Dataset 2',
                        'data': [28, 48, 40, 19, 86, 27, 90],
                        'fill': True,
                        'borderColor': 'rgb(255, 99, 132)',
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'tension': 0.4
                    }
                ]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'legend': {
                        'position': 'top'
                    },
                    'title': {
                        'display': True,
                        'text': 'Monthly Sales Data'
                    }
                },
                'interaction': {
                    'intersect': False
                },
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        },
        width=800,
        height=400
    )

    section.add(chart.element)
    DOM.add(section)


def create_pie_doughnut_demo():
    """Pie and Doughnut charts demonstration."""
    section = create_section(
        "🥧 Pie & Doughnut Charts",
        "Side-by-side comparison of pie and doughnut charts"
    )

    # Container for side-by-side charts
    charts_container = Div(style={
        "display": "flex",
        "gap": "20px",
        "justify_content": "center",
        "flex_wrap": "wrap"
    })

    # Pie chart
    pie_data = {
        'labels': ['Red', 'Blue', 'Yellow'],
        'datasets': [{
            'label': 'My Dataset',
            'data': [300, 50, 100],
            'backgroundColor': [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)'
            ],
            'hoverOffset': 4
        }]
    }

    pie_chart = Chart(
        config={
            'type': 'pie',
            'data': pie_data,
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Pie Chart'
                    }
                }
            }
        },
        width=400,
        height=400
    )

    # Doughnut chart
    doughnut_chart = Chart(
        config={
            'type': 'doughnut',
            'data': pie_data,
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Doughnut Chart'
                    }
                }
            }
        },
        width=400,
        height=400
    )

    charts_container.add(pie_chart.element, doughnut_chart.element)
    section.add(charts_container)
    DOM.add(section)


def create_radar_chart_demo():
    """Radar chart demonstration."""
    section = create_section(
        "🎯 Radar Chart",
        "Multi-dimensional data visualization"
    )

    chart = Chart(
        config={
            'type': 'radar',
            'data': {
                'labels': ['Speed', 'Strength', 'Intelligence', 'Endurance', 'Agility', 'Luck'],
                'datasets': [
                    {
                        'label': 'Player 1',
                        'data': [80, 70, 90, 75, 85, 60],
                        'fill': True,
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'borderColor': 'rgb(255, 99, 132)',
                        'pointBackgroundColor': 'rgb(255, 99, 132)',
                        'pointBorderColor': '#fff',
                        'pointHoverBackgroundColor': '#fff',
                        'pointHoverBorderColor': 'rgb(255, 99, 132)'
                    },
                    {
                        'label': 'Player 2',
                        'data': [70, 90, 60, 85, 75, 80],
                        'fill': True,
                        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                        'borderColor': 'rgb(54, 162, 235)',
                        'pointBackgroundColor': 'rgb(54, 162, 235)',
                        'pointBorderColor': '#fff',
                        'pointHoverBackgroundColor': '#fff',
                        'pointHoverBorderColor': 'rgb(54, 162, 235)'
                    }
                ]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Character Stats Comparison'
                    }
                },
                'elements': {
                    'line': {
                        'borderWidth': 3
                    }
                }
            }
        },
        width=600,
        height=600
    )

    section.add(chart.element)
    DOM.add(section)


def create_polar_area_demo():
    """Polar area chart demonstration."""
    section = create_section(
        "⭕ Polar Area Chart",
        "Circular statistical chart"
    )

    chart = Chart(
        config={
            'type': 'polarArea',
            'data': {
                'labels': ['Red', 'Green', 'Yellow', 'Grey', 'Blue'],
                'datasets': [{
                    'label': 'My Dataset',
                    'data': [11, 16, 7, 3, 14],
                    'backgroundColor': [
                        'rgb(255, 99, 132)',
                        'rgb(75, 192, 192)',
                        'rgb(255, 205, 86)',
                        'rgb(201, 203, 207)',
                        'rgb(54, 162, 235)'
                    ]
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Distribution by Category'
                    }
                }
            }
        },
        width=600,
        height=600
    )

    section.add(chart.element)
    DOM.add(section)


def create_scatter_bubble_demo():
    """Scatter and Bubble charts demonstration."""
    section = create_section(
        "🔵 Scatter & Bubble Charts",
        "Point-based data visualization"
    )

    # Container for side-by-side charts
    charts_container = Div(style={
        "display": "flex",
        "gap": "20px",
        "justify_content": "center",
        "flex_wrap": "wrap"
    })

    # Scatter chart
    scatter_chart = Chart(
        config={
            'type': 'scatter',
            'data': {
                'datasets': [{
                    'label': 'Scatter Dataset',
                    'data': [
                        {'x': -10, 'y': 0},
                        {'x': 0, 'y': 10},
                        {'x': 10, 'y': 5},
                        {'x': 0.5, 'y': 5.5},
                        {'x': -5, 'y': 3}
                    ],
                    'backgroundColor': 'rgb(255, 99, 132)'
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Scatter Plot'
                    }
                },
                'scales': {
                    'x': {
                        'type': 'linear',
                        'position': 'bottom'
                    }
                }
            }
        },
        width=400,
        height=400
    )

    # Bubble chart
    bubble_chart = Chart(
        config={
            'type': 'bubble',
            'data': {
                'datasets': [{
                    'label': 'Bubble Dataset',
                    'data': [
                        {'x': 20, 'y': 30, 'r': 15},
                        {'x': 40, 'y': 10, 'r': 10},
                        {'x': 30, 'y': 25, 'r': 20},
                        {'x': 15, 'y': 35, 'r': 8}
                    ],
                    'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                    'borderColor': 'rgb(54, 162, 235)',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Bubble Chart'
                    }
                }
            }
        },
        width=400,
        height=400
    )

    charts_container.add(scatter_chart.element, bubble_chart.element)
    section.add(charts_container)
    DOM.add(section)


def create_mixed_chart_demo():
    """Mixed chart type demonstration."""
    section = create_section(
        "🌈 Mixed Chart Types",
        "Combining bar and line charts in one visualization"
    )

    chart = Chart(
        config={
            'type': 'bar',
            'data': {
                'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
                'datasets': [
                    {
                        'type': 'bar',
                        'label': 'Revenue',
                        'data': [120, 150, 180, 200],
                        'backgroundColor': 'rgba(54, 162, 235, 0.5)',
                        'borderColor': 'rgb(54, 162, 235)',
                        'borderWidth': 1
                    },
                    {
                        'type': 'line',
                        'label': 'Target',
                        'data': [140, 160, 170, 190],
                        'borderColor': 'rgb(255, 99, 132)',
                        'borderWidth': 2,
                        'fill': False
                    }
                ]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Quarterly Performance vs Target'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        },
        width=800,
        height=400
    )

    section.add(chart.element)
    DOM.add(section)


def create_dynamic_update_demo():
    """Dynamic chart update demonstration."""
    section = create_section(
        "⚡ Dynamic Updates",
        "Click the button to update the chart data in real-time"
    )

    # Create initial chart
    chart = Chart(
        config={
            'type': 'bar',
            'data': {
                'labels': ['A', 'B', 'C', 'D', 'E'],
                'datasets': [{
                    'label': 'Dynamic Data',
                    'data': [10, 20, 15, 25, 18],
                    'backgroundColor': '#ffffff',
                    'borderColor': 'rgb(75, 192, 192)',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': 'Click Update to See Random Data'
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                }
            }
        },
        width=800,
        height=400
    )

    # Update button
    def update_chart(event):
        """Update chart with random data."""
        import random

        new_data = [random.randint(5, 50) for _ in range(5)]
        config = chart.config.copy()
        config['data']['datasets'][0]['data'] = new_data
        chart.update(config)

    update_btn = Button("🔄 Update Chart", style={
        "background_color": "#28a745",
        "color": "white",
        "border": "none",
        "padding": "10px 20px",
        "border_radius": "5px",
        "cursor": "pointer",
        "font_weight": "bold",
        "margin": "20px 0"
    })
    update_btn.on_click(update_chart)

    section.add(update_btn, chart.element)
    DOM.add(section)


def create_section(title, description):
    """Create a styled section container."""
    section = Div(style={
        "background_color": "white",
        "border_radius": "8px",
        "padding": "30px",
        "margin_bottom": "30px",
        "box_shadow": "0 2px 4px rgba(0,0,0,0.1)"
    })

    section.add(
        H2(title, style={"color": "#333", "margin": "0 0 10px 0"}),
        P(description, style={"color": "#666", "margin": "0 0 20px 0"})
    )

    return section


if __name__ == "__main__":
    main()
