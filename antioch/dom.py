import js
from typing import Union, Optional
from .elements import Element


class DOMHelper:
    """Helper class for DOM manipulation operations."""

    def __init__(self):
        self._document = js.document
    
    def add(self, *items, target: Optional[Union[Element, str]] = None) -> 'DOMHelper':
        """
        Add one or more elements to the DOM.

        Args:
            *items: Elements to add (Element instances, Macro objects, or strings)
            target: Target container (Element, CSS selector string, or None for document.body)

        Returns:
            Self for method chaining
        """
        # Handle target parameter
        if target is None:
            # Default to document body
            target_node = self._document.body
        elif isinstance(target, Element):
            # Use the Element's DOM node
            target_node = target._dom_element
        elif isinstance(target, str):
            # CSS selector
            target_node = self._document.querySelector(target)
            if not target_node:
                raise ValueError(f"No element found with selector: {target}")
        else:
            # Assume it's already a DOM node
            target_node = target

        # Add each item (same logic as Element.add())
        for item in items:
            if isinstance(item, Element):
                target_node.appendChild(item._dom_element)
            elif hasattr(item, 'element') and hasattr(item.element, '_dom_element'):
                # Handle Macro objects - use their root element
                target_node.appendChild(item.element._dom_element)
            elif isinstance(item, str):
                text_node = self._document.createTextNode(item)
                target_node.appendChild(text_node)
            elif hasattr(item, '__iter__') and not isinstance(item, str):
                self.add(*item, target=target)
            else:
                text_node = self._document.createTextNode(str(item))
                target_node.appendChild(text_node)

        return self
    
    def remove(self, element: Union[Element, str]) -> bool:
        """
        Remove an element from the DOM.
        
        Args:
            element: Element to remove (Element instance or CSS selector)
        
        Returns:
            True if element was removed, False if not found
        """
        if isinstance(element, Element):
            return element.remove() is not None
        elif isinstance(element, str):
            # CSS selector
            dom_element = self._document.querySelector(element)
            if dom_element and dom_element.parentNode:
                dom_element.parentNode.removeChild(dom_element)
                return True
            return False
        else:
            raise TypeError("element must be an Element instance or CSS selector string")
    
    def find(self, selector: str) -> Optional[Element]:
        """
        Find an element by CSS selector and wrap it in an Element.
        
        Args:
            selector: CSS selector string
        
        Returns:
            Element wrapper or None if not found
        """
        dom_element = self._document.querySelector(selector)
        if dom_element:
            # Create a wrapper Element
            from .elements import Element
            wrapper = Element.__new__(Element)
            wrapper._dom_element = dom_element
            wrapper._style = Element._create_style_proxy(wrapper)
            return wrapper
        return None
    
    def find_all(self, selector: str) -> list[Element]:
        """
        Find all elements by CSS selector and wrap them in Elements.
        
        Args:
            selector: CSS selector string
        
        Returns:
            List of Element wrappers
        """
        dom_elements = self._document.querySelectorAll(selector)
        result = []
        
        for dom_element in dom_elements:
            # Create a wrapper Element
            from .elements import Element
            wrapper = Element.__new__(Element)
            wrapper._dom_element = dom_element
            wrapper._style = Element._create_style_proxy(wrapper)
            result.append(wrapper)
        
        return result
    
    def clear(self, target: Optional[Union[Element, str]] = None) -> None:
        """
        Clear all children from a target element.
        
        Args:
            target: Target element (Element, CSS selector, or None for document.body)
        """
        if target is None:
            target_node = self._document.body
        elif isinstance(target, Element):
            target_node = target._dom_element
        elif isinstance(target, str):
            target_node = self._document.querySelector(target)
            if not target_node:
                raise ValueError(f"No element found with selector: {target}")
        else:
            target_node = target
        
        target_node.innerHTML = ""

    @property
    def body(self) -> Element:
        """Get document.body as an Element wrapper."""
        if not hasattr(self, '_body_wrapper'):
            from .elements import Element
            self._body_wrapper = Element.__new__(Element)
            self._body_wrapper._dom_element = self._document.body
            self._body_wrapper._style = Element._create_style_proxy(self._body_wrapper)
        return self._body_wrapper
    
    @property
    def head(self) -> Element:
        """Get document.head as an Element wrapper."""
        if not hasattr(self, '_head_wrapper'):
            from .elements import Element
            self._head_wrapper = Element.__new__(Element)
            self._head_wrapper._dom_element = self._document.head
            self._head_wrapper._style = Element._create_style_proxy(self._head_wrapper)
        return self._head_wrapper


# Create a global DOM instance
DOM = DOMHelper()