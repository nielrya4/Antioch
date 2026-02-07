"""
Toast macro - A reusable toast notification system.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Button, Span


class Toast(Macro):
    """
    A single toast notification with auto-dismiss and manual close capabilities.
    """
    
    def __init__(self, message, toast_type="info", duration=4000, 
                 position="top-right", closable=True, show_icon=True, 
                 show_progress=True, **kwargs):
        """
        Initialize a toast notification.
        
        Args:
            message: Toast message text
            toast_type: Type of toast ("info", "success", "warning", "error")
            duration: Auto-dismiss duration in milliseconds (0 = no auto-dismiss)
            position: Position on screen ("top-right", "top-left", "bottom-right", "bottom-left", "top-center", "bottom-center")
            closable: Whether toast can be manually closed
            show_icon: Whether to show type icon
            show_progress: Whether to show progress bar for auto-dismiss
        """
        # Initialize base macro
        super().__init__(macro_type="toast", **kwargs)
        
        # Set up state
        self._set_state(
            message=message,
            toast_type=toast_type,
            duration=duration,
            position=position,
            closable=closable,
            show_icon=show_icon,
            show_progress=show_progress,
            visible=True,
            start_time=None
        )
        
        # Add callback types
        self._add_callback_type('close')
        self._add_callback_type('click')
        
        # Initialize macro
        self._init_macro()
        
        # Start auto-dismiss timer if enabled
        if duration > 0:
            self._start_auto_dismiss()
    
    def _get_toast_styles(self):
        """Get styles for different toast types."""
        return {
            "info": {
                "background_color": "#3498db",
                "color": "white",
                "icon": "ℹ️"
            },
            "success": {
                "background_color": "#2ecc71",
                "color": "white",
                "icon": "✅"
            },
            "warning": {
                "background_color": "#f39c12",
                "color": "white",
                "icon": "⚠️"
            },
            "error": {
                "background_color": "#e74c3c",
                "color": "white",
                "icon": "❌"
            },
            "danger": {  # Alias for error
                "background_color": "#e74c3c",
                "color": "white",
                "icon": "❌"
            }
        }
    
    def _get_position_styles(self):
        """Get styles for different positions."""
        return {
            "top-right": {"top": "20px", "right": "20px"},
            "top-left": {"top": "20px", "left": "20px"},
            "bottom-right": {"bottom": "20px", "right": "20px"},
            "bottom-left": {"bottom": "20px", "left": "20px"},
            "top-center": {"top": "20px", "left": "50%", "transform": "translateX(-50%)"},
            "bottom-center": {"bottom": "20px", "left": "50%", "transform": "translateX(-50%)"}
        }
    
    def _create_elements(self):
        """Create the toast UI elements."""
        toast_type = self._get_state('toast_type')
        position = self._get_state('position')
        
        toast_styles = self._get_toast_styles()
        position_styles = self._get_position_styles()
        type_style = toast_styles.get(toast_type, toast_styles["info"])
        pos_style = position_styles.get(position, position_styles["top-right"])
        
        # Base toast styles
        base_style = {
            "position": "fixed",
            "padding": "16px 20px",
            "border_radius": "6px",
            "box_shadow": "0 4px 12px rgba(0,0,0,0.15)",
            "font_size": "14px",
            "min_width": "300px",
            "max_width": "500px",
            "z_index": "9999",
            "display": "flex",
            "align_items": "center",
            "animation": "toastSlideIn 0.3s ease-out",
            "word_wrap": "break-word"
        }
        
        # Merge all styles
        container_styles = {**base_style, **type_style, **pos_style}
        
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
                "margin_right": "10px",
                "font_size": "16px"
            }))
            content_wrapper.add(icon)
        
        # Message
        message_elem = self._register_element('message', 
                                            Span(self._get_state('message'), style={
                                                "flex": "1",
                                                "line_height": "1.4"
                                            }))
        content_wrapper.add(message_elem)
        
        container.add(content_wrapper)
        
        # Close button (if closable)
        if self._get_state('closable'):
            close_btn = self._register_element('close_btn', Button("×", style={
                "background": "none",
                "border": "none",
                "color": "inherit",
                "cursor": "pointer",
                "padding": "0",
                "margin_left": "15px",
                "width": "20px",
                "height": "20px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "border_radius": "50%",
                "font_size": "16px",
                "opacity": "0.8",
                "transition": "opacity 0.2s ease"
            }))
            close_btn.on_click(lambda e: self.close())
            close_btn.on_mouseenter(lambda e: self._set_close_btn_hover(True))
            close_btn.on_mouseleave(lambda e: self._set_close_btn_hover(False))
            container.add(close_btn)
        
        # Progress bar (if enabled and auto-dismiss)
        if self._get_state('show_progress') and self._get_state('duration') > 0:
            progress_container = self._register_element('progress_container', Div(style={
                "position": "absolute",
                "bottom": "0",
                "left": "0",
                "right": "0",
                "height": "3px",
                "background_color": "rgba(255,255,255,0.3)",
                "border_radius": "0 0 6px 6px",
                "overflow": "hidden"
            }))
            
            progress_bar = self._register_element('progress_bar', Div(style={
                "width": "100%",
                "height": "100%",
                "background_color": "rgba(255,255,255,0.8)",
                "transition": f"width {self._get_state('duration')}ms linear",
                "animation": f"toastProgress {self._get_state('duration')}ms linear"
            }))
            
            progress_container.add(progress_bar)
            container.add(progress_container)
        
        # Click handler for whole toast
        container.on_click(lambda e: self._handle_toast_click(e))
        
        return container
    
    def _set_close_btn_hover(self, is_hover):
        """Set close button hover state."""
        close_btn = self._get_element('close_btn')
        if close_btn:
            if is_hover:
                close_btn.style.opacity = "1"
                close_btn.style.background_color = "rgba(255,255,255,0.2)"
            else:
                close_btn.style.opacity = "0.8"
                close_btn.style.background_color = "transparent"
    
    def _handle_toast_click(self, event):
        """Handle toast click (excluding close button)."""
        # Only trigger if not clicking the close button
        close_btn = self._get_element('close_btn')
        if close_btn and event.target != close_btn._dom_element:
            self._trigger_callbacks('click')
    
    def _start_auto_dismiss(self):
        """Start auto-dismiss timer (simulation)."""
        # In a real implementation, this would use setTimeout
        # For now, we mark the start time for potential progress updates
        import time
        self._set_state(start_time=time.time())
    
    def close(self):
        """Close the toast with animation."""
        if self._get_state('visible'):
            self._set_state(visible=False)
            
            container = self._get_element('container')
            if container:
                # Slide out animation
                container.style.transform = "translateX(100%)"
                container.style.opacity = "0"
                container.style.transition = "transform 0.3s ease, opacity 0.3s ease"
                
                # After animation, remove completely (simulation)
                # In real implementation, would use setTimeout
                container.style.display = "none"
            
            self._trigger_callbacks('close')
        
        return self
    
    def update_message(self, message):
        """Update the toast message."""
        self._set_state(message=message)
        message_elem = self._get_element('message')
        if message_elem:
            message_elem.set_text(message)
        return self
    
    def update_type(self, toast_type):
        """Update the toast type and styling."""
        self._set_state(toast_type=toast_type)
        
        toast_styles = self._get_toast_styles()
        type_style = toast_styles.get(toast_type, toast_styles["info"])
        
        container = self._get_element('container')
        if container:
            container.style.background_color = type_style["background_color"]
            container.style.color = type_style["color"]
        
        # Update icon
        if self._get_state('show_icon'):
            icon = self._get_element('icon')
            if icon:
                icon.set_text(type_style["icon"])
        
        return self
    
    def reset_timer(self):
        """Reset the auto-dismiss timer."""
        if self._get_state('duration') > 0:
            self._start_auto_dismiss()
            
            # Reset progress bar
            if self._get_state('show_progress'):
                progress_bar = self._get_element('progress_bar')
                if progress_bar:
                    progress_bar.style.width = "100%"
        
        return self
    
    @property
    def is_visible(self):
        """Check if toast is visible."""
        return self._get_state('visible')
    
    def on_close(self, callback):
        """Register callback for close event."""
        return self.on('close', callback)
    
    def on_click(self, callback):
        """Register callback for click event."""
        return self.on('click', callback)


class ToastManager:
    """
    Manages multiple toasts, positioning, and queueing.
    Provides convenience methods for showing different types of toasts.
    """
    
    def __init__(self, max_toasts=5, default_position="top-right"):
        self.toasts = []
        self.max_toasts = max_toasts
        self.default_position = default_position
    
    def show(self, message, toast_type="info", **kwargs):
        """Show a toast notification."""
        # Set default position if not specified
        if 'position' not in kwargs:
            kwargs['position'] = self.default_position
        
        toast = Toast(message, toast_type, **kwargs)
        
        # Auto-close callback to remove from manager
        toast.on_close(lambda t: self._remove_toast(toast))
        
        # Add toast to DOM
        from ..dom import DOM
        DOM.add(toast.element)
        
        self.toasts.append(toast)
        
        # Remove oldest toasts if exceeding max
        while len(self.toasts) > self.max_toasts:
            oldest = self.toasts.pop(0)
            oldest.close()
        
        return toast
    
    def info(self, message, **kwargs):
        """Show an info toast."""
        return self.show(message, "info", **kwargs)
    
    def success(self, message, **kwargs):
        """Show a success toast."""
        return self.show(message, "success", **kwargs)
    
    def warning(self, message, **kwargs):
        """Show a warning toast."""
        return self.show(message, "warning", **kwargs)
    
    def error(self, message, **kwargs):
        """Show an error toast."""
        return self.show(message, "error", **kwargs)
    
    def clear_all(self):
        """Close all toasts."""
        for toast in self.toasts[:]:  # Copy list to avoid modification during iteration
            toast.close()
        self.toasts.clear()
    
    def _remove_toast(self, toast):
        """Remove a toast from the manager."""
        if toast in self.toasts:
            self.toasts.remove(toast)
    
    @property
    def active_count(self):
        """Get number of active toasts."""
        return len([t for t in self.toasts if t.is_visible])


# Global toast manager instance for convenience
_global_toast_manager = ToastManager()

# Convenience functions using the global manager
def show_toast(message, toast_type="info", **kwargs):
    """Show a toast using the global manager."""
    return _global_toast_manager.show(message, toast_type, **kwargs)

def info_toast(message, **kwargs):
    """Show an info toast using the global manager."""
    return _global_toast_manager.info(message, **kwargs)

def success_toast(message, **kwargs):
    """Show a success toast using the global manager."""
    return _global_toast_manager.success(message, **kwargs)

def warning_toast(message, **kwargs):
    """Show a warning toast using the global manager."""
    return _global_toast_manager.warning(message, **kwargs)

def error_toast(message, **kwargs):
    """Show an error toast using the global manager."""
    return _global_toast_manager.error(message, **kwargs)

def clear_all_toasts():
    """Clear all toasts using the global manager."""
    return _global_toast_manager.clear_all()