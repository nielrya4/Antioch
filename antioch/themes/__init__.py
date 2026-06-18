"""
Antioch Themes Package

A collection of pre-built themes for Antioch applications.
Themes provide styled components with cohesive color palettes and typography.

Quick Start:
    from antioch.themes import set_theme, Container, H1, P, Button

    # Set your preferred theme
    set_theme('diorite')  # Dark theme

    # Use themed components
    container = Container(
        H1("Welcome!"),
        P("This text is automatically styled by the theme"),
        Button("Click Me")
    )

Available Themes:
    - diorite: Modern dark theme (recommended for dark mode apps)
    - marble: Clean light theme (recommended for light mode apps)
    - rhyolite: Earthy theme inspired by eastern Oregon
    - quartzite: Alpine theme inspired by Idaho mountains
    - jasper: Rich earthy theme with warm colors
    - basalt: Pacific Northwest coastal theme

Each theme includes:
    - Styled HTML elements (H1-H6, P, Button, Input, etc.)
    - Custom components (Card, Container)
    - Color palette (COLORS)
    - Typography settings (FONTS)

Usage Patterns:

1. Basic Usage:
    from antioch.themes import *
    set_theme('marble')
    DOM.add(H1("Hello World"))

2. Multiple Themes in One App:
    from antioch.themes import set_theme, get_theme

    # Save current theme
    original_theme = get_theme()

    # Temporarily switch themes
    set_theme('diorite')
    dark_section = Container(H1("Dark Section"))

    set_theme('marble')
    light_section = Container(H1("Light Section"))

    # Restore original theme
    set_theme(original_theme)

3. Access Theme Properties:
    from antioch.themes import COLORS, FONTS
    set_theme('diorite')

    custom_div = Div(style={
        "background-color": COLORS['surface'],
        "color": COLORS['text'],
        "font-family": FONTS['family']
    })

4. Get Theme Info:
    from antioch.themes import get_theme_info

    themes = get_theme_info()
    for name, info in themes.items():
        print(f"{info['name']}: {info['description']}")
"""

from .theme_manager import (
    # Theme management functions
    set_theme,
    get_theme,
    get_theme_module,
    get_available_themes,
    get_theme_info,

    # Themed components (only available after set_theme() is called)
    Button,
    H1, H2, H3, H4, H5, H6,
    P,
    Div,
    Input,
    Textarea,
    Select,
    A,
    Code,
    Pre,
    Hr,
    Card,
    Container,

    # Theme properties (only available after set_theme() is called)
    COLORS,
    FONTS,
)

# Also expose the theme modules directly if needed
from . import diorite
from . import marble
from . import rhyolite
from . import quartzite
from . import jasper
from . import basalt

__all__ = [
    # Theme management
    'set_theme',
    'get_theme',
    'get_theme_module',
    'get_available_themes',
    'get_theme_info',

    # Themed components
    'Button',
    'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
    'P',
    'Div',
    'Input',
    'Textarea',
    'Select',
    'A',
    'Code',
    'Pre',
    'Hr',
    'Card',
    'Container',

    # Theme properties
    'COLORS',
    'FONTS',

    # Theme modules (for direct access)
    'diorite',
    'marble',
    'rhyolite',
    'quartzite',
    'jasper',
    'basalt',
]

__version__ = '1.0.0'
__author__ = 'Antioch Team'
__description__ = 'Pre-built themes for Antioch applications'
