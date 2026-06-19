"""
Marble Light Theme
A clean, elegant light theme for Antioch applications
"""

# Animation keyframes defined as Python dictionaries
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

# Element styles
ELEMENT_STYLES = {
    "Button": {
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
        "animation": "fadeIn 0.5s ease-in",
        "box-shadow": "0 1px 3px rgba(0,0,0,0.1)",
    },
    "H1": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "700",
        "letter-spacing": "-0.02em",
    },
    "H2": {
        "color": COLORS["text"],
        "font-family": FONTS["family"],
        "margin": "0.5em 0",
        "font-weight": "700",
        "letter-spacing": "-0.01em",
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
        "border-radius": "8px",
        "padding": "10px 14px",
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
        "border-radius": "8px",
        "padding": "10px 14px",
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
        "border-radius": "8px",
        "padding": "10px 14px",
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
        "padding": "3px 6px",
        "border-radius": "4px",
        "font-family": "'SF Mono', 'Monaco', 'Inconsolata', 'Courier New', monospace",
        "font-size": "0.9em",
    },
    "Pre": {
        "background-color": COLORS["surface_variant"],
        "color": COLORS["text"],
        "padding": "16px",
        "border-radius": "8px",
        "overflow-x": "auto",
        "font-family": "'SF Mono', 'Monaco', 'Inconsolata', 'Courier New', monospace",
        "font-size": "0.9em",
        "line-height": "1.5",
    },
    "Hr": {
        "border": "none",
        "height": "2px",
        "background": f"linear-gradient(to right, {COLORS['surface_variant']}, {COLORS['accent']}, {COLORS['accent_hover']}, {COLORS['accent']}, {COLORS['surface_variant']})",
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
        "border-radius": "8px",
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
        "background-color": COLORS["accent"],
        "color": "#ffffff",
        "padding": "2px 4px",
    },
    "Kbd": {
        "background-color": COLORS["surface_variant"],
        "color": COLORS["text"],
        "padding": "2px 6px",
        "border-radius": "4px",
        "font-family": "'SF Mono', 'Monaco', 'Inconsolata', 'Courier New', monospace",
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
        "mouseenter": lambda element: lambda sender, *args: (
            setattr(sender.style, 'background_color', COLORS["accent_hover"]),
            setattr(sender.style, 'box_shadow', "0 2px 6px rgba(0,0,0,0.15)")
        ),
        "mouseleave": lambda element: lambda sender, *args: (
            setattr(sender.style, 'background_color', COLORS["accent"]),
            setattr(sender.style, 'box_shadow', "0 1px 3px rgba(0,0,0,0.1)")
        ),
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
