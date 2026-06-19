"""
Container macros for layout and organization.
"""
from .base import Macro
from ..elements import Div


class Card(Macro):
    """
    A themed card container for grouping related content.

    Cards automatically pick up theme colors when a theme is active.
    """

    def __init__(self, *content, style=None, **kwargs):
        super().__init__(macro_type="card")

        # Try to get theme colors
        try:
            from antioch.themes.theme_manager import get_theme_module
            theme = get_theme_module()
            if theme:
                background = theme.COLORS.get('surface', '#ffffff')
                border_color = theme.COLORS.get('border', '#ddd')
            else:
                background = '#ffffff'
                border_color = '#ddd'
        except:
            background = '#ffffff'
            border_color = '#ddd'

        # Default card styles
        default_style = {
            "background-color": background,
            "border": f"1px solid {border_color}",
            "border-radius": "8px",
            "padding": "16px",
            "margin": "8px 0",
        }

        # Merge with user styles
        final_style = self._merge_styles(default_style, style or {})

        # Create container element
        self._container = Div(*content, style=final_style, **kwargs)
        self._register_element('container', self._container)

    @property
    def element(self):
        """Return the root element."""
        return self._container

    def add(self, *items):
        """Add content to the card."""
        self._container.add(*items)
        return self


class Container(Macro):
    """
    A centered container with max-width for page layouts.

    Perfect for creating centered page content with consistent margins.
    """

    def __init__(self, *content, max_width="1200px", style=None, **kwargs):
        super().__init__(macro_type="container")

        # Default container styles
        default_style = {
            "max-width": max_width,
            "margin": "0 auto",
            "padding": "20px",
        }

        # Merge with user styles
        final_style = self._merge_styles(default_style, style or {})

        # Create container element
        self._container = Div(*content, style=final_style, **kwargs)
        self._register_element('container', self._container)

    @property
    def element(self):
        """Return the root element."""
        return self._container

    def add(self, *items):
        """Add content to the container."""
        self._container.add(*items)
        return self