"""
Event management for document-level event listeners with automatic proxy cleanup.

Provides a global EventManager singleton for managing document-level event listeners
with automatic Pyodide proxy creation, tracking, and cleanup.
"""
import js
from typing import Callable, Dict, List, Any, Optional, Set
from pyodide.ffi import create_proxy


class EventManager:
    """
    Manages document-level event listeners with automatic proxy management.

    This singleton class handles:
    - Automatic proxy creation and storage (prevents GC)
    - Multiple subscribers to the same event type
    - Owner-based cleanup (remove all listeners for a macro instance)
    - Automatic cleanup on page unload

    Example:
        from antioch.events import Events

        # Add a listener
        Events.add_listener('keydown', self._handle_keydown, owner=self)

        # Remove all listeners for this owner
        Events.remove_all_for_owner(self)
    """

    def __init__(self):
        """Initialize the event manager."""
        # Structure: {event_type: [(handler, proxy, owner), ...]}
        self._listeners: Dict[str, List[tuple[Callable, Any, Any]]] = {}

        # Track which event types have active document listeners
        self._active_event_types: Set[str] = set()

    def add_listener(self, event_type: str, handler: Callable, owner: Any = None) -> None:
        """
        Add a document-level event listener with automatic proxy management.

        Args:
            event_type: DOM event type (e.g., 'click', 'keydown', 'mousemove')
            handler: Python function to call when event fires
            owner: Optional owner object (usually a macro instance) for cleanup tracking

        Example:
            Events.add_listener('keydown', self._handle_escape, owner=self)
        """
        # Create proxy for the handler
        proxy = create_proxy(handler)

        # Initialize event type list if needed
        if event_type not in self._listeners:
            self._listeners[event_type] = []

        # Store the handler, proxy, and owner
        self._listeners[event_type].append((handler, proxy, owner))

        # Add document listener if this is the first handler for this event type
        if event_type not in self._active_event_types:
            js.document.addEventListener(event_type, self._create_dispatcher(event_type))
            self._active_event_types.add(event_type)

    def remove_listener(self, event_type: str, handler: Callable) -> bool:
        """
        Remove a specific event listener.

        Args:
            event_type: DOM event type
            handler: The handler function to remove

        Returns:
            True if the listener was found and removed, False otherwise
        """
        if event_type not in self._listeners:
            return False

        # Find and remove the handler
        listeners = self._listeners[event_type]
        for i, (h, proxy, owner) in enumerate(listeners):
            if h is handler:
                # Destroy the proxy
                try:
                    proxy.destroy()
                except:
                    pass

                # Remove from list
                listeners.pop(i)

                # If no more listeners for this event type, remove document listener
                if not listeners:
                    self._cleanup_event_type(event_type)

                return True

        return False

    def remove_all_for_owner(self, owner: Any) -> int:
        """
        Remove all event listeners associated with a specific owner.

        This is useful for cleanup when a macro is destroyed.

        Args:
            owner: The owner object whose listeners should be removed

        Returns:
            Number of listeners removed
        """
        if owner is None:
            return 0

        removed_count = 0

        # Iterate through all event types
        for event_type in list(self._listeners.keys()):
            listeners = self._listeners[event_type]
            remaining_listeners = []

            # Filter out listeners for this owner
            for h, proxy, o in listeners:
                if o is owner:
                    # Destroy the proxy
                    try:
                        proxy.destroy()
                    except:
                        pass
                    removed_count += 1
                else:
                    remaining_listeners.append((h, proxy, o))

            # Update the listeners list
            self._listeners[event_type] = remaining_listeners

            # If no more listeners for this event type, cleanup
            if not remaining_listeners:
                self._cleanup_event_type(event_type)

        return removed_count

    def _create_dispatcher(self, event_type: str) -> Any:
        """
        Create a dispatcher function that calls all registered handlers for an event type.

        Args:
            event_type: The event type to dispatch

        Returns:
            A Pyodide proxy that dispatches to all handlers
        """
        def dispatcher(event):
            """Dispatch event to all registered handlers."""
            if event_type in self._listeners:
                # Call each handler (iterate over a copy in case handlers modify the list)
                for handler, proxy, owner in list(self._listeners[event_type]):
                    try:
                        handler(event)
                    except Exception as e:
                        print(f"Error in event handler for {event_type}: {e}")

        # Create and store proxy for the dispatcher
        proxy = create_proxy(dispatcher)
        return proxy

    def _cleanup_event_type(self, event_type: str) -> None:
        """
        Remove document listener and cleanup for an event type with no more handlers.

        Args:
            event_type: The event type to cleanup
        """
        # Remove from active event types
        if event_type in self._active_event_types:
            self._active_event_types.remove(event_type)

        # Clean up the listeners list
        if event_type in self._listeners:
            del self._listeners[event_type]

    def clear_all(self) -> None:
        """
        Remove all event listeners and clean up all proxies.

        WARNING: This will remove all event listeners managed by this EventManager.
        Use with caution.
        """
        # Destroy all proxies
        for event_type in list(self._listeners.keys()):
            for handler, proxy, owner in self._listeners[event_type]:
                try:
                    proxy.destroy()
                except:
                    pass

        # Clear all tracking
        self._listeners.clear()
        self._active_event_types.clear()

    def get_listener_count(self, event_type: Optional[str] = None) -> int:
        """
        Get the number of registered listeners.

        Args:
            event_type: Optional event type to count. If None, returns total count.

        Returns:
            Number of registered listeners
        """
        if event_type is not None:
            return len(self._listeners.get(event_type, []))
        else:
            return sum(len(listeners) for listeners in self._listeners.values())

    def __repr__(self) -> str:
        """String representation showing active event types and listener counts."""
        if not self._listeners:
            return "<EventManager: no active listeners>"

        parts = []
        for event_type, listeners in self._listeners.items():
            parts.append(f"{event_type}({len(listeners)})")

        return f"<EventManager: {', '.join(parts)}>"


# Create a global EventManager instance
Events = EventManager()