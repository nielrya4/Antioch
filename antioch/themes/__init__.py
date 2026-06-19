"""
Antioch Themes Package

A collection of pre-built themes for Antioch applications.
Themes provide automatic styling for elements with cohesive color palettes and typography.

Quick Start:
    from antioch import Button, H1, P
    from antioch.themes import set_theme, Card, Container

    # Set your preferred theme - all new elements will be automatically styled
    set_theme('diorite')  # Dark theme

    # Create elements - they automatically get theme styles!
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

How It Works:
    1. Call set_theme('diorite') to activate a theme
    2. All new Button, Input, H1, etc. elements automatically get theme styles
    3. You can still override with style={...} parameter
    4. Access theme colors/fonts via COLORS and FONTS

Usage Patterns:

1. Basic Usage:
    from antioch import DOM, Button, H1
    from antioch.themes import set_theme

    set_theme('marble')
    DOM.add(H1("Hello World"))  # Automatically styled!

2. Access Theme Properties:
    from antioch import Div
    from antioch.themes import set_theme, COLORS, FONTS

    set_theme('diorite')
    custom_div = Div(style={
        "background-color": COLORS['surface'],
        "color": COLORS['text'],
        "font-family": FONTS['family']
    })

3. Get Theme Info:
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

    # Theme properties (access active theme's colors and fonts)
    COLORS,
    FONTS,

    # Macros (re-exported for convenience)
    Card,
    Container,
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

    # Theme properties
    'COLORS',
    'FONTS',

    # Macros
    'Card',
    'Container',

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
