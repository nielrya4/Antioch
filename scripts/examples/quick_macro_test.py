"""
Quick Macro Test - A simple test of the most commonly used new macros.
"""

from antioch import Div, H1, H2, P, Button, DOM, Hr
from antioch.macros import ProgressBar, Alert, Dropdown, Slider, success_toast, info_toast

def main():
    """Simple test of key macros."""
    
    # Define button style
    button_style = {
        "padding": "8px 16px",
        "margin": "0 5px",
        "border": "1px solid #007bff",
        "background_color": "#007bff",
        "color": "white",
        "border_radius": "4px",
        "cursor": "pointer",
        "font_size": "14px",
        "transition": "all 0.2s ease"
    }
    
    container = Div(style={
        "max_width": "600px",
        "margin": "50px auto",
        "padding": "30px",
        "background": "white",
        "border_radius": "10px",
        "box_shadow": "0 4px 20px rgba(0,0,0,0.1)"
    })
    
    # Title
    container.add(H1("Quick Macro Test", style={"text_align": "center", "color": "#333"}))
    
    # Progress bar that we can control
    progress = ProgressBar(initial_progress=25, width="100%", animate=True)
    container.add(H2("Progress Bar:"))
    container.add(progress.element)
    
    # Controls for progress
    progress_btns = Div(style={"margin": "10px 0", "text_align": "center"})
    
    start_btn = Button("Start Progress", style=button_style)
    complete_btn = Button("Complete", style=button_style)
    
    # Simulate progress
    def start_progress(e):
        progress.set_progress(0)
        # In a real app, you'd use a timer here
        progress.increment(25)
        info_toast("Progress started!")
    
    def complete_progress(e):
        progress.set_progress(100)
        success_toast("Task completed!")
    
    start_btn.on_click(start_progress)
    complete_btn.on_click(complete_progress)
    
    progress_btns.add(start_btn, complete_btn)
    container.add(progress_btns)
    
    container.add(Hr())
    
    # Alert
    alert = Alert("Welcome! This is a quick test of the new macro components.", "info")
    container.add(alert.element)
    
    container.add(Hr())
    
    # Dropdown
    options = ["Python", "JavaScript", "TypeScript", "Rust", "Go"]
    dropdown = Dropdown(items=options, placeholder="Choose your favorite language")
    container.add(H2("Pick a programming language:"))
    container.add(dropdown.element)
    
    container.add(Hr())
    
    # Slider
    slider = Slider(min_value=1, max_value=10, initial_value=5, label="Rate this demo (1-10)")
    container.add(slider.element)
    
    # Feedback button
    feedback_btn_style = {**button_style, "margin_top": "20px", "width": "100%"}
    feedback_btn = Button("Submit Feedback", style=feedback_btn_style)
    
    def show_feedback(e):
        language = dropdown.selected_value or "No language"
        rating = slider.value
        success_toast(f"Thanks! Language: {language}, Rating: {rating}/10")
    
    feedback_btn.on_click(show_feedback)
    container.add(feedback_btn)
    
    DOM.add(container)
    print("🧪 Quick Macro Test loaded!")

if __name__ == "__main__":
    main()