"""
Google Map Demo - Interactive Google Maps integration

This demo showcases the GoogleMap macro which provides integration
with Google Maps JavaScript API.

Features demonstrated:
- Creating a Google Map with API key
- Adding markers with info windows
- Map controls and interactions
- Different map types (roadmap, satellite, hybrid, terrain)
- Event handling (@when decorator)
- Shapes (circles, polygons, polylines)
- Programmatic map control
"""

from antioch import *
from antioch.macros import GoogleMap


def main():
    """Main demo function."""

    # IMPORTANT: Replace with your own Google Maps API key
    # Get one at: https://developers.google.com/maps/documentation/javascript/get-api-key
    API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE"

    # Check if API key is set
    if API_KEY == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
        DOM.add(
            Div(
                H1("Google Map Demo", style={"color": "#4285F4"}),
                Div(
                    H2("⚠️ API Key Required"),
                    P("To use this demo, you need a Google Maps API key."),
                    P("Get one at:", style={"margin": "10px 0"}),
                    A(
                        "https://developers.google.com/maps/documentation/javascript/get-api-key",
                        href="https://developers.google.com/maps/documentation/javascript/get-api-key",
                        target="_blank",
                        style={
                            "color": "#4285F4",
                            "text-decoration": "none",
                            "font-weight": "bold"
                        }
                    ),
                    P("Then replace 'YOUR_GOOGLE_MAPS_API_KEY_HERE' in the code with your key.",
                      style={"margin-top": "20px"}),
                    style={
                        "background-color": "#fff3cd",
                        "border": "1px solid #ffc107",
                        "border-radius": "4px",
                        "padding": "20px",
                        "margin": "20px 0",
                        "max-width": "600px"
                    }
                ),
                style={
                    "padding": "20px",
                    "font-family": "Arial, sans-serif"
                }
            )
        )
        return

    # Page title
    DOM.add(
        H1("Google Map Demo", style={
            "color": "#4285F4",
            "text-align": "center",
            "margin": "20px 0"
        })
    )

    # Info section
    DOM.add(
        Div(
            P("This demo shows Google Maps integration with markers, shapes, and event handling."),
            style={
                "text-align": "center",
                "color": "#666",
                "margin-bottom": "20px"
            }
        )
    )

    # Create the Google Map (centered on San Francisco)
    google_map = GoogleMap(
        api_key=API_KEY,
        center={"lat": 37.7749, "lng": -122.4194},
        zoom=12,
        width="900px",
        height="500px",
        map_type="roadmap"
    )

    DOM.add(google_map.element)

    # Status display
    status_display = Div(
        "Map loading...",
        style={
            "margin-top": "10px",
            "padding": "10px",
            "background-color": "#f0f0f0",
            "border-radius": "4px",
            "text-align": "center",
            "font-family": "monospace"
        }
    )
    DOM.add(status_display)

    # Wait for map to be ready before adding markers
    @when(google_map.events.ready)
    def on_map_ready(sender, event):
        status_display.set_text("✓ Map ready! Click the map to add markers.")

        # Add some initial markers with info windows
        google_map.add_marker(
            37.7749, -122.4194,
            title="San Francisco",
            label="SF",
            animation="drop",
            info_content="<h3>San Francisco</h3><p>The Golden Gate City</p>"
        )

        google_map.add_marker(
            37.8199, -122.4783,
            title="Golden Gate Bridge",
            label="GGB",
            animation="drop",
            info_content="<h3>Golden Gate Bridge</h3><p>Iconic suspension bridge</p>"
        )

        google_map.add_marker(
            37.8080, -122.4177,
            title="Alcatraz Island",
            label="AI",
            animation="drop",
            info_content="<h3>Alcatraz Island</h3><p>Historic federal prison</p>"
        )

        # Add a circle around San Francisco
        google_map.add_circle(
            37.7749, -122.4194,
            radius=5000,  # 5km radius
            stroke_color="#4285F4",
            fill_color="#4285F4",
            fill_opacity=0.2
        )

        # Add a polygon (triangle around SF landmarks)
        google_map.add_polygon(
            [
                {"lat": 37.7749, "lng": -122.4194},  # SF
                {"lat": 37.8199, "lng": -122.4783},  # GGB
                {"lat": 37.8080, "lng": -122.4177}   # Alcatraz
            ],
            stroke_color="#FF0000",
            fill_color="#FF0000",
            fill_opacity=0.15
        )

    # Handle map clicks to add new markers
    @when(google_map.events.click)
    def on_map_click(sender, event_data):
        lat = event_data['lat']
        lng = event_data['lng']

        google_map.add_marker(
            lat, lng,
            title=f"Marker at ({lat:.4f}, {lng:.4f})",
            draggable=True,
            animation="drop",
            info_content=f"<p><b>Custom Marker</b></p><p>Lat: {lat:.4f}<br>Lng: {lng:.4f}</p>"
        )

        status_display.set_text(f"Added marker at: ({lat:.4f}, {lng:.4f})")

    # Handle marker clicks
    @when(google_map.events.marker_click)
    def on_marker_click(sender, event_data):
        lat = event_data['lat']
        lng = event_data['lng']
        status_display.set_text(f"Marker clicked at: ({lat:.4f}, {lng:.4f})")

    # Handle zoom changes
    @when(google_map.events.zoom_changed)
    def on_zoom_change(sender, zoom_level):
        status_display.set_text(f"Zoom level: {zoom_level}")

    # Control panel
    controls = Div(style={
        "margin-top": "20px",
        "padding": "15px",
        "background-color": "#f8f9fa",
        "border-radius": "4px",
        "text-align": "center"
    })
    DOM.add(controls)

    controls.add(H3("Map Controls", style={"margin-top": "0"}))

    # Map type buttons
    button_style = {
        "padding": "10px 20px",
        "margin": "5px",
        "font-size": "14px",
        "cursor": "pointer",
        "background-color": "#4285F4",
        "color": "white",
        "border": "none",
        "border-radius": "4px"
    }

    roadmap_btn = Button("Roadmap", style=button_style)
    satellite_btn = Button("Satellite", style=button_style)
    hybrid_btn = Button("Hybrid", style=button_style)
    terrain_btn = Button("Terrain", style=button_style)

    @when(roadmap_btn.events.click)
    def set_roadmap(sender, event):
        google_map.set_map_type("roadmap")
        status_display.set_text("Map type: Roadmap")

    @when(satellite_btn.events.click)
    def set_satellite(sender, event):
        google_map.set_map_type("satellite")
        status_display.set_text("Map type: Satellite")

    @when(hybrid_btn.events.click)
    def set_hybrid(sender, event):
        google_map.set_map_type("hybrid")
        status_display.set_text("Map type: Hybrid")

    @when(terrain_btn.events.click)
    def set_terrain(sender, event):
        google_map.set_map_type("terrain")
        status_display.set_text("Map type: Terrain")

    controls.add(
        Div(
            Strong("Map Type: "),
            roadmap_btn,
            satellite_btn,
            hybrid_btn,
            terrain_btn,
            style={"margin": "10px 0"}
        )
    )

    # Zoom controls
    zoom_in_btn = Button("Zoom In", style=button_style)
    zoom_out_btn = Button("Zoom Out", style=button_style)

    @when(zoom_in_btn.events.click)
    def zoom_in(sender, event):
        google_map.zoom_in()

    @when(zoom_out_btn.events.click)
    def zoom_out(sender, event):
        google_map.zoom_out()

    controls.add(
        Div(
            Strong("Zoom: "),
            zoom_in_btn,
            zoom_out_btn,
            style={"margin": "10px 0"}
        )
    )

    # Clear markers button
    clear_btn = Button("Clear All Markers", style={
        **button_style,
        "background-color": "#dc3545"
    })

    @when(clear_btn.events.click)
    def clear_markers(sender, event):
        google_map.clear_markers()
        status_display.set_text("All markers cleared")

    # Jump to locations
    sf_btn = Button("San Francisco", style=button_style)
    nyc_btn = Button("New York", style=button_style)
    london_btn = Button("London", style=button_style)
    tokyo_btn = Button("Tokyo", style=button_style)

    @when(sf_btn.events.click)
    def go_to_sf(sender, event):
        google_map.pan_to(37.7749, -122.4194)
        google_map.set_zoom(12)
        status_display.set_text("Moved to: San Francisco")

    @when(nyc_btn.events.click)
    def go_to_nyc(sender, event):
        google_map.pan_to(40.7128, -74.0060)
        google_map.set_zoom(12)
        status_display.set_text("Moved to: New York")

    @when(london_btn.events.click)
    def go_to_london(sender, event):
        google_map.pan_to(51.5074, -0.1278)
        google_map.set_zoom(12)
        status_display.set_text("Moved to: London")

    @when(tokyo_btn.events.click)
    def go_to_tokyo(sender, event):
        google_map.pan_to(35.6762, 139.6503)
        google_map.set_zoom(12)
        status_display.set_text("Moved to: Tokyo")

    controls.add(
        Div(
            Strong("Jump to: "),
            sf_btn,
            nyc_btn,
            london_btn,
            tokyo_btn,
            style={"margin": "10px 0"}
        )
    )

    controls.add(
        Div(
            clear_btn,
            style={"margin-top": "15px"}
        )
    )

    # Instructions
    DOM.add(
        Div(
            H3("Instructions:"),
            Ul(
                Li("Click anywhere on the map to add a draggable marker"),
                Li("Click on markers to see their info windows"),
                Li("Use the controls above to change map type and zoom"),
                Li("Jump to different cities around the world"),
                Li("Clear all markers with the red button")
            ),
            style={
                "margin-top": "20px",
                "padding": "15px",
                "background-color": "#e7f3ff",
                "border-radius": "4px",
                "max-width": "600px",
                "margin-left": "auto",
                "margin-right": "auto"
            }
        )
    )


if __name__ == "__main__":
    main()