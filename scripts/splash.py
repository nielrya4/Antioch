"""
Antioch Demo Splash Screen

This splash screen displays while Pyodide loads, providing SEO-friendly
static HTML content for search engines and a better user experience.
"""

from antioch.static import StaticPage, Div, H1, P, Span


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

    # Add keyframe animations as CSS (can't be done pythonically)
    page.add_style("""
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    """)

    # Set body styles pythonically - don't override background completely,
    # just set styles for the splash that won't interfere with DOM
    page.set_body_style(
        margin='0',
        padding='0',
        font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
        background='linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        min_height='100vh',
        display='flex',
        justify_content='center',
        align_items='center',
        color='white'
    )

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

    # Loading text
    loading_text = P("Initializing Python environment...", style={
        'font-size': '1.1em',
        'margin-bottom': '20px',
        'opacity': '0.8',
        'animation': 'fadeInUp 0.8s ease-out 0.4s both'
    })

    # Spinner
    spinner_container = Div(style={
        'margin': '30px auto',
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

    # Progress bar
    progress_bar = Div(style={
        'width': '300px',
        'height': '4px',
        'background': 'rgba(255, 255, 255, 0.2)',
        'border-radius': '2px',
        'margin': '30px auto 10px auto',
        'overflow': 'hidden',
        'animation': 'fadeInUp 0.8s ease-out 0.8s both'
    })
    progress_fill = Div(style={
        'height': '100%',
        'background': 'white',
        'border-radius': '2px',
        'animation': 'progress 2s ease-in-out infinite'
    })
    progress_bar.add(progress_fill)

    # Status text
    status = P("Loading WebAssembly modules...", style={
        'font-size': '0.9em',
        'opacity': '0.7',
        'animation': 'fadeInUp 0.8s ease-out 1s both'
    })

    # Feature highlights (good for SEO)
    features = Div(style={
        'margin-top': '40px',
        'display': 'flex',
        'gap': '20px',
        'justify-content': 'center',
        'flex-wrap': 'wrap',
        'animation': 'fadeInUp 0.8s ease-out 1.2s both'
    })

    # Individual feature badges
    feature1 = Span("🐍 Pure Python", style={
        'background': 'rgba(255, 255, 255, 0.1)',
        'padding': '15px 25px',
        'border-radius': '20px',
        'font-size': '0.9em',
        'backdrop-filter': 'blur(10px)'
    })
    feature2 = Span("⚡ Fast", style={
        'background': 'rgba(255, 255, 255, 0.1)',
        'padding': '15px 25px',
        'border-radius': '20px',
        'font-size': '0.9em',
        'backdrop-filter': 'blur(10px)'
    })
    feature3 = Span("🎨 Modern", style={
        'background': 'rgba(255, 255, 255, 0.1)',
        'padding': '15px 25px',
        'border-radius': '20px',
        'font-size': '0.9em',
        'backdrop-filter': 'blur(10px)'
    })

    features.add(feature1, feature2, feature3)

    # Add all elements to container
    container.add(logo, tagline, loading_text, spinner_container, progress_bar, status, features)

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