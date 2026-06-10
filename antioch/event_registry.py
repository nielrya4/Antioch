"""
Event Registry - Namespace for accessing events on objects.

Provides a clean way to access events via object.events.event_name
without naming collisions with methods or properties.
"""
from typing import Any, Optional, Dict
from .event import Event


class EventRegistry:
    """
    Registry for events on an object (Macro, Element, or DOM).

    Provides attribute and dictionary access to events:
        modal.events.open
        modal.events['open']

    Example:
        # In Macro.__init__:
        self.events = EventRegistry(owner=self)
        self.events.register('open')
        self.events.register('close')

        # Usage:
        @when(modal.events.open)
        def on_open(sender):
            print("Opened!")

        # Or dictionary style:
        @when(modal.events['open'])
        def on_open(sender):
            print("Opened!")
    """

    def __init__(self, owner: Any):
        """
        Initialize event registry.

        Args:
            owner: Object that owns these events (Macro, Element, or DOM instance)
        """
        self._owner = owner
        self._events: Dict[str, Event] = {}

    def register(self, event_name: str) -> Event:
        """
        Register a new event.

        Args:
            event_name: Name of the event to register

        Returns:
            The Event object
        """
        if event_name not in self._events:
            self._events[event_name] = Event(event_name, owner=self._owner)
        return self._events[event_name]

    def get(self, event_name: str) -> Optional[Event]:
        """
        Get an event by name.

        Args:
            event_name: Name of the event

        Returns:
            Event object or None if not found
        """
        return self._events.get(event_name)

    def fire(self, event_name: str, *args, **kwargs) -> None:
        """
        Fire an event by name.

        Args:
            event_name: Name of the event to fire
            *args: Arguments to pass to handlers
            **kwargs: Keyword arguments to pass to handlers
        """
        if event_name in self._events:
            self._events[event_name].fire(*args, **kwargs)

    def clear(self, event_name: Optional[str] = None) -> None:
        """
        Clear subscribers from events.

        Args:
            event_name: Specific event to clear, or None to clear all
        """
        if event_name:
            if event_name in self._events:
                self._events[event_name].clear()
        else:
            for event in self._events.values():
                event.clear()

    def __getattr__(self, name: str) -> Event:
        """
        Get event by attribute access: modal.events.open

        Args:
            name: Event name

        Returns:
            Event object

        Raises:
            AttributeError: If event not found
        """
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

        if name in self._events:
            return self._events[name]

        raise AttributeError(
            f"Event '{name}' not registered. "
            f"Available events: {list(self._events.keys())}"
        )

    def __getitem__(self, name: str) -> Event:
        """
        Get event by dictionary access: modal.events['open']

        Args:
            name: Event name

        Returns:
            Event object

        Raises:
            KeyError: If event not found
        """
        if name not in self._events:
            raise KeyError(
                f"Event '{name}' not registered. "
                f"Available events: {list(self._events.keys())}"
            )
        return self._events[name]

    def __contains__(self, name: str) -> bool:
        """Check if event is registered."""
        return name in self._events

    def __len__(self) -> int:
        """Get number of registered events."""
        return len(self._events)

    def __iter__(self):
        """Iterate over event names."""
        return iter(self._events)

    def keys(self):
        """Get all event names."""
        return self._events.keys()

    def values(self):
        """Get all Event objects."""
        return self._events.values()

    def items(self):
        """Get all (name, Event) pairs."""
        return self._events.items()

    def __repr__(self) -> str:
        owner_name = getattr(self._owner, '__class__', type(self._owner)).__name__
        event_names = list(self._events.keys())
        return f"EventRegistry(owner={owner_name}, events={event_names})"
