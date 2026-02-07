"""
Alert macro - A reusable alert/notification component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Button, Span, P


class Alert(Macro):
    """
    An alert component for displaying important messages.
    Supports different types (info, success, warning, error) and dismissible functionality.
    """
    
    def __init__(self, message, alert_type="info", dismissible=True, 
                 auto_dismiss=False, dismiss_delay=5000, show_icon=True, **kwargs):
        """
        Initialize an alert component.
        
        Args:
            message: Alert message text
            alert_type: Type of alert ("info", "success", "warning", "error")
            dismissible: Whether alert can be manually dismissed
            auto_dismiss: Whether alert auto-dismisses after delay
            dismiss_delay: Auto-dismiss delay in milliseconds
            show_icon: Whether to show type icon
        """
        # Initialize base macro
        super().__init__(macro_type="alert", **kwargs)
        
        # Set up state
        self._set_state(
            message=message,
            alert_type=alert_type,
            dismissible=dismissible,
            auto_dismiss=auto_dismiss,
            dismiss_delay=dismiss_delay,
            show_icon=show_icon,
            visible=True
        )
        
        # Add callback types
        self._add_callback_type('dismiss')
        self._add_callback_type('show')
        self._add_callback_type('auto_dismiss')
        
        # Initialize the macro
        self._init_macro()
        
        # Set up auto-dismiss if enabled
        if auto_dismiss:
            self._setup_auto_dismiss()
    
    def _get_alert_styles(self):
        """Get styles for different alert types."""
        return {
            "info": {
                "background_color": "#d1ecf1",
                "color": "#0c5460",
                "border": "1px solid #bee5eb",
                "icon": "ℹ️"
            },
            "success": {
                "background_color": "#d4edda",
                "color": "#155724",
                "border": "1px solid #c3e6cb",
                "icon": "✅"
            },
            "warning": {
                "background_color": "#fff3cd",
                "color": "#856404",
                "border": "1px solid #ffeaa7",
                "icon": "⚠️"
            },
            "error": {
                "background_color": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
                "icon": "❌"
            },
            "danger": {  # Alias for error
                "background_color": "#f8d7da",
                "color": "#721c24",
                "border": "1px solid #f5c6cb",
                "icon": "❌"
            }
        }
    
    def _create_elements(self):
        """Create the alert UI elements."""
        alert_type = self._get_state('alert_type')
        alert_styles = self._get_alert_styles()
        type_style = alert_styles.get(alert_type, alert_styles["info"])
        
        # Base alert styles
        base_style = {
            "padding": "12px 16px",
            "border_radius": "4px",
            "margin": "10px 0",
            "position": "relative",
            "font_size": "14px",
            "display": "flex",
            "align_items": "center",
            "box_shadow": "0 1px 3px rgba(0,0,0,0.1)"
        }
        
        # Merge with type-specific styles
        container_styles = {**base_style, **type_style}
        
        # Create container
        container = self._register_element('container', self._create_container(container_styles))
        
        # Content wrapper
        content_wrapper = self._register_element('content_wrapper', Div(style={
            "flex": "1",
            "display": "flex",
            "align_items": "center"
        }))
        
        # Icon (if enabled)
        if self._get_state('show_icon'):
            icon = self._register_element('icon', Span(type_style["icon"], style={
                "margin_right": "8px",
                "font_size": "16px"
            }))
            content_wrapper.add(icon)
        
        # Message
        message_elem = self._register_element('message', 
                                            Span(self._get_state('message'), style={
                                                "flex": "1"
                                            }))
        content_wrapper.add(message_elem)
        
        container.add(content_wrapper)
        
        # Dismiss button (if dismissible)
        if self._get_state('dismissible'):
            close_btn = self._register_element('close_btn', Button("×", style={
                "background": "none",
                "border": "none",
                "font_size": "18px",
                "cursor": "pointer",
                "padding": "0",
                "margin_left": "10px",
                "width": "20px",
                "height": "20px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "border_radius": "50%",
                "color": "inherit",
                "opacity": "0.7"
            }))
            close_btn.on_click(lambda e: self.dismiss())
            close_btn.on_mouseenter(lambda e: self._set_close_btn_hover(True))
            close_btn.on_mouseleave(lambda e: self._set_close_btn_hover(False))
            container.add(close_btn)
        
        return container
    
    def _set_close_btn_hover(self, is_hover):
        """Handle close button hover state."""
        close_btn = self._get_element('close_btn')
        if close_btn:
            if is_hover:
                close_btn.style.opacity = "1"
                close_btn.style.background_color = "rgba(0,0,0,0.1)"
            else:
                close_btn.style.opacity = "0.7"
                close_btn.style.background_color = "transparent"
    
    def _setup_auto_dismiss(self):
        """Set up auto-dismiss timer (simulation)."""
        # In a real implementation, this would set up a JavaScript timer
        # For now, we'll just mark it as configured
        pass
    
    def dismiss(self):
        """Dismiss the alert."""
        if self._get_state('visible'):
            self._set_state(visible=False)
            
            # Hide the alert with animation
            container = self._get_element('container')
            if container:
                container.style.opacity = "0"
                container.style.transform = "translateY(-10px)"
                container.style.transition = "opacity 0.3s ease, transform 0.3s ease"
                
                # After animation, hide completely (simulation)
                # In real implementation, would use setTimeout
                container.style.display = "none"
            
            self._trigger_callbacks('dismiss')
        return self
    
    def show(self):
        """Show the alert if hidden."""
        if not self._get_state('visible'):
            self._set_state(visible=True)
            
            container = self._get_element('container')
            if container:
                container.style.display = "flex"
                container.style.opacity = "1"
                container.style.transform = "translateY(0)"
            
            self._trigger_callbacks('show')
            
            # Reset auto-dismiss if enabled
            if self._get_state('auto_dismiss'):
                self._setup_auto_dismiss()
        
        return self
    
    def set_message(self, message):
        """Update the alert message."""
        self._set_state(message=message)
        message_elem = self._get_element('message')
        if message_elem:
            message_elem.set_text(message)
        return self
    
    def set_type(self, alert_type):
        """Change the alert type."""
        old_type = self._get_state('alert_type')
        self._set_state(alert_type=alert_type)
        
        # Update styles
        alert_styles = self._get_alert_styles()
        type_style = alert_styles.get(alert_type, alert_styles["info"])
        
        container = self._get_element('container')
        if container:
            container.style.background_color = type_style["background_color"]
            container.style.color = type_style["color"]
            container.style.border = type_style["border"]
        
        # Update icon
        if self._get_state('show_icon'):
            icon = self._get_element('icon')
            if icon:
                icon.set_text(type_style["icon"])
        
        return self
    
    def toggle_dismissible(self, enable=None):
        """Toggle dismissible state."""
        current = self._get_state('dismissible')
        new_state = not current if enable is None else enable
        
        self._set_state(dismissible=new_state)
        
        close_btn = self._get_element('close_btn')
        if close_btn:
            close_btn.style.display = "flex" if new_state else "none"
        
        return self
    
    def set_auto_dismiss(self, enable, delay=5000):
        """Configure auto-dismiss behavior."""
        self._set_state(auto_dismiss=enable, dismiss_delay=delay)
        
        if enable and self._get_state('visible'):
            self._setup_auto_dismiss()
        
        return self
    
    @property
    def is_visible(self):
        """Check if alert is currently visible."""
        return self._get_state('visible')
    
    @property
    def message(self):
        """Get current message."""
        return self._get_state('message')
    
    @property
    def alert_type(self):
        """Get current alert type."""
        return self._get_state('alert_type')
    
    def on_dismiss(self, callback):
        """Register callback for dismiss event."""
        return self.on('dismiss', callback)
    
    def on_show(self, callback):
        """Register callback for show event."""
        return self.on('show', callback)
    
    def on_auto_dismiss(self, callback):
        """Register callback for auto-dismiss event."""
        return self.on('auto_dismiss', callback)


# Convenience functions for creating specific alert types
def info_alert(message, **kwargs):
    """Create an info alert."""
    return Alert(message, alert_type="info", **kwargs)

def success_alert(message, **kwargs):
    """Create a success alert."""
    return Alert(message, alert_type="success", **kwargs)

def warning_alert(message, **kwargs):
    """Create a warning alert."""
    return Alert(message, alert_type="warning", **kwargs)

def error_alert(message, **kwargs):
    """Create an error alert."""
    return Alert(message, alert_type="error", **kwargs)