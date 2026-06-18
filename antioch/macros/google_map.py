"""
GoogleMap macro - An interactive map component using Google Maps JavaScript API.
Provides mapping, markers, info windows, and various map interactions.
"""
import js
from pyodide.ffi import create_proxy
from .base import Macro
from ..elements import Div
from ..lib.loader import inject_script


class GoogleMap(Macro):
    """
    An interactive map component powered by Google Maps JavaScript API.
    Supports markers, info windows, various map types, and interactions.

    Note: Requires a Google Maps API key. Get one at:
    https://developers.google.com/maps/documentation/javascript/get-api-key
    """

    # Class-level variable to track if API is loaded
    _api_loaded = False
    _api_loading = False
    _pending_maps = []

    def __init__(self, api_key, center=None, zoom=13, width="100%", height="400px",
                 map_type="roadmap", container_style=None, **kwargs):
        """
        Initialize a Google Map component.

        Args:
            api_key: Your Google Maps API key (required)
            center: {"lat": latitude, "lng": longitude} coordinates for map center
                   Defaults to San Francisco
            zoom: Initial zoom level (1-20)
            width: Width of map container
            height: Height of map container
            map_type: Map type - "roadmap", "satellite", "hybrid", or "terrain"
            container_style: Custom styles for map container
        """
        # Initialize base macro
        super().__init__(macro_type="google_map", **kwargs)

        # Validate API key
        if not api_key:
            raise ValueError("Google Maps API key is required. Get one at: https://developers.google.com/maps/documentation/javascript/get-api-key")

        # Default center (San Francisco)
        if center is None:
            center = {"lat": 37.7749, "lng": -122.4194}

        # Set up state
        self._set_state(
            api_key=api_key,
            center=center,
            zoom=zoom,
            width=width,
            height=height,
            map_type=map_type,
            map_instance=None,
            markers=[],
            info_windows=[],
            overlays=[],
            initialized=False,
            init_retry_count=0
        )

        # Store references to proxied callbacks for cleanup
        self._map_callbacks = {}

        # Create unified Events for decorator usage
        self._create_event('click')
        self._create_event('zoom_changed')
        self._create_event('center_changed')
        self._create_event('ready')
        self._create_event('marker_click')

        # Default container style
        default_container_style = {
            "width": width,
            "height": height,
            "border": "1px solid #ccc",
            "border_radius": "4px",
            "overflow": "hidden",
            "position": "relative"
        }

        # Merge with user styles
        self._container_style = self._merge_styles(default_container_style, container_style)

        # Load Google Maps API if not already loaded
        if not GoogleMap._api_loaded and not GoogleMap._api_loading:
            self._load_google_maps_api()

        # Initialize macro
        self._init_macro()

    def _load_google_maps_api(self):
        """Load the Google Maps JavaScript API."""
        GoogleMap._api_loading = True
        api_key = self._get_state('api_key')

        # Create callback function name
        callback_name = "initGoogleMaps"

        # Define callback that will be called when API loads
        def on_api_loaded():
            GoogleMap._api_loaded = True
            GoogleMap._api_loading = False

            # Initialize all pending maps
            for map_instance in GoogleMap._pending_maps:
                map_instance._initialize_map()

            GoogleMap._pending_maps.clear()

        # Register callback in global scope
        js.window[callback_name] = create_proxy(on_api_loaded)

        # Load Google Maps API script
        api_url = f"https://maps.googleapis.com/maps/api/js?key={api_key}&callback={callback_name}"
        inject_script(api_url)

    def _create_elements(self):
        """Create the map container element."""
        # Create container with unique ID for Google Maps
        container = self._register_element('container',
                                           self._create_container(self._container_style))

        # Set the ID
        container.set_attribute("id", self._id)

        # Also set it directly on the DOM element
        if container._dom_element:
            container._dom_element.id = self._id

        # Check if API is loaded, otherwise add to pending
        if GoogleMap._api_loaded:
            # Initialize map after delay to ensure DOM is ready
            init_proxy = create_proxy(lambda: self._initialize_map())
            js.setTimeout(init_proxy, 500)
        else:
            # Add to pending maps
            GoogleMap._pending_maps.append(self)

        return container

    def _initialize_map(self):
        """Initialize the Google Maps instance."""
        if self._get_state('initialized'):
            return

        # Check retry count
        retry_count = self._get_state('init_retry_count')
        if retry_count > 50:
            print("Error: Failed to initialize Google Map after 50 retries")
            return

        try:
            # Check if Google Maps API is loaded
            if not hasattr(js, 'google') or not hasattr(js.google, 'maps'):
                # API not loaded yet, retry
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_map())
                js.setTimeout(init_proxy, 100)
                return

            container = self._get_element('container')
            if not container or not container._dom_element:
                # Container not ready yet
                self._set_state(init_retry_count=retry_count + 1)
                init_proxy = create_proxy(lambda: self._initialize_map())
                js.setTimeout(init_proxy, 100)
                return

            # Get map configuration
            center = self._get_state('center')
            zoom = self._get_state('zoom')
            map_type = self._get_state('map_type')

            # Convert map_type to Google Maps constant
            map_type_id_map = {
                'roadmap': 'ROADMAP',
                'satellite': 'SATELLITE',
                'hybrid': 'HYBRID',
                'terrain': 'TERRAIN'
            }
            map_type_id = map_type_id_map.get(map_type.lower(), 'ROADMAP')

            # Create map options object
            options = js.Object.new()

            # Set center
            center_obj = js.Object.new()
            center_obj.lat = center['lat']
            center_obj.lng = center['lng']
            options.center = center_obj

            # Set zoom and map type
            options.zoom = zoom
            options.mapTypeId = getattr(js.google.maps.MapTypeId, map_type_id)

            # Create Google Map instance
            map_instance = js.google.maps.Map.new(container._dom_element, options)

            # Store map instance
            self._set_state(map_instance=map_instance, initialized=True)

            # Setup event handlers
            self._setup_map_events(map_instance)

            # Trigger ready callback
            self._fire_event('ready')

        except Exception as e:
            # Initialization failed, retry
            print(f"Google Map initialization error: {e}")
            self._set_state(init_retry_count=retry_count + 1)
            init_proxy = create_proxy(lambda: self._initialize_map())
            js.setTimeout(init_proxy, 200)

    def _setup_map_events(self, map_instance):
        """Setup event handlers for map interactions."""
        # Map click event
        def handle_map_click(event):
            lat = event.latLng.lat()
            lng = event.latLng.lng()
            self._fire_event('click', {'lat': lat, 'lng': lng}, event)

        click_proxy = create_proxy(handle_map_click)
        self._map_callbacks['click'] = click_proxy
        map_instance.addListener('click', click_proxy)

        # Zoom changed event
        def handle_zoom_changed():
            zoom = map_instance.getZoom()
            self._set_state(zoom=zoom)
            self._fire_event('zoom_changed', zoom)

        zoom_proxy = create_proxy(handle_zoom_changed)
        self._map_callbacks['zoom_changed'] = zoom_proxy
        map_instance.addListener('zoom_changed', zoom_proxy)

        # Center changed event
        def handle_center_changed():
            center_obj = map_instance.getCenter()
            if center_obj:
                center = {'lat': center_obj.lat(), 'lng': center_obj.lng()}
                self._set_state(center=center)
                self._fire_event('center_changed', center)

        center_proxy = create_proxy(handle_center_changed)
        self._map_callbacks['center_changed'] = center_proxy
        map_instance.addListener('center_changed', center_proxy)

    def add_marker(self, lat, lng, title=None, label=None, draggable=False,
                   icon=None, animation=None, info_content=None):
        """
        Add a marker to the map.

        Args:
            lat: Latitude
            lng: Longitude
            title: Marker title (shows on hover)
            label: Short text label on marker (single character or short string)
            draggable: Whether marker can be dragged
            icon: Custom icon URL or icon object
            animation: "drop" or "bounce" animation
            info_content: HTML content for info window that opens on click

        Returns:
            Google Maps marker object or None if map not ready
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            print("Warning: Map not initialized yet")
            return None

        # Create marker options
        options = js.Object.new()

        # Set position
        position = js.Object.new()
        position.lat = lat
        position.lng = lng
        options.position = position

        # Set map
        options.map = map_instance

        # Optional properties
        if title:
            options.title = title

        if label:
            options.label = label

        options.draggable = draggable

        if icon:
            options.icon = icon

        if animation:
            if animation.lower() == "drop":
                options.animation = js.google.maps.Animation.DROP
            elif animation.lower() == "bounce":
                options.animation = js.google.maps.Animation.BOUNCE

        # Create marker
        marker = js.google.maps.Marker.new(options)

        # Add info window if content provided
        if info_content:
            info_window = self._create_info_window(info_content)

            def handle_marker_click():
                info_window.open(map_instance, marker)
                self._fire_event('marker_click', {'lat': lat, 'lng': lng, 'marker': marker})

            marker_click_proxy = create_proxy(handle_marker_click)
            marker.addListener('click', marker_click_proxy)

        # Store marker reference
        markers = self._get_state('markers')
        markers.append(marker)
        self._set_state(markers=markers)

        return marker

    def _create_info_window(self, content):
        """Create an info window with the given content."""
        options = js.Object.new()
        options.content = content

        info_window = js.google.maps.InfoWindow.new(options)

        # Store reference
        info_windows = self._get_state('info_windows')
        info_windows.append(info_window)
        self._set_state(info_windows=info_windows)

        return info_window

    def remove_marker(self, marker):
        """Remove a marker from the map."""
        if not marker:
            return

        # Remove from map
        marker.setMap(None)

        # Remove from stored markers
        markers = self._get_state('markers')
        if marker in markers:
            markers.remove(marker)
            self._set_state(markers=markers)

    def clear_markers(self):
        """Remove all markers from the map."""
        markers = self._get_state('markers')
        for marker in markers:
            marker.setMap(None)
        self._set_state(markers=[])

    def set_center(self, lat, lng):
        """
        Change the map center.

        Args:
            lat: Latitude
            lng: Longitude
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        center = js.Object.new()
        center.lat = lat
        center.lng = lng

        map_instance.setCenter(center)
        self._set_state(center={'lat': lat, 'lng': lng})

    def pan_to(self, lat, lng):
        """
        Smoothly pan the map to a new center.

        Args:
            lat: Latitude
            lng: Longitude
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        position = js.Object.new()
        position.lat = lat
        position.lng = lng

        map_instance.panTo(position)
        self._set_state(center={'lat': lat, 'lng': lng})

    def set_zoom(self, zoom):
        """
        Set the zoom level.

        Args:
            zoom: Zoom level (1-20)
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        map_instance.setZoom(zoom)
        self._set_state(zoom=zoom)

    def zoom_in(self):
        """Zoom in by one level."""
        current_zoom = self._get_state('zoom')
        self.set_zoom(current_zoom + 1)

    def zoom_out(self):
        """Zoom out by one level."""
        current_zoom = self._get_state('zoom')
        self.set_zoom(current_zoom - 1)

    def set_map_type(self, map_type):
        """
        Change the map type.

        Args:
            map_type: "roadmap", "satellite", "hybrid", or "terrain"
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        map_type_id_map = {
            'roadmap': 'ROADMAP',
            'satellite': 'SATELLITE',
            'hybrid': 'HYBRID',
            'terrain': 'TERRAIN'
        }
        map_type_id = map_type_id_map.get(map_type.lower(), 'ROADMAP')

        map_instance.setMapTypeId(getattr(js.google.maps.MapTypeId, map_type_id))
        self._set_state(map_type=map_type)

    def fit_bounds(self, bounds):
        """
        Adjust map to fit given bounds.

        Args:
            bounds: List of {"lat": lat, "lng": lng} dictionaries
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return

        # Create LatLngBounds object
        bounds_obj = js.google.maps.LatLngBounds.new()

        for point in bounds:
            position = js.Object.new()
            position.lat = point['lat']
            position.lng = point['lng']
            bounds_obj.extend(position)

        map_instance.fitBounds(bounds_obj)

    def add_circle(self, lat, lng, radius, stroke_color="#FF0000", stroke_opacity=0.8,
                   stroke_weight=2, fill_color="#FF0000", fill_opacity=0.35):
        """
        Add a circle overlay to the map.

        Args:
            lat: Center latitude
            lng: Center longitude
            radius: Radius in meters
            stroke_color: Stroke color (hex)
            stroke_opacity: Stroke opacity (0-1)
            stroke_weight: Stroke width in pixels
            fill_color: Fill color (hex)
            fill_opacity: Fill opacity (0-1)

        Returns:
            Google Maps circle object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Create circle options
        options = js.Object.new()

        # Set center
        center = js.Object.new()
        center.lat = lat
        center.lng = lng
        options.center = center

        # Set properties
        options.radius = radius
        options.strokeColor = stroke_color
        options.strokeOpacity = stroke_opacity
        options.strokeWeight = stroke_weight
        options.fillColor = fill_color
        options.fillOpacity = fill_opacity
        options.map = map_instance

        # Create circle
        circle = js.google.maps.Circle.new(options)

        # Store overlay reference
        overlays = self._get_state('overlays')
        overlays.append(circle)
        self._set_state(overlays=overlays)

        return circle

    def add_polygon(self, paths, stroke_color="#FF0000", stroke_opacity=0.8,
                    stroke_weight=2, fill_color="#FF0000", fill_opacity=0.35):
        """
        Add a polygon to the map.

        Args:
            paths: List of {"lat": lat, "lng": lng} dictionaries
            stroke_color: Stroke color (hex)
            stroke_opacity: Stroke opacity (0-1)
            stroke_weight: Stroke width in pixels
            fill_color: Fill color (hex)
            fill_opacity: Fill opacity (0-1)

        Returns:
            Google Maps polygon object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Convert paths to JavaScript array
        js_paths = js.Array.new()
        for point in paths:
            position = js.Object.new()
            position.lat = point['lat']
            position.lng = point['lng']
            js_paths.push(position)

        # Create polygon options
        options = js.Object.new()
        options.paths = js_paths
        options.strokeColor = stroke_color
        options.strokeOpacity = stroke_opacity
        options.strokeWeight = stroke_weight
        options.fillColor = fill_color
        options.fillOpacity = fill_opacity
        options.map = map_instance

        # Create polygon
        polygon = js.google.maps.Polygon.new(options)

        # Store overlay reference
        overlays = self._get_state('overlays')
        overlays.append(polygon)
        self._set_state(overlays=overlays)

        return polygon

    def add_polyline(self, paths, stroke_color="#FF0000", stroke_opacity=1.0, stroke_weight=2):
        """
        Add a polyline to the map.

        Args:
            paths: List of {"lat": lat, "lng": lng} dictionaries
            stroke_color: Stroke color (hex)
            stroke_opacity: Stroke opacity (0-1)
            stroke_weight: Stroke width in pixels

        Returns:
            Google Maps polyline object
        """
        map_instance = self._get_state('map_instance')
        if not map_instance:
            return None

        # Convert paths to JavaScript array
        js_paths = js.Array.new()
        for point in paths:
            position = js.Object.new()
            position.lat = point['lat']
            position.lng = point['lng']
            js_paths.push(position)

        # Create polyline options
        options = js.Object.new()
        options.path = js_paths
        options.strokeColor = stroke_color
        options.strokeOpacity = stroke_opacity
        options.strokeWeight = stroke_weight
        options.map = map_instance

        # Create polyline
        polyline = js.google.maps.Polyline.new(options)

        # Store overlay reference
        overlays = self._get_state('overlays')
        overlays.append(polyline)
        self._set_state(overlays=overlays)

        return polyline

    def remove_overlay(self, overlay):
        """Remove an overlay (circle, polygon, polyline) from the map."""
        if not overlay:
            return

        overlay.setMap(None)

        overlays = self._get_state('overlays')
        if overlay in overlays:
            overlays.remove(overlay)
            self._set_state(overlays=overlays)

    def clear_overlays(self):
        """Remove all overlays from the map."""
        overlays = self._get_state('overlays')
        for overlay in overlays:
            overlay.setMap(None)
        self._set_state(overlays=[])

    def on_click(self, callback):
        """Register callback for map click events."""
        return self.on('click', callback)

    def on_zoom_changed(self, callback):
        """Register callback for zoom changes."""
        return self.on('zoom_changed', callback)

    def on_center_changed(self, callback):
        """Register callback for center changes."""
        return self.on('center_changed', callback)

    def on_ready(self, callback):
        """Register callback for when map is initialized and ready."""
        return self.on('ready', callback)

    def on_marker_click(self, callback):
        """Register callback for marker click events."""
        return self.on('marker_click', callback)

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