"""
Rhyolite Theme
An earthy theme inspired by the landscapes of eastern and central Oregon
Colors from rhyolite rock, clear water, junipers, sagebrush, and ponderosa pines
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

# Rhyolite Color Palette - Eastern Oregon Landscape
COLORS = {
    "background": "#f4ede1",       # Light rhyolite/cream
    "surface": "#faf6f0",          # Warm off-white
    "surface_variant": "#e8dcc8",  # Sandy tan
    "text": "#3d3428",             # Dark brown earth
    "text_secondary": "#6b5d4f",   # Medium brown
    "accent": "#4a7c7e",           # Clear water teal
    "accent_hover": "#5a9295",     # Lighter teal
    "border": "#d4c4ab",           # Warm beige border
    "juniper": "#4a6352",          # Juniper green
    "sage": "#8b9d8a",             # Sagebrush green
    "ponderosa": "#a67c52",        # Ponderosa bark
    "error": "#b5704f",            # Terracotta
    "success": "#6b8e6f",          # Forest green
}

# Base font configuration
FONTS = {
    "family": "Georgia, 'Times New Roman', serif",
    "size": "14px",
    "line_height": "1.7",
}


class Button(_Button):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["accent"],
            "color": "#ffffff",
            "border": "none",
            "border-radius": "6px",
            "padding": "10px 18px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "font-weight": "500",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "box-shadow": "0 2px 4px rgba(74, 124, 126, 0.2)",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]
            sender.style.box_shadow = "0 3px 6px rgba(74, 124, 126, 0.3)"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]
            sender.style.box_shadow = "0 2px 4px rgba(74, 124, 126, 0.2)"


class H1(_H1):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
            "letter-spacing": "-0.01em",
        })


class H2(_H2):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H3(_H3):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["juniper"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H4(_H4):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["juniper"],
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
            "transition": "border-color 0.2s ease, box-shadow 0.2s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 124, 126, 0.15)"

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
            "transition": "border-color 0.2s ease, box-shadow 0.2s ease",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]
            sender.style.box_shadow = f"0 0 0 3px rgba(74, 124, 126, 0.15)"

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
            "color": COLORS["accent"],
            "text-decoration": "underline",
            "text-decoration-color": COLORS["sage"],
            "text-decoration-thickness": "2px",
            "text-underline-offset": "3px",
            "font-family": FONTS["family"],
            "transition": "color 0.2s ease, text-decoration-color 0.2s ease",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.color = COLORS["juniper"]
            sender.style.text_decoration_color = COLORS["accent"]

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.color = COLORS["accent"]
            sender.style.text_decoration_color = COLORS["sage"]


class Code(_Code):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["juniper"],
            "padding": "3px 8px",
            "border-radius": "4px",
            "font-family": "'Courier New', Courier, monospace",
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
            "font-family": "'Courier New', Courier, monospace",
            "font-size": "0.9em",
            "overflow-x": "auto",
            "line-height": "1.6",
        })


class Hr(_Hr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style.update({
            "border": "none",
            "border-top": f"2px solid {COLORS['border']}",
            "margin": "1.5em 0",
        })


class Card(Div):
    """A themed card container with natural earth tones"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "10px",
            "padding": "20px",
            "margin": "12px 0",
            "box-shadow": "0 2px 8px rgba(61, 52, 40, 0.08)",
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