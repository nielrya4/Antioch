"""
Rhyolite Earthy Theme
Inspired by the high desert of eastern Oregon
"""

# Animation keyframes
KEYFRAMES = {
    "fadeIn": {
        "from": {
            "opacity": 0,
            "transform": "translateY(-10px)"
        },
        "to": {
            "opacity": 1,
            "transform": "translateY(0)"
        }
    }
}

# Rhyolite Color Palette
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
    "success": "#6b8e5c",          # Forest green
}

# Base font configuration
FONTS = {
    "family": "Georgia, 'Times New Roman', serif",
    "size": "14px",
    "line_height": "1.7",
}

# Element styles
ELEMENT_STYLES = {
    "Button": {
        "background-color": COLORS["accent"],
        "color": "#ffffff",
        "border": "none",
        "border-radius": "4px",
        "padding": "8px 16px",
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "cursor": "pointer",
        "transition": "background-color 0.2s ease",
        "animation": "fadeIn 0.5s ease-in",
    },
    "H1": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "H2": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "H3": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "H4": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "H5": {
        "color": COLORS["text_secondary"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "H6": {
        "color": COLORS["text_secondary"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "600",
    },
    "P": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "line-height": FONTS["line_height"],
        "margin": "0.5em 0",
    },
    "Input": {
        "background-color": COLORS["surface"],
        "color": COLORS["text"],
        "border": f"1px solid {COLORS['border']}",
        "border-radius": "4px",
        "padding": "8px 12px",
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "outline": "none",
        "transition": "border-color 0.2s ease",
        "animation": "fadeIn 0.5s ease-in",
    },
    "Textarea": {
        "background-color": COLORS["surface"],
        "color": COLORS["text"],
        "border": f"1px solid {COLORS['border']}",
        "border-radius": "4px",
        "padding": "8px 12px",
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "outline": "none",
        "resize": "vertical",
        "transition": "border-color 0.2s ease",
        "animation": "fadeIn 0.5s ease-in",
    },
    "Select": {
        "background-color": COLORS["surface"],
        "color": COLORS["text"],
        "border": f"1px solid {COLORS['border']}",
        "border-radius": "4px",
        "padding": "8px 12px",
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "outline": "none",
        "cursor": "pointer",
        "transition": "border-color 0.2s ease",
        "animation": "fadeIn 0.5s ease-in",
    },
    "A": {
        "color": COLORS["accent"],
        "text-decoration": "none",
        "transition": "color 0.2s ease",
    },
    "Code": {
        "background-color": COLORS["surface_variant"],
        "color": COLORS["text"],
        "padding": "2px 6px",
        "border-radius": "3px",
        "font-family": "'Courier New', monospace",
        "font-size": "0.9em",
    },
    "Pre": {
        "background-color": COLORS["surface"],
        "color": COLORS["text"],
        "padding": "12px",
        "border-radius": "4px",
        "border": f"1px solid {COLORS['border']}",
        "overflow-x": "auto",
        "font-family": "'Courier New', monospace",
        "font-size": "0.9em",
    },
    "Hr": {
        "border": "none",
        "height": "2px",
        "background": f"linear-gradient(to right, {COLORS['surface_variant']}, {COLORS['juniper']}, {COLORS['accent']}, {COLORS['sage']}, {COLORS['surface_variant']})",
        "margin": "1.5em 0",
    },
    "Form": {
        "margin": "1em 0",
    },
    "Label": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "display": "block",
        "margin": "0.5em 0 0.25em 0",
    },
    "Ul": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "line-height": FONTS["line_height"],
        "margin": "0.5em 0",
        "padding-left": "2em",
    },
    "Ol": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
        "line-height": FONTS["line_height"],
        "margin": "0.5em 0",
        "padding-left": "2em",
    },
    "Li": {
        "margin": "0.25em 0",
    },
    "Table": {
        "border-collapse": "collapse",
        "width": "100%",
        "margin": "1em 0",
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-size": FONTS["size"],
    },
    "Tr": {
        "border-bottom": f"1px solid {COLORS['border']}",
    },
    "Td": {
        "padding": "8px 12px",
        "text-align": "left",
    },
    "Th": {
        "padding": "8px 12px",
        "text-align": "left",
        "font-weight": "600",
        "background-color": COLORS["surface_variant"],
        "border-bottom": f"2px solid {COLORS['border']}",
    },
    "Thead": {
        "background-color": COLORS["surface_variant"],
    },
    "Tbody": {
    },
    "Blockquote": {
        "margin": "1em 0",
        "padding": "1em 1.5em",
        "border-left": f"4px solid {COLORS['accent']}",
        "background-color": COLORS["surface"],
        "color": COLORS["text_secondary"],
        "font-style": "italic",
    },
    "Fieldset": {
        "border": f"1px solid {COLORS['border']}",
        "border-radius": "4px",
        "padding": "1em",
        "margin": "1em 0",
    },
    "Legend": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "font-weight": "600",
        "padding": "0 0.5em",
    },
    "Mark": {
        "background-color": COLORS["ponderosa"],
        "color": COLORS["surface"],
        "padding": "2px 4px",
    },
    "Kbd": {
        "background-color": COLORS["surface_variant"],
        "color": COLORS["text"],
        "padding": "2px 6px",
        "border-radius": "3px",
        "font-family": "'Courier New', monospace",
        "font-size": "0.9em",
        "border": f"1px solid {COLORS['border']}",
    },
    "Q": {
        "color": COLORS["text_secondary"],
        "font-style": "italic",
    },
}

# Event handler factories
ELEMENT_HANDLERS = {
    "Button": {
        "mouseenter": lambda element: lambda sender, *args: setattr(sender.style, 'background_color', COLORS["accent_hover"]),
        "mouseleave": lambda element: lambda sender, *args: setattr(sender.style, 'background_color', COLORS["accent"]),
    },
    "Input": {
        "focus": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["accent"]),
        "blur": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["border"]),
    },
    "Textarea": {
        "focus": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["accent"]),
        "blur": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["border"]),
    },
    "Select": {
        "focus": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["accent"]),
        "blur": lambda element: lambda sender, *args: setattr(sender.style, 'border_color', COLORS["border"]),
    },
    "A": {
        "mouseenter": lambda element: lambda sender, *args: setattr(sender.style, 'color', COLORS["accent_hover"]),
        "mouseleave": lambda element: lambda sender, *args: setattr(sender.style, 'color', COLORS["accent"]),
    },
}
