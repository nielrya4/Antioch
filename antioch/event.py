"""
Unified event system for Antioch.

Provides a consistent event handling interface across elements, macros, and global events
with support for decorator-based subscriptions.

Usage:
    # Decorator syntax
    @when(modal.close)
    def handle_close(sender, args):
        print(f"Modal closed: {sender}")

    # Direct subscription
    modal.close.subscribe(handle_close)

    # Firing events
    modal.close.fire(some_data)
"""
from typing import Callable, Any, List, Optional
from pyodide.ffi import create_proxy


class Event:
    """
    Represents a single event that can be subscribed to and fired.

    Events can be attached to elements, macros, or used as standalone global events.
    They provide a consistent interface for event handling across Antioch.

    Attributes:
        name: Event name (e.g., 'click', 'close', 'change')
        owner: Object that owns this event (Element, Macro, or None for global)

    Example:
        # Create an event
        close_event = Event('close', owner=my_modal)

        # Subscribe using decorator
        @when(close_event)
        def handle_close(sender, args):
            print("Modal closed")

        # Subscribe directly
        close_event.subscribe(lambda sender, args: print("Closed"))

        # Fire the event
        close_event.fire(some_args)
    """

    def __init__(self, name: str, owner: Any = None):
        """
        Initialize an event.

        Args:
            name: Name of the event (e.g., 'click', 'change', 'close')
            owner: Object that owns this event (optional)
        """
        self.name = name
        self.owner = owner
        self._subscribers: List[Callable] = []
        self._proxies: List[Any] = []  # Store Pyodide proxies to prevent GC

    def subscribe(self, handler: Callable) -> Callable:
        """
        Subscribe a handler to this event.

        Args:
            handler: Callback function with signature (sender, *args, **kwargs)
                    where sender is the event owner

        Returns:
            The handler (for decorator usage)
        """
        if handler not in self._subscribers:
            self._subscribers.append(handler)
        return handler

    def unsubscribe(self, handler: Callable) -> None:
        """
        Unsubscribe a handler from this event.

        Args:
            handler: The handler to remove
        """
        if handler in self._subscribers:
            self._subscribers.remove(handler)

    def fire(self, *args, **kwargs) -> None:
        """
        Fire this event, calling all subscribed handlers.

        Args:
            *args: Positional arguments to pass to handlers
            **kwargs: Keyword arguments to pass to handlers
        """
        sender = self.owner
        for handler in self._subscribers[:]:  # Copy list to allow modifications during iteration
            try:
                handler(sender, *args, **kwargs)
            except Exception as e:
                # Log error but continue firing other handlers
                print(f"Error in event handler for '{self.name}': {e}")

    def __call__(self, handler: Callable) -> Callable:
        """
        Allow event to be used as a decorator.

        Example:
            @my_event
            def handle_event(sender, args):
                pass
        """
        return self.subscribe(handler)

    def clear(self) -> None:
        """Remove all subscribers."""
        self._subscribers.clear()
        self._proxies.clear()

    @property
    def subscriber_count(self) -> int:
        """Get the number of subscribers to this event."""
        return len(self._subscribers)

    def __or__(self, other):
        """
        Combine events using | operator for multi-event subscriptions.

        Example:
            @when(button1.events.click | button2.events.click)
            def handle_any_click(sender):
                print(f"{sender} clicked!")
        """
        if isinstance(other, EventGroup):
            # Combining Event with EventGroup
            return EventGroup([self] + list(other.events))
        elif isinstance(other, Event):
            # Combining two Events
            return EventGroup([self, other])
        else:
            raise TypeError(f"Cannot combine Event with {type(other).__name__}")

    def __repr__(self) -> str:
        owner_name = getattr(self.owner, '__class__', type(self.owner)).__name__ if self.owner else "Global"
        return f"Event('{self.name}', owner={owner_name}, subscribers={self.subscriber_count})"


def when(event) -> Callable:
    """
    Decorator for subscribing to events.

    Args:
        event: Event or EventGroup to subscribe to

    Returns:
        Decorator function

    Example:
        # Single event
        @when(modal.events.close)
        def handle_close(sender, args):
            print(f"Modal {sender} closed")

        # Multiple events with | operator
        @when(button1.events.click | button2.events.click)
        def handle_click(sender):
            print(f"{sender} clicked")

        # EventGroup
        @when(EventGroup([event1, event2, event3]))
        def handle_any(sender):
            print("Any event fired")
    """
    def decorator(func: Callable) -> Callable:
        if isinstance(event, EventGroup):
            event.subscribe_all(func)
        elif isinstance(event, Event):
            event.subscribe(func)
        else:
            raise TypeError(f"@when requires Event or EventGroup, got {type(event).__name__}")
        return func
    return decorator


class EventGroup:
    """
    Groups related events together for batch operations.

    Example:
        modal_events = EventGroup([modal.open, modal.close, modal.confirm])

        @modal_events.subscribe_all
        def log_modal_event(sender, *args):
            print(f"Modal event from {sender}: {args}")
    """

    def __init__(self, events: List[Event]):
        """
        Initialize event group.

        Args:
            events: List of Event objects to group
        """
        self.events = events

    def subscribe_all(self, handler: Callable) -> Callable:
        """
        Subscribe handler to all events in the group.

        Args:
            handler: Callback function

        Returns:
            The handler (for decorator usage)
        """
        for event in self.events:
            event.subscribe(handler)
        return handler

    def unsubscribe_all(self, handler: Callable) -> None:
        """
        Unsubscribe handler from all events in the group.

        Args:
            handler: The handler to remove
        """
        for event in self.events:
            event.unsubscribe(handler)

    def clear_all(self) -> None:
        """Clear all subscribers from all events in the group."""
        for event in self.events:
            event.clear()

    def __call__(self, handler: Callable) -> Callable:
        """Allow EventGroup to be used as a decorator."""
        return self.subscribe_all(handler)

    def __or__(self, other):
        """
        Combine EventGroup with another Event or EventGroup using | operator.

        Example:
            group = event1 | event2 | event3
        """
        if isinstance(other, EventGroup):
            return EventGroup(self.events + other.events)
        elif isinstance(other, Event):
            return EventGroup(self.events + [other])
        else:
            raise TypeError(f"Cannot combine EventGroup with {type(other).__name__}")
