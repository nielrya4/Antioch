"""
Counter macro - A reusable counter component with increment/decrement functionality.
Uses unique IDs to ensure multiple instances work independently.
"""
from .base import Macro
from ..elements import Div, Button, Span


class Counter(Macro):
    """A counter component with increment/decrement buttons."""
    
    def __init__(self, initial_value=0, min_value=None, max_value=None, step=1, 
                 label="Count", button_style=None, counter_style=None, container_style=None):
        """
        Initialize a counter component.
        
        Args:
            initial_value: Starting count value
            min_value: Minimum allowed value (None for no limit)
            max_value: Maximum allowed value (None for no limit)
            step: Amount to increment/decrement
            label: Text label for the counter
            button_style: Style dict for buttons
            counter_style: Style dict for counter display
            container_style: Style dict for container
        """
        # Initialize base macro
        super().__init__(macro_type="counter")
        
        # Set up counter-specific state
        self._set_state(
            value=initial_value,
            min_value=min_value,
            max_value=max_value,
            step=step,
            label=label
        )
        
        # Add callback types
        self._add_callback_type('change')
        
        # Store initial value for reset functionality
        self._initial_value = initial_value
        
        # Default styles
        default_button_style = {
            "background_color": "#007bff",
            "color": "white",
            "border": "none",
            "padding": "8px 12px",
            "border_radius": "4px",
            "cursor": "pointer",
            "margin": "0 4px",
            "font_size": "14px",
            "min_width": "30px"
        }
        
        default_counter_style = {
            "font_size": "18px",
            "font_weight": "bold",
            "margin": "0 8px",
            "min_width": "40px",
            "text_align": "center",
            "display": "inline-block"
        }
        
        default_container_style = {
            "display": "inline-flex",
            "align_items": "center",
            "margin": "10px",
            "padding": "10px",
            "border": "1px solid #ddd",
            "border_radius": "6px",
            "background_color": "#f8f9fa"
        }
        
        # Merge with user styles using base class method
        self._button_style = self._merge_styles(default_button_style, button_style)
        self._counter_style = self._merge_styles(default_counter_style, counter_style)
        self._container_style = self._merge_styles(default_container_style, container_style)
        
        # Initialize macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the counter UI elements."""
        # Container using base class helper
        container = self._create_container(self._container_style)
        
        # Decrement button
        decrement_btn = self._register_element('decrement_btn',
            Button("-", style=self._button_style))
        decrement_btn.on_click(self._decrement)
        
        # Counter display
        counter_display = self._register_element('counter_display',
            Span(str(self._get_state('value')), style=self._counter_style))
        
        # Increment button  
        increment_btn = self._register_element('increment_btn',
            Button("+", style=self._button_style))
        increment_btn.on_click(self._increment)
        
        # Label (if provided)
        label = self._get_state('label')
        if label:
            label_span = Span(f"{label}: ", style={"margin_right": "8px"})
            container.add(label_span)
        
        # Add all elements to container
        container.add(
            decrement_btn,
            counter_display, 
            increment_btn
        )
        
        # Update button states
        self._update_button_states()
        
        return container
    
    def _increment(self, event=None):
        """Handle increment button click."""
        current_value = self._get_state('value')
        step = self._get_state('step')
        max_value = self._get_state('max_value')
        
        new_value = current_value + step
        if max_value is None or new_value <= max_value:
            self._set_state(value=new_value)
            self._update_display()
            self._trigger_callbacks('change', new_value, current_value)
    
    def _decrement(self, event=None):
        """Handle decrement button click."""
        current_value = self._get_state('value')
        step = self._get_state('step')
        min_value = self._get_state('min_value')
        
        new_value = current_value - step
        if min_value is None or new_value >= min_value:
            self._set_state(value=new_value)
            self._update_display()
            self._trigger_callbacks('change', new_value, current_value)
    
    def _update_display(self):
        """Update the counter display and button states."""
        counter_display = self._get_element('counter_display')
        counter_display.set_text(str(self._get_state('value')))
        self._update_button_states()
    
    def _update_button_states(self):
        """Enable/disable buttons based on min/max limits."""
        value = self._get_state('value')
        min_value = self._get_state('min_value')
        max_value = self._get_state('max_value')
        
        decrement_btn = self._get_element('decrement_btn')
        increment_btn = self._get_element('increment_btn')
        
        # Update decrement button
        if min_value is not None and value <= min_value:
            decrement_btn.style.opacity = "0.5"
            decrement_btn.style.cursor = "not-allowed"
            decrement_btn.set_attribute("disabled", "true")
        else:
            decrement_btn.style.opacity = "1"
            decrement_btn.style.cursor = "pointer"
            decrement_btn._dom_element.removeAttribute("disabled")
        
        # Update increment button
        if max_value is not None and value >= max_value:
            increment_btn.style.opacity = "0.5"
            increment_btn.style.cursor = "not-allowed"
            increment_btn.set_attribute("disabled", "true")
        else:
            increment_btn.style.opacity = "1"
            increment_btn.style.cursor = "pointer"
            increment_btn._dom_element.removeAttribute("disabled")
    
    @property
    def value(self):
        """Get the current counter value."""
        return self._get_state('value')
    
    @value.setter
    def value(self, new_value):
        """Set the counter value (respects min/max limits)."""
        min_value = self._get_state('min_value')
        max_value = self._get_state('max_value')
        
        if min_value is not None and new_value < min_value:
            new_value = min_value
        if max_value is not None and new_value > max_value:
            new_value = max_value
        
        old_value = self._get_state('value')
        self._set_state(value=new_value)
        self._update_display()
        self._trigger_callbacks('change', new_value, old_value)
    
    def reset(self, value=None):
        """Reset counter to initial value or specified value."""
        if value is None:
            self.value = self._initial_value
        else:
            self.value = value
        return self
    
    def on_change(self, callback):
        """Register a callback for value changes.
        
        Args:
            callback: Function that takes (counter_instance, new_value, old_value)
        """
        return self.on('change', callback)
    
    def set_limits(self, min_value=None, max_value=None):
        """Update the min/max limits for this counter."""
        self._set_state(min_value=min_value, max_value=max_value)
        
        current_value = self._get_state('value')
        
        # Adjust current value if needed
        if min_value is not None and current_value < min_value:
            self.value = min_value
        elif max_value is not None and current_value > max_value:
            self.value = max_value
        else:
            self._update_button_states()
        
        return self