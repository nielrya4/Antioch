"""
Map macro - An interactive map component using Leaflet.
Provides mapping, markers, popups, and geolocation features.
"""
import js
from pyodide.ffi import create_proxy
from .base import Macro
from ..elements import Div
from ..lib.loader import inject_script, inject_stylesheet

# Ensure Leaflet and GIS libraries are loaded when this module is imported
inject_stylesheet('antioch/lib/vendor/leaflet.css')
inject_script('antioch/lib/vendor/leaflet.js')
inject_script('antioch/lib/vendor/shp.js')
inject_script('antioch/lib/vendor/georaster.browser.bundle.min.js')
inject_script('antioch/lib/vendor/georaster-layer-for-leaflet.min.js')
inject_script('antioch/lib/vendor/proj4.js')
inject_script('antioch/lib/vendor/geotiff.js')


class Map(Macro):
    """
    An interactive map component powered by Leaflet.
    Supports markers, popups, tiles, and various map interactions.
    """

    def __init__(self, center=None, zoom=13, width="100%", height="400px",
                 tile_layer="OpenStreetMap", show_layer_control=True, container_style=None, **kwargs):
        """
        Initialize a map component.

        Args:
            center: [lat, lon] coordinates for map center (defaults to [51.505, -0.09])
            zoom: Initial zoom level (1-18)
            width: Width of map container
            height: Height of map container
            tile_layer: Tile layer to use ('OpenStreetMap', 'CartoDB', 'Satellite')
            show_layer_control: Whether to show layer control widget (default: True)
            container_style: Custom styles for map container
        """
        # Initialize base macro
        super().__init__(macro_type="map", **kwargs)

        # Default center (London)
        if center is None:
            center = [51.505, -0.09]

        # Set up state
        self._set_state(
            center=center,
            zoom=zoom,
            width=width,
            height=height,
            tile_layer=tile_layer,
            show_layer_control=show_layer_control,  # Whether to show layer control
            map_instance=None,
            markers=[],
            layers=[],
            layer_control=None,  # Leaflet layer control instance (lazy init)
            overlay_layers={},  # Dict of layer name -> layer object for control
            initialized=False,
            init_retry_count=0
        )

        # Store references to proxied callbacks for cleanup
        self._map_callbacks = {}

        # Add callback types
        self._add_callback_type('click')
        self._add_callback_type('zoom')
        self._add_callback_type('move')
        self._add_callback_type('ready')

        # Default container style
        default_container_style = {
            "width": width,
            "height": height,
            "border": "1px solid #ccc",
            "border_radius": "4px",
            "overflow": "hidden",
            "position": "relative",
            "z_index": "1"
        }

        # Merge with user styles
        self._container_style = self._merge_styles(default_container_style, container_style)

        # Initialize macro
        self._init_macro()

    def _create_elements(self):
        """Create the map container element."""
        # Create container with unique ID for Leaflet
        container = self._register_element('container',
                                           self._create_container(self._container_style))

        # Set the ID both via set_attribute and directly on the DOM element
        container.set_attribute("id", self._id)

        # Also set it directly on the DOM element to ensure it's available
        if container._dom_element:
            container._dom_element.id = self._id

        # Initialize map after a longer delay to ensure DOM is fully ready
        # We need to wait for the element to be in the document
        init_proxy = create_proxy(lambda: self._initialize_map())
        js.setTimeout(init_proxy, 500)

        return container

    def _initialize_map(self):
        """Initialize the Leaflet map instance."""
        if self._get_state('initialized'):
            return

        # Check retry count to prevent infinite loops
        retry_count = self._get_state('init_retry_count')

        if retry_count > 50:  # Stop after 50 retries
            return

        try:
            # Check if Leaflet is loaded
            if not hasattr(js, 'L') or not js.L:
                # Leaflet not loaded yet, retry
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_map())
                js.setTimeout(init_proxy, 100)
                return

            container = self._get_element('container')
            if not container or not container._dom_element:
                # Container element not ready yet
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_map())
                js.setTimeout(init_proxy, 100)
                return

            # Create Leaflet map instance
            center = self._get_state('center')
            zoom = self._get_state('zoom')

            # Initialize map using the DOM element directly
            map_instance = js.L.map(container._dom_element)

            # Convert Python list to JavaScript array for Leaflet
            js_center = js.Array.new()
            js_center.push(center[0])
            js_center.push(center[1])
            map_instance.setView(js_center, zoom)

            # Add tile layer
            self._add_tile_layer(map_instance)

            # Store map instance
            self._set_state(map_instance=map_instance, initialized=True)

            # Force Leaflet to recalculate size after DOM settles
            def invalidate_later():
                map_instance.invalidateSize()

            invalidate_proxy = create_proxy(invalidate_later)
            js.setTimeout(invalidate_proxy, 100)

            # Setup event handlers
            self._setup_map_events(map_instance)

            # Note: Layer control is initialized lazily when first layer is added

            # Trigger ready callback
            self._trigger_callbacks('ready')

        except Exception as e:
            # Initialization failed, retry
            error_msg = str(e)

            # Don't retry if container is already initialized
            if "already initialized" in error_msg:
                return

            self._set_state(init_retry_count=retry_count + 1)
            init_proxy = create_proxy(lambda: self._initialize_map())
            js.setTimeout(init_proxy, 200)

    def _add_tile_layer(self, map_instance):
        """Add tile layer to map based on configured tile_layer."""
        tile_layer_name = self._get_state('tile_layer')

        # Define tile layer configurations
        tile_configs = {
            'OpenStreetMap': {
                'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                'maxZoom': 19
            },
            'CartoDB': {
                'url': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                'maxZoom': 19
            },
            'Satellite': {
                'url': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                'attribution': 'Tiles &copy; Esri',
                'maxZoom': 18
            }
        }

        # Get config for selected tile layer
        config = tile_configs.get(tile_layer_name, tile_configs['OpenStreetMap'])

        # Create options object for Leaflet
        options = js.Object.new()
        options.attribution = config['attribution']
        options.maxZoom = config['maxZoom']

        # Add tile layer to map
        js.L.tileLayer(config['url'], options).addTo(map_instance)

    def _setup_map_events(self, map_instance):
        """Setup event handlers for map interactions."""
        # Map click event
        def handle_map_click(event):
            lat = event.latlng.lat
            lng = event.latlng.lng
            self._trigger_callbacks('click', {'lat': lat, 'lng': lng}, event)

        click_proxy = create_proxy(handle_map_click)
        self._map_callbacks['click'] = click_proxy
        map_instance.on('click', click_proxy)

        # Zoom event
        def handle_zoom(event):
            zoom = map_instance.getZoom()
            self._set_state(zoom=zoom)
            self._trigger_callbacks('zoom', zoom, event)

        zoom_proxy = create_proxy(handle_zoom)
        self._map_callbacks['zoom'] = zoom_proxy
        map_instance.on('zoomend', zoom_proxy)

        # Move event
        def handle_move(event):
            center_obj = map_instance.getCenter()
            center = [center_obj.lat, center_obj.lng]
            self._set_state(center=center)
            self._trigger_callbacks('move', center, event)

        move_proxy = create_proxy(handle_move)
        self._map_callbacks['move'] = move_proxy
        map_instance.on('moveend', move_proxy)

    def _initialize_layer_control(self, map_instance):
        """Initialize the Leaflet layer control."""
        try:
            # Create layer control with empty base layers and overlays
            # We'll add overlay layers dynamically using addOverlay()
            base_layers = js.Object.new()
            overlay_layers = js.Object.new()

            layer_control = js.L.control.layers(base_layers, overlay_layers).addTo(map_instance)

            # Store the control instance
            self._set_state(layer_control=layer_control)

            print("✓ Layer control initialized")
        except Exception as e:
            print(f"Error initializing layer control: {e}")

    def _add_to_layer_control(self, layer, name):
        """Add a layer to the layer control with the given name."""
        # Check if layer control is enabled
        if not self._get_state('show_layer_control'):
            return

        # Lazy initialization: create layer control on first use
        layer_control = self._get_state('layer_control')
        if not layer_control:
            map_instance = self._get_state('map_instance')
            if map_instance:
                self._initialize_layer_control(map_instance)
                layer_control = self._get_state('layer_control')
            else:
                print(f"Warning: Map not initialized, cannot add '{name}' to layer control")
                return

        try:
            # Add layer to control using Leaflet's addOverlay method
            layer_control.addOverlay(layer, name)

            # Track the layer in our overlay_layers dict
            overlay_layers = self._get_state('overlay_layers')
            overlay_layers[name] = layer
            self._set_state(overlay_layers=overlay_layers)

            print(f"✓ Added '{name}' to layer control")
        except Exception as e:
            print(f"Error adding layer '{name}' to control: {e}")

    def add_marker(self, lat, lng, popup_text=None, draggable=False, icon=None):
        """
        Add a marker to the map.

        Args:
            lat: Latitude
            lng: Longitude
            popup_text: Optional popup text to display when marker is clicked
            draggable: Whether marker can be dragged
            icon: Custom icon (Leaflet icon object)

        Returns:
            Leaflet marker object or None if map not ready
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            # Silently return None if map not initialized yet
            # The map will initialize eventually via setTimeout
            return None

        # Create marker options
        options = js.Object.new()
        options.draggable = draggable
        if icon:
            options.icon = icon

        # Convert Python list to JavaScript array
        js_coords = js.Array.new()
        js_coords.push(lat)
        js_coords.push(lng)

        # Create marker
        marker = js.L.marker(js_coords, options).addTo(map_instance)

        # Add popup if provided
        if popup_text:
            marker.bindPopup(popup_text)

        # Store marker reference
        markers = self._get_state('markers')
        markers.append(marker)
        self._set_state(markers=markers)

        return marker

    def remove_marker(self, marker):
        """Remove a marker from the map."""
        map_instance = self._get_state('map_instance')
        if not map_instance or not marker:
            return

        # Remove from map
        map_instance.removeLayer(marker)

        # Remove from stored markers
        markers = self._get_state('markers')
        if marker in markers:
            markers.remove(marker)
            self._set_state(markers=markers)

    def clear_markers(self):
        """Remove all markers from the map."""
        markers = self._get_state('markers')
        # Iterate over a copy since remove_marker modifies the list
        for marker in markers[:]:
            self.remove_marker(marker)
        self._set_state(markers=[])

    def set_view(self, center, zoom=None):
        """
        Change the map view to a new center and/or zoom level.

        Args:
            center: [lat, lng] coordinates
            zoom: Zoom level (optional, keeps current if not specified)
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        if zoom is None:
            zoom = self._get_state('zoom')

        # Convert to JS array
        js_center = js.Array.new()
        js_center.push(center[0])
        js_center.push(center[1])

        map_instance.setView(js_center, zoom)
        self._set_state(center=center, zoom=zoom)

    def pan_to(self, center):
        """Smoothly pan the map to a new center."""
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        # Convert to JS array
        js_center = js.Array.new()
        js_center.push(center[0])
        js_center.push(center[1])

        map_instance.panTo(js_center)
        self._set_state(center=center)

    def zoom_in(self):
        """Zoom in by one level."""
        map_instance = self._get_state('map_instance')
        if map_instance:
            map_instance.zoomIn()

    def zoom_out(self):
        """Zoom out by one level."""
        map_instance = self._get_state('map_instance')
        if map_instance:
            map_instance.zoomOut()

    def fit_bounds(self, bounds):
        """
        Adjust map to fit given bounds.

        Args:
            bounds: [[south, west], [north, east]] or list of [lat, lng] points
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        # Convert all coordinate pairs to JS arrays
        def convert_point(point):
            js_point = js.Array.new()
            js_point.push(point[0])
            js_point.push(point[1])
            return js_point

        # If bounds is a list of points, create Leaflet LatLngBounds
        if len(bounds) > 2:
            # Multiple points - create bounds from them
            js_point1 = convert_point(bounds[0])
            js_point2 = convert_point(bounds[1])
            leaflet_bounds = js.L.latLngBounds(js_point1, js_point2)
            for point in bounds[2:]:
                js_point = convert_point(point)
                leaflet_bounds.extend(js_point)
            map_instance.fitBounds(leaflet_bounds)
        else:
            # Two corners provided
            js_bounds = js.Array.new()
            for corner in bounds:
                js_bounds.push(convert_point(corner))
            map_instance.fitBounds(js_bounds)

    def zoom_to_layers(self, padding=None):
        """
        Zoom the map to fit all currently visible layers.

        Args:
            padding: Optional padding in pixels [top, right, bottom, left] or uniform value
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        layers = self._get_state('layers')
        if not layers:
            print("No layers to zoom to")
            return

        try:
            # Create a feature group containing all layers
            feature_group = js.L.featureGroup.new()

            # Add all layers to the feature group
            for layer in layers:
                if layer:
                    feature_group.addLayer(layer)

            # Get bounds of the feature group
            bounds = feature_group.getBounds()

            # Create options if padding specified
            if padding is not None:
                options = js.Object.new()
                if isinstance(padding, (list, tuple)):
                    # Array padding: [top, right, bottom, left]
                    padding_array = js.Array.new()
                    for p in padding:
                        padding_array.push(p)
                    options.padding = padding_array
                else:
                    # Uniform padding
                    options.padding = js.Array.new()
                    options.padding.push(padding)
                    options.padding.push(padding)

                map_instance.fitBounds(bounds, options)
            else:
                map_instance.fitBounds(bounds)

            print(f"✓ Zoomed to fit {len(layers)} layer(s)")

        except Exception as e:
            print(f"Error zooming to layers: {e}")

    def add_circle(self, lat, lng, radius, color="#3388ff", fill_color=None, fill_opacity=0.2):
        """
        Add a circle overlay to the map.

        Args:
            lat: Center latitude
            lng: Center longitude
            radius: Radius in meters
            color: Stroke color
            fill_color: Fill color (defaults to stroke color)
            fill_opacity: Fill opacity (0-1)

        Returns:
            Leaflet circle object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        if fill_color is None:
            fill_color = color

        # Convert to JS array
        js_center = js.Array.new()
        js_center.push(lat)
        js_center.push(lng)

        # Create options
        options = js.Object.new()
        options.color = color
        options.fillColor = fill_color
        options.fillOpacity = fill_opacity
        options.radius = radius

        # Create circle
        circle = js.L.circle(js_center, options).addTo(map_instance)

        # Store layer reference
        layers = self._get_state('layers')
        layers.append(circle)
        self._set_state(layers=layers)

        return circle

    def add_polyline(self, points, color="#3388ff", weight=3, opacity=1.0):
        """
        Add a polyline (connected line segments) to the map.

        Args:
            points: List of [lat, lng] coordinates
            color: Line color
            weight: Line width in pixels
            opacity: Line opacity (0-1)

        Returns:
            Leaflet polyline object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Convert Python list of lists to JavaScript array of arrays
        js_points = js.Array.new()
        for point in points:
            js_point = js.Array.new()
            js_point.push(point[0])
            js_point.push(point[1])
            js_points.push(js_point)

        # Create options
        options = js.Object.new()
        options.color = color
        options.weight = weight
        options.opacity = opacity

        # Create polyline
        polyline = js.L.polyline(js_points, options).addTo(map_instance)

        # Store layer reference
        layers = self._get_state('layers')
        layers.append(polyline)
        self._set_state(layers=layers)

        return polyline

    def add_polygon(self, points, color="#3388ff", fill_color=None, fill_opacity=0.2):
        """
        Add a polygon to the map.

        Args:
            points: List of [lat, lng] coordinates
            color: Stroke color
            fill_color: Fill color (defaults to stroke color)
            fill_opacity: Fill opacity (0-1)

        Returns:
            Leaflet polygon object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        if fill_color is None:
            fill_color = color

        # Convert Python list of lists to JavaScript array of arrays
        js_points = js.Array.new()
        for point in points:
            js_point = js.Array.new()
            js_point.push(point[0])
            js_point.push(point[1])
            js_points.push(js_point)

        # Create options
        options = js.Object.new()
        options.color = color
        options.fillColor = fill_color
        options.fillOpacity = fill_opacity

        # Create polygon
        polygon = js.L.polygon(js_points, options).addTo(map_instance)

        # Store layer reference
        layers = self._get_state('layers')
        layers.append(polygon)
        self._set_state(layers=layers)

        return polygon

    def add_shapefile(self, url, name=None, style_options=None, on_each_feature=None, add_to_control=True):
        """
        Add a shapefile overlay to the map.

        Args:
            url: URL to the shapefile (.zip containing .shp, .shx, .dbf files)
            name: Layer name for layer control (defaults to filename from URL)
            style_options: Dictionary of style options (color, weight, fillColor, fillOpacity, etc.)
            on_each_feature: Optional callback function(feature, layer) called for each feature
            add_to_control: If True, add layer to layer control (default: True)

        Returns:
            Promise that resolves to Leaflet GeoJSON layer or None if map not ready
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Check if shp library is available
        if not hasattr(js, 'shp'):
            print("Error: shp.js library not loaded. Shapefile support unavailable.")
            return None

        # Create style options object if provided
        js_style = None
        if style_options:
            js_style = js.Object.new()
            for key, value in style_options.items():
                setattr(js_style, key, value)

        # Create callback proxy if provided
        feature_callback = None
        if on_each_feature:
            feature_callback = create_proxy(on_each_feature)

        # Extract filename from URL if name not provided
        layer_name = name
        if layer_name is None and add_to_control:
            # Extract filename from URL (e.g., "http://example.com/data.zip" -> "data.zip")
            layer_name = url.split('/')[-1].replace('.zip', '')

        # Load and parse shapefile
        def handle_shapefile_load(geojson):
            # Create GeoJSON layer options
            options = js.Object.new()
            if js_style:
                options.style = js_style
            if feature_callback:
                options.onEachFeature = feature_callback

            # Create GeoJSON layer from parsed shapefile
            layer = js.L.geoJSON(geojson, options).addTo(map_instance)

            # Store layer reference
            layers = self._get_state('layers')
            layers.append(layer)
            self._set_state(layers=layers)

            # Add to layer control if requested
            if add_to_control and layer_name:
                self._add_to_layer_control(layer, layer_name)

            return layer

        # Parse shapefile using shp.js
        parse_proxy = create_proxy(handle_shapefile_load)
        promise = js.shp(url)
        promise.then(parse_proxy)

        return promise

    def add_geojson(self, geojson_data, name=None, style_options=None, on_each_feature=None, add_to_control=True):
        """
        Add a GeoJSON layer to the map.

        Args:
            geojson_data: GeoJSON object or URL to GeoJSON file
            name: Layer name for layer control (defaults to "GeoJSON Layer")
            style_options: Dictionary of style options (color, weight, fillColor, fillOpacity, etc.)
            on_each_feature: Optional callback function(feature, layer) called for each feature
            add_to_control: If True, add layer to layer control (default: True)

        Returns:
            Leaflet GeoJSON layer or None if map not ready
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Create style options object if provided
        js_style = None
        if style_options:
            js_style = js.Object.new()
            for key, value in style_options.items():
                setattr(js_style, key, value)

        # Create callback proxy if provided
        feature_callback = None
        if on_each_feature:
            feature_callback = create_proxy(on_each_feature)

        # Default layer name if not provided
        layer_name = name if name else "GeoJSON Layer"

        # Create GeoJSON layer options
        options = js.Object.new()
        if js_style:
            options.style = js_style
        if feature_callback:
            options.onEachFeature = feature_callback

        # Create GeoJSON layer
        layer = js.L.geoJSON(geojson_data, options).addTo(map_instance)

        # Store layer reference
        layers = self._get_state('layers')
        layers.append(layer)
        self._set_state(layers=layers)

        # Add to layer control if requested
        if add_to_control and layer_name:
            self._add_to_layer_control(layer, layer_name)

        return layer

    def add_geotiff(self, url, name=None, opacity=1.0, colormap=None, add_to_control=True):
        """
        Add a GeoTIFF raster overlay to the map by converting it to a PNG image overlay.

        This approach:
        - Works with any projection (UTM, lat/lon, etc.)
        - Simple and reliable (uses L.imageOverlay)
        - Allows custom Python colormaps
        - Client-side processing (no server needed)

        Args:
            url: URL to the GeoTIFF file
            name: Layer name for layer control (defaults to filename from URL)
            opacity: Layer opacity (0-1)
            colormap: Optional Python function (values_array) => [r, g, b, a] to colorize pixels
            add_to_control: If True, add layer to layer control (default: True)

        Returns:
            Leaflet ImageOverlay layer or None if map not ready
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Ensure geotiff.js is loaded
        if not hasattr(js, 'GeoTIFF'):
            script = js.document.createElement('script')
            script.src = 'antioch/lib/vendor/geotiff.js'
            js.document.head.appendChild(script)
            return None

        # Ensure proj4.js is loaded for coordinate transformation
        if not hasattr(js, 'proj4'):
            script = js.document.createElement('script')
            script.src = 'antioch/lib/vendor/proj4.js'
            js.document.head.appendChild(script)
            return None

        # Extract filename from URL if name not provided
        layer_name = name
        if layer_name is None and add_to_control:
            layer_name = url.split('/')[-1]

        # Fetch and parse the GeoTIFF
        def handle_geotiff_loaded(tiff):
            """Process the loaded GeoTIFF."""
            try:
                # Get the first image
                image = tiff.getImage()

                def handle_image_ready(image):
                    """Process the GeoTIFF image."""
                    try:
                        # Read raster data
                        def handle_rasters_read(rasters):
                            """Process the raster data."""
                            try:
                                # Get image metadata
                                width = image.getWidth()
                                height = image.getHeight()
                                bbox = image.getBoundingBox()

                                # Create canvas
                                canvas = js.document.createElement('canvas')
                                canvas.width = width
                                canvas.height = height
                                ctx = canvas.getContext('2d')

                                # Create image data
                                image_data = ctx.createImageData(width, height)
                                data = image_data.data

                                # Process pixels
                                num_bands = len(rasters)

                                for y in range(height):
                                    for x in range(width):
                                        idx = y * width + x
                                        pixel_idx = idx * 4

                                        # Get pixel values from all bands
                                        values = []
                                        for band in range(num_bands):
                                            values.append(rasters[band][idx])

                                        # Apply colormap
                                        if colormap and callable(colormap):
                                            try:
                                                rgba = colormap(values)
                                                data[pixel_idx] = rgba[0]      # R
                                                data[pixel_idx + 1] = rgba[1]  # G
                                                data[pixel_idx + 2] = rgba[2]  # B
                                                data[pixel_idx + 3] = rgba[3]  # A
                                            except:
                                                # Fallback to grayscale
                                                val = min(255, max(0, int(values[0]))) if values else 0
                                                data[pixel_idx] = val
                                                data[pixel_idx + 1] = val
                                                data[pixel_idx + 2] = val
                                                data[pixel_idx + 3] = 255
                                        else:
                                            # Default: RGB if 3+ bands, grayscale if 1 band
                                            if num_bands >= 3:
                                                # RGB
                                                data[pixel_idx] = min(255, max(0, int(values[0])))
                                                data[pixel_idx + 1] = min(255, max(0, int(values[1])))
                                                data[pixel_idx + 2] = min(255, max(0, int(values[2])))
                                                data[pixel_idx + 3] = 255
                                            else:
                                                # Grayscale
                                                val = min(255, max(0, int(values[0]))) if values else 0
                                                data[pixel_idx] = val
                                                data[pixel_idx + 1] = val
                                                data[pixel_idx + 2] = val
                                                data[pixel_idx + 3] = 255

                                # Put image data on canvas
                                ctx.putImageData(image_data, 0, 0)

                                # Convert canvas to data URL
                                data_url = canvas.toDataURL('image/png')

                                # Get bounds and convert to lat/lon if needed
                                # bbox is [minX, minY, maxX, maxY] in image's projection
                                minX, minY, maxX, maxY = bbox[0], bbox[1], bbox[2], bbox[3]

                                # Try to get projection info
                                epsg_code = None
                                try:
                                    geoKeys = image.getGeoKeys()
                                    if hasattr(geoKeys, 'ProjectedCSTypeGeoKey'):
                                        epsg_code = geoKeys.ProjectedCSTypeGeoKey
                                    elif hasattr(geoKeys, 'GeographicTypeGeoKey'):
                                        epsg_code = geoKeys.GeographicTypeGeoKey
                                except:
                                    pass

                                # Define overlay creation function (used for both WGS84 and reprojected)
                                def create_overlay(south, west, north, east):
                                    """Create the image overlay with the given bounds."""
                                    # Create bounds array for Leaflet: [[south, west], [north, east]]
                                    js_bounds = js.Array.new()
                                    sw_corner = js.Array.new()
                                    sw_corner.push(south)
                                    sw_corner.push(west)
                                    ne_corner = js.Array.new()
                                    ne_corner.push(north)
                                    ne_corner.push(east)
                                    js_bounds.push(sw_corner)
                                    js_bounds.push(ne_corner)

                                    # Create image overlay with crisp rendering options
                                    overlay_options = js.Object.new()
                                    overlay_options.opacity = opacity
                                    overlay_options.className = 'geotiff-overlay'

                                    layer = js.L.imageOverlay(data_url, js_bounds, overlay_options).addTo(map_instance)

                                    # Add CSS for crisp image rendering (no blurring when scaling)
                                    try:
                                        img_element = layer.getElement()
                                        if img_element:
                                            img_element.style.imageRendering = 'pixelated'
                                            img_element.style.setProperty('image-rendering', '-webkit-optimize-contrast', 'important')
                                    except:
                                        pass

                                    # Store layer reference
                                    layers = self._get_state('layers')
                                    layers.append(layer)
                                    self._set_state(layers=layers)

                                    # Add to layer control
                                    if add_to_control and layer_name:
                                        self._add_to_layer_control(layer, layer_name)

                                    # Zoom to layer bounds
                                    try:
                                        map_instance.fitBounds(js_bounds)
                                    except:
                                        pass

                                # Convert to lat/lon if needed
                                if epsg_code and epsg_code != 4326:
                                    # Not WGS84, need to reproject
                                    # Fetch projection definition dynamically from epsg.io
                                    def handle_projection_ready(proj_def_text=None):
                                        """Called when projection definition is ready or failed."""
                                        try:
                                            source_proj = f"EPSG:{epsg_code}"
                                            target_proj = "EPSG:4326"  # WGS84 lat/lon

                                            # Convert corners
                                            sw = js.proj4(source_proj, target_proj, js.Array.of(minX, minY))
                                            ne = js.proj4(source_proj, target_proj, js.Array.of(maxX, maxY))

                                            # Extract lat/lon (proj4 returns [lon, lat])
                                            west, south = sw[0], sw[1]
                                            east, north = ne[0], ne[1]
                                        except:
                                            # Fallback: assume already in degrees
                                            south, west, north, east = minY, minX, maxY, maxX

                                        # Continue with creating the overlay
                                        create_overlay(south, west, north, east)

                                    # Check if proj4 already knows this projection
                                    try:
                                        # Try a test transformation - if it works, definition exists
                                        test_result = js.proj4(f"EPSG:{epsg_code}", "EPSG:4326", js.Array.of(0, 0))
                                        # If we got here, projection is already defined
                                        handle_projection_ready()
                                    except:
                                        # Projection not defined, fetch from epsg.io
                                        def handle_proj_fetch(response):
                                            def handle_proj_text(text):
                                                try:
                                                    # Register the projection definition
                                                    js.proj4.defs(f"EPSG:{epsg_code}", text)
                                                    handle_projection_ready(text)
                                                except:
                                                    # Failed to parse/register, use fallback
                                                    handle_projection_ready(None)

                                            response.text().then(create_proxy(handle_proj_text))

                                        def handle_proj_error(error):
                                            # Failed to fetch, use fallback coordinates
                                            handle_projection_ready(None)

                                        # Fetch proj4 definition from epsg.io
                                        epsg_url = f"https://epsg.io/{epsg_code}.proj4"
                                        js.fetch(epsg_url).then(create_proxy(handle_proj_fetch), create_proxy(handle_proj_error))

                                    # Return early - overlay will be created asynchronously
                                    return
                                else:
                                    # Already in WGS84 or unknown projection
                                    south, west, north, east = minY, minX, maxY, maxX
                                    create_overlay(south, west, north, east)

                            except:
                                pass

                        # Read all rasters
                        def handle_raster_error(error):
                            pass

                        read_promise = image.readRasters()
                        read_promise.then(create_proxy(handle_rasters_read), create_proxy(handle_raster_error))

                    except:
                        pass

                # Handle promise from getImage()
                def handle_image_error(error):
                    pass

                if hasattr(image, 'then'):
                    image.then(create_proxy(handle_image_ready), create_proxy(handle_image_error))
                else:
                    handle_image_ready(image)

            except:
                pass

        # Start loading - fetch entire file then parse
        # This is more reliable than fromUrl for local files
        try:
            def handle_fetch_response(response):
                return response.arrayBuffer()

            def handle_array_buffer(array_buffer):
                tiff_promise = js.GeoTIFF.fromArrayBuffer(array_buffer)

                def handle_tiff_error(error):
                    pass

                tiff_promise.then(create_proxy(handle_geotiff_loaded), create_proxy(handle_tiff_error))
                return tiff_promise

            def handle_fetch_error(error):
                pass

            # Fetch the file
            fetch_promise = js.fetch(url)
            fetch_promise.then(create_proxy(handle_fetch_response), create_proxy(handle_fetch_error)).then(create_proxy(handle_array_buffer))

        except:
            return None

        return None  # Layer will be added asynchronously

    def remove_layer(self, layer):
        """
        Remove a layer (shapefile, GeoJSON, GeoTIFF, etc.) from the map.

        Args:
            layer: Leaflet layer object to remove
        """
        map_instance = self._get_state('map_instance')
        if not map_instance or not layer:
            return

        # Remove from map
        map_instance.removeLayer(layer)

        # Remove from stored layers
        layers = self._get_state('layers')
        if layer in layers:
            layers.remove(layer)
            self._set_state(layers=layers)

        # Remove from layer control if present and enabled
        if self._get_state('show_layer_control'):
            layer_control = self._get_state('layer_control')
            overlay_layers = self._get_state('overlay_layers')

            # Find layer name in overlay_layers and remove from control
            for name, stored_layer in list(overlay_layers.items()):
                if stored_layer == layer:
                    if layer_control:
                        layer_control.removeLayer(layer)
                    del overlay_layers[name]
                    self._set_state(overlay_layers=overlay_layers)
                    break

    def clear_layers(self):
        """Remove all layers (excluding markers) from the map."""
        layers = self._get_state('layers')
        # Iterate over a copy since remove_layer modifies the list
        for layer in layers[:]:
            self.remove_layer(layer)
        self._set_state(layers=[])

    def on_click(self, callback):
        """Register callback for map click events."""
        return self.on('click', callback)

    def on_zoom(self, callback):
        """Register callback for zoom changes."""
        return self.on('zoom', callback)

    def on_move(self, callback):
        """Register callback for map movement."""
        return self.on('move', callback)

    def on_ready(self, callback):
        """Register callback for when map is initialized and ready."""
        return self.on('ready', callback)

    @property
    def current_center(self):
        """Get current map center coordinates."""
        return self._get_state('center')

    @property
    def current_zoom(self):
        """Get current zoom level."""
        return self._get_state('zoom')

    @property
    def is_ready(self):
        """Check if map is initialized and ready."""
        return self._get_state('initialized')
