import js
from pyodide.ffi import create_proxy
from typing import Union, Optional, List, Any, Dict

class StyleProxy:
    """Proxy object for seamless CSS style manipulation."""

    def __init__(self, element):
        self._element = element
        self._dom_element = element._dom_element

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
            return

        css_property = name.replace('_', '-')

        if value is None:
            self._dom_element.style.removeProperty(css_property)
        else:
            self._dom_element.style.setProperty(css_property, str(value))

    def __getattr__(self, name):
        if name.startswith('_'):
            return super().__getattribute__(name)
        css_property = name.replace('_', '-')
        return self._dom_element.style.getPropertyValue(css_property)

    def update(self, styles: Dict[str, Any]) -> 'StyleProxy':
        """Update multiple styles using a dictionary."""
        for property_name, value in styles.items():
            css_property = property_name.replace('_', '-')

            if value is None:
                self._dom_element.style.removeProperty(css_property)
            else:
                self._dom_element.style.setProperty(css_property, str(value))
        return self

class Element:
    """Base class for all DOM elements with real js.document integration."""
    
    @staticmethod
    def _create_style_proxy(element):
        """Helper method to create StyleProxy for existing DOM elements."""
        return StyleProxy(element)
    
    def __init__(self, tag_name: str, *content, **kwargs):
        # Create real DOM element
        self._dom_element = js.document.createElement(tag_name)
        self._style = StyleProxy(self)

        # Handle style dictionary for direct style binding
        styles = kwargs.pop('style', {})

        # Handle events dictionary for direct event binding
        events = kwargs.pop('events', {})

        # Handle content parameter(s) - supports variable arguments
        # P("text")  -> single string
        # P(element) -> single element
        # P("text", element, "more text") -> multiple items
        # P(["text", element]) -> list of items
        if content:
            if len(content) == 1:
                # Single argument - handle as before for backwards compatibility
                item = content[0]
                if isinstance(item, str):
                    self.set_text(item)
                elif isinstance(item, Element):
                    self.add(item)
                elif hasattr(item, '__iter__') and not isinstance(item, str):
                    self.add(*item)
                else:
                    self.add(item)
            else:
                # Multiple arguments - add all
                self.add(*content)

        # Set attributes
        for attr, value in kwargs.items():
            self.set_attribute(attr, value)

        # Bind events
        if events:
            self.handle(events)

        # Apply styles
        if styles:
            self._style.update(styles)
    
    @property
    def style(self) -> StyleProxy:
        """Access CSS styles with dot notation."""
        return self._style
    
    @style.setter
    def style(self, styles: Dict[str, Any]):
        """Set multiple styles using dictionary assignment."""
        self._style.update(styles)
    
    @property
    def dom_element(self):
        """Access to the underlying DOM element."""
        return self._dom_element
    
    def add(self, *items) -> 'Element':
        """Add child elements or text content. Returns self for method chaining."""
        for item in items:
            if isinstance(item, Element):
                self._dom_element.appendChild(item._dom_element)
            elif hasattr(item, 'element') and hasattr(item.element, '_dom_element'):
                # Handle Macro objects - use their root element
                self._dom_element.appendChild(item.element._dom_element)
            elif isinstance(item, str):
                text_node = js.document.createTextNode(item)
                self._dom_element.appendChild(text_node)
            elif hasattr(item, '__iter__') and not isinstance(item, str):
                self.add(*item)
            else:
                text_node = js.document.createTextNode(str(item))
                self._dom_element.appendChild(text_node)
        return self
    
    def set_attribute(self, name: str, value: Any) -> 'Element':
        """Set an HTML attribute."""
        attr_name = name.replace('_', '-')
        self._dom_element.setAttribute(attr_name, str(value))
        return self
    
    def get_attribute(self, name: str) -> Optional[str]:
        """Get an HTML attribute value."""
        attr_name = name.replace('_', '-')
        return self._dom_element.getAttribute(attr_name)
    
    def set_text(self, text: str) -> 'Element':
        """Set the text content of this element."""
        self._dom_element.textContent = text
        return self
    
    def append_to(self, parent) -> 'Element':
        """Append this element to a parent element."""
        if isinstance(parent, Element):
            parent._dom_element.appendChild(self._dom_element)
        else:
            parent.appendChild(self._dom_element)
        return self
    
    def remove(self) -> 'Element':
        """Remove this element from the DOM."""
        if self._dom_element.parentNode:
            self._dom_element.parentNode.removeChild(self._dom_element)
        return self
    
    # Event handling methods
    def on(self, event: str, handler) -> 'Element':
        """Add a single event listener."""
        if handler:
            proxy_handler = create_proxy(handler)
            self._dom_element.addEventListener(event, proxy_handler)
        return self
    
    def handle(self, event_handlers: Dict[str, Any]) -> 'Element':
        """Add multiple event handlers using a dictionary."""
        for event, handler in event_handlers.items():
            if handler:
                proxy_handler = create_proxy(handler)
                self._dom_element.addEventListener(event, proxy_handler)
        return self
    
    # Pythonic event handling methods
    def on_click(self, handler) -> 'Element':
        """Add a click event handler."""
        return self.on('click', handler)
    
    def on_change(self, handler) -> 'Element':
        """Add a change event handler."""
        return self.on('change', handler)
    
    def on_input(self, handler) -> 'Element':
        """Add an input event handler."""
        return self.on('input', handler)
    
    def on_submit(self, handler) -> 'Element':
        """Add a submit event handler."""
        return self.on('submit', handler)
    
    def on_focus(self, handler) -> 'Element':
        """Add a focus event handler."""
        return self.on('focus', handler)
    
    def on_blur(self, handler) -> 'Element':
        """Add a blur event handler."""
        return self.on('blur', handler)
    
    def on_mouseenter(self, handler) -> 'Element':
        """Add a mouseenter event handler."""
        return self.on('mouseenter', handler)
    
    def on_mouseleave(self, handler) -> 'Element':
        """Add a mouseleave event handler."""
        return self.on('mouseleave', handler)
    
    def on_mousedown(self, handler) -> 'Element':
        """Add a mousedown event handler."""
        return self.on('mousedown', handler)
    
    def on_mouseup(self, handler) -> 'Element':
        """Add a mouseup event handler."""
        return self.on('mouseup', handler)
    
    def on_keydown(self, handler) -> 'Element':
        """Add a keydown event handler."""
        return self.on('keydown', handler)
    
    def on_keyup(self, handler) -> 'Element':
        """Add a keyup event handler."""
        return self.on('keyup', handler)
    
    def __str__(self):
        """Return the DOM element's HTML representation."""
        return self._dom_element.outerHTML


# HTML Elements following the clean sci_ux pattern
class Div(Element):
    """Division element for grouping content."""
    def __init__(self, *content, **kwargs):
        super().__init__('div', *content, **kwargs)

class Span(Element):
    """Inline text container."""
    def __init__(self, *content, **kwargs):
        super().__init__('span', *content, **kwargs)

class P(Element):
    """Paragraph element."""
    def __init__(self, *content, **kwargs):
        super().__init__('p', *content, **kwargs)

class H1(Element):
    """Heading level 1."""
    def __init__(self, *content, **kwargs):
        super().__init__('h1', *content, **kwargs)

class H2(Element):
    """Heading level 2."""
    def __init__(self, *content, **kwargs):
        super().__init__('h2', *content, **kwargs)

class H3(Element):
    """Heading level 3."""
    def __init__(self, *content, **kwargs):
        super().__init__('h3', *content, **kwargs)

class H4(Element):
    """Heading level 4."""
    def __init__(self, *content, **kwargs):
        super().__init__('h4', *content, **kwargs)

class H5(Element):
    """Heading level 5."""
    def __init__(self, *content, **kwargs):
        super().__init__('h5', *content, **kwargs)

class H6(Element):
    """Heading level 6."""
    def __init__(self, *content, **kwargs):
        super().__init__('h6', *content, **kwargs)

class Hr(Element):
    """Horizontal rule (line) element."""
    def __init__(self, **kwargs):
        super().__init__('hr', "", **kwargs)

class Button(Element):
    """Button element."""
    def __init__(self, *content, **kwargs):
        super().__init__('button', *content, **kwargs)

class Input(Element):
    """Input element for form controls."""
    def __init__(self, input_type='text', **kwargs):
        kwargs['type'] = input_type
        super().__init__('input', **kwargs)
    
    @property
    def value(self):
        return self._dom_element.value
    
    @value.setter
    def value(self, val):
        self._dom_element.value = str(val)

class Textarea(Element):
    """Textarea element for multi-line text input."""
    def __init__(self, *content, **kwargs):
        super().__init__('textarea', *content, **kwargs)
    
    @property
    def value(self):
        return self._dom_element.value
    
    @value.setter
    def value(self, val):
        self._dom_element.value = str(val)

class Select(Element):
    """Select dropdown element."""
    def __init__(self, *content, **kwargs):
        super().__init__('select', *content, **kwargs)
    
    @property
    def value(self):
        return self._dom_element.value
    
    @value.setter
    def value(self, val):
        self._dom_element.value = str(val)

class Option(Element):
    """Option element for select dropdowns."""
    def __init__(self, *content, value=None, **kwargs):
        if value is not None:
            kwargs['value'] = value
        super().__init__('option', *content, **kwargs)

class A(Element):
    """Anchor/link element."""
    def __init__(self, *content, href=None, **kwargs):
        if href is not None:
            kwargs['href'] = href
        super().__init__('a', *content, **kwargs)

class Img(Element):
    """Image element."""
    def __init__(self, src=None, alt=None, **kwargs):
        if src is not None:
            kwargs['src'] = src
        if alt is not None:
            kwargs['alt'] = alt
        super().__init__('img', **kwargs)

class Form(Element):
    """Form element."""
    def __init__(self, *content, **kwargs):
        super().__init__('form', *content, **kwargs)

class Label(Element):
    """Label element for form controls."""
    def __init__(self, *content, **kwargs):
        super().__init__('label', *content, **kwargs)

class Ul(Element):
    """Unordered list element."""
    def __init__(self, *content, **kwargs):
        super().__init__('ul', *content, **kwargs)

class Ol(Element):
    """Ordered list element."""
    def __init__(self, *content, **kwargs):
        super().__init__('ol', *content, **kwargs)

class Li(Element):
    """List item element."""
    def __init__(self, *content, **kwargs):
        super().__init__('li', *content, **kwargs)

class Table(Element):
    """Table element."""
    def __init__(self, *content, **kwargs):
        super().__init__('table', *content, **kwargs)

class Tr(Element):
    """Table row element."""
    def __init__(self, *content, **kwargs):
        super().__init__('tr', *content, **kwargs)

class Td(Element):
    """Table data cell element."""
    def __init__(self, *content, **kwargs):
        super().__init__('td', *content, **kwargs)

class Th(Element):
    """Table header cell element."""
    def __init__(self, *content, **kwargs):
        super().__init__('th', *content, **kwargs)

class Thead(Element):
    """Table head element."""
    def __init__(self, *content, **kwargs):
        super().__init__('thead', *content, **kwargs)

class Tbody(Element):
    """Table body element."""
    def __init__(self, *content, **kwargs):
        super().__init__('tbody', *content, **kwargs)

class Nav(Element):
    """Navigation element."""
    def __init__(self, *content, **kwargs):
        super().__init__('nav', *content, **kwargs)

class Header(Element):
    """Header element."""
    def __init__(self, *content, **kwargs):
        super().__init__('header', *content, **kwargs)

class Footer(Element):
    """Footer element."""
    def __init__(self, *content, **kwargs):
        super().__init__('footer', *content, **kwargs)

class Section(Element):
    """Section element."""
    def __init__(self, *content, **kwargs):
        super().__init__('section', *content, **kwargs)

class Article(Element):
    """Article element."""
    def __init__(self, *content, **kwargs):
        super().__init__('article', *content, **kwargs)

class Main(Element):
    """Main content element."""
    def __init__(self, *content, **kwargs):
        super().__init__('main', *content, **kwargs)

class Aside(Element):
    """Aside element for sidebar content."""
    def __init__(self, *content, **kwargs):
        super().__init__('aside', *content, **kwargs)

class Pre(Element):
    """Preformatted text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('pre', *content, **kwargs)

class Code(Element):
    """Inline code element."""
    def __init__(self, *content, **kwargs):
        super().__init__('code', *content, **kwargs)

class Br(Element):
    """Line break element."""
    def __init__(self, **kwargs):
        super().__init__('br', "", **kwargs)

class Strong(Element):
    """Strong importance (bold) element."""
    def __init__(self, *content, **kwargs):
        super().__init__('strong', *content, **kwargs)

class Em(Element):
    """Emphasized (italic) element."""
    def __init__(self, *content, **kwargs):
        super().__init__('em', *content, **kwargs)

class I(Element):
    """Italic text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('i', *content, **kwargs)

class B(Element):
    """Bold text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('b', *content, **kwargs)

class Small(Element):
    """Smaller text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('small', *content, **kwargs)

class Mark(Element):
    """Highlighted/marked text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('mark', *content, **kwargs)

class Del(Element):
    """Deleted text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('del', *content, **kwargs)

class Ins(Element):
    """Inserted text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('ins', *content, **kwargs)

class Sub(Element):
    """Subscript text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('sub', *content, **kwargs)

class Sup(Element):
    """Superscript text element."""
    def __init__(self, *content, **kwargs):
        super().__init__('sup', *content, **kwargs)

class Blockquote(Element):
    """Block quotation element."""
    def __init__(self, *content, **kwargs):
        super().__init__('blockquote', *content, **kwargs)

class Canvas(Element):
    """Canvas element for graphics."""
    def __init__(self, width=None, height=None, **kwargs):
        if width is not None:
            kwargs['width'] = width
        if height is not None:
            kwargs['height'] = height
        super().__init__('canvas', **kwargs)

class Svg(Element):
    """SVG graphics element."""
    def __init__(self, *content, **kwargs):
        super().__init__('svg', *content, **kwargs)

class Video(Element):
    """Video element."""
    def __init__(self, src=None, **kwargs):
        if src is not None:
            kwargs['src'] = src
        super().__init__('video', **kwargs)

class Audio(Element):
    """Audio element."""
    def __init__(self, src=None, **kwargs):
        if src is not None:
            kwargs['src'] = src
        super().__init__('audio', **kwargs)

class Iframe(Element):
    """Inline frame element."""
    def __init__(self, src=None, **kwargs):
        if src is not None:
            kwargs['src'] = src
        super().__init__('iframe', **kwargs)

class Details(Element):
    """Disclosure widget element."""
    def __init__(self, *content, **kwargs):
        super().__init__('details', *content, **kwargs)

class Summary(Element):
    """Summary for details element."""
    def __init__(self, *content, **kwargs):
        super().__init__('summary', *content, **kwargs)

class Progress(Element):
    """Progress bar element."""
    def __init__(self, value=None, max_value=None, **kwargs):
        if value is not None:
            kwargs['value'] = value
        if max_value is not None:
            kwargs['max'] = max_value
        super().__init__('progress', **kwargs)

class Meter(Element):
    """Scalar measurement element."""
    def __init__(self, value=None, min_value=None, max_value=None, **kwargs):
        if value is not None:
            kwargs['value'] = value
        if min_value is not None:
            kwargs['min'] = min_value
        if max_value is not None:
            kwargs['max'] = max_value
        super().__init__('meter', **kwargs)

class Fieldset(Element):
    """Fieldset element for grouping form controls."""
    def __init__(self, *content, **kwargs):
        super().__init__('fieldset', *content, **kwargs)

class Legend(Element):
    """Legend element for fieldset caption."""
    def __init__(self, *content, **kwargs):
        super().__init__('legend', *content, **kwargs)

class Dl(Element):
    """Description list element."""
    def __init__(self, *content, **kwargs):
        super().__init__('dl', *content, **kwargs)

class Dt(Element):
    """Description term element."""
    def __init__(self, *content, **kwargs):
        super().__init__('dt', *content, **kwargs)

class Dd(Element):
    """Description details element."""
    def __init__(self, *content, **kwargs):
        super().__init__('dd', *content, **kwargs)

class Figure(Element):
    """Figure element for content with caption."""
    def __init__(self, *content, **kwargs):
        super().__init__('figure', *content, **kwargs)

class Figcaption(Element):
    """Figure caption element."""
    def __init__(self, *content, **kwargs):
        super().__init__('figcaption', *content, **kwargs)

class Time(Element):
    """Time element."""
    def __init__(self, *content, datetime=None, **kwargs):
        if datetime is not None:
            kwargs['datetime'] = datetime
        super().__init__('time', *content, **kwargs)

class Abbr(Element):
    """Abbreviation element."""
    def __init__(self, *content, title=None, **kwargs):
        if title is not None:
            kwargs['title'] = title
        super().__init__('abbr', *content, **kwargs)

class Kbd(Element):
    """Keyboard input element."""
    def __init__(self, *content, **kwargs):
        super().__init__('kbd', *content, **kwargs)

class Samp(Element):
    """Sample output element."""
    def __init__(self, *content, **kwargs):
        super().__init__('samp', *content, **kwargs)

class Var(Element):
    """Variable element."""
    def __init__(self, *content, **kwargs):
        super().__init__('var', *content, **kwargs)

class Q(Element):
    """Inline quotation element."""
    def __init__(self, *content, **kwargs):
        super().__init__('q', *content, **kwargs)

class Cite(Element):
    """Citation element."""
    def __init__(self, *content, **kwargs):
        super().__init__('cite', *content, **kwargs)