# Unified Event System

Antioch provides a unified event system that works consistently across elements, macros, and global application events. The system supports both decorator-based and traditional callback subscriptions.

## Overview

The unified event system consists of:

- **`Event`** - First-class event objects that can be subscribed to and fired
- **`@when` decorator** - Declarative event subscription
- **`EventGroup`** - Subscribe to multiple events with one handler
- **`DOM` events** - Application-wide events accessible via the DOM object

## Quick Start

```python
from antioch import *
from antioch.macros import Modal

# Create a modal (events are auto-created)
modal = Modal(title="Hello")

# Subscribe using @when decorator
@when(modal.open_event)
def on_open(sender):
    print(f"Modal {sender.id} opened!")

@when(modal.close_event)
def on_close(sender):
    print("Modal closed!")

# Open the modal (fires the event)
modal.open()  # This is the method, fires modal.open_event
```

## Event Class

The `Event` class represents a single event that can be subscribed to and fired.

### Creating Events

In macros, use `_create_event()`:

```python
class MyMacro(Macro):
    def __init__(self):
        super().__init__()

        # Create event objects
        self.click = self._create_event('click')
        self.change = self._create_event('change')
        self.custom_event = self._create_event('custom_event')
```

### Event Methods

```python
# Subscribe to event
event.subscribe(handler)

# Unsubscribe from event
event.unsubscribe(handler)

# Fire the event
event.fire(*args, **kwargs)

# Clear all subscribers
event.clear()

# Get subscriber count
count = event.subscriber_count
```

### Event Signature

All event handlers receive the event owner as the first parameter:

```python
@when(modal.close_event)
def handle_close(sender, *args, **kwargs):
    # sender is the modal instance
    # args are event-specific arguments
    print(f"Closed: {sender.id}")
```

## @when Decorator

The `@when` decorator provides declarative event subscription:

```python
from antioch import when

@when(modal.open)
def on_modal_open(sender):
    print("Modal opened!")
```

This is equivalent to:

```python
def on_modal_open(sender):
    print("Modal opened!")

modal.open.subscribe(on_modal_open)
```

### Multiple Handlers

You can attach multiple handlers to the same event:

```python
@when(modal.open)
def log_open(sender):
    print("Logging open event")

@when(modal.open)
def track_open(sender):
    print("Tracking analytics")

# Both handlers will be called when modal opens
```

## EventGroup

Subscribe one handler to multiple events:

```python
from antioch import EventGroup

# Create group of related events
modal_events = EventGroup([
    modal.open,
    modal.close_event,
    modal.confirm,
    modal.cancel
])

# Subscribe to all at once
@modal_events
def log_any_modal_event(sender, *args):
    print(f"Modal event: {args}")

# Or programmatically
modal_events.subscribe_all(my_handler)
```

## Global Events via DOM

Use `DOM` for application-wide events:

```python
from antioch import DOM, when

# Subscribe to global events
@when(DOM.app_ready)
def on_app_ready(sender, *args):
    print("Application is ready!")

@when(DOM.app_error)
def on_app_error(sender, error_msg):
    print(f"Error: {error_msg}")

# Fire global events
DOM.app_ready.fire()
DOM.app_error.fire("Something went wrong")

# Define custom global events
DOM.user_login = Event('user_login', owner=DOM)
DOM.user_logout = Event('user_logout', owner=DOM)
```

Built-in DOM events:
- `DOM.app_ready` - Application ready event
- `DOM.app_error` - Application error event
- `DOM.page_load` - Page load event
- `DOM.page_unload` - Page unload event

## Macro Integration

Macros can expose events as properties for use with `@when`:

### Creating Events in Macros

```python
class MyMacro(Macro):
    def __init__(self):
        super().__init__(macro_type="mymacro")

        # Create unified Event objects with _event suffix
        self.click_event = self._create_event('click')
        self.change_event = self._create_event('change')
        self.submit_event = self._create_event('submit')

        self._init_macro()

    def _some_method(self):
        # Fire events using _fire_event()
        self._fire_event('click', click_data)

        # Or fire the Event directly
        self.click_event.fire(click_data)
```

### Backwards Compatibility

The unified event system is fully compatible with the existing callback system:

```python
# Old style - still works
modal.on('open', lambda sender: print("opened"))
modal.on_open(lambda sender: print("opened"))

# New style - also works
@when(modal.open_event)
def handle_open(sender):
    print("opened")

# Both will be called!
```

When `_fire_event()` is called, it:
1. Fires the `Event` object (calling `@when` handlers)
2. The Event automatically triggers old-style callbacks for backwards compatibility

## Element Events

While elements don't currently expose Event objects, you can create custom events:

```python
button = Button("Click me")

# Create a custom event with _event suffix
button.clicked_event = Event('clicked', owner=button)

# Subscribe with @when
@when(button.clicked_event)
def on_button_click(sender):
    print("Button clicked!")

# Wire to actual DOM event
button.on_click(lambda e: button.clicked_event.fire())
```

## Best Practices

### 1. Name Events as Properties

Make events accessible as properties for clean decorator usage. **Use `_event` suffix to avoid method name collisions:**

```python
# Good - use _event suffix
class Modal(Macro):
    def __init__(self):
        # Avoid collisions with open() and close() methods
        self.open_event = self._create_event('open')
        self.close_event = self._create_event('close')

@when(modal.open_event)
def handle_open(sender):
    pass

# Bad - conflicts with modal.open() method
class Modal(Macro):
    def __init__(self):
        self.open = self._create_event('open')  # Overwrites open() method!

# Less clean (but still works)
@when(modal._get_event('open'))
def handle_open(sender):
    pass
```

### 2. Use Descriptive Event Names

```python
# Good
self.item_added = self._create_event('item_added')
self.validation_failed = self._create_event('validation_failed')

# Less clear
self.e1 = self._create_event('e1')
self.event = self._create_event('event')
```

### 3. Document Event Arguments

Document what arguments each event passes to handlers:

```python
class DataTable(Macro):
    def __init__(self):
        # Event fired when cell changes
        # Args: (row_idx, col_idx, new_value, old_value)
        self.cell_change = self._create_event('cell_change')

        # Event fired when row is clicked
        # Args: (row_data,)
        self.row_click = self._create_event('row_click')
```

### 4. Fire Events with _fire_event()

Use `_fire_event()` instead of `_trigger_callbacks()` to support both systems:

```python
# Good - fires Event + old callbacks
self._fire_event('close', close_reason)

# Works but misses Event subscribers
self._trigger_callbacks('close', close_reason)
```

## Migration Guide

### Updating Existing Macros

To add unified event support to existing macros:

1. Create Event properties in `__init__`:

```python
class MyMacro(Macro):
    def __init__(self):
        super().__init__()

        # Existing code
        self._add_callback_type('change')

        # Add event objects with _event suffix
        self.change_event = self._create_event('change')
```

2. Replace `_trigger_callbacks()` with `_fire_event()`:

```python
# Before
def _handle_change(self, new_value):
    self._trigger_callbacks('change', new_value)

# After
def _handle_change(self, new_value):
    self._fire_event('change', new_value)
```

3. Done! Old `.on()` code still works, plus new `@when` code works too.

## Examples

See these examples:
- `/scripts/examples/when_decorator_demo.py` - Simple @when usage
- `/scripts/examples/unified_events_demo.py` - Comprehensive event system demo

## API Reference

### Event

```python
class Event:
    def __init__(name: str, owner: Any = None)
    def subscribe(handler: Callable) -> Callable
    def unsubscribe(handler: Callable) -> None
    def fire(*args, **kwargs) -> None
    def clear() -> None

    @property
    def subscriber_count() -> int
```

### when

```python
def when(event: Event) -> Callable:
    """Decorator for subscribing to events."""
```

### EventGroup

```python
class EventGroup:
    def __init__(events: List[Event])
    def subscribe_all(handler: Callable) -> Callable
    def unsubscribe_all(handler: Callable) -> None
    def clear_all() -> None
```

### Macro Methods

```python
class Macro:
    def _create_event(event_name: str) -> Event
    def _get_event(event_name: str) -> Optional[Event]
    def _fire_event(event_name: str, *args, **kwargs) -> None
```
