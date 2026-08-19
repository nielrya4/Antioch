"""
Static HTML generator for splash screens and SEO.

This module provides a subset of Antioch's API that generates static HTML
without requiring Pyodide or JavaScript. Perfect for creating splash screens
and SEO-friendly content.
"""

from typing import Dict, List, Optional, Union, Any


class Keyframe:
    """Pythonic way to define CSS keyframes."""

    def __init__(self, name: str):
        """
        Create a CSS keyframe animation.

        Args:
            name: Animation name
        """
        self.name = name
        # frames: {percentage: {property: [values...]}}
        # Multiple properties can be set at same percentage
        self.frames: Dict[str, Dict[str, List[str]]] = {}

    def add_property(self, percentage: int, property_name: str, value: str):
        """Add a property value at a specific percentage."""
        percent_key = f'{percentage}%'
        if percent_key not in self.frames:
            self.frames[percent_key] = {}
        if property_name not in self.frames[percent_key]:
            self.frames[percent_key][property_name] = []
        self.frames[percent_key][property_name].append(value)

    def render(self) -> str:
        """Render the keyframe to CSS."""
        lines = [f'@keyframes {self.name} {{']

        for percentage, properties in sorted(self.frames.items(), key=lambda x: int(x[0].rstrip('%'))):
            lines.append(f'    {percentage} {{')
            for property_name, values in properties.items():
                css_property = property_name.replace('_', '-')
                # Combine multiple transform values with space
                if property_name == 'transform':
                    combined_value = ' '.join(values)
                    lines.append(f'        {css_property}: {combined_value};')
                else:
                    # For non-transform properties, just use the last value
                    lines.append(f'        {css_property}: {values[-1]};')
            lines.append('    }')

        lines.append('}')
        return '\n'.join(lines)


# Global state for decorator
_current_keyframe: Optional[Keyframe] = None


# Transform and property helper functions
def rotate(values: Dict[int, Union[int, float, str]]):
    """Add rotation keyframes. Values in degrees."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("rotate() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        # Convert to string with 'deg' unit if numeric
        if isinstance(value, (int, float)):
            value_str = f'{value}deg'
        else:
            value_str = value
        _current_keyframe.add_property(percentage, 'transform', f'rotate({value_str})')


def translateX(values: Dict[int, Union[int, float, str]]):
    """Add translateX keyframes. Values in px or other units."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("translateX() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        if isinstance(value, (int, float)):
            value_str = f'{value}px'
        else:
            value_str = value
        _current_keyframe.add_property(percentage, 'transform', f'translateX({value_str})')


def translateY(values: Dict[int, Union[int, float, str]]):
    """Add translateY keyframes. Values in px or other units."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("translateY() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        if isinstance(value, (int, float)):
            value_str = f'{value}px'
        else:
            value_str = value
        _current_keyframe.add_property(percentage, 'transform', f'translateY({value_str})')


def opacity(values: Dict[int, Union[int, float, str]]):
    """Add opacity keyframes."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("opacity() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        _current_keyframe.add_property(percentage, 'opacity', str(value))


def scale(values: Dict[int, Union[int, float, str]]):
    """Add scale keyframes."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("scale() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        _current_keyframe.add_property(percentage, 'transform', f'scale({value})')


def width(values: Dict[int, Union[int, float, str]]):
    """Add width keyframes. Values in % or other units."""
    global _current_keyframe
    if _current_keyframe is None:
        raise RuntimeError("width() must be called inside a @keyframe decorated function")

    for percentage, value in values.items():
        if isinstance(value, (int, float)):
            value_str = f'{value}%'
        else:
            value_str = value
        _current_keyframe.add_property(percentage, 'width', value_str)


# Decorator
def keyframe(func):
    """
    Decorator to define CSS keyframes pythonically.

    Usage:
        @keyframe
        def spin():
            rotate({0: 0, 100: 360})

        @keyframe
        def fadeInUp():
            opacity({0: 0, 100: 1})
            translateY({0: 30, 100: 0})
    """
    global _current_keyframe

    # Create keyframe with function name
    _current_keyframe = Keyframe(func.__name__)

    # Execute function to collect property calls
    func()

    # Get the rendered CSS
    result = _current_keyframe

    # Reset global state
    _current_keyframe = None

    return result


class StaticElement:
    """Base class for static HTML elements."""

    def __init__(self, tag: str, *children, **attrs):
        self.tag = tag
        self.children: List[Union[str, 'StaticElement']] = []
        self.attrs: Dict[str, str] = {}
        self.styles: Dict[str, str] = {}

        # Process attributes
        for key, value in attrs.items():
            if key == 'style' and isinstance(value, dict):
                self.styles.update(value)
            elif key == 'class_name':
                self.attrs['class'] = value
            else:
                # Convert Python-style attributes to HTML
                html_key = key.replace('_', '-')
                self.attrs[html_key] = str(value)

        # Add children
        for child in children:
            self.add(child)

    def add(self, *children) -> 'StaticElement':
        """Add child elements or text."""
        for child in children:
            if isinstance(child, (str, StaticElement)):
                self.children.append(child)
            elif child is None:
                pass  # Skip None values
            else:
                self.children.append(str(child))
        return self

    def set_style(self, **styles) -> 'StaticElement':
        """Set CSS styles."""
        self.styles.update(styles)
        return self

    def set_attr(self, **attrs) -> 'StaticElement':
        """Set HTML attributes."""
        for key, value in attrs.items():
            html_key = key.replace('_', '-')
            self.attrs[html_key] = str(value)
        return self

    def render(self, indent: int = 0) -> str:
        """Render the element to HTML."""
        ind = '  ' * indent

        # Build opening tag
        parts = [f'<{self.tag}']

        # Add attributes
        for key, value in self.attrs.items():
            parts.append(f' {key}="{self._escape_attr(value)}"')

        # Add styles
        if self.styles:
            style_str = '; '.join(f'{k.replace("_", "-")}: {v}' for k, v in self.styles.items())
            parts.append(f' style="{self._escape_attr(style_str)}"')

        # Self-closing tags
        if self.tag in ('img', 'br', 'hr', 'input', 'meta', 'link'):
            parts.append(' />')
            return ind + ''.join(parts)

        parts.append('>')

        # Render children
        if not self.children:
            return ind + ''.join(parts) + f'</{self.tag}>'

        # Check if all children are text
        all_text = all(isinstance(child, str) for child in self.children)

        if all_text and len(self.children) == 1:
            # Single text child - inline
            text = self._escape_html(self.children[0])
            return ind + ''.join(parts) + text + f'</{self.tag}>'

        # Multiple children or element children - multiline
        result = [ind + ''.join(parts)]
        for child in self.children:
            if isinstance(child, str):
                result.append(ind + '  ' + self._escape_html(child))
            else:
                result.append(child.render(indent + 1))
        result.append(ind + f'</{self.tag}>')
        return '\n'.join(result)

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

    @staticmethod
    def _escape_attr(text: str) -> str:
        """Escape attribute values."""
        return (text
                .replace('&', '&amp;')
                .replace('"', '&quot;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))


# HTML Element Classes
class Div(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('div', *children, **attrs)


class Span(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('span', *children, **attrs)


class H1(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h1', text, **attrs)


class H2(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h2', text, **attrs)


class H3(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h3', text, **attrs)


class H4(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h4', text, **attrs)


class H5(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h5', text, **attrs)


class H6(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('h6', text, **attrs)


class P(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('p', text, **attrs)


class A(StaticElement):
    def __init__(self, text: str = '', href: str = '#', **attrs):
        attrs['href'] = href
        super().__init__('a', text, **attrs)


class Img(StaticElement):
    def __init__(self, src: str = '', alt: str = '', **attrs):
        attrs['src'] = src
        attrs['alt'] = alt
        super().__init__('img', **attrs)


class Ul(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('ul', *children, **attrs)


class Ol(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('ol', *children, **attrs)


class Li(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('li', text, **attrs)


class Button(StaticElement):
    def __init__(self, text: str = '', **attrs):
        super().__init__('button', text, **attrs)


class Input(StaticElement):
    def __init__(self, type: str = 'text', **attrs):
        attrs['type'] = type
        super().__init__('input', **attrs)


class Section(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('section', *children, **attrs)


class Header(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('header', *children, **attrs)


class Footer(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('footer', *children, **attrs)


class Nav(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('nav', *children, **attrs)


class Main(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('main', *children, **attrs)


class Article(StaticElement):
    def __init__(self, *children, **attrs):
        super().__init__('article', *children, **attrs)


class Meta(StaticElement):
    def __init__(self, **attrs):
        super().__init__('meta', **attrs)


class Link(StaticElement):
    def __init__(self, **attrs):
        super().__init__('link', **attrs)


class Script(StaticElement):
    def __init__(self, src: str = '', content: str = '', **attrs):
        if src:
            attrs['src'] = src
        super().__init__('script', content, **attrs)


class Style(StaticElement):
    def __init__(self, css: str = '', **attrs):
        super().__init__('style', css, **attrs)


class StaticStyleProxy:
    """Style proxy for StaticPage body element (mimics element StyleProxy)."""

    def __init__(self, styles_dict: Dict[str, str]):
        self._styles = styles_dict

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        css_property = name.replace('_', '-')
        if value is None:
            self._styles.pop(css_property, None)
        else:
            self._styles[css_property] = str(value)

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        css_property = name.replace('_', '-')
        return self._styles.get(css_property, '')

    def update(self, styles: Dict[str, Any]) -> 'StaticStyleProxy':
        """Update multiple styles using a dictionary."""
        for property_name, value in styles.items():
            css_property = property_name.replace('_', '-')
            if value is None:
                self._styles.pop(css_property, None)
            else:
                self._styles[css_property] = str(value)
        return self


class StaticBodyProxy:
    """Proxy for StaticPage body to provide element-like API."""

    def __init__(self, page: 'StaticPage'):
        object.__setattr__(self, '_page', page)
        object.__setattr__(self, '_style', StaticStyleProxy(page.body_styles))

    @property
    def style(self):
        """Get the style proxy."""
        return self._style

    @style.setter
    def style(self, styles: Dict[str, Any]):
        """Set styles using a dictionary."""
        if isinstance(styles, dict):
            self._style.update(styles)
        else:
            raise TypeError("style must be set to a dictionary")


FAVICON_MIME_TYPES = {
    '.png': 'image/png',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.gif': 'image/gif',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
}


def emoji_favicon(emoji: str) -> str:
    """
    An emoji as an inline SVG data URI, usable anywhere an icon href is.

    Lets a page have a favicon without shipping an image file.
    """
    from urllib.parse import quote

    escaped = StaticElement._escape_html(emoji)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           '<text x="50%" y="50%" dy=".35em" text-anchor="middle" '
           f'font-size="80">{escaped}</text></svg>')
    return 'data:image/svg+xml,' + quote(svg)


def _is_emoji(value: str) -> bool:
    """Distinguish a literal emoji from a path, URL or data URI."""
    if not value or len(value) > 8:
        return False
    return not any(c in value for c in '/\\.:')


class StaticPage:
    """Static HTML page generator with SEO support."""

    def __init__(self, title: str = '', lang: str = 'en'):
        self.title = title
        self.lang = lang
        self.head_elements: List[StaticElement] = []
        self.body_elements: List[Union[str, StaticElement]] = []
        self.meta_tags: Dict[str, str] = {}
        self.og_tags: Dict[str, str] = {}
        self.body_attrs: Dict[str, str] = {}
        self.body_styles: Dict[str, str] = {}
        self.favicon: Optional[Dict[str, str]] = None
        self.body = StaticBodyProxy(self)

    def set_title(self, title: str) -> 'StaticPage':
        """Set the page title."""
        self.title = title
        return self

    def set_favicon(self, icon: str, type: str = None, sizes: str = None) -> 'StaticPage':
        """
        Set the browser-tab icon.

        Args:
            icon: An emoji (rendered as an inline SVG), a path such as
                  "assets/favicon.png", or an absolute URL / data URI.
            type: MIME type. Inferred from the file extension when omitted.
            sizes: Optional `sizes` attribute, e.g. "32x32".
        """
        import os

        if _is_emoji(icon):
            href, inferred = emoji_favicon(icon), 'image/svg+xml'
        else:
            href = icon
            inferred = FAVICON_MIME_TYPES.get(os.path.splitext(icon.lower())[1])

        self.favicon = {'href': href}
        if type or inferred:
            self.favicon['type'] = type or inferred
        if sizes:
            self.favicon['sizes'] = sizes
        return self

    def add_meta(self, name: str = '', content: str = '', **attrs) -> 'StaticPage':
        """Add a meta tag."""
        if name:
            attrs['name'] = name
        if content:
            attrs['content'] = content
        self.head_elements.append(Meta(**attrs))
        return self

    def set_description(self, description: str) -> 'StaticPage':
        """Set the meta description for SEO."""
        self.meta_tags['description'] = description
        return self

    def set_keywords(self, *keywords: str) -> 'StaticPage':
        """Set meta keywords for SEO."""
        self.meta_tags['keywords'] = ', '.join(keywords)
        return self

    def set_author(self, author: str) -> 'StaticPage':
        """Set the author meta tag."""
        self.meta_tags['author'] = author
        return self

    def set_og_title(self, title: str) -> 'StaticPage':
        """Set Open Graph title."""
        self.og_tags['og:title'] = title
        return self

    def set_og_description(self, description: str) -> 'StaticPage':
        """Set Open Graph description."""
        self.og_tags['og:description'] = description
        return self

    def set_og_image(self, url: str) -> 'StaticPage':
        """Set Open Graph image."""
        self.og_tags['og:image'] = url
        return self

    def set_og_url(self, url: str) -> 'StaticPage':
        """Set Open Graph URL."""
        self.og_tags['og:url'] = url
        return self

    def add_stylesheet(self, href: str, **attrs) -> 'StaticPage':
        """Add a stylesheet link."""
        attrs['rel'] = 'stylesheet'
        attrs['href'] = href
        self.head_elements.append(Link(**attrs))
        return self

    def add_style(self, css: str) -> 'StaticPage':
        """Add inline CSS."""
        self.head_elements.append(Style(css))
        return self

    def add_script(self, src: str = '', content: str = '', **attrs) -> 'StaticPage':
        """Add a script to the head."""
        self.head_elements.append(Script(src=src, content=content, **attrs))
        return self

    def add_to_head(self, element: StaticElement) -> 'StaticPage':
        """Add a custom element to the head."""
        self.head_elements.append(element)
        return self

    def add(self, *elements: Union[str, StaticElement]) -> 'StaticPage':
        """Add elements to the body."""
        self.body_elements.extend(elements)
        return self

    def set_body_style(self, **styles) -> 'StaticPage':
        """Set styles on the body element."""
        for key, value in styles.items():
            css_key = key.replace('_', '-')
            self.body_styles[css_key] = str(value)
        return self

    def set_body_attr(self, **attrs) -> 'StaticPage':
        """Set attributes on the body element."""
        self.body_attrs.update(attrs)
        return self

    def render(self) -> str:
        """Render the complete HTML page."""
        lines = ['<!DOCTYPE html>']
        lines.append(f'<html lang="{self.lang}">')
        lines.append('<head>')
        lines.append('  <meta charset="UTF-8">')
        lines.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')

        # Title
        if self.title:
            lines.append(f'  <title>{StaticElement._escape_html(self.title)}</title>')

        # Standard meta tags
        for name, content in self.meta_tags.items():
            lines.append(f'  <meta name="{name}" content="{StaticElement._escape_attr(content)}">')

        # Open Graph tags
        for property, content in self.og_tags.items():
            lines.append(f'  <meta property="{property}" content="{StaticElement._escape_attr(content)}">')

        # Favicon
        if self.favicon:
            attrs = ''.join(
                f' {key}="{StaticElement._escape_attr(value)}"'
                for key, value in self.favicon.items()
            )
            lines.append(f'  <link rel="icon"{attrs}>')
            lines.append(f'  <link rel="apple-touch-icon"'
                         f' href="{StaticElement._escape_attr(self.favicon["href"])}">')

        # Additional head elements
        for element in self.head_elements:
            lines.append('  ' + element.render().replace('\n', '\n  '))

        lines.append('</head>')

        # Body tag with attributes and styles
        body_parts = ['<body']
        for key, value in self.body_attrs.items():
            html_key = key.replace('_', '-')
            body_parts.append(f' {html_key}="{StaticElement._escape_attr(value)}"')
        if self.body_styles:
            style_str = '; '.join(f'{k.replace("_", "-")}: {v}' for k, v in self.body_styles.items())
            escaped_style = StaticElement._escape_attr(style_str)
            body_parts.append(f' style="{escaped_style}"')
        body_parts.append('>')
        lines.append(''.join(body_parts))

        # Body elements
        for element in self.body_elements:
            if isinstance(element, str):
                lines.append('  ' + StaticElement._escape_html(element))
            else:
                rendered = element.render(1)
                lines.append(rendered)

        lines.append('</body>')
        lines.append('</html>')

        return '\n'.join(lines)


def create_loading_splash(
    title: str = "Loading...",
    message: str = "Initializing application...",
    spinner: bool = True,
    background_color: str = "#1e1e1e",
    text_color: str = "#ffffff",
    spinner_color: str = "#4a9eff"
) -> StaticPage:
    """
    Create a default loading splash screen.

    Args:
        title: Page title
        message: Loading message to display
        spinner: Whether to show a loading spinner
        background_color: Background color
        text_color: Text color
        spinner_color: Spinner color

    Returns:
        StaticPage configured as a loading splash screen
    """
    page = StaticPage(title=title)

    # Add spinner CSS if requested
    if spinner:
        spinner_css = f"""
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}

        .spinner {{
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid {spinner_color};
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px auto;
        }}
        """
        page.add_style(spinner_css)

    # Set body styles
    page.set_body_style(
        margin='0',
        padding='0',
        display='flex',
        justify_content='center',
        align_items='center',
        min_height='100vh',
        background_color=background_color,
        color=text_color,
        font_family='system-ui, -apple-system, sans-serif'
    )

    # Create loading container
    container = Div(
        id='loading-splash',
        style={
            'text-align': 'center',
            'padding': '40px'
        }
    )

    if spinner:
        container.add(Div(class_name='spinner'))

    container.add(
        H1(title, style={'margin': '0 0 10px 0', 'font-size': '2em'}),
        P(message, style={'margin': '0', 'opacity': '0.8'})
    )

    page.add(container)

    return page