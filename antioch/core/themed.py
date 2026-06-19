"""
Theming support for Antioch elements.

This module provides automatic theme application for elements. When a theme is set,
all newly created elements automatically receive the theme's styles and event handlers.

Usage:
    from antioch import Button
    from antioch.themes import set_theme

    set_theme('diorite')
    btn = Button("Click me")  # Automatically gets diorite theme styles
"""

# Global registries populated by theme_manager when set_theme() is called
_current_theme_styles = {}
_current_theme_handlers = {}


def apply_theme_to_element(element, element_type):
    """
    Apply active theme styles and handlers to an element.

    This function is called by element constructors to automatically apply
    theme styling. It checks the global registries and applies any styles
    or event handlers defined for the element type.

    Args:
        element: The element instance to theme
        element_type: String name of the element type (e.g., 'Button', 'Input')

    Example:
        class Button(_Button):
            def __init__(self, *content, **kwargs):
                super().__init__(*content, **kwargs)
                apply_theme_to_element(self, 'Button')
    """
    # Apply styles from theme
    if element_type in _current_theme_styles:
        element.style.update(_current_theme_styles[element_type])

    # Apply event handlers from theme (hover, focus, etc.)
    if element_type in _current_theme_handlers:
        handlers = _current_theme_handlers[element_type]
        for event_name, handler_factory in handlers.items():
            # Handler factory creates the actual handler with proper closure
            handler = handler_factory(element)
            getattr(element.events, event_name).subscribe(handler)


def update_theme_registries(element_styles, element_handlers):
    """
    Update the global theme registries.

    Called by theme_manager.set_theme() to update what styles/handlers
    are applied to newly created elements.

    Args:
        element_styles: Dictionary mapping element types to style dicts
        element_handlers: Dictionary mapping element types to event handler factories
    """
    global _current_theme_styles, _current_theme_handlers

    _current_theme_styles.clear()
    _current_theme_styles.update(element_styles or {})

    _current_theme_handlers.clear()
    _current_theme_handlers.update(element_handlers or {})


def clear_theme():
    """Clear all theme styles and handlers."""
    global _current_theme_styles, _current_theme_handlers

    _current_theme_styles.clear()
    _current_theme_handlers.clear()


def get_current_theme_styles():
    """Get a copy of current theme styles registry."""
    return _current_theme_styles.copy()


def get_current_theme_handlers():
    """Get a copy of current theme handlers registry."""
    return _current_theme_handlers.copy()