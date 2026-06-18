# Events Namespace - Unified Event System

Antioch provides a clean, organized event system through the `.events` namespace. This eliminates naming collisions and makes event access intuitive and consistent across macros, elements, and DOM.

## Quick Start

```python
from antioch import *
from antioch.macros import Modal

# Create a modal
modal = Modal(title="Hello")

# Subscribe to events using @when decorator
@when(modal.events.open)
def on_open(sender):
    print("Modal opened!")

@when(modal.events.close)
def on_close(sender):
    print("Modal closed!")

# Call methods without collision
modal.open()  # Method - opens the modal
modal.events.open  # Event object - for subscriptions
```

## Why .events Namespace?

### Before (with naming collisions):
```python
# Bad - event overwrites method!
modal.open = modal._create_event('open')

@when(modal.open)  # Tries to use event
def on_open(sender):
    pass

modal.open()  # Error! open is now an Event, not a method
```

### After (with .events namespace):
```python
# Good - no collision!
modal._create_event('open')  # Creates modal.events.open

@when(modal.events.open)  # Event
def on_open(sender):
    pass

modal.open()  # Method - works perfectly!
```

## Accessing Events

### Attribute Access (Recommended)
```python
@when(modal.events.open)
@when(modal.events.close)
@when(DOM.events.app_ready)
```

### Dictionary Access
```python
@when(modal.events['open'])
@when(modal.events['close'])
@when(DOM.events['app_ready'])
```

### Direct Subscription
```python
modal.events.open.subscribe(my_handler)
modal.events.close.subscribe(lambda s: print("Closed"))
```

## Element Events

Elements can create custom events using `element.create_event()`:

```python
# Create a button with a unified click event
button = Button("Click me")
button.create_event('click')  # Auto-wires to DOM click event

# Subscribe with @when
@when(button.events.click)
def on_click(sender, dom_event):
    print(f"Button clicked! Event: {dom_event}")

# The button click now fires both the DOM event AND the unified event
```

### Auto-wiring to DOM Events

By default, `create_event()` automatically wires the unified event to the DOM event:

```python
input_field = Input("text")

# These auto-wire to DOM events
input_field.create_event('input')
input_field.create_event('change')
input_field.create_event('focus')
input_field.create_event('blur')

@when(input_field.events.input)
def on_input(sender, dom_event):
    value = dom_event.target.value
    print(f"Input value: {value}")

@when(input_field.events.change)
def on_change(sender, dom_event):
    print("Input changed!")
```

### Custom Non-DOM Events

For custom events not tied to DOM events, use `auto_wire=False`:

```python
div = Div()

# Custom events (not DOM events)
div.create_event('data_loaded', auto_wire=False)
div.create_event('threshold_reached', auto_wire=False)

@when(div.events.data_loaded)
def on_data_loaded(sender, data):
    print(f"Data loaded: {data}")

@when(div.events.threshold_reached)
def on_threshold(sender, value):
    print(f"Threshold reached: {value}")

# Fire custom events manually
div.events.data_loaded.fire(some_data)
div.events.threshold_reached.fire(100)
```

## DOM Global Events

Global application events are accessed via `DOM.events`:

```python
# Subscribe to global events
@when(DOM.events.app_ready)
def on_ready(sender):
    print("App is ready!")

@when(DOM.events.app_error)
def on_error(sender, error_msg):
    print(f"Error: {error_msg}")

# Fire global events
DOM.events.app_ready.fire()
DOM.events.app_error.fire("Something went wrong")

# Add custom global events
DOM.events.register('user_login')
DOM.events.register('user_logout')

@when(DOM.events.user_login)
def on_login(sender, user):
    print(f"User {user} logged in")

DOM.events.user_login.fire(current_user)
```

Built-in DOM events:
- `DOM.events.app_ready`
- `DOM.events.app_error`
- `DOM.events.page_load`
- `DOM.events.page_unload`

## Creating Events in Macros

```python
class MyMacro(Macro):
    def __init__(self):
        super().__init__(macro_type="mymacro")

        # Create events - they'll be accessible via self.events.{name}
        self._create_event('click')
        self._create_event('change')
        self._create_event('submit')
        self._create_event('cancel')

        self._init_macro()

    def _handle_click(self):
        # Fire events
        self._fire_event('click', click_data)

    def some_method(self):
        # Methods and events coexist peacefully
        self._fire_event('change', new_value)
```

### Usage:
```python
my_macro = MyMacro()

@when(my_macro.events.click)
def on_click(sender):
    print("Clicked!")

@when(my_macro.events.change)
def on_change(sender, value):
    print(f"Changed to {value}")

# Methods work fine
my_macro.some_method()
```

## EventRegistry API

The `.events` attribute is an `EventRegistry` instance with these methods:

```python
# Register new events
modal.events.register('custom_event')

# Get an event
event = modal.events.get('open')

# Fire an event
modal.events.fire('open', some_data)

# Check if event exists
if 'open' in modal.events:
    print("Event exists!")

# List all events
print(list(modal.events.keys()))
print(len(modal.events))  # Count

# Iterate over events
for name in modal.events:
    print(f"Event: {name}")

# Get event objects
for name, event in modal.events.items():
    print(f"{name}: {event.subscriber_count} subscribers")

# Clear subscribers
modal.events.clear('open')  # Clear one event
modal.events.clear()  # Clear all events
```

## Event Signature

All event handlers receive the sender (owner) as the first parameter:

```python
@when(modal.events.close)
def handle_close(sender, *args, **kwargs):
    # sender is the modal instance
    # args/kwargs are event-specific data
    print(f"Modal {sender.id} closed")
```

## EventGroup

Subscribe to multiple events with one handler:

```python
from antioch import EventGroup

# Group related events
modal_events = EventGroup([
    modal.events.open,
    modal.events.close,
    modal.events.confirm,
    modal.events.cancel
])

# Subscribe to all at once
@modal_events
def log_any_event(sender, *args):
    print(f"Modal event from {sender.id}")

# Or programmatically
modal_events.subscribe_all(my_handler)
```

## Backwards Compatibility

The `.events` namespace works seamlessly with existing callback methods:

```python
# Old style - still works
modal.on('open', lambda s: print("Opened"))
modal.on_open(lambda s: print("Opened"))

# New style - also works
@when(modal.events.open)
def on_open(sender):
    print("Opened")

# All three handlers will be called!
modal.open()  # Fires event, triggers all handlers
```

## Best Practices

### 1. Always Use .events Namespace

```python
# Good
@when(modal.events.open)
@when(DOM.events.app_ready)

# Avoid
@when(some_event_stored_elsewhere)
```

### 2. Create Events in __init__

```python
class MyMacro(Macro):
    def __init__(self):
        super().__init__()

        # Create all events upfront
        self._create_event('start')
        self._create_event('stop')
        self._create_event('update')

        self._init_macro()
```

### 3. Document Event Arguments

```python
class DataTable(Macro):
    def __init__(self):
        super().__init__()

        # Event: cell_change(row_idx, col_idx, new_value, old_value)
        self._create_event('cell_change')

        # Event: row_click(row_data)
        self._create_event('row_click')
```

### 4. Fire Events with _fire_event()

```python
# Good - fires both Event subscribers and old callbacks
self._fire_event('change', new_value)

# Avoid - only fires old callbacks, misses Event subscribers
self._trigger_callbacks('change', new_value)
```

## Migration Guide

### Updating Existing Code

If you have code using the old `_event` suffix pattern:

```python
# Old way
modal.open_event = modal._create_event('open')
@when(modal.open_event)

# New way
modal._create_event('open')
@when(modal.events.open)
```

### Updating Existing Macros

```python
# Before
class MyMacro(Macro):
    def __init__(self):
        super().__init__()
        self.click_event = self._create_event('click')

# After
class MyMacro(Macro):
    def __init__(self):
        super().__init__()
        self._create_event('click')  # Now accessible as self.events.click
```

## Examples

See these example files:
- `/scripts/examples/events_namespace_demo.py` - Complete demo of .events namespace
- `/scripts/examples/element_events_demo.py` - Element and DOM events
- `/scripts/examples/when_decorator_demo.py` - @when decorator patterns

## API Reference

### EventRegistry

```python
class EventRegistry:
    def register(event_name: str) -> Event
    def get(event_name: str) -> Optional[Event]
    def fire(event_name: str, *args, **kwargs) -> None
    def clear(event_name: Optional[str] = None) -> None

    def __getattr__(name: str) -> Event  # modal.events.open
    def __getitem__(name: str) -> Event  # modal.events['open']
    def __contains__(name: str) -> bool  # 'open' in modal.events
    def __len__() -> int
    def __iter__()

    def keys()  # All event names
    def values()  # All Event objects
    def items()  # (name, Event) pairs
```

### Element Methods

```python
class Element:
    events: EventRegistry

    def create_event(event_name: str, auto_wire: bool = True) -> Event
        """Create unified event, optionally auto-wired to DOM event"""

    # Existing methods still work:
    def on(event: str, handler) -> Element
    def on_click(handler) -> Element
    def on_change(handler) -> Element
    # ... etc
```

### Macro Methods

```python
class Macro:
    events: EventRegistry

    def _create_event(event_name: str) -> Event
    def _get_event(event_name: str) -> Optional[Event]
    def _fire_event(event_name: str, *args, **kwargs) -> None
```

### DOMHelper

```python
class DOMHelper:
    events: EventRegistry  # Global events

    # Built-in events:
    # - app_ready
    # - app_error
    # - page_load
    # - page_unload
```
