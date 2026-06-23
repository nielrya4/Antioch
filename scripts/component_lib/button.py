"""
Button component library for Antioch.

Provides pre-styled button components with consistent design.
"""
from antioch import *
from antioch.macros.base import Macro


class ButtonPrimary(Macro):
    """
    A primary action button with consistent styling.

    Features:
    - Pre-styled with primary theme colors
    - Hover and active states
    - Click event handling
    - Disabled state support
    - Loading state support

    Usage:
        btn = ButtonPrimary("Click Me")
        DOM.add(btn.element)

        # With decorator event handling
        @when(btn.events.click)
        def handle_click(sender):
            print("Button clicked!")

        @when(btn.events.hover)
        def handle_hover(sender):
            print("Button hovered!")
    """

    def __init__(self, text="Button", disabled=False, loading=False,
                 full_width=False, size="medium", **kwargs):
        """
        Initialize a primary button.

        Args:
            text: Button text/label
            disabled: Whether button is disabled
            loading: Whether to show loading state
            full_width: Whether button should span full width
            size: Button size - "small", "medium", or "large"
            **kwargs: Additional arguments passed to Button element
        """
        # Initialize base macro
        super().__init__(macro_type="button_primary", **kwargs)

        # Set up state
        self._set_state(
            text=text,
            disabled=disabled,
            loading=loading,
            full_width=full_width,
            size=size
        )

        # Create unified Events for decorator usage
        self._create_event('click')
        self._create_event('hover_start')
        self._create_event('hover_end')
        self._create_event('mouse_down')
        self._create_event('mouse_up')

        # Initialize the macro
        self._init_macro()

    def _get_size_styles(self):
        """Get size-specific styles."""
        sizes = {
            "small": {
                "padding": "6px 12px",
                "font_size": "12px",
                "min_height": "28px"
            },
            "medium": {
                "padding": "10px 20px",
                "font_size": "14px",
                "min_height": "36px"
            },
            "large": {
                "padding": "14px 28px",
                "font_size": "16px",
                "min_height": "44px"
            }
        }
        size = self._get_state('size')
        return sizes.get(size, sizes["medium"])

    def _create_elements(self):
        """Create the button UI element."""
        # Get size-specific styles
        size_styles = self._get_size_styles()

        # Base button styles
        base_styles = {
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "color": "white",
            "border": "none",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        # Merge with size styles
        button_styles = {**base_styles, **size_styles}

        # Full width if specified
        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        # Disabled state
        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        # Loading state
        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        # Create button element
        btn = Button(text, style=button_styles)

        # Register element
        self._register_element('button', btn)

        # Wire up events
        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events(btn)

        return btn

    def _wire_events(self, btn):
        """Wire DOM events to the unified event system."""

        # Click event
        @when(btn.events.click)
        def on_click(sender, *args):
            self.events.fire('click', *args)

        # Hover effects with event triggers
        @when(btn.events.mouseenter)
        def on_mouseenter(sender, *args):
            btn.style.transform = "translateY(-1px)"
            btn.style.box_shadow = "0 4px 8px rgba(0, 0, 0, 0.15)"
            self.events.fire('hover_start', *args)

        @when(btn.events.mouseleave)
        def on_mouseleave(sender, *args):
            btn.style.transform = "translateY(0)"
            btn.style.box_shadow = "0 2px 4px rgba(0, 0, 0, 0.1)"
            self.events.fire('hover_end', *args)

        @when(btn.events.mousedown)
        def on_mousedown(sender, *args):
            btn.style.transform = "translateY(0)"
            btn.style.box_shadow = "0 1px 2px rgba(0, 0, 0, 0.1)"
            self.events.fire('mouse_down', *args)

        @when(btn.events.mouseup)
        def on_mouseup(sender, *args):
            btn.style.transform = "translateY(-1px)"
            btn.style.box_shadow = "0 4px 8px rgba(0, 0, 0, 0.15)"
            self.events.fire('mouse_up', *args)

    def set_text(self, text):
        """Update the button text."""
        self._set_state(text=text)
        btn = self._get_element('button')
        if btn:
            btn.dom_element.textContent = text

    def set_loading(self, loading):
        """Set the loading state."""
        self._set_state(loading=loading)
        btn = self._get_element('button')
        if btn:
            if loading:
                btn.dom_element.textContent = "Loading..."
                btn.style.opacity = "0.8"
                btn.style.cursor = "wait"
            else:
                btn.dom_element.textContent = self._get_state('text')
                btn.style.opacity = "1"
                btn.style.cursor = "pointer"

    def set_disabled(self, disabled):
        """Set the disabled state."""
        self._set_state(disabled=disabled)
        btn = self._get_element('button')
        if btn:
            if disabled:
                btn.style.opacity = "0.6"
                btn.style.cursor = "not-allowed"
                btn.dom_element.disabled = True
            else:
                btn.style.opacity = "1"
                btn.style.cursor = "pointer"
                btn.dom_element.disabled = False


class ButtonSuccess(ButtonPrimary):
    """Success button with green gradient."""

    def _create_elements(self):
        """Create button with success (green) styling."""
        size_styles = self._get_size_styles()

        base_styles = {
            "background": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
            "color": "white",
            "border": "none",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        button_styles = {**base_styles, **size_styles}

        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        btn = Button(text, style=button_styles)
        self._register_element('button', btn)

        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events(btn)

        return btn


class ButtonWarning(ButtonPrimary):
    """Warning button with orange/amber gradient."""

    def _create_elements(self):
        """Create button with warning (orange) styling."""
        size_styles = self._get_size_styles()

        base_styles = {
            "background": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
            "color": "white",
            "border": "none",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        button_styles = {**base_styles, **size_styles}

        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        btn = Button(text, style=button_styles)
        self._register_element('button', btn)

        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events(btn)

        return btn


class ButtonDanger(ButtonPrimary):
    """Danger/error button with red gradient."""

    def _create_elements(self):
        """Create button with danger (red) styling."""
        size_styles = self._get_size_styles()

        base_styles = {
            "background": "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
            "color": "white",
            "border": "none",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        button_styles = {**base_styles, **size_styles}

        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        btn = Button(text, style=button_styles)
        self._register_element('button', btn)

        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events(btn)

        return btn


class ButtonInfo(ButtonPrimary):
    """Info button with blue gradient."""

    def _create_elements(self):
        """Create button with info (blue) styling."""
        size_styles = self._get_size_styles()

        base_styles = {
            "background": "linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)",
            "color": "white",
            "border": "none",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        button_styles = {**base_styles, **size_styles}

        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        btn = Button(text, style=button_styles)
        self._register_element('button', btn)

        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events(btn)

        return btn


class ButtonSecondary(ButtonPrimary):
    """
    A secondary action button with outlined styling.

    Outlined button with transparent background and border.
    """

    def _create_elements(self):
        """Create button with outlined (secondary) styling."""
        size_styles = self._get_size_styles()

        base_styles = {
            "background": "white",
            "color": "#667eea",
            "border": "2px solid #667eea",
            "border_radius": "6px",
            "font_weight": "600",
            "cursor": "pointer",
            "transition": "all 0.2s ease",
            "outline": "none",
            "font_family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
        }

        button_styles = {**base_styles, **size_styles}

        if self._get_state('full_width'):
            button_styles["width"] = "100%"

        if self._get_state('disabled'):
            button_styles["opacity"] = "0.6"
            button_styles["cursor"] = "not-allowed"

        text = self._get_state('text')
        if self._get_state('loading'):
            text = "Loading..."
            button_styles["opacity"] = "0.8"
            button_styles["cursor"] = "wait"

        btn = Button(text, style=button_styles)
        self._register_element('button', btn)

        if not self._get_state('disabled') and not self._get_state('loading'):
            self._wire_events_secondary(btn)

        return btn

    def _wire_events_secondary(self, btn):
        """Wire DOM events with secondary-specific hover effects."""

        @when(btn.events.click)
        def on_click(sender, *args):
            self.events.fire('click', *args)

        @when(btn.events.mouseenter)
        def on_mouseenter(sender, *args):
            btn.style.background = "#667eea"
            btn.style.color = "white"
            self.events.fire('hover_start', *args)

        @when(btn.events.mouseleave)
        def on_mouseleave(sender, *args):
            btn.style.background = "white"
            btn.style.color = "#667eea"
            self.events.fire('hover_end', *args)

        @when(btn.events.mousedown)
        def on_mousedown(sender, *args):
            btn.style.opacity = "0.9"
            self.events.fire('mouse_down', *args)

        @when(btn.events.mouseup)
        def on_mouseup(sender, *args):
            btn.style.opacity = "1"
            self.events.fire('mouse_up', *args)