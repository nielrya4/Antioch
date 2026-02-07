"""
WebCanvas macro - A programmatic canvas drawing component for Antioch.

Provides a Pythonic interface to the HTML Canvas 2D API with method chaining,
allowing developers to create graphics, animations, and interactive visualizations
entirely in Python without writing JavaScript.

Example:
    canvas = WebCanvas(width=600, height=400)
    canvas.rect(50, 50, 100, 100, fill="#ff0000", stroke="#000", line_width=2)
    canvas.circle(300, 200, 75, fill="#00ff00")
    canvas.text("Hello!", 300, 100, fill="#333", font="bold 24px Arial")
"""

import js
from pyodide.ffi import create_proxy
from typing import Optional, Callable, Union, Any
from .base import Macro
from ..elements import Canvas


class WebCanvas(Macro):
    """
    A programmatic canvas drawing component with minimal API.

    Provides drawing primitives (rectangles, circles, lines, paths, text),
    image support, transformations, and export capabilities.
    """

    def __init__(self, width: int = 800, height: int = 600,
                 background: str = "#ffffff",
                 container_style: Optional[dict] = None,
                 **kwargs):
        """
        Initialize a WebCanvas macro.

        Args:
            width: Canvas width in pixels (default: 800)
            height: Canvas height in pixels (default: 600)
            background: Initial background color (default: "#ffffff")
            container_style: Optional custom container styles
            **kwargs: Additional macro arguments passed to base Macro class

        Example:
            canvas = WebCanvas(width=600, height=400, background="#f0f0f0")
        """
        super().__init__(macro_type="webcanvas", **kwargs)

        # Store initial parameters in state
        self._set_state(
            width=width,
            height=height,
            background=background,
            context=None  # Will be set in _create_elements
        )

        # Store container style
        self._container_style = container_style or {}

        # Image caching for async loading
        self._image_cache = {}  # Dict[str, Image]
        self._pending_images = {}  # Dict[str, List[Callable]]

        # Register callback types
        self._add_callback_type('draw')
        self._add_callback_type('clear')
        self._add_callback_type('image_loaded')

        # Initialize the macro (calls _create_elements)
        self._init_macro()

    def _create_elements(self):
        """Create the canvas element and initialize the 2D rendering context."""
        width = self._get_state('width')
        height = self._get_state('height')
        background = self._get_state('background')

        # Create container
        container = self._create_container(self._container_style)

        # Create canvas element with specified dimensions
        canvas = self._register_element('canvas', Canvas(
            width=width,
            height=height,
            style={
                "display": "block",
                "background_color": background
            }
        ))

        # Get 2D rendering context from the canvas
        ctx = canvas._dom_element.getContext("2d")
        self._set_state(context=ctx)

        # Set initial context properties
        ctx.fillStyle = "#000000"
        ctx.strokeStyle = "#000000"
        ctx.lineWidth = 1
        ctx.lineCap = "butt"
        ctx.lineJoin = "miter"
        ctx.font = "10px sans-serif"
        ctx.textAlign = "start"
        ctx.textBaseline = "alphabetic"
        ctx.globalAlpha = 1.0

        container.add(canvas)
        return container

    # ========== Shape Drawing Methods ==========

    def rect(self, x: float, y: float, width: float, height: float,
             fill: Optional[str] = None,
             stroke: Optional[str] = None,
             line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Draw a rectangle.

        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Rectangle width
            height: Rectangle height
            fill: Optional fill color (CSS color string)
            stroke: Optional stroke color (CSS color string)
            line_width: Optional line width for stroke

        Returns:
            Self for method chaining

        Example:
            canvas.rect(50, 50, 100, 100, fill="#ff0000", stroke="#000", line_width=2)
        """
        ctx = self.context

        # Save and set line width if provided
        if line_width is not None:
            old_width = ctx.lineWidth
            ctx.lineWidth = line_width

        # Fill the rectangle if fill color provided
        if fill:
            old_fill = ctx.fillStyle
            ctx.fillStyle = fill
            ctx.fillRect(x, y, width, height)
            ctx.fillStyle = old_fill

        # Stroke the rectangle if stroke color provided
        if stroke:
            old_stroke = ctx.strokeStyle
            ctx.strokeStyle = stroke
            ctx.strokeRect(x, y, width, height)
            ctx.strokeStyle = old_stroke

        # Restore line width if changed
        if line_width is not None:
            ctx.lineWidth = old_width

        return self

    def circle(self, x: float, y: float, radius: float,
               fill: Optional[str] = None,
               stroke: Optional[str] = None,
               line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Draw a circle.

        Args:
            x: X coordinate of circle center
            y: Y coordinate of circle center
            radius: Circle radius
            fill: Optional fill color
            stroke: Optional stroke color
            line_width: Optional line width for stroke

        Returns:
            Self for method chaining

        Example:
            canvas.circle(100, 100, 50, fill="#00ff00", stroke="#000", line_width=2)
        """
        ctx = self.context

        # Save and set line width if provided
        if line_width is not None:
            old_width = ctx.lineWidth
            ctx.lineWidth = line_width

        # Create the circle path
        ctx.beginPath()
        ctx.arc(x, y, radius, 0, 2 * js.Math.PI)

        # Fill if fill color provided
        if fill:
            old_fill = ctx.fillStyle
            ctx.fillStyle = fill
            ctx.fill()
            ctx.fillStyle = old_fill

        # Stroke if stroke color provided
        if stroke:
            old_stroke = ctx.strokeStyle
            ctx.strokeStyle = stroke
            ctx.stroke()
            ctx.strokeStyle = old_stroke

        # Restore line width if changed
        if line_width is not None:
            ctx.lineWidth = old_width

        return self

    def ellipse(self, x: float, y: float,
                radius_x: float, radius_y: float,
                rotation: float = 0,
                fill: Optional[str] = None,
                stroke: Optional[str] = None,
                line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Draw an ellipse.

        Args:
            x: X coordinate of ellipse center
            y: Y coordinate of ellipse center
            radius_x: Horizontal radius
            radius_y: Vertical radius
            rotation: Rotation angle in radians (default: 0)
            fill: Optional fill color
            stroke: Optional stroke color
            line_width: Optional line width for stroke

        Returns:
            Self for method chaining

        Example:
            canvas.ellipse(200, 200, 80, 50, 0, fill="#ffff00", stroke="#000")
        """
        ctx = self.context

        # Save and set line width if provided
        if line_width is not None:
            old_width = ctx.lineWidth
            ctx.lineWidth = line_width

        # Create the ellipse path
        ctx.beginPath()
        ctx.ellipse(x, y, radius_x, radius_y, rotation, 0, 2 * js.Math.PI)

        # Fill if fill color provided
        if fill:
            old_fill = ctx.fillStyle
            ctx.fillStyle = fill
            ctx.fill()
            ctx.fillStyle = old_fill

        # Stroke if stroke color provided
        if stroke:
            old_stroke = ctx.strokeStyle
            ctx.strokeStyle = stroke
            ctx.stroke()
            ctx.strokeStyle = old_stroke

        # Restore line width if changed
        if line_width is not None:
            ctx.lineWidth = old_width

        return self

    def line(self, x1: float, y1: float, x2: float, y2: float,
             stroke: Optional[str] = None,
             line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Draw a straight line between two points.

        Args:
            x1: Starting X coordinate
            y1: Starting Y coordinate
            x2: Ending X coordinate
            y2: Ending Y coordinate
            stroke: Optional stroke color (uses current if not provided)
            line_width: Optional line width

        Returns:
            Self for method chaining

        Example:
            canvas.line(0, 0, 100, 100, stroke="#000", line_width=2)
        """
        ctx = self.context

        # Save and set line width if provided
        if line_width is not None:
            old_width = ctx.lineWidth
            ctx.lineWidth = line_width

        # Save and set stroke color if provided
        if stroke:
            old_stroke = ctx.strokeStyle
            ctx.strokeStyle = stroke

        # Draw the line
        ctx.beginPath()
        ctx.moveTo(x1, y1)
        ctx.lineTo(x2, y2)
        ctx.stroke()

        # Restore stroke color if changed
        if stroke:
            ctx.strokeStyle = old_stroke

        # Restore line width if changed
        if line_width is not None:
            ctx.lineWidth = old_width

        return self

    def clear_rect(self, x: float, y: float, width: float, height: float) -> 'WebCanvas':
        """
        Clear a rectangular area (make transparent).

        Args:
            x: X coordinate of top-left corner
            y: Y coordinate of top-left corner
            width: Rectangle width
            height: Rectangle height

        Returns:
            Self for method chaining

        Example:
            canvas.clear_rect(50, 50, 100, 100)
        """
        self.context.clearRect(x, y, width, height)
        return self

    # ========== Path Methods ==========

    def begin_path(self) -> 'WebCanvas':
        """
        Begin a new path. Call before creating complex paths.

        Returns:
            Self for method chaining

        Example:
            canvas.begin_path().move_to(10, 10).line_to(100, 100).stroke()
        """
        self.context.beginPath()
        return self

    def close_path(self) -> 'WebCanvas':
        """
        Close the current path by drawing a line to the start point.

        Returns:
            Self for method chaining
        """
        self.context.closePath()
        return self

    def move_to(self, x: float, y: float) -> 'WebCanvas':
        """
        Move the drawing cursor to a point without drawing.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Self for method chaining
        """
        self.context.moveTo(x, y)
        return self

    def line_to(self, x: float, y: float) -> 'WebCanvas':
        """
        Draw a line from current position to specified point.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            Self for method chaining
        """
        self.context.lineTo(x, y)
        return self

    def arc(self, x: float, y: float, radius: float,
            start_angle: float, end_angle: float,
            counterclockwise: bool = False) -> 'WebCanvas':
        """
        Add an arc to the current path.

        Args:
            x: X coordinate of arc center
            y: Y coordinate of arc center
            radius: Arc radius
            start_angle: Starting angle in radians
            end_angle: Ending angle in radians
            counterclockwise: Draw counterclockwise if True

        Returns:
            Self for method chaining

        Example:
            import math
            canvas.begin_path().arc(100, 100, 50, 0, math.pi).stroke()
        """
        self.context.arc(x, y, radius, start_angle, end_angle, counterclockwise)
        return self

    def arc_to(self, x1: float, y1: float, x2: float, y2: float,
               radius: float) -> 'WebCanvas':
        """
        Add an arc to the current path using control points.

        Args:
            x1: X coordinate of first control point
            y1: Y coordinate of first control point
            x2: X coordinate of second control point
            y2: Y coordinate of second control point
            radius: Arc radius

        Returns:
            Self for method chaining
        """
        self.context.arcTo(x1, y1, x2, y2, radius)
        return self

    def quadratic_curve_to(self, cpx: float, cpy: float,
                          x: float, y: float) -> 'WebCanvas':
        """
        Draw a quadratic Bézier curve.

        Args:
            cpx: Control point X coordinate
            cpy: Control point Y coordinate
            x: End point X coordinate
            y: End point Y coordinate

        Returns:
            Self for method chaining
        """
        self.context.quadraticCurveTo(cpx, cpy, x, y)
        return self

    def bezier_curve_to(self, cp1x: float, cp1y: float,
                       cp2x: float, cp2y: float,
                       x: float, y: float) -> 'WebCanvas':
        """
        Draw a cubic Bézier curve.

        Args:
            cp1x: First control point X
            cp1y: First control point Y
            cp2x: Second control point X
            cp2y: Second control point Y
            x: End point X
            y: End point Y

        Returns:
            Self for method chaining
        """
        self.context.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)
        return self

    def fill(self, color: Optional[str] = None) -> 'WebCanvas':
        """
        Fill the current path with the current or specified fill style.

        Args:
            color: Optional fill color to override current fillStyle

        Returns:
            Self for method chaining

        Example:
            canvas.begin_path().move_to(50, 50).line_to(150, 50).line_to(100, 150).close_path().fill("#ffd700")
        """
        ctx = self.context

        if color:
            old_fill = ctx.fillStyle
            ctx.fillStyle = color
            ctx.fill()
            ctx.fillStyle = old_fill
        else:
            ctx.fill()

        return self

    def stroke(self, color: Optional[str] = None,
               line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Stroke the current path with the current or specified stroke style.

        Args:
            color: Optional stroke color to override current strokeStyle
            line_width: Optional line width to override current lineWidth

        Returns:
            Self for method chaining
        """
        ctx = self.context

        # Save current values if we're overriding
        if color or line_width is not None:
            old_stroke = ctx.strokeStyle if color else None
            old_width = ctx.lineWidth if line_width is not None else None

            if color:
                ctx.strokeStyle = color
            if line_width is not None:
                ctx.lineWidth = line_width

            ctx.stroke()

            # Restore
            if color:
                ctx.strokeStyle = old_stroke
            if line_width is not None:
                ctx.lineWidth = old_width
        else:
            ctx.stroke()

        return self

    # ========== Text Methods ==========

    def text(self, text: str, x: float, y: float,
             fill: Optional[str] = None,
             stroke: Optional[str] = None,
             font: Optional[str] = None,
             align: Optional[str] = None,
             baseline: Optional[str] = None,
             max_width: Optional[float] = None,
             line_width: Optional[float] = None) -> 'WebCanvas':
        """
        Draw text at the specified position.

        Args:
            text: Text string to draw
            x: X coordinate (alignment depends on textAlign)
            y: Y coordinate (baseline position)
            fill: Optional fill color for filled text
            stroke: Optional stroke color for outlined text
            font: Optional font CSS string (e.g., "24px Arial")
            align: Optional horizontal alignment ("left", "right", "center", "start", "end")
            baseline: Optional vertical baseline ("top", "middle", "bottom", "alphabetic", etc.)
            max_width: Optional maximum width for text scaling
            line_width: Optional line width for stroked text

        Returns:
            Self for method chaining

        Example:
            canvas.text("Hello World", 300, 100,
                       fill="#333",
                       font="bold 48px Arial",
                       align="center",
                       baseline="middle")
        """
        ctx = self.context

        # Save current values if we're overriding
        old_font = ctx.font if font else None
        old_align = ctx.textAlign if align else None
        old_baseline = ctx.textBaseline if baseline else None
        old_width = ctx.lineWidth if line_width is not None else None

        # Set temporary values
        if font:
            ctx.font = font
        if align:
            ctx.textAlign = align
        if baseline:
            ctx.textBaseline = baseline
        if line_width is not None:
            ctx.lineWidth = line_width

        # Draw filled text if fill color provided
        if fill:
            old_fill = ctx.fillStyle
            ctx.fillStyle = fill
            if max_width is not None:
                ctx.fillText(text, x, y, max_width)
            else:
                ctx.fillText(text, x, y)
            ctx.fillStyle = old_fill

        # Draw stroked text if stroke color provided
        if stroke:
            old_stroke = ctx.strokeStyle
            ctx.strokeStyle = stroke
            if max_width is not None:
                ctx.strokeText(text, x, y, max_width)
            else:
                ctx.strokeText(text, x, y)
            ctx.strokeStyle = old_stroke

        # Restore values
        if font:
            ctx.font = old_font
        if align:
            ctx.textAlign = old_align
        if baseline:
            ctx.textBaseline = old_baseline
        if line_width is not None:
            ctx.lineWidth = old_width

        return self

    def measure_text(self, text: str, font: Optional[str] = None) -> float:
        """
        Measure the width of text in pixels.

        Args:
            text: Text to measure
            font: Optional font to use for measurement

        Returns:
            Width of text in pixels with current or specified font

        Example:
            width = canvas.measure_text("Hello", font="24px Arial")
        """
        ctx = self.context

        if font:
            old_font = ctx.font
            ctx.font = font
            width = ctx.measureText(text).width
            ctx.font = old_font
            return width
        else:
            return ctx.measureText(text).width

    # ========== Style & State Methods ==========

    def set_fill_color(self, color: str) -> 'WebCanvas':
        """
        Set the fill color for shapes and text.

        Args:
            color: CSS color string (hex, rgb, rgba, named)

        Returns:
            Self for method chaining

        Example:
            canvas.set_fill_color("#ff0000")
            canvas.set_fill_color("rgb(255, 0, 0)")
            canvas.set_fill_color("rgba(255, 0, 0, 0.5)")
        """
        self.context.fillStyle = color
        return self

    def set_stroke_color(self, color: str) -> 'WebCanvas':
        """
        Set the stroke color for lines and outlines.

        Args:
            color: CSS color string

        Returns:
            Self for method chaining
        """
        self.context.strokeStyle = color
        return self

    def set_line_width(self, width: float) -> 'WebCanvas':
        """
        Set the line width for strokes.

        Args:
            width: Line width in pixels

        Returns:
            Self for method chaining

        Example:
            canvas.set_line_width(3).line(0, 0, 100, 100)
        """
        self.context.lineWidth = width
        return self

    def set_line_cap(self, cap: str) -> 'WebCanvas':
        """
        Set the line cap style.

        Args:
            cap: "butt", "round", or "square"

        Returns:
            Self for method chaining
        """
        self.context.lineCap = cap
        return self

    def set_line_join(self, join: str) -> 'WebCanvas':
        """
        Set the line join style.

        Args:
            join: "miter", "round", or "bevel"

        Returns:
            Self for method chaining
        """
        self.context.lineJoin = join
        return self

    def set_font(self, font: str) -> 'WebCanvas':
        """
        Set the font for text drawing.

        Args:
            font: CSS font string (e.g., "20px Arial", "bold 16px sans-serif")

        Returns:
            Self for method chaining

        Example:
            canvas.set_font("24px Arial")
            canvas.set_font("bold 18px 'Courier New'")
        """
        self.context.font = font
        return self

    def set_text_align(self, align: str) -> 'WebCanvas':
        """
        Set horizontal text alignment.

        Args:
            align: "left", "right", "center", "start", or "end"

        Returns:
            Self for method chaining
        """
        self.context.textAlign = align
        return self

    def set_text_baseline(self, baseline: str) -> 'WebCanvas':
        """
        Set vertical text baseline.

        Args:
            baseline: "top", "hanging", "middle", "alphabetic", "ideographic", "bottom"

        Returns:
            Self for method chaining
        """
        self.context.textBaseline = baseline
        return self

    def set_global_alpha(self, alpha: float) -> 'WebCanvas':
        """
        Set global transparency level.

        Args:
            alpha: Alpha value from 0.0 (transparent) to 1.0 (opaque)

        Returns:
            Self for method chaining

        Example:
            canvas.set_global_alpha(0.5).rect(0, 0, 100, 100, fill="#ff0000")
        """
        self.context.globalAlpha = alpha
        return self

    def save(self) -> 'WebCanvas':
        """
        Save the current drawing state (styles, transformations) to a stack.
        Use with restore() to temporarily change settings.

        Returns:
            Self for method chaining

        Example:
            canvas.save().set_fill_color("#ff0000").rect(0, 0, 50, 50).restore()
        """
        self.context.save()
        return self

    def restore(self) -> 'WebCanvas':
        """
        Restore the most recently saved drawing state from the stack.

        Returns:
            Self for method chaining
        """
        self.context.restore()
        return self

    # ========== Transformation Methods ==========

    def translate(self, x: float, y: float) -> 'WebCanvas':
        """
        Translate (move) the canvas origin.

        Args:
            x: Horizontal translation
            y: Vertical translation

        Returns:
            Self for method chaining
        """
        self.context.translate(x, y)
        return self

    def rotate(self, angle: float) -> 'WebCanvas':
        """
        Rotate the canvas.

        Args:
            angle: Rotation angle in radians

        Returns:
            Self for method chaining

        Example:
            import math
            canvas.save().translate(100, 100).rotate(math.pi / 4).rect(-25, -25, 50, 50, fill="#f00").restore()
        """
        self.context.rotate(angle)
        return self

    def scale(self, x: float, y: float) -> 'WebCanvas':
        """
        Scale the canvas.

        Args:
            x: Horizontal scaling factor
            y: Vertical scaling factor

        Returns:
            Self for method chaining
        """
        self.context.scale(x, y)
        return self

    # ========== Image Methods ==========

    def load_image(self, src: str, callback: Optional[Callable] = None) -> 'WebCanvas':
        """
        Load an image from a URL for later drawing.
        Images load asynchronously; use callback or on_image_loaded event.

        Args:
            src: Image URL or data URL
            callback: Optional callback(canvas, src, image) when loaded

        Returns:
            Self for method chaining

        Example:
            canvas.load_image("path/to/image.png",
                             lambda c, src, img: c.draw_image(img, 0, 0))

            # Or with event:
            canvas.on('image_loaded', lambda c, src, img: c.draw_image(img, 0, 0))
            canvas.load_image("path/to/image.png")
        """
        # Check if image already in cache
        if src in self._image_cache:
            image = self._image_cache[src]
            if callback:
                callback(self, src, image)
            return self

        # Check if already loading
        if src in self._pending_images:
            if callback:
                self._pending_images[src].append(callback)
            return self

        # Start loading
        self._pending_images[src] = [callback] if callback else []

        # Create image object
        img = js.Image.new()

        def on_load(event):
            # Cache the image
            self._image_cache[src] = img

            # Call user callback if provided
            if callback:
                callback(self, src, img)

            # Call all pending callbacks
            for pending_cb in self._pending_images.get(src, []):
                if pending_cb:
                    pending_cb(self, src, img)

            # Trigger event
            self._trigger_callbacks('image_loaded', src, img)

            # Clean up
            if src in self._pending_images:
                del self._pending_images[src]

        def on_error(event):
            print(f"Failed to load image: {src}")
            if src in self._pending_images:
                del self._pending_images[src]

        # Attach event handlers with proxies
        img.onload = create_proxy(on_load)
        img.onerror = create_proxy(on_error)

        # Start loading
        img.src = src

        return self

    def draw_image(self, image_or_src: Union[Any, str],
                   dx: float, dy: float,
                   dwidth: Optional[float] = None,
                   dheight: Optional[float] = None,
                   sx: Optional[float] = None,
                   sy: Optional[float] = None,
                   swidth: Optional[float] = None,
                   sheight: Optional[float] = None) -> 'WebCanvas':
        """
        Draw an image on the canvas.

        Args:
            image_or_src: Image object or URL string (must be pre-loaded if URL)
            dx: Destination X coordinate
            dy: Destination Y coordinate
            dwidth: Optional destination width (scales image)
            dheight: Optional destination height (scales image)
            sx: Optional source X coordinate (for cropping)
            sy: Optional source Y coordinate (for cropping)
            swidth: Optional source width (for cropping)
            sheight: Optional source height (for cropping)

        Returns:
            Self for method chaining

        Example:
            # Simple draw (using cached image):
            canvas.draw_image("path/to/image.png", 10, 10)

            # Draw with scaling:
            canvas.draw_image(img, 10, 10, 200, 150)

            # Draw with cropping and scaling:
            canvas.draw_image(img, 10, 10, 100, 100, 50, 50, 100, 100)
        """
        ctx = self.context

        # If string provided, look up in cache
        if isinstance(image_or_src, str):
            if image_or_src not in self._image_cache:
                print(f"Warning: Image not loaded: {image_or_src}. Call load_image() first.")
                return self
            img = self._image_cache[image_or_src]
        else:
            img = image_or_src

        # Determine which drawImage overload to use
        if sx is not None and sy is not None and swidth is not None and sheight is not None:
            # Full 9-argument version (crop + scale)
            if dwidth is not None and dheight is not None:
                ctx.drawImage(img, sx, sy, swidth, sheight, dx, dy, dwidth, dheight)
            else:
                print("Warning: sx, sy, swidth, sheight provided but dwidth, dheight missing")
                ctx.drawImage(img, dx, dy)
        elif dwidth is not None and dheight is not None:
            # 5-argument version (scale only)
            ctx.drawImage(img, dx, dy, dwidth, dheight)
        else:
            # 3-argument version (no scaling)
            ctx.drawImage(img, dx, dy)

        return self

    # ========== Utility Methods ==========

    def clear(self, color: Optional[str] = None) -> 'WebCanvas':
        """
        Clear the entire canvas. Optionally fill with a color.

        Args:
            color: Optional color to fill after clearing

        Returns:
            Self for method chaining

        Example:
            canvas.clear()  # Clear to transparent
            canvas.clear("#ffffff")  # Clear and fill white
        """
        width = self._get_state('width')
        height = self._get_state('height')
        ctx = self.context

        # Clear the canvas
        ctx.clearRect(0, 0, width, height)

        # Fill with color if provided
        if color:
            ctx.save()
            ctx.fillStyle = color
            ctx.fillRect(0, 0, width, height)
            ctx.restore()

        # Trigger callback
        self._trigger_callbacks('clear')

        return self

    def resize(self, width: int, height: int, clear: bool = True) -> 'WebCanvas':
        """
        Resize the canvas dimensions.

        Args:
            width: New width in pixels
            height: New height in pixels
            clear: Whether to clear the canvas (default: True)

        Returns:
            Self for method chaining

        Note:
            Resizing clears the canvas content due to Canvas API behavior.

        Example:
            canvas.resize(1024, 768)
        """
        # Update state
        self._set_state(width=width, height=height)

        # Get canvas element
        canvas = self._get_element('canvas')

        # Set attributes and DOM properties
        canvas.set_attribute('width', str(width))
        canvas.set_attribute('height', str(height))
        canvas._dom_element.width = width
        canvas._dom_element.height = height

        # Clear if requested
        if clear:
            self.clear()

        return self

    def to_data_url(self, mime_type: str = "image/png",
                    quality: Optional[float] = None) -> str:
        """
        Export canvas as a data URL string.

        Args:
            mime_type: Image MIME type ("image/png", "image/jpeg", "image/webp")
            quality: Quality for lossy formats (0.0 to 1.0), ignored for PNG

        Returns:
            Data URL string that can be used in <img> src or downloaded

        Example:
            # PNG (lossless):
            data_url = canvas.to_data_url()

            # JPEG with quality:
            data_url = canvas.to_data_url("image/jpeg", 0.8)
        """
        canvas = self._get_element('canvas')

        if quality is not None:
            return canvas._dom_element.toDataURL(mime_type, quality)
        else:
            return canvas._dom_element.toDataURL(mime_type)

    def download(self, filename: str = "canvas.png",
                 mime_type: str = "image/png",
                 quality: Optional[float] = None) -> 'WebCanvas':
        """
        Trigger browser download of canvas as an image file.

        Args:
            filename: Name for downloaded file
            mime_type: Image MIME type
            quality: Quality for lossy formats (0.0 to 1.0)

        Returns:
            Self for method chaining

        Example:
            canvas.download("my-drawing.png")
            canvas.download("my-photo.jpg", "image/jpeg", 0.9)
        """
        # Get data URL
        data_url = self.to_data_url(mime_type, quality)

        # Create temporary link element
        link = js.document.createElement('a')
        link.download = filename
        link.href = data_url
        link.click()

        return self

    # ========== Properties ==========

    @property
    def width(self) -> int:
        """Get canvas width."""
        return self._get_state('width')

    @property
    def height(self) -> int:
        """Get canvas height."""
        return self._get_state('height')

    @property
    def context(self) -> Any:
        """Get the 2D rendering context for advanced operations."""
        return self._get_state('context')
