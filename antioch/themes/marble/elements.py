"""
Marble Light Theme
A clean, elegant light theme for Antioch applications
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

# Marble Color Palette
COLORS = {
    "background": "#f5f5f7",       # Light gray background
    "surface": "#ffffff",          # Pure white for cards
    "surface_variant": "#e8e8ed",  # Subtle gray variant
    "text": "#1d1d1f",             # Dark charcoal text
    "text_secondary": "#6e6e73",   # Medium gray
    "accent": "#0066cc",           # Vibrant blue accent
    "accent_hover": "#0077ed",     # Lighter blue hover
    "border": "#d2d2d7",           # Light border
    "error": "#d1403f",            # Bright red
    "success": "#34c759",          # Bright green
}

# Base font configuration
FONTS = {
    "family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif",
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
            "border-radius": "8px",
            "padding": "10px 20px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "font-weight": "500",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "box-shadow": "0 1px 3px rgba(0,0,0,0.1)",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]
            sender.style.box_shadow = "0 2px 6px rgba(0,0,0,0.15)"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]
            sender.style.box_shadow = "0 1px 3px rgba(0,0,0,0.1)"


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
            "border-radius": "8px",
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
            sender.style.box_shadow = f"0 0 0 3px rgba(0, 102, 204, 0.1)"

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
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "8px",
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
            sender.style.box_shadow = f"0 0 0 3px rgba(0, 102, 204, 0.1)"

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
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "8px",
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
            "background-color": COLORS["surface_variant"],
            "color": COLORS["accent"],
            "padding": "3px 8px",
            "border-radius": "4px",
            "font-family": "'SF Mono', Monaco, 'Cascadia Code', monospace",
            "font-size": "0.9em",
        })


class Pre(_Pre):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["text"],
            "padding": "16px",
            "border-radius": "8px",
            "border": f"1px solid {COLORS['border']}",
            "font-family": "'SF Mono', Monaco, 'Cascadia Code', monospace",
            "font-size": "0.9em",
            "overflow-x": "auto",
            "line-height": "1.5",
        })


class Hr(_Hr):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style.update({
            "border": "none",
            "border-top": f"1px solid {COLORS['border']}",
            "margin": "1.5em 0",
        })


class Card(Div):
    """A themed card container with shadow"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"1px solid {COLORS['border']}",
            "border-radius": "12px",
            "padding": "20px",
            "margin": "12px 0",
            "box-shadow": "0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1)",
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