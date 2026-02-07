"""
Slider macro - A reusable range input/slider component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Input, Span, Label


class Slider(Macro):
    """
    A customizable range slider component with value display and multiple styling options.
    Perfect for settings, filters, volume controls, and any numeric range selection.
    """
    
    def __init__(self, min_value=0, max_value=100, initial_value=50, step=1,
                 label=None, show_value=True, show_min_max=True, show_ticks=False,
                 orientation="horizontal", track_style=None, thumb_style=None,
                 container_style=None, **kwargs):
        """
        Initialize a slider component.
        
        Args:
            min_value: Minimum slider value
            max_value: Maximum slider value
            initial_value: Initial slider value
            step: Step size for value changes
            label: Label text for the slider
            show_value: Whether to show current value
            show_min_max: Whether to show min/max labels
            show_ticks: Whether to show tick marks
            orientation: Slider orientation ("horizontal" or "vertical")
            track_style: Custom styles for slider track
            thumb_style: Custom styles for slider thumb
            container_style: Custom styles for container
        """
        # Initialize base macro
        super().__init__(macro_type="slider", **kwargs)
        
        # Validate and set up state
        initial_value = max(min_value, min(max_value, initial_value))
        
        self._set_state(
            min_value=min_value,
            max_value=max_value,
            value=initial_value,
            step=step,
            label=label,
            show_value=show_value,
            show_min_max=show_min_max,
            show_ticks=show_ticks,
            orientation=orientation
        )
        
        # Add callback types
        self._add_callback_type('change')
        self._add_callback_type('input')  # Continuous updates while sliding
        self._add_callback_type('start')  # Start of slide
        self._add_callback_type('end')    # End of slide
        
        # Default styles
        default_container_style = {
            "padding": "15px",
            "font_family": "Arial, sans-serif"
        }
        
        default_track_style = {
            "width": "100%" if orientation == "horizontal" else "6px",
            "height": "6px" if orientation == "horizontal" else "200px",
            "background": "linear-gradient(to right, #ddd 0%, #ddd 50%, #ddd 100%)",
            "border_radius": "3px",
            "outline": "none",
            "cursor": "pointer"
        }
        
        default_thumb_style = {
            "width": "18px",
            "height": "18px",
            "border_radius": "50%",
            "background_color": "#007bff",
            "cursor": "pointer",
            "border": "2px solid #fff",
            "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
        }
        
        # Merge with user styles
        self._container_style = self._merge_styles(default_container_style, container_style)
        self._track_style = self._merge_styles(default_track_style, track_style)
        self._thumb_style = self._merge_styles(default_thumb_style, thumb_style)
        
        # Initialize macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the slider UI elements."""
        # Main container
        container = self._register_element('container', self._create_container(self._container_style))
        
        # Label (if provided)
        if self._get_state('label'):
            label_elem = self._register_element('label', 
                                               Label(self._get_state('label'), style={
                                                   "display": "block",
                                                   "margin_bottom": "8px",
                                                   "font_weight": "600",
                                                   "color": "#333"
                                               }))
            container.add(label_elem)
        
        # Slider container
        slider_container = self._register_element('slider_container', Div(style={
            "position": "relative",
            "margin": "10px 0"
        }))
        
        # Min/Max labels
        if self._get_state('show_min_max'):
            labels_container = Div(style={
                "display": "flex",
                "justify_content": "space-between",
                "margin_bottom": "5px"
            })
            
            min_label = Span(str(self._get_state('min_value')), style={
                "font_size": "12px",
                "color": "#666"
            })
            
            max_label = Span(str(self._get_state('max_value')), style={
                "font_size": "12px",
                "color": "#666"
            })
            
            labels_container.add(min_label, max_label)
            slider_container.add(labels_container)
        
        # Range input element
        range_input = self._register_element('range_input', Input("range", style={
            "width": "100%",
            "margin": "5px 0",
            "appearance": "none",
            "-webkit-appearance": "none",
            "background": "transparent",
            "cursor": "pointer",
            **self._get_range_input_styles()
        }))
        
        # Set input attributes
        range_input.set_attribute("min", str(self._get_state('min_value')))
        range_input.set_attribute("max", str(self._get_state('max_value')))
        range_input.set_attribute("step", str(self._get_state('step')))
        range_input.set_attribute("value", str(self._get_state('value')))
        
        # Event handlers
        range_input.on_input(lambda e: self._handle_input(e))
        range_input.on_change(lambda e: self._handle_change(e))
        range_input.on_mousedown(lambda e: self._handle_start(e))
        range_input.on_mouseup(lambda e: self._handle_end(e))
        
        slider_container.add(range_input)
        
        # Tick marks (if enabled)
        if self._get_state('show_ticks'):
            ticks_container = self._create_ticks()
            slider_container.add(ticks_container)
        
        container.add(slider_container)
        
        # Value display (if enabled)
        if self._get_state('show_value'):
            value_display = self._create_value_display()
            container.add(value_display)
        
        # Update track gradient
        self._update_track_gradient()
        
        return container
    
    def _get_range_input_styles(self):
        """Get styles for the range input element."""
        return {
            # Track styles
            "background": "linear-gradient(to right, #007bff 0%, #007bff 50%, #ddd 50%, #ddd 100%)",
            "height": "6px",
            "border_radius": "3px",
            "outline": "none",
            
            # WebKit thumb styles (for Chrome/Safari)
            "-webkit-slider-thumb": {
                "-webkit-appearance": "none",
                "width": "18px",
                "height": "18px", 
                "border_radius": "50%",
                "background": "#007bff",
                "cursor": "pointer",
                "border": "2px solid #fff",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
            },
            
            # Mozilla thumb styles (for Firefox)
            "-moz-range-thumb": {
                "width": "18px",
                "height": "18px",
                "border_radius": "50%",
                "background": "#007bff",
                "cursor": "pointer",
                "border": "2px solid #fff",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.2)"
            }
        }
    
    def _create_value_display(self):
        """Create value display element."""
        value_container = Div(style={
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "margin_top": "10px"
        })
        
        value_label = Span("Value:", style={
            "font_size": "14px",
            "color": "#333",
            "font_weight": "600"
        })
        
        value_span = self._register_element('value_display', Span(str(self._get_state('value')), style={
            "font_size": "16px",
            "color": "#007bff",
            "font_weight": "bold",
            "padding": "4px 8px",
            "background_color": "#f8f9fa",
            "border_radius": "4px",
            "border": "1px solid #e9ecef"
        }))
        
        value_container.add(value_label, value_span)
        return value_container
    
    def _create_ticks(self):
        """Create tick marks for the slider."""
        min_val = self._get_state('min_value')
        max_val = self._get_state('max_value')
        step = self._get_state('step')
        
        ticks_container = Div(style={
            "display": "flex",
            "justify_content": "space-between",
            "margin_top": "5px",
            "padding": "0 9px"  # Align with slider track
        })
        
        # Calculate tick positions
        tick_count = min(11, int((max_val - min_val) / step) + 1)  # Max 11 ticks
        tick_step = (max_val - min_val) / (tick_count - 1) if tick_count > 1 else 0
        
        for i in range(tick_count):
            tick_value = min_val + (i * tick_step)
            
            tick = Div(style={
                "width": "1px",
                "height": "8px",
                "background_color": "#999",
                "position": "relative"
            })
            
            # Tick label
            if i % 2 == 0:  # Show every other tick label
                tick_label = Span(f"{tick_value:.0f}" if step >= 1 else f"{tick_value:.1f}", style={
                    "position": "absolute",
                    "top": "10px",
                    "left": "50%",
                    "transform": "translateX(-50%)",
                    "font_size": "10px",
                    "color": "#666",
                    "white_space": "nowrap"
                })
                tick.add(tick_label)
            
            ticks_container.add(tick)
        
        return ticks_container
    
    def _handle_input(self, event):
        """Handle input event (continuous while sliding)."""
        new_value = float(event.target.value)
        old_value = self._get_state('value')
        
        self._set_state(value=new_value)
        self._update_display()
        self._update_track_gradient()
        
        self._trigger_callbacks('input', new_value, old_value)
    
    def _handle_change(self, event):
        """Handle change event (final value)."""
        new_value = float(event.target.value)
        old_value = self._get_state('value')
        
        self._trigger_callbacks('change', new_value, old_value)
    
    def _handle_start(self, event):
        """Handle start of sliding."""
        self._trigger_callbacks('start', self._get_state('value'))
    
    def _handle_end(self, event):
        """Handle end of sliding."""
        self._trigger_callbacks('end', self._get_state('value'))
    
    def _update_display(self):
        """Update value display."""
        if self._get_state('show_value'):
            value_display = self._get_element('value_display')
            if value_display:
                value_display.set_text(str(self._get_state('value')))
    
    def _update_track_gradient(self):
        """Update track gradient to show progress."""
        min_val = self._get_state('min_value')
        max_val = self._get_state('max_value')
        current_val = self._get_state('value')
        
        # Calculate percentage
        percentage = ((current_val - min_val) / (max_val - min_val)) * 100 if max_val != min_val else 0
        
        range_input = self._get_element('range_input')
        if range_input:
            # Update background gradient to show filled portion
            gradient = f"linear-gradient(to right, #007bff 0%, #007bff {percentage}%, #ddd {percentage}%, #ddd 100%)"
            range_input.style.background = gradient
    
    def set_value(self, value):
        """Set slider value."""
        min_val = self._get_state('min_value')
        max_val = self._get_state('max_value')
        
        # Clamp value to valid range
        clamped_value = max(min_val, min(max_val, value))
        old_value = self._get_state('value')
        
        self._set_state(value=clamped_value)
        
        # Update input element
        range_input = self._get_element('range_input')
        if range_input:
            range_input.value = str(clamped_value)
        
        self._update_display()
        self._update_track_gradient()
        
        self._trigger_callbacks('change', clamped_value, old_value)
        return self
    
    def set_range(self, min_value, max_value):
        """Set slider range."""
        current_value = self._get_state('value')
        
        self._set_state(min_value=min_value, max_value=max_value)
        
        # Clamp current value to new range
        new_value = max(min_value, min(max_value, current_value))
        if new_value != current_value:
            self.set_value(new_value)
        
        # Update input attributes
        range_input = self._get_element('range_input')
        if range_input:
            range_input.set_attribute("min", str(min_value))
            range_input.set_attribute("max", str(max_value))
        
        self._update_track_gradient()
        return self
    
    def set_step(self, step):
        """Set slider step size."""
        self._set_state(step=step)
        
        range_input = self._get_element('range_input')
        if range_input:
            range_input.set_attribute("step", str(step))
        
        return self
    
    def increment(self, amount=None):
        """Increment slider value by step or specified amount."""
        if amount is None:
            amount = self._get_state('step')
        
        current_value = self._get_state('value')
        return self.set_value(current_value + amount)
    
    def decrement(self, amount=None):
        """Decrement slider value by step or specified amount."""
        if amount is None:
            amount = self._get_state('step')
        
        current_value = self._get_state('value')
        return self.set_value(current_value - amount)
    
    def reset(self):
        """Reset to initial value."""
        # We don't store initial value in state, so reset to middle of range
        min_val = self._get_state('min_value')
        max_val = self._get_state('max_value')
        middle_value = (min_val + max_val) / 2
        return self.set_value(middle_value)
    
    def set_label(self, label):
        """Update slider label."""
        self._set_state(label=label)
        
        label_elem = self._get_element('label')
        if label_elem:
            label_elem.set_text(label)
        
        return self
    
    def toggle_value_display(self, show=None):
        """Toggle value display visibility."""
        current_show = self._get_state('show_value')
        new_show = not current_show if show is None else show
        
        self._set_state(show_value=new_show)
        
        # Would need to recreate elements to toggle display
        # For simplicity, just update the current display if it exists
        value_display = self._get_element('value_display')
        if value_display:
            value_display.style.display = "block" if new_show else "none"
        
        return self
    
    @property
    def value(self):
        """Get current slider value."""
        return self._get_state('value')
    
    @property
    def min_value(self):
        """Get minimum value."""
        return self._get_state('min_value')
    
    @property
    def max_value(self):
        """Get maximum value."""
        return self._get_state('max_value')
    
    @property
    def percentage(self):
        """Get current value as percentage of range."""
        min_val = self.min_value
        max_val = self.max_value
        current_val = self.value
        
        return ((current_val - min_val) / (max_val - min_val)) * 100 if max_val != min_val else 0
    
    def on_change(self, callback):
        """Register callback for value changes (final)."""
        return self.on('change', callback)
    
    def on_input(self, callback):
        """Register callback for continuous input."""
        return self.on('input', callback)
    
    def on_start(self, callback):
        """Register callback for start of sliding."""
        return self.on('start', callback)
    
    def on_end(self, callback):
        """Register callback for end of sliding."""
        return self.on('end', callback)