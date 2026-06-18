"""
Diorite Dark Theme
A cohesive dark theme for Antioch applications
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

# Diorite Color Palette
COLORS = {
    "background": "#1a1b1a",       # Very dark gray
    "surface": "#282a29",          # Dark charcoal
    "surface_variant": "#3a3c3b",  # Medium gray
    "text": "#d2d3d8",             # Light gray text
    "text_secondary": "#9ca0a3",   # Muted gray
    "accent": "#5c8ab0",           # Muted blue accent
    "accent_hover": "#7aa3c7",     # Lighter blue
    "border": "#404240",           # Subtle border
    "error": "#c77979",            # Muted red
    "success": "#79c79a",          # Muted green
}

# Base font configuration
FONTS = {
    "family": "Arial, Helvetica, sans-serif",
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
            "border-radius": "4px",
            "padding": "8px 16px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "cursor": "pointer",
            "transition": "background-color 0.2s ease",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]


class H1(_H1):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
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
            "color": COLORS["text"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H4(_H4):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["text"],
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
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "4px",
            "padding": "8px 12px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]

        @self.events.blur.subscribe
        def on_blur(sender, *args):
            sender.style.border_color = COLORS["border"]


class Textarea(_Textarea):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "4px",
            "padding": "8px 12px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "outline": "none",
            "resize": "vertical",
        })

        # Add focus effect
        @self.events.focus.subscribe
        def on_focus(sender, *args):
            sender.style.border_color = COLORS["accent"]

        @self.events.blur.subscribe
        def on_blur(sender, *args):
            sender.style.border_color = COLORS["border"]


class Select(_Select):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "4px",
            "padding": "8px 12px",
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
            "transition": "color 0.2s ease",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.color = COLORS["accent_hover"]
            sender.style.text_decoration = "underline"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.color = COLORS["accent"]
            sender.style.text_decoration = "none"


class Code(_Code):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["accent"],
            "padding": "2px 6px",
            "border-radius": "3px",
            "font-family": "monospace",
            "font-size": "0.9em",
        })


class Pre(_Pre):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "color": COLORS["text"],
            "padding": "12px",
            "border-radius": "4px",
            "border": f"1px solid {COLORS['border']}",
            "font-family": "monospace",
            "font-size": "0.9em",
            "overflow-x": "auto",
        })


class Hr(_Hr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style.update({
            "border": "none",
            "border-top": f"1px solid {COLORS['border']}",
            "margin": "1em 0",
        })


class Card(Div):
    """A themed card container"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "8px",
            "padding": "16px",
            "margin": "8px 0",
        })


class Container(Div):
    """A centered container with max-width"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "max-width": "1200px",
            "margin": "0 auto",
            "padding": "20px",
        })