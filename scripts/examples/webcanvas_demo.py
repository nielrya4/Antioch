"""
WebCanvas Demo - Showcasing the WebCanvas macro capabilities.

Demonstrates various drawing features:
- Basic shapes (rectangles, circles, ellipses)
- Lines and complex paths
- Text rendering
- Transformations (translate, rotate, scale)
- Animations
- Export functionality
"""

import math
import js
from pyodide.ffi import create_proxy
from antioch import DOM, Div, H1, H2, P, Button
from antioch.macros import WebCanvas


def create_section(title, description=""):
    """Helper to create a section header."""
    section = Div(style={
        "margin_bottom": "30px",
        "padding": "20px",
        "background_color": "#f9f9f9",
        "border_radius": "8px"
    })

    section.add(H2(title, style={"margin_top": "0", "color": "#333"}))

    if description:
        section.add(P(description, style={"color": "#666", "margin_bottom": "15px"}))

    return section


def demo_basic_shapes():
    """Demo: Basic shape drawing with fill and stroke."""
    section = create_section(
        "Basic Shapes",
        "Rectangles, circles, and ellipses with fill and stroke parameters"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")

    # Rectangle with fill only
    canvas.rect(50, 50, 100, 80, fill="#ff6b6b")

    # Rectangle with stroke only
    canvas.rect(180, 50, 100, 80, stroke="#4ecdc4", line_width=3)

    # Rectangle with both fill and stroke
    canvas.rect(310, 50, 100, 80, fill="#ffe66d", stroke="#333", line_width=2)

    # Circle with fill
    canvas.circle(100, 200, 40, fill="#95e1d3")

    # Circle with stroke
    canvas.circle(230, 200, 40, stroke="#f38181", line_width=3)

    # Circle with both
    canvas.circle(360, 200, 40, fill="#aa96da", stroke="#333", line_width=2)

    # Ellipse
    canvas.ellipse(490, 150, 60, 40, 0, fill="#fec8d8", stroke="#333", line_width=2)

    section.add(canvas.element)
    return section


def demo_lines_and_paths():
    """Demo: Lines and complex path drawing."""
    section = create_section(
        "Lines & Paths",
        "Drawing lines and creating complex shapes with paths"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")

    # Simple lines
    canvas.line(50, 50, 150, 50, stroke="#e74c3c", line_width=2)
    canvas.line(50, 80, 150, 80, stroke="#3498db", line_width=4)
    canvas.line(50, 120, 150, 120, stroke="#2ecc71", line_width=6)

    # Triangle using paths
    canvas.begin_path()
    canvas.move_to(230, 50)
    canvas.line_to(280, 150)
    canvas.line_to(180, 150)
    canvas.close_path()
    canvas.fill("#f39c12")
    canvas.stroke("#333", 2)

    # Star shape using paths
    canvas.begin_path()
    cx, cy = 450, 100
    outer_radius, inner_radius = 50, 25
    points = 5

    for i in range(points * 2):
        angle = (i * math.pi / points) - math.pi / 2
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)

        if i == 0:
            canvas.move_to(x, y)
        else:
            canvas.line_to(x, y)

    canvas.close_path()
    canvas.fill("#ffd700")
    canvas.stroke("#333", 2)

    # Curved path
    canvas.begin_path()
    canvas.move_to(50, 200)
    canvas.quadratic_curve_to(150, 150, 250, 200)
    canvas.stroke("#9b59b6", 3)

    # Bezier curve
    canvas.begin_path()
    canvas.move_to(300, 200)
    canvas.bezier_curve_to(350, 150, 450, 250, 550, 200)
    canvas.stroke("#e67e22", 3)

    section.add(canvas.element)
    return section


def demo_text_rendering():
    """Demo: Text rendering with various styles."""
    section = create_section(
        "Text Rendering",
        "Drawing text with different fonts, sizes, and alignment"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")

    # Different font sizes
    canvas.text("Small Text", 50, 50, fill="#333", font="12px Arial")
    canvas.text("Medium Text", 50, 80, fill="#333", font="18px Arial")
    canvas.text("Large Text", 50, 120, fill="#333", font="24px Arial")
    canvas.text("Extra Large", 50, 160, fill="#333", font="32px Arial")

    # Different fonts
    canvas.text("Arial Font", 300, 50, fill="#333", font="20px Arial")
    canvas.text("Courier Font", 300, 80, fill="#333", font="20px 'Courier New'")
    canvas.text("Sans-Serif", 300, 110, fill="#333", font="20px sans-serif")
    canvas.text("Monospace", 300, 140, fill="# 333", font="20px monospace")

    # Text alignment
    canvas.line(300, 200, 300, 280, stroke="#ddd", line_width=1)  # Center line
    canvas.text("Left", 300, 210, fill="#e74c3c", font="16px Arial", align="left")
    canvas.text("Center", 300, 235, fill="#3498db", font="16px Arial", align="center")
    canvas.text("Right", 300, 260, fill="#2ecc71", font="16px Arial", align="right")

    # Bold and styled
    canvas.text("Bold Text", 50, 210, fill="#333", font="bold 20px Arial")
    canvas.text("Italic Text", 50, 240, fill="#333", font="italic 20px Arial")
    canvas.text("Bold Italic", 50, 270, fill="#333", font="bold italic 20px Arial")

    # Text with stroke
    canvas.text("OUTLINED", 450, 220, stroke="#e74c3c", font="bold 28px Arial", line_width=2)

    section.add(canvas.element)
    return section


def demo_transformations():
    """Demo: Transformations (translate, rotate, scale)."""
    section = create_section(
        "Transformations",
        "Translate, rotate, and scale operations"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")

    # Original (no transformation)
    canvas.rect(50, 50, 60, 40, fill="#3498db", stroke="#333", line_width=2)
    canvas.text("Original", 55, 105, fill="#333", font="12px Arial")

    # Translated
    canvas.save()
    canvas.translate(150, 0)
    canvas.rect(50, 50, 60, 40, fill="#e74c3c", stroke="#333", line_width=2)
    canvas.text("Translated", 55, 105, fill="#333", font="12px Arial")
    canvas.restore()

    # Rotated
    canvas.save()
    canvas.translate(300, 70)
    canvas.rotate(math.pi / 6)  # 30 degrees
    canvas.rect(-30, -20, 60, 40, fill="#2ecc71", stroke="#333", line_width=2)
    canvas.restore()
    canvas.text("Rotated", 270, 105, fill="#333", font="12px Arial")

    # Scaled
    canvas.save()
    canvas.translate(450, 70)
    canvas.scale(1.5, 1.5)
    canvas.rect(-30, -20, 60, 40, fill="#f39c12", stroke="#333", line_width=2)
    canvas.restore()
    canvas.text("Scaled", 420, 115, fill="#333", font="12px Arial")

    # Complex transformation
    canvas.save()
    canvas.translate(150, 200)
    canvas.rotate(math.pi / 4)  # 45 degrees
    canvas.scale(0.8, 1.2)
    canvas.rect(-40, -30, 80, 60, fill="#9b59b6", stroke="#333", line_width=2)
    canvas.restore()
    canvas.text("Combined", 110, 250, fill="#333", font="12px Arial")

    # Multiple rotated rectangles (flower pattern)
    canvas.save()
    canvas.translate(450, 200)
    for i in range(8):
        canvas.rotate(math.pi / 4)
        canvas.rect(0, -10, 50, 20, fill="#ff6b9d", stroke="#333", line_width=1)
    canvas.restore()
    canvas.text("Pattern", 420, 250, fill="#333", font="12px Arial")

    section.add(canvas.element)
    return section


def demo_gradients_and_alpha():
    """Demo: Transparency and alpha blending."""
    section = create_section(
        "Transparency",
        "Using global alpha for transparency effects"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")

    # Overlapping circles with different alpha
    alphas = [1.0, 0.8, 0.6, 0.4, 0.2]
    colors = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6"]

    for i, (alpha, color) in enumerate(zip(alphas, colors)):
        canvas.set_global_alpha(alpha)
        canvas.circle(100 + i * 40, 100, 50, fill=color)

    canvas.set_global_alpha(1.0)  # Reset
    canvas.text("Varying Alpha", 70, 180, fill="#333", font="16px Arial")

    # Overlapping rectangles
    canvas.rect(350, 50, 80, 80, fill="#e74c3c")
    canvas.set_global_alpha(0.7)
    canvas.rect(390, 70, 80, 80, fill="#3498db")
    canvas.set_global_alpha(0.5)
    canvas.rect(430, 90, 80, 80, fill="#2ecc71")
    canvas.set_global_alpha(1.0)  # Reset

    canvas.text("Overlapping", 380, 200, fill="#333", font="16px Arial")

    section.add(canvas.element)
    return section


def demo_animation():
    """Demo: Simple animation using requestAnimationFrame."""
    section = create_section(
        "Animation",
        "Animated bouncing balls using requestAnimationFrame"
    )

    canvas = WebCanvas(width=600, height=300, background="#1a1a2e")

    # Ball state
    balls = [
        {"x": 100, "y": 150, "dx": 3, "dy": 2, "radius": 15, "color": "#e74c3c"},
        {"x": 300, "y": 100, "dx": -2, "dy": 3, "radius": 20, "color": "#3498db"},
        {"x": 500, "y": 200, "dx": -3, "dy": -2, "radius": 18, "color": "#2ecc71"},
    ]

    def animate():
        # Clear canvas
        canvas.clear("#1a1a2e")

        # Update and draw each ball
        for ball in balls:
            # Move
            ball["x"] += ball["dx"]
            ball["y"] += ball["dy"]

            # Bounce off walls
            if ball["x"] - ball["radius"] < 0 or ball["x"] + ball["radius"] > 600:
                ball["dx"] = -ball["dx"]
            if ball["y"] - ball["radius"] < 0 or ball["y"] + ball["radius"] > 300:
                ball["dy"] = -ball["dy"]

            # Keep in bounds
            ball["x"] = max(ball["radius"], min(600 - ball["radius"], ball["x"]))
            ball["y"] = max(ball["radius"], min(300 - ball["radius"], ball["y"]))

            # Draw
            canvas.circle(ball["x"], ball["y"], ball["radius"], fill=ball["color"])

        # Continue animation
        js.requestAnimationFrame(create_proxy(lambda t: animate()))

    # Start animation
    animate()

    section.add(canvas.element)
    return section


def demo_interactive_drawing():
    """Demo: Interactive drawing with mouse events."""
    section = create_section(
        "Interactive Drawing",
        "Click and drag to draw on the canvas"
    )

    canvas = WebCanvas(width=600, height=300, background="#ffffff")
    canvas_element = canvas._get_element('canvas')

    # Drawing state
    drawing_state = {
        "is_drawing": False,
        "last_x": 0,
        "last_y": 0
    }

    def get_mouse_pos(event):
        """Get mouse position relative to canvas."""
        rect = canvas_element._dom_element.getBoundingClientRect()
        return event.clientX - rect.left, event.clientY - rect.top

    def on_mousedown(event):
        x, y = get_mouse_pos(event)
        drawing_state["is_drawing"] = True
        drawing_state["last_x"] = x
        drawing_state["last_y"] = y
        canvas.context.beginPath()
        canvas.context.moveTo(x, y)

    def on_mousemove(event):
        if not drawing_state["is_drawing"]:
            return

        x, y = get_mouse_pos(event)
        canvas.set_stroke_color("#333")
        canvas.set_line_width(2)
        canvas.set_line_cap("round")
        canvas.line(drawing_state["last_x"], drawing_state["last_y"], x, y)
        drawing_state["last_x"] = x
        drawing_state["last_y"] = y

    def on_mouseup(event):
        drawing_state["is_drawing"] = False

    # Attach event handlers
    canvas_element.on_mousedown(on_mousedown)
    canvas_element.on('mousemove', on_mousemove)  # Use generic on() for mousemove
    canvas_element.on_mouseup(on_mouseup)
    canvas_element.on_mouseleave(on_mouseup)

    # Add clear button
    clear_btn = Button("Clear Canvas", style={
        "margin_top": "10px",
        "padding": "8px 16px",
        "background_color": "#e74c3c",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px"
    })
    clear_btn.on_click(lambda e: canvas.clear("#ffffff"))

    section.add(canvas.element)
    section.add(clear_btn)
    return section


def demo_export():
    """Demo: Export canvas to image file."""
    section = create_section(
        "Export Functionality",
        "Export canvas as PNG or JPEG image"
    )

    canvas = WebCanvas(width=400, height=200, background="#ecf0f1")

    # Draw something interesting
    canvas.text("Export Me!", 200, 60,
               fill="#2c3e50",
               font="bold 32px Arial",
               align="center")

    canvas.circle(100, 130, 40, fill="#e74c3c", stroke="#c0392b", line_width=3)
    canvas.rect(160, 90, 80, 80, fill="#3498db", stroke="#2980b9", line_width=3)
    canvas.begin_path()
    canvas.move_to(300, 130)
    canvas.line_to(340, 90)
    canvas.line_to(380, 130)
    canvas.close_path()
    canvas.fill("#2ecc71")
    canvas.stroke("#27ae60", 3)

    # Export buttons
    buttons_div = Div(style={"margin_top": "10px", "display": "flex", "gap": "10px"})

    png_btn = Button("Download PNG", style={
        "padding": "8px 16px",
        "background_color": "#3498db",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px"
    })
    png_btn.on_click(lambda e: canvas.download("my-canvas.png", "image/png"))

    jpg_btn = Button("Download JPEG", style={
        "padding": "8px 16px",
        "background_color": "#2ecc71",
        "color": "white",
        "border": "none",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px"
    })
    jpg_btn.on_click(lambda e: canvas.download("my-canvas.jpg", "image/jpeg", 0.9))

    buttons_div.add(png_btn, jpg_btn)

    section.add(canvas.element)
    section.add(buttons_div)
    return section


def demo_complex_scene():
    """Demo: Complex scene combining multiple techniques."""
    section = create_section(
        "Complex Scene",
        "Combining shapes, text, and transformations"
    )

    canvas = WebCanvas(width=600, height=400, background="#87CEEB")  # Sky blue

    # Sun
    canvas.circle(500, 80, 40, fill="#FDB813")
    for i in range(12):
        angle = i * (2 * math.pi / 12)
        x1 = 500 + 50 * math.cos(angle)
        y1 = 80 + 50 * math.sin(angle)
        x2 = 500 + 70 * math.cos(angle)
        y2 = 80 + 70 * math.sin(angle)
        canvas.line(x1, y1, x2, y2, stroke="#FDB813", line_width=3)

    # Ground
    canvas.rect(0, 300, 600, 100, fill="#90EE90")

    # House
    canvas.rect(150, 200, 150, 100, fill="#D2691E", stroke="#8B4513", line_width=2)
    canvas.begin_path()
    canvas.move_to(140, 200)
    canvas.line_to(225, 150)
    canvas.line_to(310, 200)
    canvas.close_path()
    canvas.fill("#8B0000")
    canvas.stroke("#800000", 2)

    # Door
    canvas.rect(200, 240, 50, 60, fill="#654321", stroke="#000", line_width=2)
    canvas.circle(240, 270, 3, fill="#FFD700")

    # Windows
    canvas.rect(170, 220, 30, 30, fill="#87CEEB", stroke="#000", line_width=2)
    canvas.line(185, 220, 185, 250, stroke="#000", line_width=1)
    canvas.line(170, 235, 200, 235, stroke="#000", line_width=1)

    canvas.rect(250, 220, 30, 30, fill="#87CEEB", stroke="#000", line_width=2)
    canvas.line(265, 220, 265, 250, stroke="#000", line_width=1)
    canvas.line(250, 235, 280, 235, stroke="#000", line_width=1)

    # Tree
    canvas.rect(420, 250, 30, 50, fill="#8B4513")
    canvas.circle(435, 240, 40, fill="#228B22")
    canvas.circle(410, 220, 35, fill="#228B22")
    canvas.circle(460, 220, 35, fill="#228B22")

    # Clouds
    def draw_cloud(x, y):
        canvas.circle(x, y, 20, fill="#FFFFFF")
        canvas.circle(x + 20, y - 5, 25, fill="#FFFFFF")
        canvas.circle(x + 45, y, 20, fill="#FFFFFF")
        canvas.circle(x + 25, y + 10, 20, fill="#FFFFFF")

    draw_cloud(50, 80)
    draw_cloud(350, 120)

    # Birds
    def draw_bird(x, y):
        canvas.begin_path()
        canvas.move_to(x, y)
        canvas.quadratic_curve_to(x + 10, y - 8, x + 20, y)
        canvas.stroke("#000", 2)
        canvas.begin_path()
        canvas.move_to(x + 20, y)
        canvas.quadratic_curve_to(x + 30, y - 8, x + 40, y)
        canvas.stroke("#000", 2)

    draw_bird(100, 150)
    draw_bird(450, 100)
    draw_bird(250, 130)

    # Title
    canvas.text("My Canvas Scene", 300, 380,
               fill="#333",
               font="bold 20px Arial",
               align="center")

    section.add(canvas.element)
    return section


# Main demo assembly
def main():
    """Assemble and display all WebCanvas demos."""
    container = Div(style={
        "max_width": "800px",
        "margin": "0 auto",
        "padding": "20px",
        "font_family": "Arial, sans-serif"
    })

    # Main title
    title = H1("WebCanvas Demo", style={
        "text_align": "center",
        "color": "#2c3e50",
        "margin_bottom": "10px"
    })

    subtitle = P(
        "A comprehensive demonstration of the WebCanvas macro for Antioch",
        style={
            "text_align": "center",
            "color": "#7f8c8d",
            "margin_bottom": "40px",
            "font_size": "18px"
        }
    )

    container.add(title, subtitle)

    # Add all demos
    container.add(demo_basic_shapes())
    container.add(demo_lines_and_paths())
    container.add(demo_text_rendering())
    container.add(demo_transformations())
    container.add(demo_gradients_and_alpha())
    container.add(demo_animation())
    container.add(demo_interactive_drawing())
    container.add(demo_export())
    container.add(demo_complex_scene())

    # Add to DOM
    DOM.add(container)


# Run demo when explicitly called from main.py
# (Don't run on import, only when main() is called)
