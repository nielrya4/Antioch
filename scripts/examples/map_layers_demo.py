"""
Map Layers Demo - Demonstrate GIS layer control functionality.
Shows how vector and raster layers automatically appear in the layer control.
"""

from antioch import Div, H1, H2, Button, P, DOM
from antioch.macros import Map
import js


def main():
    """Main entry point for Map Layers demo."""
    # Create page container
    page = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Add title
    title = H1("Antioch Map Layer Control Demo", style={
        "color": "#333",
        "margin_bottom": "10px"
    })
    page.add(title)

    # Add description
    description = P(
        "Vector and raster layers automatically appear in the layer control widget (top-right corner). Click to toggle layers on/off!",
        style={"color": "#666", "margin_bottom": "30px"}
    )
    page.add(description)

    # ============================================================================
    # DEMO: Map with Multiple GeoJSON Layers
    # ============================================================================

    section1 = Div(style={"margin_bottom": "40px"})
    section1.add(H2("Multiple Vector Layers", style={"color": "#444", "margin_bottom": "10px"}))

    info_text = P(
        "Each layer is automatically added to the layer control. Use the control in the top-right to toggle layers!",
        style={"color": "#666", "margin_bottom": "10px", "font_style": "italic"}
    )
    section1.add(info_text)

    # Create map centered on USA
    map1 = Map(
        center=[39.8283, -98.5795],
        zoom=4,
        height="500px",
        tile_layer="OpenStreetMap"
    )

    # Sample GeoJSON data for different regions
    def create_geojson_objects():
        """Create sample GeoJSON data as JavaScript objects."""
        import json

        # West Coast polygon
        west_coast_dict = {
            "type": "Feature",
            "properties": {"name": "West Coast Region"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-125, 32],
                    [-114, 32],
                    [-114, 42],
                    [-125, 42],
                    [-125, 32]
                ]]
            }
        }

        # East Coast polygon
        east_coast_dict = {
            "type": "Feature",
            "properties": {"name": "East Coast Region"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-80, 25],
                    [-67, 25],
                    [-67, 45],
                    [-80, 45],
                    [-80, 25]
                ]]
            }
        }

        # Central route line
        central_route_dict = {
            "type": "Feature",
            "properties": {"name": "Central Route"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-100, 30],
                    [-95, 35],
                    [-90, 40],
                    [-85, 42]
                ]
            }
        }

        # Convert Python dicts to JavaScript objects via JSON
        west_coast = js.JSON.parse(json.dumps(west_coast_dict))
        east_coast = js.JSON.parse(json.dumps(east_coast_dict))
        central_route = js.JSON.parse(json.dumps(central_route_dict))

        return west_coast, east_coast, central_route

    # Add layers when map is ready
    def add_layers(map_instance):
        import json
        west_coast, east_coast, central_route = create_geojson_objects()

        # Add West Coast layer with custom styling
        west_layer = map_instance.add_geojson(
            west_coast,
            name="West Coast Region",
            style_options={
                "color": "#ff7800",
                "weight": 2,
                "fillColor": "#ff7800",
                "fillOpacity": 0.2
            },
            add_to_control=True  # This is the default
        )

        # Add East Coast layer with custom styling
        east_layer = map_instance.add_geojson(
            east_coast,
            name="East Coast Region",
            style_options={
                "color": "#0078ff",
                "weight": 2,
                "fillColor": "#0078ff",
                "fillOpacity": 0.2
            },
            add_to_control=True
        )

        # Add Central Route line
        route_layer = map_instance.add_geojson(
            central_route,
            name="Central Route",
            style_options={
                "color": "#00ff00",
                "weight": 4,
                "opacity": 0.7
            },
            add_to_control=True
        )

        # Add a layer that's NOT in the control (for comparison)
        hidden_polygon_dict = {
            "type": "Feature",
            "properties": {"name": "Hidden Area"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-105, 35],
                    [-100, 35],
                    [-100, 40],
                    [-105, 40],
                    [-105, 35]
                ]]
            }
        }

        hidden_polygon = js.JSON.parse(json.dumps(hidden_polygon_dict))

        hidden_layer = map_instance.add_geojson(
            hidden_polygon,
            name="Hidden Layer",
            style_options={
                "color": "#ff00ff",
                "weight": 2,
                "fillColor": "#ff00ff",
                "fillOpacity": 0.1
            },
            add_to_control=False  # This layer won't appear in the control
        )

    map1.on_ready(add_layers)

    section1.add(map1)

    # Add control buttons
    button_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px"
    })

    # Zoom to fit all layers button
    zoom_btn = Button("Zoom to Fit All Layers", style={
        "padding": "8px 16px",
        "background_color": "#007bff",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px"
    })
    zoom_btn.on_click(lambda e: map1.zoom_to_layers(padding=20))
    button_container.add(zoom_btn)

    section1.add(button_container)

    # Add info about the hidden layer
    hidden_info = P(
        "Note: There's also a purple 'Hidden Layer' on the map that doesn't appear in the layer control (add_to_control=False).",
        style={
            "color": "#999",
            "font_size": "12px",
            "margin_top": "10px",
            "font_style": "italic"
        }
    )
    section1.add(hidden_info)

    page.add(section1)

    # Add page to DOM
    DOM.add(page)

    print("✅ Map Layers Demo loaded!")
    print("Check the top-right corner of the map for the layer control widget!")


if __name__ == "__main__":
    main()
