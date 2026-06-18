"""
Quartzite Theme
An alpine theme inspired by the Albion Mountains of Idaho
Colors from Lake Cleveland, Mt. Harrison, quartzite rocks, and alpine wildflowers
"""
from antioch.elements import (
    Button as _Button,
    H1 as _H1,
    H2 as _H2,
    H3 as _H3,
    H4 as _H4,
    H5 as _H5,
    H6 as _H6,
    P as _P,
    Div as _Div,
    Input as _Input,
    Textarea as _Textarea,
    Select as _Select,
    A as _A,
    Code as _Code,
    Pre as _Pre,
    Hr as _Hr,
)

# Quartzite Color Palette - Albion Mountains Alpine
COLORS = {
    "background": "#f8f9fa",       # Bright quartzite white
    "surface": "#ffffff",          # Pure white (sunlit rock)
    "surface_variant": "#e9ecef",  # Light gray stone
    "text": "#2c3e50",             # Deep charcoal
    "text_secondary": "#6c757d",   # Medium gray
    "accent": "#4a9fb0",           # Alpine lake teal (Lake Cleveland)
    "accent_hover": "#5bb5c7",     # Lighter teal
    "border": "#dee2e6",           # Soft gray border
    "lupine": "#6b5b95",           # Wild lupine purple
    "alpine_yellow": "#f4a261",    # Mountain buttercup
    "mountain_pink": "#e76f8f",    # Indian paintbrush
    "rock_gray": "#95a5a6",        # Quartzite gray
    "error": "#e63946",            # Bright red
    "success": "#52b788",          # Alpine green
}

# Base font configuration
FONTS = {
    "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    "size": "14px",
    "line_height": "1.6",
}


class Button(_Button):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["accent"],
            "color": "#ffffff",
            "border": "none",
            "border-radius": "12px",
            "padding": "10px 20px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "font-weight": "600",
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "box-shadow": "0 2px 8px rgba(74, 159, 176, 0.2)",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]
            sender.style.box_shadow = "0 4px 12px rgba(74, 159, 176, 0.3)"
            sender.style.transform = "translateY(-1px)"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]
            sender.style.box_shadow = "0 2px 8px rgba(74, 159, 176, 0.2)"
            sender.style.transform = "translateY(0)"


class H1(_H1):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "700",
            "letter-spacing": "-0.02em",
        })


class H2(_H2):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "700",
            "letter-spacing": "-0.01em",
        })


class H3(_H3):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["lupine"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H4(_H4):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["lupine"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H5(_H5):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text_secondary"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H6(_H6):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text_secondary"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class P(_P):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "line-height": FONTS["line_height"],
            "margin": "0.5em 0",
        })


class Div(_Div):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        # Divs don't get default styling unless specified
        # Users can add their own styles


class Input(_Input):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "10px",
            "padding": "10px 14px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "transition": "all 0.3s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 159, 176, 0.1)"

        @self.events.blur.subscribe
        def on_blur(sender, *args):
            sender.style.border_color = COLORS["border"]
            sender.style.box_shadow = "none"


class Textarea(_Textarea):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "10px",
            "padding": "10px 14px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "resize": "vertical",
            "transition": "all 0.3s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 159, 176, 0.1)"

        @self.events.blur.subscribe
        def on_blur(sender, *args):
            sender.style.border_color = COLORS["border"]
            sender.style.box_shadow = "none"


class Select(_Select):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "10px",
            "padding": "10px 14px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "cursor": "pointer",
        })


class A(_A):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["accent"],
            "text-decoration": "none",
            "font-family": FONTS["family"],
            "border-bottom": f"2px solid {COLORS['alpine_yellow']}",
            "transition": "all 0.2s ease",
            "padding-bottom": "2px",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.color = COLORS["lupine"]
            sender.style.border_bottom_color = COLORS["mountain_pink"]

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.color = COLORS["accent"]
            sender.style.border_bottom_color = COLORS["alpine_yellow"]


class Code(_Code):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["lupine"],
            "padding": "3px 8px",
            "border-radius": "6px",
            "font-family": "'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace",
            "font-size": "0.9em",
            "border": f"1px solid {COLORS['border']}",
        })


class Pre(_Pre):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["text"],
            "padding": "16px",
            "border-radius": "12px",
            "border": f"2px solid {COLORS['border']}",
            "font-family": "'SF Mono', Monaco, 'Cascadia Code', 'Courier New', monospace",
            "font-size": "0.9em",
            "overflow-x": "auto",
            "line-height": "1.5",
        })


class Hr(_Hr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style.update({
            "border": "none",
            "height": "2px",
            "background": f"linear-gradient(to right, {COLORS['alpine_yellow']}, {COLORS['accent']}, {COLORS['lupine']}, {COLORS['mountain_pink']})",
            "margin": "2em 0",
            "border-radius": "2px",
        })


class Card(Div):
    """A themed card container with alpine styling"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "16px",
            "padding": "24px",
            "margin": "16px 0",
            "box-shadow": "0 4px 12px rgba(0,0,0,0.05), 0 1px 4px rgba(0,0,0,0.08)",
        })


class Container(Div):
    """A centered container with max-width"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "max-width": "1200px",
            "margin": "0 auto",
            "padding": "24px",
        })