"""
Custom Macro Development Example
Demonstrates how to create new macros using the base Macro class.
"""
from antioch import Div, H1, H2, H3, P, Button, Input, Span, DOM

# Import the base classes for creating custom macros
from antioch.macros import Macro, SimpleMacro, Counter


class ProgressBar(Macro):
    """
    Example custom macro: A progress bar with animated progress.
    Demonstrates how easy it is to create new macros with the base class.
    """
    
    def __init__(self, initial_progress=0, max_progress=100, 
                 width="300px", height="20px", color="#28a745", **kwargs):
        """
        Initialize a progress bar macro.
        
        Args:
            initial_progress: Starting progress value
            max_progress: Maximum progress value
            width: Width of progress bar
            height: Height of progress bar
            color: Color of progress fill
        """
        # Initialize base macro
        super().__init__(macro_type="progress_bar", **kwargs)
        
        # Set up state
        self._set_state(
            progress=initial_progress,
            max_progress=max_progress,
            width=width,
            height=height,
            color=color
        )
        
        # Add callback types
        self._add_callback_type('progress_change')
        self._add_callback_type('complete')
        
        # Initialize the macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the progress bar UI elements."""
        # Container with base class helper
        container = self._create_container({
            "width": self._get_state('width'),
            "height": self._get_state('height'),
            "background_color": "#e9ecef",
            "border_radius": "4px",
            "overflow": "hidden",
            "position": "relative",
            "margin": "10px 0"
        })
        
        # Progress fill element
        progress_fill = self._register_element('progress_fill', Div(style={
            "height": "100%",
            "background_color": self._get_state('color'),
            "width": "0%",
            "transition": "width 0.3s ease",
            "position": "absolute",
            "left": "0",
            "top": "0"
        }))
        
        # Progress text
        progress_text = self._register_element('progress_text', Span("0%", style={
            "position": "absolute",
            "left": "50%",
            "top": "50%",
            "transform": "translate(-50%, -50%)",
            "font_size": "12px",
            "font_weight": "bold",
            "color": "#495057",
            "z_index": "1"
        }))
        
        container.add(progress_fill, progress_text)
        
        # Set initial progress
        self._update_display()
        
        return container
    
    def _update_display(self):
        """Update the progress bar display."""
        progress = self._get_state('progress')
        max_progress = self._get_state('max_progress')
        
        # Calculate percentage
        percentage = min(100, max(0, (progress / max_progress) * 100))
        
        # Update fill width
        fill = self._get_element('progress_fill')
        fill.style.width = f"{percentage}%"
        
        # Update text
        text = self._get_element('progress_text')
        text.set_text(f"{percentage:.0f}%")
        
        # Change text color based on progress
        if percentage > 50:
            text.style.color = "white"
        else:
            text.style.color = "#495057"
    
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
    
    def reset(self):
        """Reset progress to 0."""
        return self.set_progress(0)
    
    @property
    def progress(self):
        """Get current progress value."""
        return self._get_state('progress')
    
    def on_progress_change(self, callback):
        """Register callback for progress changes."""
        return self.on('progress_change', callback)
    
    def on_complete(self, callback):
        """Register callback for completion."""
        return self.on('complete', callback)


class SimpleAlert(SimpleMacro):
    """
    Example using SimpleMacro: A simple alert message.
    Shows how SimpleMacro makes basic components even easier.
    """
    
    def __init__(self, message, alert_type="info", dismissible=True, **kwargs):
        # Set up styling based on alert type
        alert_styles = {
            "info": {"background_color": "#d1ecf1", "color": "#0c5460", "border": "1px solid #bee5eb"},
            "success": {"background_color": "#d4edda", "color": "#155724", "border": "1px solid #c3e6cb"},
            "warning": {"background_color": "#fff3cd", "color": "#856404", "border": "1px solid #ffeaa7"},
            "error": {"background_color": "#f8d7da", "color": "#721c24", "border": "1px solid #f5c6cb"}
        }
        
        base_style = {
            "padding": "12px 16px",
            "border_radius": "4px",
            "margin": "10px 5px",
            "position": "relative",
            "font_size": "14px"
        }
        
        # Merge styles
        container_styles = {**base_style, **alert_styles.get(alert_type, alert_styles["info"])}
        
        # Create content
        content = Div()
        content.add(Span(message, style={
            "padding_right": "10px"
        }))
        
        if dismissible:
            close_btn = Button("×", style={
                "position": "absolute",
                "right": "8px",
                "top": "8px",
                "background": "none",
                "border": "none",
                "font_size": "18px",
                "cursor": "pointer",
                "padding": "0",
                "width": "20px",
                "height": "20px",
                "display": "flex",
                "align_items": "center",
                "justify_content": "center"
            })
            close_btn.on_click(lambda e: self.hide())
            content.add(close_btn)
        
        # Initialize SimpleMacro
        super().__init__(content=content, container_styles=container_styles, 
                        macro_type="alert", **kwargs)


def create_demo():
    """Create a demo showing custom macro usage."""
    demo_section = Div(style={
        "margin": "20px auto",
        "max_width": "600px",
        "padding": "20px",
        "border": "1px solid #ddd",
        "border_radius": "8px",
        "background_color": "#f8f9fa"
    })
    
    demo_section.add(H2("Custom Macro Demo"))
    demo_section.add(P("This demonstrates how easy it is to create custom macros using the base classes."))
    
    # Progress bar demo
    demo_section.add(H3("ProgressBar Macro"))
    demo_section.add(P("A custom progress bar with smooth animations:"))
    
    progress_bar = ProgressBar(initial_progress=25, color="#007bff")
    progress_bar.on_progress_change(lambda macro, new_val, old_val: 
                                   print(f"Progress: {old_val} → {new_val}"))
    progress_bar.on_complete(lambda macro, value: 
                           print(f"Progress completed at {value}!"))
    
    demo_section.add(progress_bar.element)
    
    # Controls for progress bar
    controls = Div(style={"margin": "10px 0"})
    
    increment_btn = Button("Increment +10", style={
        "background_color": "#28a745",
        "color": "white",
        "border": "none",
        "padding": "8px 12px",
        "border_radius": "4px",
        "margin": "0 5px",
        "cursor": "pointer"
    })
    increment_btn.on_click(lambda e: progress_bar.increment(10))
    
    reset_btn = Button("Reset", style={
        "background_color": "#dc3545",
        "color": "white",
        "border": "none",
        "padding": "8px 12px",
        "border_radius": "4px",
        "margin": "0 5px",
        "cursor": "pointer"
    })
    reset_btn.on_click(lambda e: progress_bar.reset())
    
    controls.add(increment_btn, reset_btn)
    demo_section.add(controls)
    
    # SimpleAlert demo
    demo_section.add(H3("SimpleAlert Macro"))
    demo_section.add(P("Simple alerts using SimpleMacro:"))
    
    alerts = [
        SimpleAlert("This is an info alert!", "info"),
        SimpleAlert("Success! Operation completed.", "success"),
        SimpleAlert("Warning: Check your input.", "warning"),
        SimpleAlert("Error: Something went wrong.", "error")
    ]
    
    for alert in alerts:
        demo_section.add(alert.element)
    
    return demo_section


def create_counter_with_progress_demo():
    """Demo showing how existing Counter can work with new ProgressBar."""
    demo_section = Div(style={
        "margin": "20px auto",
        "max_width": "600px",
        "padding": "20px",
        "border": "1px solid #ddd",
        "border_radius": "8px",
        "background_color": "#fff"
    })
    
    demo_section.add(H2("Integrated Macro Demo"))
    demo_section.add(P("Counter controlling ProgressBar - showing how macros work together:"))
    
    # Create counter and progress bar
    counter = Counter(initial_value=0, min_value=0, max_value=100, step=5, 
                     label="Progress")
    progress_bar = ProgressBar(max_progress=100, color="#6f42c1")
    
    # Connect them
    def update_progress(macro, new_value, old_value):
        progress_bar.set_progress(new_value)
        if new_value == 100:
            print("🎉 Goal reached!")
    
    counter.on_change(update_progress)
    
    demo_section.add(counter.element)
    demo_section.add(progress_bar.element)
    
    return demo_section


def main():
    """Main demo function."""
    title = H1("Custom Macro Development", style={
        "text_align": "center",
        "color": "#333"
    })
    DOM.add(title)
    
    intro = P(
        "This demo shows how to create custom macros using the base Macro and SimpleMacro classes. "
        "Creating new components is now much easier with built-in ID management, callbacks, and styling!",
        style={
            "max_width": "800px",
            "margin": "0 auto 30px",
            "text_align": "center",
            "font_size": "16px",
            "color": "#666"
        }
    )
    DOM.add(intro)
    
    # Add demos
    custom_demo = create_demo()
    integrated_demo = create_counter_with_progress_demo()
    
    DOM.add(custom_demo)
    DOM.add(integrated_demo)
    
    print("✅ Custom Macro Development Demo loaded!")


if __name__ == "__main__":
    main()