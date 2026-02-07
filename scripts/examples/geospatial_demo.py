"""
Geospatial Demo - Showcase shapefile and GeoTIFF overlay capabilities.
Demonstrates loading and displaying shapefiles and GeoTIFF raster data on maps.
"""

from antioch import *
from antioch.macros import Map, FileUpload, FileSelect, Tabs, Tab
from antioch.core import get_filesystem, LocalStorageBackend
import js

def main():
    """Main entry point for Geospatial demo."""
    # Initialize filesystem
    fs = get_filesystem(LocalStorageBackend())
    _ensure_directories(fs)

    # Create page container
    page = Div(style={
        "max_width": "1400px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Add title
    title = H1("Antioch Geospatial Data Demo", style={
        "color": "#333",
        "margin_bottom": "10px"
    })
    page.add(title)

    # Add description
    description = P(
        "Demonstration of shapefile and GeoTIFF overlay capabilities. Upload files or load from URLs.",
        style={"color": "#666", "margin_bottom": "30px"}
    )
    page.add(description)

    # ============================================================================
    # DEMO 1: Shapefile Overlay
    # ============================================================================

    section1 = Div(style={"margin_bottom": "40px"})
    section1.add(H2("Shapefile Overlay", style={"color": "#444", "margin_bottom": "10px"}))
    section1.add(P(
        "Load and display shapefile data (.shp) on the map. Shapefiles are a popular format for vector GIS data.",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Create map for shapefile demo
    map1 = Map(
        center=[40.7128, -74.0060],  # New York City
        zoom=10,
        height="500px",
        tile_layer="CartoDB"
    )
    section1.add(map1)

    # Store loaded layers for cleanup
    loaded_layers = {"shapefile": None, "geotiff": None}

    # Define shapefile loading function (used by both URL and file methods)
    def load_shapefile_from_source(url_or_blob):
        """Load shapefile from URL or Blob."""
        # Clear previous layer if exists
        if loaded_layers["shapefile"]:
            map1.remove_layer(loaded_layers["shapefile"])

        # Define style for shapefile features
        style_options = {
            "color": "#ff7800",
            "weight": 2,
            "fillColor": "#ffaa00",
            "fillOpacity": 0.4
        }

        # Define callback for each feature
        def on_feature(feature, layer):
            if hasattr(feature, 'properties'):
                props = feature.properties
                popup_html = "<div style='max-width:200px;'>"
                popup_html += "<b>Feature Properties:</b><br>"
                try:
                    for key in dir(props):
                        if not key.startswith('_'):
                            value = getattr(props, key)
                            if not callable(value):
                                popup_html += f"{key}: {value}<br>"
                except:
                    popup_html += "No properties available"
                popup_html += "</div>"
                layer.bindPopup(popup_html)

        # Load shapefile with layer name
        layer_name = "Shapefile Layer"
        if isinstance(url_or_blob, str) and '/' in url_or_blob:
            # Extract filename from URL
            layer_name = url_or_blob.split('/')[-1].replace('.zip', '')

        promise = map1.add_shapefile(
            url_or_blob,
            name=layer_name,
            style_options=style_options,
            on_each_feature=on_feature,
            add_to_control=True
        )
        if promise:
            print(f"Shapefile loading initiated from: {url_or_blob}")
            # Store the promise to track the layer
            def on_loaded(layer):
                loaded_layers["shapefile"] = layer
                print(f"✓ Shapefile '{layer_name}' loaded")
            from pyodide.ffi import create_proxy
            promise.then(create_proxy(on_loaded))

    # Tabbed controls for different loading methods
    # Tab 1: Load from URL
    url_tab_content = Div(style={"padding": "15px"})

    url_controls = Div(style={
        "display": "flex",
        "gap": "10px",
        "align_items": "center",
        "flex_wrap": "wrap",
        "margin_bottom": "10px"
    })

    url_controls.add(Label("Shapefile URL (.zip):", style={"font_weight": "bold"}))

    input1 = Input(style={
        "flex": "1",
        "min_width": "300px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border_radius": "4px"
    })
    input1.set_attribute("placeholder", "https://example.com/data.zip")
    url_controls.add(input1)

    load_btn1 = Button("Load from URL", style={
        "padding": "8px 16px",
        "background_color": "#007bff",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })

    def load_from_url(event):
        url = input1.value
        if not url:
            print("Please enter a shapefile URL")
            return
        load_shapefile_from_source(url)

    load_btn1.on_click(load_from_url)
    url_controls.add(load_btn1)

    url_tab_content.add(url_controls)
    url_tab_content.add(P(
        "Note: Shapefile must be a .zip archive containing .shp, .shx, and .dbf files. "
        "Try public datasets from Natural Earth Data or similar sources.",
        style={"color": "#666", "font_size": "0.9em", "font_style": "italic"}
    ))

    # Tab 2: Upload File
    upload_tab_content = Div(style={"padding": "15px"})

    shapefile_selector = None  # Will be set below

    def on_shapefile_upload(file_path, success):
        if success:
            print(f"✅ Shapefile uploaded: {file_path}")
            if shapefile_selector:
                shapefile_selector.refresh()

    shapefile_uploader = FileUpload(
        destination_path=['maps', 'shapefiles'],
        allowed_extensions=['.zip'],
        max_size_mb=100,
        on_upload=on_shapefile_upload,
        multiple=False
    )
    upload_tab_content.add(shapefile_uploader)

    # Tab 3: Select from VFS
    select_tab_content = Div(style={"padding": "15px"})

    def on_shapefile_selected(file_path, file_content):
        if file_content:
            print(f"Selected shapefile: {file_path}")
            # Create a Blob from the file content
            uint8_array = js.Uint8Array.new(file_content)
            blob = js.Blob.new([uint8_array], js.Object.new(type="application/zip"))
            blob_url = js.URL.createObjectURL(blob)
            load_shapefile_from_source(blob_url)

    shapefile_selector = FileSelect(
        on_select=on_shapefile_selected,
        file_filter=['.zip'],
        height='300px'
    )
    select_tab_content.add(shapefile_selector)

    # Create tabs
    shapefile_tabs = Tabs([
        Tab("Load from URL", url_tab_content),
        Tab("Upload File", upload_tab_content),
        Tab("Select from VFS", select_tab_content)
    ])

    section1.add(shapefile_tabs)

    # Add zoom button for shapefile map
    shapefile_btn_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px"
    })
    zoom_shapefile_btn = Button("Zoom to Fit Layers", style={
        "padding": "8px 16px",
        "background_color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_shapefile_btn.on_click(lambda e: map1.zoom_to_layers(padding=20))
    shapefile_btn_container.add(zoom_shapefile_btn)
    section1.add(shapefile_btn_container)

    page.add(section1)

    # ============================================================================
    # DEMO 2: GeoTIFF Raster Overlay
    # ============================================================================

    section2 = Div(style={"margin_bottom": "40px"})
    section2.add(H2("GeoTIFF Raster Overlay", style={"color": "#444", "margin_bottom": "10px"}))
    section2.add(P(
        "Display GeoTIFF raster data on the map. GeoTIFF is commonly used for elevation data, satellite imagery, and other gridded datasets.",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Create map for GeoTIFF demo
    map2 = Map(
        center=[37.7749, -122.4194],  # San Francisco
        zoom=10,
        height="500px",
        tile_layer="Satellite"
    )
    section2.add(map2)

    # Define GeoTIFF loading function
    def load_geotiff_from_source(url_or_blob, opacity=0.7):
        """Load GeoTIFF from URL or Blob."""
        # Clear previous layer if exists
        if loaded_layers["geotiff"]:
            map2.remove_layer(loaded_layers["geotiff"])

        # Extract layer name from URL
        layer_name = "GeoTIFF Layer"
        if isinstance(url_or_blob, str) and '/' in url_or_blob:
            layer_name = url_or_blob.split('/')[-1]

        print(f"GeoTIFF loading initiated from: {url_or_blob}")

        # Custom colormap for RGB satellite imagery
        # Track min/max values for auto-scaling - separate for each band
        value_stats = {'count': 0, 'r_samples': [], 'g_samples': [], 'b_samples': []}

        def satellite_colormap(values):
            """Convert satellite imagery values to RGB colors with per-band auto-scaling."""
            if not values or len(values) == 0:
                return [0, 0, 0, 0]  # Transparent

            # Sample first 1000 pixels to determine value range PER BAND
            if value_stats['count'] < 1000:
                value_stats['count'] += 1
                if len(values) >= 3:
                    value_stats['r_samples'].append(values[0])
                    value_stats['g_samples'].append(values[1])
                    value_stats['b_samples'].append(values[2])

                # After 1000 samples, compute statistics PER BAND
                if value_stats['count'] == 1000:
                    # Red band
                    r_sorted = sorted(value_stats['r_samples'])
                    value_stats['r_min'] = r_sorted[int(len(r_sorted) * 0.02)]
                    value_stats['r_max'] = r_sorted[int(len(r_sorted) * 0.98)]

                    # Green band
                    g_sorted = sorted(value_stats['g_samples'])
                    value_stats['g_min'] = g_sorted[int(len(g_sorted) * 0.02)]
                    value_stats['g_max'] = g_sorted[int(len(g_sorted) * 0.98)]

                    # Blue band
                    b_sorted = sorted(value_stats['b_samples'])
                    value_stats['b_min'] = b_sorted[int(len(b_sorted) * 0.02)]
                    value_stats['b_max'] = b_sorted[int(len(b_sorted) * 0.98)]

            # Handle RGB imagery (3+ bands)
            if len(values) >= 3:
                r, g, b = values[0], values[1], values[2]

                # Make very dark pixels transparent (no-data)
                if r < 10 and g < 10 and b < 10:
                    return [0, 0, 0, 0]

                # Use per-band auto-detected range if available
                if 'r_min' in value_stats:
                    r_min = value_stats['r_min']
                    r_max = value_stats['r_max']
                    r_range = r_max - r_min if r_max > r_min else 1.0

                    g_min = value_stats['g_min']
                    g_max = value_stats['g_max']
                    g_range = g_max - g_min if g_max > g_min else 1.0

                    b_min = value_stats['b_min']
                    b_max = value_stats['b_max']
                    b_range = b_max - b_min if b_max > b_min else 1.0

                    r = int((r - r_min) / r_range * 255)
                    g = int((g - g_min) / g_range * 255)
                    b = int((b - b_min) / b_range * 255)
                else:
                    # Fallback: assume 0-2000 range
                    r = int(r * 255 / 2000)
                    g = int(g * 255 / 2000)
                    b = int(b * 255 / 2000)

                # Clamp to 0-255
                r = min(255, max(0, r))
                g = min(255, max(0, g))
                b = min(255, max(0, b))

                return [r, g, b, 255]
            else:
                # Grayscale (single band)
                val = values[0]

                # Use auto-detected range if available
                if 'r_min' in value_stats:
                    vmin = value_stats['r_min']
                    vmax = value_stats['r_max']
                    vrange = vmax - vmin if vmax > vmin else 1.0
                    val = int((val - vmin) / vrange * 255)
                else:
                    val = int(val * 255 / 2000) if val > 2000 else int(val)

                val = min(255, max(0, val))
                return [val, val, val, 255]

        # Load GeoTIFF with PNG conversion approach
        layer = map2.add_geotiff(
            url_or_blob,
            name=layer_name,
            opacity=opacity,
            colormap=satellite_colormap,
            add_to_control=True
        )
        # Layer will be added asynchronously

    # Tabbed controls for different loading methods
    # Tab 1: Load from URL
    geotiff_url_tab = Div(style={"padding": "15px"})

    url_controls2 = Div(style={
        "display": "flex",
        "gap": "10px",
        "align_items": "center",
        "flex_wrap": "wrap",
        "margin_bottom": "10px"
    })

    url_controls2.add(Label("GeoTIFF URL:", style={"font_weight": "bold"}))

    input2 = Input(style={
        "flex": "1",
        "min_width": "250px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border_radius": "4px"
    })
    input2.set_attribute("placeholder", "https://example.com/elevation.tif")
    url_controls2.add(input2)

    url_controls2.add(Label("Opacity:", style={"font_weight": "bold"}))

    opacity_input = Input(style={
        "width": "80px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border_radius": "4px"
    })
    opacity_input.set_attribute("type", "number")
    opacity_input.set_attribute("min", "0")
    opacity_input.set_attribute("max", "1")
    opacity_input.set_attribute("step", "0.1")
    opacity_input.set_attribute("value", "0.7")
    url_controls2.add(opacity_input)

    load_btn2 = Button("Load from URL", style={
        "padding": "8px 16px",
        "background_color": "#28a745",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })

    def load_from_url2(event):
        url = input2.value
        if not url:
            print("Please enter a GeoTIFF URL")
            return
        try:
            opacity = float(opacity_input.value)
        except:
            opacity = 0.7
        load_geotiff_from_source(url, opacity)

    load_btn2.on_click(load_from_url2)
    url_controls2.add(load_btn2)

    geotiff_url_tab.add(url_controls2)

    # Add test button for sample.tif
    test_btn_container = Div(style={"margin_top": "10px"})
    test_sample_btn = Button("Load Test Sample (assets/sample_2.tif)", style={
        "padding": "8px 16px",
        "background_color": "#6c757d",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    def load_test_sample(e):
        load_geotiff_from_source("assets/sample_2.tif", 1.0)
    test_sample_btn.on_click(load_test_sample)
    test_btn_container.add(test_sample_btn)
    geotiff_url_tab.add(test_btn_container)

    geotiff_url_tab.add(P(
        "Note: GeoTIFF rendering uses automatic colormap for single-band data (grayscale) and true color for RGB data. "
        "Use files with embedded georeferencing information. "
        "Try public datasets from USGS Earth Explorer, Copernicus Open Access Hub, or similar sources.",
        style={"color": "#666", "font_size": "0.9em", "font_style": "italic"}
    ))

    # Tab 2: Upload File
    geotiff_upload_tab = Div(style={"padding": "15px"})

    geotiff_selector = None  # Will be set below

    def on_geotiff_upload(file_path, success):
        if success:
            print(f"✅ GeoTIFF uploaded: {file_path}")
            if geotiff_selector:
                geotiff_selector.refresh()

    geotiff_uploader = FileUpload(
        destination_path=['maps', 'geotiff'],
        allowed_extensions=['.tif', '.tiff', '.geotiff'],
        max_size_mb=200,
        on_upload=on_geotiff_upload,
        multiple=False
    )
    geotiff_upload_tab.add(geotiff_uploader)

    # Tab 3: Select from VFS
    geotiff_select_tab = Div(style={"padding": "15px"})

    # Opacity control for VFS selection
    vfs_opacity_div = Div(style={
        "display": "flex",
        "gap": "10px",
        "align_items": "center",
        "margin_bottom": "15px"
    })
    vfs_opacity_div.add(Label("Opacity:", style={"font_weight": "bold"}))

    vfs_opacity_input = Input(style={
        "width": "80px",
        "padding": "8px",
        "border": "1px solid #ccc",
        "border_radius": "4px"
    })
    vfs_opacity_input.set_attribute("type", "number")
    vfs_opacity_input.set_attribute("min", "0")
    vfs_opacity_input.set_attribute("max", "1")
    vfs_opacity_input.set_attribute("step", "0.1")
    vfs_opacity_input.set_attribute("value", "0.7")
    vfs_opacity_div.add(vfs_opacity_input)

    geotiff_select_tab.add(vfs_opacity_div)

    def on_geotiff_selected(file_path, file_content):
        if file_content:
            print(f"Selected GeoTIFF: {file_path}")
            try:
                opacity = float(vfs_opacity_input.value)
            except:
                opacity = 0.7
            # Create a Blob from the file content
            uint8_array = js.Uint8Array.new(file_content)
            blob = js.Blob.new([uint8_array], js.Object.new(type="image/tiff"))
            blob_url = js.URL.createObjectURL(blob)
            load_geotiff_from_source(blob_url, opacity)

    geotiff_selector = FileSelect(
        on_select=on_geotiff_selected,
        file_filter=['.tif', '.tiff', '.geotiff'],
        height='250px'
    )
    geotiff_select_tab.add(geotiff_selector)

    # Create tabs
    geotiff_tabs = Tabs([
        Tab("Load from URL", geotiff_url_tab),
        Tab("Upload File", geotiff_upload_tab),
        Tab("Select from VFS", geotiff_select_tab)
    ])

    section2.add(geotiff_tabs)

    # Add zoom button for GeoTIFF map
    geotiff_btn_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px"
    })
    zoom_geotiff_btn = Button("Zoom to Fit Layers", style={
        "padding": "8px 16px",
        "background_color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_geotiff_btn.on_click(lambda e: map2.zoom_to_layers(padding=20))
    geotiff_btn_container.add(zoom_geotiff_btn)
    section2.add(geotiff_btn_container)

    page.add(section2)

    # ============================================================================
    # DEMO 3: GeoJSON Overlay (Bonus)
    # ============================================================================

    section3 = Div(style={"margin_bottom": "40px"})
    section3.add(H2("GeoJSON Overlay", style={"color": "#444", "margin_bottom": "10px"}))
    section3.add(P(
        "Display GeoJSON data on the map. GeoJSON is a widely-used format for encoding geographic data structures.",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Create map for GeoJSON demo
    map3 = Map(
        center=[51.505, -0.09],  # London
        zoom=11,
        height="500px",
        tile_layer="OpenStreetMap"
    )

    # Example GeoJSON data (London parks)
    def add_example_geojson(map_instance):
        geojson_data = js.JSON.parse('''{
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Hyde Park",
                        "type": "Park"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-0.165, 51.508],
                            [-0.165, 51.513],
                            [-0.158, 51.513],
                            [-0.158, 51.508],
                            [-0.165, 51.508]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Regent's Park",
                        "type": "Park"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-0.158, 51.525],
                            [-0.158, 51.530],
                            [-0.151, 51.530],
                            [-0.151, 51.525],
                            [-0.158, 51.525]
                        ]]
                    }
                }
            ]
        }''')

        # Style options
        style = {
            "color": "#2ecc71",
            "weight": 2,
            "fillColor": "#27ae60",
            "fillOpacity": 0.3
        }

        # Feature callback for popups
        def on_feature(feature, layer):
            if hasattr(feature, 'properties') and hasattr(feature.properties, 'name'):
                name = feature.properties.name
                park_type = feature.properties.type if hasattr(feature.properties, 'type') else 'Area'
                layer.bindPopup(f"<b>{name}</b><br>Type: {park_type}")

        # Add GeoJSON layer with name for layer control
        map_instance.add_geojson(
            geojson_data,
            name="London Parks",
            style_options=style,
            on_each_feature=on_feature,
            add_to_control=True
        )
        print("Example GeoJSON added to map")

    map3.on_ready(add_example_geojson)

    section3.add(map3)

    # Add zoom button for GeoJSON map
    geojson_btn_container = Div(style={
        "margin_top": "10px",
        "display": "flex",
        "gap": "10px"
    })
    zoom_geojson_btn = Button("Zoom to Fit Layers", style={
        "padding": "8px 16px",
        "background_color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_geojson_btn.on_click(lambda e: map3.zoom_to_layers(padding=20))
    geojson_btn_container.add(zoom_geojson_btn)
    section3.add(geojson_btn_container)

    # Info box
    info_box = Div(style={
        "margin_top": "15px",
        "padding": "15px",
        "background": "#e7f3ff",
        "border_left": "4px solid #007bff",
        "border_radius": "4px"
    })
    info_text = P(style={"margin": "0", "color": "#333"})
    info_text.add(
        I("GeoJSON Features:"),
        " This example shows programmatically added GeoJSON data. "
        "You can also load GeoJSON from URLs or create complex geographic features with properties and styling."
    )
    info_box.add(info_text)
    section3.add(info_box)

    page.add(section3)

    # ============================================================================
    # DEMO 4: Combined Overlays
    # ============================================================================

    section4 = Div(style={"margin_bottom": "40px"})
    section4.add(H2("Combined Overlays", style={"color": "#444", "margin_bottom": "10px"}))
    section4.add(P(
        "Layer multiple data types on a single map. Combine vector and raster data for comprehensive visualization.",
        style={"color": "#666", "margin_bottom": "15px"}
    ))

    # Create map with combined overlays
    map4 = Map(
        center=[39.8283, -98.5795],  # Center of USA
        zoom=4,
        height="500px",
        tile_layer="CartoDB"
    )

    def add_example_data(map_instance):
        # Add some example circles representing cities
        cities = [
            {"name": "New York", "lat": 40.7128, "lng": -74.0060, "pop": 8419000},
            {"name": "Los Angeles", "lat": 34.0522, "lng": -118.2437, "pop": 3898000},
            {"name": "Chicago", "lat": 41.8781, "lng": -87.6298, "pop": 2716000},
            {"name": "Houston", "lat": 29.7604, "lng": -95.3698, "pop": 2328000},
            {"name": "Phoenix", "lat": 33.4484, "lng": -112.0740, "pop": 1690000}
        ]

        for city in cities:
            # Scale radius by population (sqrt for better visual)
            radius = (city["pop"] / 1000000) ** 0.5 * 50000  # meters
            map_instance.add_circle(
                city["lat"], city["lng"],
                radius=radius,
                color="#e74c3c",
                fill_color="#e74c3c",
                fill_opacity=0.3
            )
            map_instance.add_marker(
                city["lat"], city["lng"],
                f"<b>{city['name']}</b><br>Population: {city['pop']:,}"
            )

        print("Example overlay data added")

    map4.on_ready(add_example_data)

    section4.add(map4)

    # Control panel
    control_panel = Div(style={
        "margin_top": "15px",
        "padding": "15px",
        "background": "#f8f9fa",
        "border_radius": "4px",
        "display": "flex",
        "gap": "10px",
        "flex_wrap": "wrap"
    })

    clear_all_btn = Button("Clear All Layers", style={
        "padding": "8px 16px",
        "background_color": "#dc3545",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    clear_all_btn.on_click(lambda e: map4.clear_layers())
    control_panel.add(clear_all_btn)

    clear_markers_btn = Button("Clear Markers", style={
        "padding": "8px 16px",
        "background_color": "#ffc107",
        "color": "black",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    clear_markers_btn.on_click(lambda e: map4.clear_markers())
    control_panel.add(clear_markers_btn)

    zoom_combined_btn = Button("Zoom to Fit Layers", style={
        "padding": "8px 16px",
        "background_color": "#17a2b8",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer"
    })
    zoom_combined_btn.on_click(lambda e: map4.zoom_to_layers(padding=20))
    control_panel.add(zoom_combined_btn)

    section4.add(control_panel)
    page.add(section4)

    # ============================================================================
    # Information Section
    # ============================================================================

    info_section = Div(style={
        "margin_top": "40px",
        "padding": "20px",
        "background": "#f8f9fa",
        "border_radius": "4px"
    }).add(
        H3("Using Geospatial Data", style={"color": "#333", "margin_bottom": "15px"}),
        Div(style={"color": "#555", "line_height": "1.8"}).add(
            P().add(
                B("Shapefiles:"),
                " Vector data format for geographic features. Must be zipped with .shp, .shx, and .dbf files."),
            P().add(
                B("GeoTIFF:"),
                " Raster format with embedded georeference information. Supports multiple bands and data types."),
            P().add(
                B("GeoJSON:"),
                " Text-based format using JSON to encode geographic data structures. Web-friendly and human-readable."),
            P().add(
                B("Styling:"),
                " Customize colors, opacity, line weights, and fill patterns for all layer types."),
            P().add(
                B("Interactions:"),
                " Add popups, tooltips, and click handlers to make maps interactive.")
        ),
        Div(style={"margin_top": "20px"}).add(
            H3("Public Data Sources", style={"color": "#333", "margin_bottom": "10px"}),
            P("Find free geospatial data at:", style={"margin_bottom": "5px"}),
            Div(style={"color": "#555", "line_height": "1.8", "margin_left": "20px"}).add(
                P("• Natural Earth Data - naturalearthdata.com"),
                P("• USGS Earth Explorer - earthexplorer.usgs.gov"),
                P("• Copernicus Open Access Hub - scihub.copernicus.eu"),
                P("• OpenStreetMap Data Extracts - download.geofabrik.de"),
                P("• NOAA Digital Coast - ", A("coast.noaa.gov/digitalcoast", href="https://coast.noaa.gov/digitalcoast"))
            )
        )
    )


    page.add(info_section)

    DOM.add(page)

    print("✅ Antioch Geospatial Demo loaded!")


def _ensure_directories(fs):
    """Ensure required directories exist in the VFS."""
    fs.navigate_to([])

    # Create maps directory and subdirectories
    directories = [
        ['maps'],
        ['maps', 'shapefiles'],
        ['maps', 'geotiff'],
        ['documents']
    ]

    for dir_path in directories:
        try:
            current = fs.root
            for dir_name in dir_path:
                if dir_name not in current.children:
                    fs.navigate_to(dir_path[:dir_path.index(dir_name)])
                    fs.create_directory(dir_name)
                current = fs.root
                for segment in dir_path:
                    current = current.children.get(segment)
                    if not current:
                        break
        except Exception as e:
            pass  # Directory might already exist

    fs.navigate_to([])


if __name__ == "__main__":
    main()