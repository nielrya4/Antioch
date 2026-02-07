"""
Utility functions for dynamically injecting JavaScript and CSS libraries.

Each library module is responsible for loading its own dependencies using these utilities.
This keeps the ecosystem modular - no central registry needed.
"""
import js


def is_script_loaded(src):
    """
    Check if a script tag with the given src already exists in the document.

    Args:
        src: URL or path to check for (can be partial match)

    Returns:
        bool: True if script exists, False otherwise
    """
    scripts = js.document.getElementsByTagName('script')
    for i in range(scripts.length):
        script = scripts[i]
        if script.src and src in script.src:
            return True
    return False


def is_stylesheet_loaded(href):
    """
    Check if a stylesheet link with the given href already exists in the document.

    Args:
        href: URL or path to check for (can be partial match)

    Returns:
        bool: True if stylesheet exists, False otherwise
    """
    links = js.document.getElementsByTagName('link')
    for i in range(links.length):
        link = links[i]
        if link.rel == 'stylesheet' and link.href and href in link.href:
            return True
    return False


def is_global_defined(global_name):
    """
    Check if a global JavaScript object is defined.

    Args:
        global_name: Name of the global to check (e.g., 'Chart', 'L')

    Returns:
        bool: True if global exists and is truthy, False otherwise
    """
    return hasattr(js, global_name) and getattr(js, global_name)


def inject_script(src):
    """
    Inject a script tag into document.head if not already present.

    Args:
        src: URL or path to the script file

    Returns:
        bool: True if injected, False if already exists
    """
    if is_script_loaded(src):
        return False

    # Create and append script tag
    script = js.document.createElement('script')
    script.src = src
    js.document.head.appendChild(script)
    return True


def inject_stylesheet(href):
    """
    Inject a stylesheet link into document.head if not already present.

    Args:
        href: URL or path to the CSS file

    Returns:
        bool: True if injected, False if already exists
    """
    if is_stylesheet_loaded(href):
        return False

    # Create and append link tag
    link = js.document.createElement('link')
    link.rel = 'stylesheet'
    link.href = href
    js.document.head.appendChild(link)
    return True
