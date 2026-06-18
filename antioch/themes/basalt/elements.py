"""
Basalt Theme
A coastal theme inspired by the Pacific Northwest
Black basalt rock, scarlet salmonberries, western redcedar, salal, sand, and coastal waters
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

# Basalt Color Palette - Pacific Northwest Coast
COLORS = {
    "background": "#2a2f33",       # Dark basalt gray
    "surface": "#363c42",          # Lighter basalt
    "surface_variant": "#4a5259",  # Medium gray stone
    "text": "#e8e6e1",             # Light sand
    "text_secondary": "#b8aea0",   # Tan sand
    "accent": "#4a7a52",           # Western redcedar green (main accent)
    "accent_hover": "#5d9164",     # Lighter redcedar green
    "border": "#54595e",           # Stone edge
    "salmonberry": "#ff7555",      # Bright orange-red salmonberry
    "coastal_water": "#6b8e9e",    # Gray-blue coastal water
    "salal": "#6b5b7a",            # Purple salal
    "sand": "#c9b896",             # Tan sand
    "error": "#e65f5f",            # Bright red
    "success": "#6a9a6e",          # Forest green
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
            "color": COLORS["text"],
            "border": "none",
            "border-radius": "6px",
            "padding": "10px 20px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "font-weight": "600",
            "cursor": "pointer",
            "transition": "all 0.25s ease",
            "box-shadow": "0 2px 6px rgba(0, 0, 0, 0.3)",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]
            sender.style.box_shadow = "0 4px 10px rgba(0, 0, 0, 0.4)"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]
            sender.style.box_shadow = "0 2px 6px rgba(0, 0, 0, 0.3)"


class H1(_H1):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["sand"],
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
        })


class H3(_H3):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["salmonberry"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H4(_H4):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["coastal_water"],
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
            "border-radius": "6px",
            "padding": "10px 14px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "transition": "all 0.25s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 122, 82, 0.25)"

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
            "border-radius": "6px",
            "padding": "10px 14px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "resize": "vertical",
            "transition": "all 0.25s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 122, 82, 0.25)"

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
            "border-radius": "6px",
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
            "color": COLORS["salmonberry"],
            "text-decoration": "none",
            "font-family": FONTS["family"],
            "border-bottom": f"2px solid {COLORS['salal']}",
            "transition": "all 0.2s ease",
            "padding-bottom": "2px",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.color = COLORS["sand"]
            sender.style.border_bottom_color = COLORS["accent"]

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.color = COLORS["salmonberry"]
            sender.style.border_bottom_color = COLORS["salal"]


class Code(_Code):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["sand"],
            "padding": "3px 8px",
            "border-radius": "4px",
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
            "border-radius": "6px",
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
            "background": f"linear-gradient(to right, {COLORS['salmonberry']}, {COLORS['salal']}, {COLORS['coastal_water']}, {COLORS['accent']})",
            "margin": "2em 0",
            "border-radius": "1px",
        })


class Card(Div):
    """A themed card container with coastal basalt styling"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "8px",
            "padding": "20px",
            "margin": "12px 0",
            "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.4)",
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
