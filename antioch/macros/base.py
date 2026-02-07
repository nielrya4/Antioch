"""
Base Macro class - Foundation for all Antioch macro components.
Provides common functionality for ID management, styling, callbacks, and element handling.
"""
import uuid
from typing import Dict, Any, List, Callable, Optional, Union
from ..elements import Div


class Macro:
    """
    Base class for all Antioch macro components.
    
    Provides common functionality:
    - Unique ID generation for safe multi-instance usage
    - Callback management system
    - Style merging and management  
    - Element lifecycle management
    - Event handling utilities
    
    To create a new macro, inherit from this class and implement:
    - _create_elements(): Build the UI structure
    - Any specific methods your macro needs
    """
    
    def __init__(self, macro_type: str = "macro", **kwargs):
        """
        Initialize base macro functionality.
        
        Args:
            macro_type: Type identifier for this macro (used in ID generation)
            **kwargs: Additional arguments (passed to subclasses)
        """
        # Generate unique ID for this instance
        self._id = f"{macro_type}_{str(uuid.uuid4())[:8]}"
        self._macro_type = macro_type
        
        # Callback management
        self._callbacks: Dict[str, List[Callable]] = {}
        
        # Element references
        self._elements: Dict[str, Any] = {}
        self._root_element: Optional[Any] = None
        
        # Style management
        self._default_styles = {}
        self._user_styles = {}
        
        # State management
        self._state = {}
        self._destroyed = False
        
        # Store constructor kwargs for subclass access
        self._kwargs = kwargs
    
    @property
    def id(self) -> str:
        """Get the unique ID for this macro instance."""
        return self._id
    
    @property
    def element(self) -> Any:
        """Get the root DOM element for adding to page."""
        if self._destroyed:
            raise RuntimeError(f"Macro {self._id} has been destroyed")
        return self._root_element
    
    @property
    def state(self) -> Dict[str, Any]:
        """Get the current state dictionary."""
        return self._state.copy()
    
    def _create_elements(self) -> Any:
        """
        Create the macro's UI elements. Must be implemented by subclasses.
        
        Returns:
            The root element of the macro
        """
        raise NotImplementedError("Subclasses must implement _create_elements()")
    
    def _init_macro(self):
        """
        Initialize the macro after construction. Called automatically.
        Subclasses can override for custom initialization logic.
        """
        self._root_element = self._create_elements()
        if not self._root_element:
            raise ValueError("_create_elements() must return a root element")
    
    def _merge_styles(self, default_styles: Dict[str, Any], 
                      user_styles: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Merge default styles with user-provided styles.
        
        Args:
            default_styles: Default styling dictionary
            user_styles: User override styles
            
        Returns:
            Merged styles dictionary
        """
        merged = default_styles.copy()
        if user_styles:
            merged.update(user_styles)
        return merged
    
    def _create_element_with_styles(self, element_class, content=None, 
                                   default_styles=None, user_styles=None, **kwargs):
        """
        Helper to create an element with merged styles.
        
        Args:
            element_class: Element class to instantiate
            content: Element content
            default_styles: Default styles for this element
            user_styles: User style overrides
            **kwargs: Additional element attributes
            
        Returns:
            Styled element instance
        """
        styles = self._merge_styles(default_styles or {}, user_styles)
        return element_class(content, style=styles, **kwargs)
    
    def _register_element(self, name: str, element: Any) -> Any:
        """
        Register an element for later reference.
        
        Args:
            name: Name to register the element under
            element: Element to register
            
        Returns:
            The registered element (for chaining)
        """
        self._elements[name] = element
        return element
    
    def _get_element(self, name: str) -> Any:
        """
        Get a registered element by name.
        
        Args:
            name: Name of the registered element
            
        Returns:
            The registered element
            
        Raises:
            KeyError: If element name not found
        """
        if name not in self._elements:
            raise KeyError(f"Element '{name}' not registered in macro {self._id}")
        return self._elements[name]
    
    def _set_state(self, **kwargs) -> 'Macro':
        """
        Update state values and trigger state change callbacks.
        
        Args:
            **kwargs: State key-value pairs to update
            
        Returns:
            Self for method chaining
        """
        old_state = self._state.copy()
        self._state.update(kwargs)
        
        # Trigger state change callbacks
        self._trigger_callbacks('state_change', old_state, self._state)
        return self
    
    def _get_state(self, key: str, default: Any = None) -> Any:
        """
        Get a state value.
        
        Args:
            key: State key to retrieve
            default: Default value if key not found
            
        Returns:
            State value or default
        """
        return self._state.get(key, default)
    
    def _add_callback_type(self, event_type: str):
        """
        Add a new callback type for this macro.
        
        Args:
            event_type: Name of the event type (e.g., 'click', 'change')
        """
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
    
    def _trigger_callbacks(self, event_type: str, *args, **kwargs):
        """
        Trigger all callbacks for a specific event type.
        
        Args:
            event_type: Type of event to trigger
            *args: Arguments to pass to callbacks
            **kwargs: Keyword arguments to pass to callbacks
        """
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                try:
                    callback(self, *args, **kwargs)
                except Exception as e:
                    print(f"Macro {self._id} callback error ({event_type}): {e}")
    
    def on(self, event_type: str, callback: Callable) -> 'Macro':
        """
        Register a callback for an event type.
        
        Args:
            event_type: Type of event to listen for
            callback: Function to call when event occurs
            
        Returns:
            Self for method chaining
        """
        self._add_callback_type(event_type)
        self._callbacks[event_type].append(callback)
        return self
    
    def off(self, event_type: str, callback: Optional[Callable] = None) -> 'Macro':
        """
        Remove callbacks for an event type.
        
        Args:
            event_type: Event type to remove callbacks from
            callback: Specific callback to remove, or None to remove all
            
        Returns:
            Self for method chaining
        """
        if event_type in self._callbacks:
            if callback is None:
                # Remove all callbacks for this event type
                self._callbacks[event_type].clear()
            else:
                # Remove specific callback
                try:
                    self._callbacks[event_type].remove(callback)
                except ValueError:
                    pass  # Callback wasn't in the list
        return self
    
    def _create_container(self, container_styles: Optional[Dict[str, Any]] = None) -> Div:
        """
        Create a standard container div with default macro styling.
        
        Args:
            container_styles: Additional styles for the container
            
        Returns:
            Configured container div
        """
        default_container_styles = {
            "display": "inline-block",
            "position": "relative"
        }
        
        styles = self._merge_styles(default_container_styles, container_styles)
        container = Div(style=styles)
        container.set_attribute("data-macro-id", self._id)
        container.set_attribute("data-macro-type", self._macro_type)
        
        return container
    
    def show(self) -> 'Macro':
        """Show this macro (set display style)."""
        if self._root_element:
            self._root_element.style.display = "block"
        self._trigger_callbacks('show')
        return self
    
    def hide(self) -> 'Macro':
        """Hide this macro (set display to none)."""
        if self._root_element:
            self._root_element.style.display = "none"
        self._trigger_callbacks('hide')
        return self
    
    def toggle(self) -> 'Macro':
        """Toggle visibility of this macro."""
        if self._root_element:
            current = self._root_element.style.display or "block"
            if current == "none":
                self.show()
            else:
                self.hide()
        return self
    
    def set_style(self, styles: Dict[str, Any]) -> 'Macro':
        """
        Update the root element's styles.
        
        Args:
            styles: Style dictionary to apply
            
        Returns:
            Self for method chaining
        """
        if self._root_element:
            self._root_element.style.update(styles)
        return self
    
    def destroy(self):
        """
        Destroy this macro and clean up resources.
        Removes from DOM and clears all callbacks.
        """
        if self._destroyed:
            return
            
        # Trigger destroy callbacks
        self._trigger_callbacks('destroy')
        
        # Remove from DOM
        if self._root_element:
            self._root_element.remove()
        
        # Clear all callbacks
        self._callbacks.clear()
        
        # Clear element references
        self._elements.clear()
        self._root_element = None
        
        # Mark as destroyed
        self._destroyed = True
    
    def is_destroyed(self) -> bool:
        """Check if this macro has been destroyed."""
        return self._destroyed
    
    def __repr__(self) -> str:
        """String representation of this macro."""
        status = "destroyed" if self._destroyed else "active"
        return f"<{self.__class__.__name__}(id='{self._id}', status='{status}')>"


class SimpleMacro(Macro):
    """
    A simplified base class for basic macros that just need a container and content.
    Good starting point for simple macros.
    """
    
    def __init__(self, content=None, container_styles=None, **kwargs):
        """
        Initialize a simple macro with content.
        
        Args:
            content: Content to add to the macro
            container_styles: Styles for the container
            **kwargs: Additional arguments
        """
        super().__init__(**kwargs)
        self._content = content
        self._container_styles = container_styles or {}
        self._init_macro()
    
    def _create_elements(self):
        """Create a simple container with content."""
        container = self._create_container(self._container_styles)
        
        if self._content:
            if isinstance(self._content, str):
                from ..elements import P
                container.add(P(self._content))
            else:
                container.add(self._content)
        
        return self._register_element('container', container)
    
    def set_content(self, content) -> 'SimpleMacro':
        """Update the content of this simple macro."""
        container = self._get_element('container')
        container._dom_element.innerHTML = ""
        
        if content:
            if isinstance(content, str):
                from ..elements import P
                container.add(P(content))
            else:
                container.add(content)
        
        self._content = content
        self._trigger_callbacks('content_change', content)
        return self