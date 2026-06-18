"""
Theme Manager for Antioch
Automatically applies the selected theme so elements can be used without prefixes.

Usage:
    from antioch.themes import *
    set_theme('diorite')  # Choose from: diorite, marble, rhyolite, quartzite, jasper, basalt

    # Now use themed elements directly
    container = Container()
    container.add(H1("Hello!"), P("No prefix needed!"))

Available Themes:
    - diorite: Modern dark theme with muted blue accents
    - marble: Clean light theme with elegant styling
    - rhyolite: Earthy theme inspired by eastern Oregon landscapes
    - quartzite: Alpine theme inspired by Idaho's Albion Mountains
    - jasper: Rich earthy theme with warm reds and sky blues
    - basalt: Pacific Northwest coastal theme with deep earth tones
"""

from . import diorite
from . import marble
from . import rhyolite
from . import quartzite
from . import jasper
from . import basalt

# Global state for current theme
_current_theme = None
_theme_modules = {
    'diorite': diorite,
    'marble': marble,
    'rhyolite': rhyolite,
    'quartzite': quartzite,
    'jasper': jasper,
    'basalt': basalt,
}


class ThemeProxy:
    """
    Proxy class that forwards attribute access to the current theme module.
    This allows elements to dynamically reference the active theme.
    """
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __call__(self, *args, **kwargs):
        """When called, get the attribute from the current theme and call it"""
        if _current_theme is None:
            raise RuntimeError(
                "No theme set. Call set_theme('diorite') or another theme name first.\n"
                f"Available themes: {list(_theme_modules.keys())}"
            )

        theme_module = _theme_modules[_current_theme]
        attr = getattr(theme_module, self.attr_name)
        return attr(*args, **kwargs)


class ThemePropertyProxy:
    """Proxy for theme properties like COLORS and FONTS"""
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __getitem__(self, key):
        """Access theme properties like COLORS['background']"""
        if _current_theme is None:
            raise RuntimeError(
                "No theme set. Call set_theme('diorite') or another theme name first.\n"
                f"Available themes: {list(_theme_modules.keys())}"
            )

        theme_module = _theme_modules[_current_theme]
        prop = getattr(theme_module, self.attr_name)
        return prop[key]

    def items(self):
        """Support iteration like dict.items()"""
        if _current_theme is None:
            raise RuntimeError(
                "No theme set. Call set_theme('diorite') or another theme name first.\n"
                f"Available themes: {list(_theme_modules.keys())}"
            )

        theme_module = _theme_modules[_current_theme]
        prop = getattr(theme_module, self.attr_name)
        return prop.items()

    def keys(self):
        """Support iteration like dict.keys()"""
        if _current_theme is None:
            raise RuntimeError(
                "No theme set. Call set_theme('diorite') or another theme name first.\n"
                f"Available themes: {list(_theme_modules.keys())}"
            )

        theme_module = _theme_modules[_current_theme]
        prop = getattr(theme_module, self.attr_name)
        return prop.keys()

    def values(self):
        """Support iteration like dict.values()"""
        if _current_theme is None:
            raise RuntimeError(
                "No theme set. Call set_theme('diorite') or another theme name first.\n"
                f"Available themes: {list(_theme_modules.keys())}"
            )

        theme_module = _theme_modules[_current_theme]
        prop = getattr(theme_module, self.attr_name)
        return prop.values()


def set_theme(theme_name):
    """
    Set the active theme.

    Args:
        theme_name: Theme name - 'diorite', 'marble', 'rhyolite', 'quartzite', 'jasper', or 'basalt'

    Raises:
        ValueError: If theme_name is not recognized
    """
    global _current_theme

    if theme_name not in _theme_modules:
        raise ValueError(
            f"Unknown theme: {theme_name}. "
            f"Available themes: {list(_theme_modules.keys())}"
        )

    _current_theme = theme_name


def get_theme():
    """
    Get the name of the current active theme.

    Returns:
        str: The current theme name, or None if no theme is set
    """
    return _current_theme


def get_theme_module():
    """
    Get the current theme module directly.

    Returns:
        module: The current theme module

    Raises:
        RuntimeError: If no theme is set
    """
    if _current_theme is None:
        raise RuntimeError(
            "No theme set. Call set_theme('diorite') or another theme name first.\n"
            f"Available themes: {list(_theme_modules.keys())}"
        )
    return _theme_modules[_current_theme]


def get_available_themes():
    """
    Get a list of all available theme names.

    Returns:
        list: List of available theme names
    """
    return list(_theme_modules.keys())


def get_theme_info():
    """
    Get information about all available themes.

    Returns:
        dict: Dictionary mapping theme names to their descriptions
    """
    return {
        'diorite': {
            'name': 'Diorite Dark Theme',
            'description': 'A cohesive dark theme with muted blue accents and modern styling',
            'type': 'dark'
        },
        'marble': {
            'name': 'Marble Light Theme',
            'description': 'A clean, elegant light theme with modern design principles',
            'type': 'light'
        },
        'rhyolite': {
            'name': 'Rhyolite Earth Theme',
            'description': 'Earthy theme inspired by eastern Oregon landscapes - rhyolite rock, clear water, junipers, and sagebrush',
            'type': 'earth'
        },
        'quartzite': {
            'name': 'Quartzite Alpine Theme',
            'description': "Alpine theme inspired by Idaho's Albion Mountains - clear waters, quartzite rocks, and alpine wildflowers",
            'type': 'alpine'
        },
        'jasper': {
            'name': 'Jasper Theme',
            'description': 'Rich, earthy theme inspired by Owyhee, Biggs, and Willow Creek jaspers - warm reds, sky blues, and earth tones',
            'type': 'earthy'
        },
        'basalt': {
            'name': 'Basalt Coastal Theme',
            'description': 'Pacific Northwest coastal theme - black basalt, scarlet salmonberries, western redcedar, and gray-blue waters',
            'type': 'coastal'
        }
    }


# Create proxy instances for all themed components
Button = ThemeProxy('Button')
H1 = ThemeProxy('H1')
H2 = ThemeProxy('H2')
H3 = ThemeProxy('H3')
H4 = ThemeProxy('H4')
H5 = ThemeProxy('H5')
H6 = ThemeProxy('H6')
P = ThemeProxy('P')
Div = ThemeProxy('Div')
Input = ThemeProxy('Input')
Textarea = ThemeProxy('Textarea')
Select = ThemeProxy('Select')
A = ThemeProxy('A')
Code = ThemeProxy('Code')
Pre = ThemeProxy('Pre')
Hr = ThemeProxy('Hr')
Card = ThemeProxy('Card')
Container = ThemeProxy('Container')

# Create proxy instances for theme properties
COLORS = ThemePropertyProxy('COLORS')
FONTS = ThemePropertyProxy('FONTS')


# Export everything
__all__ = [
    # Theme management functions
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
]
