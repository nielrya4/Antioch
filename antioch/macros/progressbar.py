"""
ProgressBar macro - A reusable progress indicator component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Span


class ProgressBar(Macro):
    """
    A progress bar with animated progress indication.
    Perfect for showing task completion, loading states, or any percentage-based data.
    """
    
    def __init__(self, initial_progress=0, max_progress=100, 
                 width="300px", height="20px", color="#28a745", 
                 background_color="#e9ecef", show_text=True, 
                 animate=True, striped=False, **kwargs):
        """
        Initialize a progress bar macro.
        
        Args:
            initial_progress: Starting progress value
            max_progress: Maximum progress value
            width: Width of progress bar
            height: Height of progress bar
            color: Color of progress fill
            background_color: Background color of progress track
            show_text: Whether to show percentage text
            animate: Whether to animate progress changes
            striped: Whether to show striped pattern
        """
        # Initialize base macro
        super().__init__(macro_type="progress_bar", **kwargs)
        
        # Set up state
        self._set_state(
            progress=initial_progress,
            max_progress=max_progress,
            width=width,
            height=height,
            color=color,
            background_color=background_color,
            show_text=show_text,
            animate=animate,
            striped=striped
        )
        
        # Add callback types
        self._add_callback_type('progress_change')
        self._add_callback_type('complete')
        self._add_callback_type('reset')
        
        # Initialize the macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the progress bar UI elements."""
        # Container with base class helper
        container = self._register_element('container', self._create_container({
            "width": self._get_state('width'),
            "height": self._get_state('height'),
            "background_color": self._get_state('background_color'),
            "border_radius": "4px",
            "overflow": "hidden",
            "position": "relative",
            "margin": "10px 0",
            "box_shadow": "inset 0 1px 2px rgba(0,0,0,0.1)"
        }))
        
        # Progress fill element
        progress_fill = self._register_element('progress_fill', Div(style={
            "height": "100%",
            "background_color": self._get_state('color'),
            "width": "0%",
            "position": "absolute",
            "left": "0",
            "top": "0",
            "border_radius": "4px 0 0 4px"
        }))
        
        # Add animation if enabled
        if self._get_state('animate'):
            progress_fill.style.transition = "width 0.3s ease"
        
        # Add stripes if enabled
        if self._get_state('striped'):
            progress_fill.style.background_image = "linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent)"
            progress_fill.style.background_size = "1rem 1rem"
        
        # Progress text (if enabled)
        if self._get_state('show_text'):
            progress_text = self._register_element('progress_text', Span("0%", style={
                "position": "absolute",
                "left": "50%",
                "top": "50%",
                "transform": "translate(-50%, -50%)",
                "font_size": "12px",
                "font_weight": "bold",
                "color": "#495057",
                "z_index": "2",
                "text_shadow": "0 1px 1px rgba(255,255,255,0.8)"
            }))
            container.add(progress_text)
        
        container.add(progress_fill)
        
        # Set initial progress
        self._update_display()
        
        return container
    
    def _update_display(self):
        """Update the progress bar display."""
        progress = self._get_state('progress')
        max_progress = self._get_state('max_progress')
        
        # Calculate percentage
        percentage = min(100, max(0, (progress / max_progress) * 100)) if max_progress > 0 else 0
        
        # Update fill width
        fill = self._get_element('progress_fill')
        if fill:
            fill.style.width = f"{percentage}%"
            
            # Update border radius based on completion
            if percentage >= 100:
                fill.style.border_radius = "4px"
            else:
                fill.style.border_radius = "4px 0 0 4px"
        
        # Update text if enabled
        if self._get_state('show_text'):
            text = self._get_element('progress_text')
            if text:
                text.set_text(f"{percentage:.0f}%")
                
                # Change text color based on progress for better visibility
                if percentage > 50:
                    text.style.color = "white"
                    text.style.text_shadow = "0 1px 1px rgba(0,0,0,0.5)"
                else:
                    text.style.color = "#495057"
                    text.style.text_shadow = "0 1px 1px rgba(255,255,255,0.8)"
    
    def set_progress(self, value):
        """Set the progress value."""
        old_progress = self._get_state('progress')
        max_progress = self._get_state('max_progress')
        
        # Clamp value to valid range
        value = max(0, min(max_progress, value))
        
        self._set_state(progress=value)
        self._update_display()
        
        # Trigger callbacks
        self._trigger_callbacks('progress_change', value, old_progress)
        
        # Check if complete
        if value >= max_progress:
            self._trigger_callbacks('complete', value)
        
        return self
    
    def increment(self, amount=1):
        """Increment progress by amount."""
        current = self._get_state('progress')
        return self.set_progress(current + amount)
    
    def decrement(self, amount=1):
        """Decrement progress by amount."""
        current = self._get_state('progress')
        return self.set_progress(current - amount)
    
    def reset(self):
        """Reset progress to 0."""
        old_progress = self._get_state('progress')
        self.set_progress(0)
        self._trigger_callbacks('reset', old_progress)
        return self
    
    def set_max(self, max_value):
        """Set the maximum progress value."""
        self._set_state(max_progress=max_value)
        self._update_display()  # Recalculate percentage
        return self
    
    def set_color(self, color):
        """Set the progress bar color."""
        self._set_state(color=color)
        fill = self._get_element('progress_fill')
        if fill:
            fill.style.background_color = color
        return self
    
    def set_size(self, width, height=None):
        """Set the progress bar size."""
        self._set_state(width=width)
        if height:
            self._set_state(height=height)
        
        # Update container size
        container = self._get_element('container')
        if container:
            container.style.width = width
            if height:
                container.style.height = height
        return self
    
    def toggle_animation(self, enable=None):
        """Toggle or set animation state."""
        current_animate = self._get_state('animate')
        new_animate = not current_animate if enable is None else enable
        
        self._set_state(animate=new_animate)
        
        fill = self._get_element('progress_fill')
        if fill:
            if new_animate:
                fill.style.transition = "width 0.3s ease"
            else:
                fill.style.transition = "none"
        
        return self
    
    def toggle_stripes(self, enable=None):
        """Toggle or set striped pattern."""
        current_striped = self._get_state('striped')
        new_striped = not current_striped if enable is None else enable
        
        self._set_state(striped=new_striped)
        
        fill = self._get_element('progress_fill')
        if fill:
            if new_striped:
                fill.style.background_image = "linear-gradient(45deg, rgba(255,255,255,.15) 25%, transparent 25%, transparent 50%, rgba(255,255,255,.15) 50%, rgba(255,255,255,.15) 75%, transparent 75%, transparent)"
                fill.style.background_size = "1rem 1rem"
            else:
                fill.style.background_image = "none"
        
        return self
    
    @property
    def progress(self):
        """Get current progress value."""
        return self._get_state('progress')
    
    @property
    def percentage(self):
        """Get current progress as percentage."""
        progress = self._get_state('progress')
        max_progress = self._get_state('max_progress')
        return (progress / max_progress) * 100 if max_progress > 0 else 0
    
    @property
    def is_complete(self):
        """Check if progress is complete."""
        return self.progress >= self._get_state('max_progress')
    
    def on_progress_change(self, callback):
        """Register callback for progress changes."""
        return self.on('progress_change', callback)
    
    def on_complete(self, callback):
        """Register callback for completion."""
        return self.on('complete', callback)
    
    def on_reset(self, callback):
        """Register callback for reset."""
        return self.on('reset', callback)