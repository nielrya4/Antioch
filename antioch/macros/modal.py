"""
Modal macro - A reusable modal dialog component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Button, H3, P, Span
import js


class Modal(Macro):
    """A modal dialog component with overlay and customizable content."""
    
    def __init__(self, title="Modal", content="", closable=True, 
                 backdrop_click_close=True, escape_key_close=True,
                 modal_style=None, overlay_style=None, **kwargs):
        """
        Initialize a modal component.
        
        Args:
            title: Modal title text
            content: Initial content (string or Element)
            closable: Whether to show close button
            backdrop_click_close: Close when clicking overlay
            escape_key_close: Close when pressing Escape key
            modal_style: Custom styles for modal content
            overlay_style: Custom styles for overlay
        """
        # Initialize base macro
        super().__init__(macro_type="modal", **kwargs)
        
        # Set up modal-specific state
        self._set_state(
            title=title,
            closable=closable,
            backdrop_click_close=backdrop_click_close,
            escape_key_close=escape_key_close,
            is_open=False,
            initial_content=content
        )
        
        # Add callback types
        self._add_callback_type('open')
        self._add_callback_type('close')
        self._add_callback_type('confirm')
        self._add_callback_type('cancel')
        
        # Default styles
        default_overlay_style = {
            "position": "fixed",
            "top": "0",
            "left": "0", 
            "width": "100%",
            "height": "100%",
            "background_color": "rgba(0, 0, 0, 0.5)",
            "z_index": "1000",
            "display": "none",
            "justify_content": "center",
            "align_items": "center"
        }
        
        default_modal_style = {
            "background_color": "white",
            "border_radius": "8px",
            "box_shadow": "0 4px 20px rgba(0, 0, 0, 0.15)",
            "max_width": "500px",
            "min_width": "300px",
            "max_height": "80vh",
            "overflow": "auto",
            "animation": "modalFadeIn 0.3s ease-out"
        }
        
        # Merge with user styles using base class method
        self._overlay_style = self._merge_styles(default_overlay_style, overlay_style)
        self._modal_style = self._merge_styles(default_modal_style, modal_style)
        
        # Initialize macro
        self._init_macro()
        
        # Set initial content
        if content:
            self.set_content(content)
    
    def _create_elements(self):
        """Create the modal UI elements."""
        # Overlay (backdrop) using base class method
        overlay = self._register_element('overlay', Div(style=self._overlay_style))
        overlay.set_attribute("data-modal-id", self._id)
        
        # Modal container
        modal_container = self._register_element('modal_container', Div(style=self._modal_style))
        
        # Header
        header = self._register_element('header', Div(style={
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "padding": "20px 20px 10px",
            "border_bottom": "1px solid #eee"
        }))
        
        # Title
        title_element = self._register_element('title_element', H3(self._get_state('title'), style={
            "margin": "0",
            "font_size": "18px",
            "font_weight": "600"
        }))
        
        header.add(title_element)
        
        # Close button
        if self._get_state('closable'):
            close_btn = self._register_element('close_btn', Button("×", style={
                "background": "none",
                "border": "none", 
                "font_size": "24px",
                "cursor": "pointer",
                "padding": "0",
                "width": "30px",
                "height": "30px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
                "border_radius": "50%",
                "color": "#666"
            }))
            close_btn.on_click(self._handle_close)
            close_btn.on_mouseenter(lambda e: self._set_close_btn_hover(True))
            close_btn.on_mouseleave(lambda e: self._set_close_btn_hover(False))
            header.add(close_btn)
        
        # Body
        body = self._register_element('body', Div(style={
            "padding": "20px"
        }))
        
        # Footer (initially empty)
        footer = self._register_element('footer', Div(style={
            "padding": "10px 20px 20px",
            "text_align": "right",
            "border_top": "1px solid #eee",
            "display": "none"
        }))
        
        # Assemble modal
        modal_container.add(header, body, footer)
        overlay.add(modal_container)
        
        # Setup events
        self._setup_events()
        
        return overlay
    
    def _setup_events(self):
        """Setup modal event handlers."""
        overlay = self._get_element('overlay')
        modal_container = self._get_element('modal_container')
        
        # Backdrop click to close
        if self._get_state('backdrop_click_close'):
            overlay.on_click(self._handle_backdrop_click)
        
        # Prevent modal content clicks from bubbling to backdrop
        modal_container.on_click(lambda e: e.stopPropagation())
        
        # Escape key handling (global)
        if self._get_state('escape_key_close'):
            # Note: We'll handle this in the show() method
            pass
    
    def _handle_close(self, event=None):
        """Handle close button click."""
        self.close()
    
    def _handle_backdrop_click(self, event):
        """Handle clicking on the backdrop."""
        overlay = self._get_element('overlay')
        if event.target == overlay._dom_element:
            self.close()
    
    def _handle_escape_key(self, event):
        """Handle escape key press."""
        if event.key == "Escape" and self._get_state('is_open'):
            self.close()
    
    def _set_close_btn_hover(self, is_hover):
        """Set close button hover state."""
        close_btn = self._get_element('close_btn')
        if close_btn:
            if is_hover:
                close_btn.style.background_color = "#f0f0f0"
                close_btn.style.color = "#000"
            else:
                close_btn.style.background_color = "transparent"
                close_btn.style.color = "#666"
    
    # Remove custom _trigger_callbacks - use base class method
    
    def show(self):
        """Show the modal."""
        if not self._get_state('is_open'):
            overlay = self._get_element('overlay')
            overlay.style.display = "flex"
            self._set_state(is_open=True)
            
            # Add escape key listener
            if self._get_state('escape_key_close'):
                js.document.addEventListener("keydown", self._handle_escape_key)
            
            self._trigger_callbacks('open')
        return self
    
    def close(self):
        """Close the modal."""
        if self._get_state('is_open'):
            overlay = self._get_element('overlay')
            overlay.style.display = "none"
            self._set_state(is_open=False)
            
            # Remove escape key listener
            if self._get_state('escape_key_close'):
                js.document.removeEventListener("keydown", self._handle_escape_key)
            
            self._trigger_callbacks('close')
        return self
    
    def toggle(self):
        """Toggle modal visibility."""
        if self._get_state('is_open'):
            self.close()
        else:
            self.show()
        return self
    
    def set_title(self, title):
        """Set the modal title."""
        self._set_state(title=title)
        title_element = self._get_element('title_element')
        title_element.set_text(title)
        return self
    
    def set_content(self, content):
        """Set the modal body content."""
        body = self._get_element('body')
        # Clear existing content
        body._dom_element.innerHTML = ""
        
        # Add new content
        if isinstance(content, str):
            body.add(P(content))
        else:
            body.add(content)
        return self
    
    def add_content(self, *content):
        """Add content to the modal body."""
        body = self._get_element('body')
        body.add(*content)
        return self
    
    def clear_content(self):
        """Clear all content from modal body."""
        body = self._get_element('body')
        body._dom_element.innerHTML = ""
        return self
    
    def set_footer(self, *elements):
        """Set footer content and make it visible."""
        footer = self._get_element('footer')
        footer._dom_element.innerHTML = ""
        footer.add(*elements)
        footer.style.display = "block"
        return self
    
    def clear_footer(self):
        """Clear footer and hide it."""
        footer = self._get_element('footer')
        footer._dom_element.innerHTML = ""
        footer.style.display = "none"
        return self
    
    def add_confirm_cancel_buttons(self, confirm_text="Confirm", cancel_text="Cancel",
                                  confirm_style=None, cancel_style=None):
        """Add standard confirm/cancel buttons to footer."""
        # Default button styles
        default_confirm_style = {
            "background_color": "#28a745",
            "color": "white",
            "border": "none",
            "padding": "8px 16px",
            "border_radius": "4px",
            "cursor": "pointer",
            "margin_left": "8px"
        }
        
        default_cancel_style = {
            "background_color": "#6c757d",
            "color": "white", 
            "border": "none",
            "padding": "8px 16px",
            "border_radius": "4px",
            "cursor": "pointer"
        }
        
        confirm_btn = Button(confirm_text, style={
            **default_confirm_style, **(confirm_style or {})
        })
        cancel_btn = Button(cancel_text, style={
            **default_cancel_style, **(cancel_style or {})
        })
        
        # Event handlers
        confirm_btn.on_click(lambda e: self._handle_confirm())
        cancel_btn.on_click(lambda e: self._handle_cancel())
        
        self.set_footer(cancel_btn, confirm_btn)
        return self
    
    def _handle_confirm(self):
        """Handle confirm button click."""
        self._trigger_callbacks('confirm')
        self.close()
    
    def _handle_cancel(self):
        """Handle cancel button click."""
        self._trigger_callbacks('cancel')
        self.close()
    
    def on_open(self, callback):
        """Register callback for modal open event."""
        return self.on('open', callback)
    
    def on_close(self, callback):
        """Register callback for modal close event."""
        return self.on('close', callback)
    
    def on_confirm(self, callback):
        """Register callback for confirm button click."""
        return self.on('confirm', callback)
    
    def on_cancel(self, callback):
        """Register callback for cancel button click."""
        return self.on('cancel', callback)
    
    @property
    def is_open(self):
        """Check if modal is currently open."""
        return self._get_state('is_open')
    
    # element property is inherited from base class