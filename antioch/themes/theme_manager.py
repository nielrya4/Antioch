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
    Set the active theme and update global registries for automatic element styling.

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

    # Update global registries for auto-theming
    from antioch.core.themed import update_theme_registries
    theme_module = _theme_modules[theme_name]

    # Get element styles and handlers from theme
    element_styles = getattr(theme_module, 'ELEMENT_STYLES', {})
    element_handlers = getattr(theme_module, 'ELEMENT_HANDLERS', {})

    # Update the global registries
    update_theme_registries(element_styles, element_handlers)

    # Inject theme keyframes (animations) into the page
    keyframes = getattr(theme_module, 'KEYFRAMES', None)
    if keyframes:
        _inject_keyframes(theme_name, keyframes)


def _keyframes_to_css(keyframes_dict):
    """Convert Python keyframes dictionary to CSS string."""
    css_rules = []

    for animation_name, frames in keyframes_dict.items():
        frame_rules = []
        for selector, properties in frames.items():
            prop_list = [f"    {key.replace('_', '-')}: {value};" for key, value in properties.items()]
            frame_rules.append(f"  {selector} {{\n" + "\n".join(prop_list) + "\n  }")

        css_rules.append(f"@keyframes {animation_name} {{\n" + "\n".join(frame_rules) + "\n}}")

    return "\n\n".join(css_rules)


def _inject_keyframes(theme_name, keyframes_dict):
    """Inject theme keyframes into the page as CSS."""
    import js

    # Remove old theme CSS if it exists
    old_style = js.document.getElementById(f'antioch-theme-{theme_name}-keyframes')
    if old_style:
        old_style.remove()

    # Convert Python keyframes to CSS
    css_content = _keyframes_to_css(keyframes_dict)

    # Create new style element
    style = js.document.createElement('style')
    style.id = f'antioch-theme-{theme_name}-keyframes'
    style.textContent = css_content
    js.document.head.appendChild(style)


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


# Create proxy instances for theme properties
# These allow accessing COLORS and FONTS from the active theme
COLORS = ThemePropertyProxy('COLORS')
FONTS = ThemePropertyProxy('FONTS')

# Card and Container are now macros, not theme components
from antioch.macros import Card, Container


# Export everything
__all__ = [
    # Theme management functions
    'set_theme',
    'get_theme',
    'get_theme_module',
    'get_available_themes',
    'get_theme_info',

    # Theme properties
    'COLORS',
    'FONTS',

    # Macros (re-exported for convenience)
    'Card',
    'Container',
]
