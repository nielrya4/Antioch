"""
Jasper Theme
A rich, earthy theme inspired by Owyhee, Biggs, and Willow Creek jaspers
Warm reds, blues, pastels, and earth tones
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

# Jasper Color Palette - Owyhee, Biggs, and Willow Creek
COLORS = {
    "background": "#f0e6d9",       # Willow Creek cream
    "surface": "#faf5f0",          # Light cream
    "surface_variant": "#e8dcc8",  # Warm beige
    "text": "#4a3829",             # Dark brown
    "text_secondary": "#7a6552",   # Medium brown
    "accent": "#7a9eb0",           # Biggs jasper sky blue
    "accent_hover": "#8fb3c5",     # Lighter sky blue
    "border": "#d4c4ab",           # Sandy tan
    "owyhee_red": "#a85751",       # Deep Owyhee red
    "willow_pink": "#daa59a",      # Willow Creek soft pink
    "willow_green": "#a4b5a0",     # Willow Creek sage
    "earth_brown": "#8b7355",      # Rich earth brown
    "error": "#b86156",            # Warm red
    "success": "#8fa588",          # Muted green
}

# Base font configuration
FONTS = {
    "family": "Georgia, 'Palatino Linotype', 'Book Antiqua', Palatino, serif",
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
            "border-radius": "8px",
            "padding": "10px 20px",
            "font-family": FONTS["family"],
            "font-size": FONTS["size"],
            "font-weight": "600",
            "cursor": "pointer",
            "transition": "all 0.3s ease",
            "box-shadow": f"0 2px 6px rgba(122, 158, 176, 0.25)",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.background_color = COLORS["accent_hover"]
            sender.style.box_shadow = f"0 4px 10px rgba(122, 158, 176, 0.35)"

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.background_color = COLORS["accent"]
            sender.style.box_shadow = f"0 2px 6px rgba(122, 158, 176, 0.25)"


class H1(_H1):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["owyhee_red"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "700",
            "letter-spacing": "-0.01em",
        })


class H2(_H2):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["earth_brown"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "700",
        })


class H3(_H3):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["accent"],
            "font-family": FONTS["family"],
            "margin": "0.5em 0",
            "font-weight": "600",
        })


class H4(_H4):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "color": COLORS["accent"],
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
            "border-radius": "8px",
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
            sender.style.box_shadow = f"0 0 0 3px rgba(122, 158, 176, 0.15)"

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
            "border-radius": "8px",
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
            sender.style.box_shadow = f"0 0 0 3px rgba(122, 158, 176, 0.15)"

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
            "color": COLORS["owyhee_red"],
            "text-decoration": "none",
            "font-family": FONTS["family"],
            "border-bottom": f"2px solid {COLORS['willow_pink']}",
            "transition": "all 0.2s ease",
            "padding-bottom": "2px",
        })

        # Add hover effect
        @self.events.mouseenter.subscribe
        def on_hover(sender, *args):
            sender.style.color = COLORS["accent"]
            sender.style.border_bottom_color = COLORS["willow_green"]

        @self.events.mouseleave.subscribe
        def on_leave(sender, *args):
            sender.style.color = COLORS["owyhee_red"]
            sender.style.border_bottom_color = COLORS["willow_pink"]


class Code(_Code):
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface_variant"],
            "color": COLORS["earth_brown"],
            "padding": "3px 8px",
            "border-radius": "5px",
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
            "border-radius": "8px",
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
            "height": "3px",
            "background": f"linear-gradient(to right, {COLORS['owyhee_red']}, {COLORS['willow_pink']}, {COLORS['accent']}, {COLORS['willow_green']})",
            "margin": "2em 0",
            "border-radius": "2px",
        })


class Card(Div):
    """A themed card container with jasper-inspired styling"""
    def __init__(self, *content, **kwargs):
        super().__init__(*content, **kwargs)
        self.style.update({
            "background-color": COLORS["surface"],
            "border": f"2px solid {COLORS['border']}",
            "border-radius": "12px",
            "padding": "22px",
            "margin": "14px 0",
            "box-shadow": "0 3px 10px rgba(74, 56, 41, 0.08), 0 1px 3px rgba(74, 56, 41, 0.12)",
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
