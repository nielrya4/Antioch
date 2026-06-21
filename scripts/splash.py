"""
Antioch Demo Splash Screen

This splash screen displays while Pyodide loads, providing SEO-friendly
static HTML content for search engines and a better user experience.
"""

from antioch.static import StaticPage, Div, P, keyframe, rotate, opacity, translateY


# Define keyframe animations pythonically!
@keyframe
def spin():
    rotate({0: 0, 100: 360})


@keyframe
def fadeInDown():
    opacity({0: 0, 100: 1})
    translateY({0: -30, 100: 0})


@keyframe
def fadeInUp():
    opacity({0: 0, 100: 1})
    translateY({0: 30, 100: 0})


def generate_splash():
    """Generate the static splash screen HTML."""

    # Create the page with SEO metadata
    page = StaticPage(title="Antioch - Python Web Framework", lang="en")

    # SEO Meta Tags
    page.set_description(
        "Antioch is a Python web framework that runs entirely in the browser using Pyodide. "
        "Build interactive web applications with pure Python - no JavaScript required."
    )
    page.set_keywords("python", "web framework", "pyodide", "webassembly", "browser", "antioch")
    page.set_author("Ryan Nielsen")

    # Open Graph tags for social media
    page.set_og_title("Antioch - Python Web Framework")
    page.set_og_description("Build web applications with pure Python in the browser")
    page.set_og_url("https://github.com/nielrya4/antioch")

    # Add animations to page
    page.add_style(spin.render())
    page.add_style(fadeInDown.render())
    page.add_style(fadeInUp.render())

    # Set body styles using dictionary assignment (just like DOM.body.style in Antioch!)
    page.body.style = {
        'margin': '0',
        'padding': '0',
        'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'min_height': '100vh',
        'display': 'flex',
        'justify_content': 'center',
        'align_items': 'center',
        'color': 'white'
    }

    # Build the splash screen content with pythonic styles
    container = Div(id="loading-splash", style={
        'text-align': 'center',
        'padding': '40px',
        'max-width': '600px'
    })

    # Logo with gradient text effect
    logo = Div("ANTIOCH", style={
        'font-size': '4em',
        'font-weight': 'bold',
        'margin-bottom': '20px',
        'background': 'linear-gradient(135deg, #fff 0%, #f0f0f0 100%)',
        '-webkit-background-clip': 'text',
        '-webkit-text-fill-color': 'transparent',
        'background-clip': 'text',
        'animation': 'fadeInDown 0.8s ease-out'
    })

    # Tagline
    tagline = P("Python in the Browser", style={
        'font-size': '1.5em',
        'margin-bottom': '30px',
        'opacity': '0.9',
        'animation': 'fadeInUp 0.8s ease-out 0.2s both'
    })

    # Spinner
    spinner_container = Div(style={
        'margin': '30px auto 20px auto',
        'animation': 'fadeInUp 0.8s ease-out 0.6s both'
    })
    spinner = Div(style={
        'border': '4px solid rgba(255, 255, 255, 0.3)',
        'border-top': '4px solid white',
        'border-radius': '50%',
        'width': '60px',
        'height': '60px',
        'animation': 'spin 1s linear infinite',
        'margin': '0 auto'
    })
    spinner_container.add(spinner)

    # Loading text
    loading_text = P("Loading modules...", style={
        'font-size': '1.1em',
        'margin': '0',
        'opacity': '0.8',
        'animation': 'fadeInUp 0.8s ease-out 0.8s both'
    })

    # Add all elements to container
    container.add(logo, tagline, spinner_container, loading_text)

    page.add(container)

    return page


# Allow running this file directly to preview the splash screen
if __name__ == "__main__":
    import sys
    from pathlib import Path

    # Add parent directory to path to import antioch.static
    sys.path.insert(0, str(Path(__file__).parent.parent))

    page = generate_splash()
    preview_path = Path(__file__).parent.parent / "splash_preview.html"

    with open(preview_path, "w") as f:
        f.write(page.render())

    print(f"✅ Splash screen preview saved to: {preview_path}")
    print(f"   Open it in a browser to see how it looks!")