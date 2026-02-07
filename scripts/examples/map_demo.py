"""
Map Demo - Showcase Antioch Map macro capabilities.
Demonstrates markers, shapes, interactions, and various map features.
"""

from antioch import Div, H1, H2, Button, P, DOM
from antioch.macros import Map


def main():
    """Main entry point for Map demo."""
    # Create page container
    page = Div(style={
        "max_width": "1200px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Add title
    title = H1("Antioch Map Component Demo", style={
        "color": "#333",
        "margin_bottom": "10px"
    })
    page.add(title)

    # Add description
    description = P(
        "Interactive maps powered by Leaflet. Click the map, add markers, and explore different features!",
        style={"color": "#666", "margin_bottom": "30px"}
    )
    page.add(description)

    # ============================================================================
    # DEMO 1: Basic Map with Markers
    # ============================================================================

    section1 = Div(style={"margin_bottom": "40px"})
    section1.add(H2("Basic Map with Markers", style={"color": "#444", "margin_bottom": "10px"}))

    # Create map centered on London
    map1 = Map(
        center=[51.505, -0.09],
        zoom=13,
        height="400px",
        tile_layer="OpenStreetMap"
    )

    # Add markers when map is ready (callback receives map instance as parameter)
    def add_london_markers(map_instance):
        map_instance.add_marker(51.5, -0.09, "Big Ben - Iconic clock tower")
        map_instance.add_marker(51.508, -0.076, "St. Paul's Cathedral")
        map_instance.add_marker(51.501, -0.142, "Buckingham Palace")
        map_instance.add_marker(51.515, -0.072, "Bank of England")

    map1.on_ready(add_london_markers)

    section1.add(map1)
    page.add(section1)

    # ============================================================================
    # DEMO 2: Interactive Map with Click Handler
    # ============================================================================

    section2 = Div(style={"margin_bottom": "40px"})
    section2.add(H2("Click to Add Markers", style={"color": "#444", "margin_bottom": "10px"}))

    info_text = P("Click anywhere on the map to add a marker!", style={
        "color": "#666",
        "margin_bottom": "10px",
        "font_style": "italic"
    })
    section2.add(info_text)

    # Create interactive map centered on San Francisco
    map2 = Map(
        center=[37.7749, -122.4194],
        zoom=12,
        height="400px",
        tile_layer="OpenStreetMap"
    )

    # Counter for markers
    marker_count = {"count": 0}

    # Add click handler to add markers
    def handle_map_click(map_instance, coords, event):
        marker_count["count"] += 1
        lat = coords['lat']
        lng = coords['lng']
        map_instance.add_marker(
            lat, lng,
            f"Marker #{marker_count['count']}<br>Lat: {lat:.4f}, Lng: {lng:.4f}"
        )

    map2.on_click(handle_map_click)

    section2.add(map2)

    # Add control buttons
    button_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px"
    })

    clear_btn = Button("Clear All Markers", style={
        "padding": "8px 16px",
        "background_color": "#dc3545",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    clear_btn.on_click(lambda e: map2.clear_markers())
    button_container.add(clear_btn)

    section2.add(button_container)
    page.add(section2)

    # ============================================================================
    # DEMO 3: Map with Shapes and Layers
    # ============================================================================

    section3 = Div(style={"margin_bottom": "40px"})
    section3.add(H2("Shapes and Layers", style={"color": "#444", "margin_bottom": "10px"}))

    # Create map centered on New York
    map3 = Map(
        center=[40.7128, -74.0060],
        zoom=12,
        height="400px",
        tile_layer="CartoDB"
    )

    # Add shapes and markers when map is ready
    def add_nyc_features(map_instance):
        # Add a circle around Central Park
        map_instance.add_circle(
            40.785091, -73.968285,
            radius=800,
            color="#ff7800",
            fill_opacity=0.3
        )

        # Add a polyline (route)
        route_points = [
            [40.7589, -73.9851],  # Times Square
            [40.7484, -73.9857],  # Empire State Building
            [40.7128, -74.0060],  # Downtown
        ]
        map_instance.add_polyline(route_points, color="#0000ff", weight=4)

        # Add a polygon (area)
        polygon_points = [
            [40.70, -74.02],
            [40.70, -73.99],
            [40.72, -73.99],
            [40.72, -74.02]
        ]
        map_instance.add_polygon(polygon_points, color="#00ff00", fill_opacity=0.2)

        # Add markers for points of interest
        map_instance.add_marker(40.7589, -73.9851, "Times Square")
        map_instance.add_marker(40.7484, -73.9857, "Empire State Building")

    map3.on_ready(add_nyc_features)

    section3.add(map3)
    page.add(section3)

    # ============================================================================
    # DEMO 4: Navigation Controls
    # ============================================================================

    section4 = Div(style={"margin_bottom": "40px"})
    section4.add(H2("Navigation Controls", style={"color": "#444", "margin_bottom": "10px"}))

    # Create map
    map4 = Map(
        center=[48.8566, 2.3522],  # Paris
        zoom=12,
        height="400px",
        tile_layer="OpenStreetMap"
    )

    # Add some famous Paris locations
    locations = [
        {"lat": 48.8584, "lng": 2.2945, "name": "Eiffel Tower"},
        {"lat": 48.8606, "lng": 2.3376, "name": "Louvre Museum"},
        {"lat": 48.8530, "lng": 2.3499, "name": "Notre-Dame"},
        {"lat": 48.8738, "lng": 2.2950, "name": "Arc de Triomphe"},
    ]

    # Add markers when map is ready
    def add_paris_markers(map_instance):
        for loc in locations:
            map_instance.add_marker(loc["lat"], loc["lng"], loc["name"])

    map4.on_ready(add_paris_markers)

    section4.add(map4)

    # Add navigation buttons
    nav_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px",
        "flex_wrap": "wrap"
    })

    # Create location buttons
    for loc in locations:
        btn = Button(f"Go to {loc['name']}", style={
            "padding": "8px 16px",
            "background_color": "#007bff",
            "color": "white",
            "border": "none",
            "border_radius": "4px",
            "cursor": "pointer"
        })

        # Create closure to capture location
        def make_handler(location):
            return lambda e: map4.set_view([location["lat"], location["lng"]], 15)

        btn.on_click(make_handler(loc))
        nav_container.add(btn)

    # Add zoom buttons
    zoom_in_btn = Button("Zoom In", style={
        "padding": "8px 16px",
        "background_color": "#28a745",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_in_btn.on_click(lambda e: map4.zoom_in())
    nav_container.add(zoom_in_btn)

    zoom_out_btn = Button("Zoom Out", style={
        "padding": "8px 16px",
        "background_color": "#ffc107",
        "color": "black",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_out_btn.on_click(lambda e: map4.zoom_out())
    nav_container.add(zoom_out_btn)

    # Fit bounds button
    fit_btn = Button("Show All Locations", style={
        "padding": "8px 16px",
        "background_color": "#6c757d",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })

    def fit_all_locations(e):
        points = [[loc["lat"], loc["lng"]] for loc in locations]
        map4.fit_bounds(points)

    fit_btn.on_click(fit_all_locations)
    nav_container.add(fit_btn)

    section4.add(nav_container)
    page.add(section4)

    # ============================================================================
    # DEMO 5: Different Tile Layers
    # ============================================================================

    section5 = Div(style={"margin_bottom": "40px"})
    section5.add(H2("Different Tile Layers", style={"color": "#444", "margin_bottom": "10px"}))

    tile_info = P(
        "Showing three maps with different tile layer styles: OpenStreetMap, CartoDB Light, and Satellite",
        style={"color": "#666", "margin_bottom": "15px"}
    )
    section5.add(tile_info)

    # Create container for side-by-side maps
    maps_container = Div(style={
        "display": "grid",
        "grid_template_columns": "repeat(auto-fit, minmax(350px, 1fr))",
        "gap": "20px",
        "margin_bottom": "20px"
    })

    # Center location (Tokyo)
    tokyo_center = [35.6762, 139.6503]

    # Map with OpenStreetMap tiles
    osm_container = Div()
    osm_container.add(P("OpenStreetMap", style={"font_weight": "bold", "margin_bottom": "5px"}))
    map5a = Map(center=tokyo_center, zoom=11, height="250px", tile_layer="OpenStreetMap")
    map5a.on_ready(lambda map_instance: map_instance.add_marker(35.6762, 139.6503, "Tokyo Station"))
    osm_container.add(map5a)
    maps_container.add(osm_container)

    # Map with CartoDB tiles
    carto_container = Div()
    carto_container.add(P("CartoDB Light", style={"font_weight": "bold", "margin_bottom": "5px"}))
    map5b = Map(center=tokyo_center, zoom=11, height="250px", tile_layer="CartoDB")
    map5b.on_ready(lambda map_instance: map_instance.add_marker(35.6762, 139.6503, "Tokyo Station"))
    carto_container.add(map5b)
    maps_container.add(carto_container)

    # Map with Satellite tiles
    sat_container = Div()
    sat_container.add(P("Satellite Imagery", style={"font_weight": "bold", "margin_bottom": "5px"}))
    map5c = Map(center=tokyo_center, zoom=11, height="250px", tile_layer="Satellite")
    map5c.on_ready(lambda map_instance: map_instance.add_marker(35.6762, 139.6503, "Tokyo Station"))
    sat_container.add(map5c)
    maps_container.add(sat_container)

    section5.add(maps_container)
    page.add(section5)

    # Add page to DOM
    DOM.add(page)

    print("✅ Antioch Map Demo loaded!")


if __name__ == "__main__":
    main()
