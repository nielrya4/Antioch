"""
Dropdown macro - A reusable dropdown menu component.
Uses unique IDs and safe event handling for multiple instances.
"""
import js
from pyodide.ffi import create_proxy
from .base import Macro
from ..elements import Div, Button, Span


class DropdownItem:
    """Represents a single dropdown item."""
    
    def __init__(self, text, value=None, disabled=False, separator=False, item_id=None):
        """
        Initialize a dropdown item.
        
        Args:
            text: Display text for the item
            value: Value associated with the item (defaults to text)
            disabled: Whether the item is disabled
            separator: Whether this item is a visual separator
            item_id: Unique identifier (generated if not provided)
        """
        import uuid
        self.text = text
        self.value = value if value is not None else text
        self.disabled = disabled
        self.separator = separator
        self.item_id = item_id or str(uuid.uuid4())[:8]
        self.element = None


class Dropdown(Macro):
    """
    A dropdown menu component with customizable items and styling.
    Perfect for navigation menus, action lists, and option selections.
    """
    
    def __init__(self, items=None, placeholder="Select an option", 
                 selected_value=None, searchable=False, multi_select=False,
                 max_height="200px", button_style=None, menu_style=None, 
                 item_style=None, **kwargs):
        """
        Initialize a dropdown component.
        
        Args:
            items: List of DropdownItem objects, dicts, or strings
            placeholder: Placeholder text when nothing is selected
            selected_value: Initially selected value
            searchable: Whether dropdown is searchable
            multi_select: Whether multiple items can be selected
            max_height: Maximum height of dropdown menu
            button_style: Custom styles for dropdown button
            menu_style: Custom styles for dropdown menu
            item_style: Custom styles for dropdown items
        """
        # Initialize base macro
        super().__init__(macro_type="dropdown", **kwargs)
        
        # Process initial items
        processed_items = []
        if items:
            for item_data in items:
                if isinstance(item_data, DropdownItem):
                    processed_items.append(item_data)
                elif isinstance(item_data, dict):
                    processed_items.append(DropdownItem(**item_data))
                else:
                    # Assume it's a text string
                    processed_items.append(DropdownItem(str(item_data)))
        
        # Set up state
        self._set_state(
            items=processed_items,
            placeholder=placeholder,
            selected_value=selected_value,
            selected_values=[] if multi_select else None,
            searchable=searchable,
            multi_select=multi_select,
            max_height=max_height,
            is_open=False,
            search_text=""
        )

        # Store references to event handlers for cleanup
        self._click_outside_handler = None
        self._escape_handler = None
        
        # Add callback types
        self._add_callback_type('select')
        self._add_callback_type('deselect')
        self._add_callback_type('change')
        self._add_callback_type('open')
        self._add_callback_type('close')
        
        # Default styles
        default_button_style = {
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "padding": "10px 15px",
            "border": "1px solid #ddd",
            "border_radius": "4px",
            "background_color": "#fff",
            "cursor": "pointer",
            "font_size": "14px",
            "min_width": "200px",
            "transition": "border-color 0.2s ease"
        }
        
        default_menu_style = {
            "position": "absolute",
            "top": "100%",
            "left": "0",
            "right": "0",
            "background_color": "#fff",
            "border": "1px solid #ddd",
            "border_top": "none",
            "border_radius": "0 0 4px 4px",
            "box_shadow": "0 2px 8px rgba(0,0,0,0.1)",
            "z_index": "1000",
            "max_height": max_height,
            "overflow_y": "auto",
            "display": "none"
        }
        
        default_item_style = {
            "padding": "10px 15px",
            "cursor": "pointer",
            "font_size": "14px",
            "border_bottom": "1px solid #f0f0f0",
            "transition": "background-color 0.2s ease"
        }
        
        # Merge with user styles
        self._button_style = self._merge_styles(default_button_style, button_style)
        self._menu_style = self._merge_styles(default_menu_style, menu_style)
        self._item_style = self._merge_styles(default_item_style, item_style)
        
        # Initialize macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the dropdown UI elements."""
        # Main container (relative positioning for dropdown)
        container = self._register_element('container', self._create_container({
            "position": "relative",
            "display": "inline-block"
        }))
        
        # Dropdown button
        dropdown_btn = self._register_element('dropdown_btn', 
                                              Button(style=self._button_style))
        
        # Button content
        button_content = self._register_element('button_content', 
                                               Span(self._get_display_text()))
        
        # Dropdown arrow
        arrow = self._register_element('arrow', Span("▼", style={
            "font_size": "12px",
            "color": "#666",
            "transition": "transform 0.2s ease"
        }))
        
        dropdown_btn.add(button_content, arrow)
        
        # Button events
        dropdown_btn.on_click(lambda e: self._toggle_dropdown())
        dropdown_btn.on_mouseenter(lambda e: self._set_button_hover(True))
        dropdown_btn.on_mouseleave(lambda e: self._set_button_hover(False))
        
        # Dropdown menu
        menu = self._register_element('menu', Div(style=self._menu_style))
        
        # Create menu items
        self._create_menu_items(menu)
        
        container.add(dropdown_btn, menu)
        
        # Add Esc key support and blur event for closing dropdown
        container.set_attribute("tabindex", "0")  # Make container focusable
        keydown_handler = create_proxy(lambda e: self._handle_keydown(e))
        container.on_keydown(keydown_handler)
        
        # Add blur event to close dropdown when focus is lost (clicking outside)
        blur_handler = create_proxy(lambda e: self._handle_blur(e))
        container.on_blur(blur_handler)
        
        return container
    
    def _create_menu_items(self, menu):
        """Create dropdown menu items."""
        items = self._get_state('items')
        search_text = self._get_state('search_text').lower()
        
        # Clear existing items
        menu._dom_element.innerHTML = ""
        
        # Search box (if searchable)
        if self._get_state('searchable'):
            search_container = Div(style={
                "padding": "8px",
                "border_bottom": "1px solid #eee"
            })
            
            from ..elements import Input
            search_input = Input("text", style={
                "width": "94%",
                "padding": "6px 8px",
                "border": "1px solid #ddd",
                "border_radius": "3px",
                "font_size": "13px"
            })
            search_input.set_attribute("placeholder", "Search...")
            search_input.value = search_text
            search_input.on_input(lambda e: self._handle_search(e))
            search_container.add(search_input)
            menu.add(search_container)
            search_input._dom_element.focus()


        # Filter items based on search
        visible_items = []
        for item in items:
            if not search_text or search_text in item.text.lower():
                visible_items.append(item)
        
        # Create item elements
        if not visible_items:
            no_results = Div("No items found", style={
                "padding": "15px",
                "text_align": "center",
                "color": "#666",
                "font_style": "italic"
            })
            menu.add(no_results)
        else:
            for item in visible_items:
                if item.separator:
                    separator = Div(style={
                        "height": "1px",
                        "background_color": "#ddd",
                        "margin": "5px 0"
                    })
                    menu.add(separator)
                else:
                    item_element = self._create_menu_item(item)
                    menu.add(item_element)
    
    def _create_menu_item(self, item):
        """Create a single menu item element."""
        item_style = self._item_style.copy()
        
        if item.disabled:
            item_style.update({
                "opacity": "0.5",
                "cursor": "not-allowed",
                "background_color": "#f8f9fa"
            })
        
        # Check if item is selected
        is_selected = self._is_item_selected(item)
        if is_selected:
            item_style.update({
                "color": "#0056b3",
                "font-weight": "bold"
            })
        
        item_element = Div(item.text, style=item_style)
        item.element = item_element
        
        if not item.disabled:
            item_element.on_click(lambda e, i=item: self._handle_item_click(e, i))
            item_element.on_mouseenter(lambda e, elem=item_element: self._set_item_hover(elem, True))
            item_element.on_mouseleave(lambda e, elem=item_element: self._set_item_hover(elem, False))
        
        return item_element
    
    def _is_item_selected(self, item):
        """Check if an item is selected."""
        if self._get_state('multi_select'):
            selected_values = self._get_state('selected_values') or []
            return item.value in selected_values
        else:
            return item.value == self._get_state('selected_value')
    
    def _set_button_hover(self, is_hover):
        """Set dropdown button hover state."""
        btn = self._get_element('dropdown_btn')
        if btn:
            if is_hover and not self._get_state('is_open'):
                btn.style.border_color = "#999"
            else:
                btn.style.border_color = "#ddd"
    
    def _set_item_hover(self, item_element, is_hover):
        """Set menu item hover state."""
        if is_hover:
            item_element.style.background_color = "#f8f9fa"
        else:
            # Reset to default or selected state
            # This would need more logic to maintain selected state
            item_element.style.background_color = "transparent"
    
    def _get_display_text(self):
        """Get text to display in dropdown button."""
        if self._get_state('multi_select'):
            selected_values = self._get_state('selected_values') or []
            if not selected_values:
                return self._get_state('placeholder')
            elif len(selected_values) == 1:
                # Find item with this value
                items = self._get_state('items')
                for item in items:
                    if item.value == selected_values[0]:
                        return item.text
                return str(selected_values[0])
            else:
                return f"{len(selected_values)} items selected"
        else:
            selected_value = self._get_state('selected_value')
            if selected_value is None:
                return self._get_state('placeholder')
            
            # Find item with this value
            items = self._get_state('items')
            for item in items:
                if item.value == selected_value:
                    return item.text
            
            return str(selected_value)
    
    def _toggle_dropdown(self):
        """Toggle dropdown open/close state."""
        if self._get_state('is_open'):
            self._close_dropdown()
        else:
            self._open_dropdown()
    
    def _open_dropdown(self):
        """Open the dropdown menu."""
        if not self._get_state('is_open'):
            self._set_state(is_open=True)

            menu = self._get_element('menu')
            arrow = self._get_element('arrow')
            btn = self._get_element('dropdown_btn')

            if menu:
                menu.style.display = "block"

            if arrow:
                arrow.style.transform = "rotate(180deg)"

            if btn:
                btn.style.border_color = "#007bff"

            # Add global click listener to detect clicks outside dropdown
            self._add_click_outside_listener()

            # Add global escape key listener
            self._add_escape_listener()

            self._trigger_callbacks('open')
    
    def _close_dropdown(self):
        """Close the dropdown menu."""
        if self._get_state('is_open'):
            self._set_state(is_open=False, search_text="")

            menu = self._get_element('menu')
            arrow = self._get_element('arrow')
            btn = self._get_element('dropdown_btn')

            if menu:
                menu.style.display = "none"

            if arrow:
                arrow.style.transform = "rotate(0deg)"

            if btn:
                btn.style.border_color = "#ddd"

            # Remove global event listeners
            self._remove_click_outside_listener()
            self._remove_escape_listener()

            # Recreate items to clear search
            if menu:
                self._create_menu_items(menu)

            self._trigger_callbacks('close')
    
    def _handle_item_click(self, event, item):
        """Handle menu item click."""
        if item.disabled:
            return

        if self._get_state('multi_select'):
            # Stop event propagation to prevent click-outside listener from closing dropdown
            event.stopPropagation()

            selected_values = self._get_state('selected_values') or []

            if item.value in selected_values:
                # Deselect
                selected_values.remove(item.value)
                self._trigger_callbacks('deselect', item.value, item)
            else:
                # Select
                selected_values.append(item.value)
                self._trigger_callbacks('select', item.value, item)

            self._set_state(selected_values=selected_values)

            # Update button text
            button_content = self._get_element('button_content')
            if button_content:
                button_content.set_text(self._get_display_text())

            # Recreate menu to update selected states
            menu = self._get_element('menu')
            if menu:
                self._create_menu_items(menu)

            self._trigger_callbacks('change', selected_values, item)

        else:
            # Single select - close dropdown after selection
            old_value = self._get_state('selected_value')
            self._set_state(selected_value=item.value)

            # Update button text
            button_content = self._get_element('button_content')
            if button_content:
                button_content.set_text(item.text)

            self._close_dropdown()

            self._trigger_callbacks('select', item.value, item)
            self._trigger_callbacks('change', item.value, item, old_value)
    
    def _handle_search(self, event):
        """Handle search input."""
        search_text = event.target.value
        self._set_state(search_text=search_text)
        # Recreate menu items with filter
        menu = self._get_element('menu')
        if menu:
            self._create_menu_items(menu)
    
    def add_item(self, text, value=None, disabled=False):
        """Add a new item to the dropdown."""
        item = DropdownItem(text, value, disabled)
        items = self._get_state('items')
        items.append(item)
        self._set_state(items=items)
        
        # Recreate menu if open
        if self._get_state('is_open'):
            menu = self._get_element('menu')
            if menu:
                self._create_menu_items(menu)
        
        return item
    
    def remove_item(self, value):
        """Remove an item by value."""
        items = self._get_state('items')
        items = [item for item in items if item.value != value]
        self._set_state(items=items)
        
        # Update selection if removed item was selected
        if self._get_state('multi_select'):
            selected_values = self._get_state('selected_values') or []
            if value in selected_values:
                selected_values.remove(value)
                self._set_state(selected_values=selected_values)
        else:
            if self._get_state('selected_value') == value:
                self._set_state(selected_value=None)
        
        # Update display
        self._update_display()
        
        return self
    
    def select_item(self, value):
        """Select an item by value."""
        items = self._get_state('items')
        item = next((i for i in items if i.value == value), None)
        
        if item and not item.disabled:
            if self._get_state('multi_select'):
                selected_values = self._get_state('selected_values') or []
                if value not in selected_values:
                    selected_values.append(value)
                    self._set_state(selected_values=selected_values)
                    self._trigger_callbacks('select', value, item)
                    self._trigger_callbacks('change', selected_values, item)
            else:
                old_value = self._get_state('selected_value')
                self._set_state(selected_value=value)
                self._trigger_callbacks('select', value, item)
                self._trigger_callbacks('change', value, item, old_value)
            
            self._update_display()
        
        return self
    
    def clear_selection(self):
        """Clear all selections."""
        if self._get_state('multi_select'):
            self._set_state(selected_values=[])
        else:
            self._set_state(selected_value=None)
        
        self._update_display()
        return self
    
    def _update_display(self):
        """Update button display text."""
        button_content = self._get_element('button_content')
        if button_content:
            button_content.set_text(self._get_display_text())
    
    def _handle_keydown(self, event):
        """Handle keyboard events for the dropdown."""
        if event.key == "Escape" and self._get_state('is_open'):
            self._close_dropdown()
    
    def _handle_blur(self, event):
        """Handle blur event when dropdown loses focus (clicked outside)."""
        if not self._get_state('is_open'):
            return
            
        # Check if focus is moving to an element inside the dropdown
        container = self._get_element('container')
        if container and container._dom_element:
            # Use setTimeout to check relatedTarget after blur event completes
            check_focus = create_proxy(lambda: self._check_focus_after_blur())
            js.setTimeout(check_focus, 10)
    
    def _check_focus_after_blur(self):
        """Check if focus moved to an element inside the dropdown."""
        if not self._get_state('is_open'):
            return

        container = self._get_element('container')
        if container and container._dom_element:
            active_element = js.document.activeElement
            # If the currently focused element is inside our dropdown, don't close
            if not container._dom_element.contains(active_element):
                self._close_dropdown()

    def _add_click_outside_listener(self):
        """Add global document click listener to detect clicks outside dropdown."""
        if self._click_outside_handler is None:
            def handle_click_outside(event):
                if not self._get_state('is_open'):
                    return

                container = self._get_element('container')
                if container and container._dom_element:
                    # Check if click target is outside the dropdown container
                    if not container._dom_element.contains(event.target):
                        self._close_dropdown()

            # Create proxy and store reference for cleanup
            self._click_outside_handler = create_proxy(handle_click_outside)
            js.document.addEventListener('click', self._click_outside_handler)

    def _remove_click_outside_listener(self):
        """Remove global document click listener."""
        if self._click_outside_handler is not None:
            js.document.removeEventListener('click', self._click_outside_handler)
            self._click_outside_handler = None

    def _add_escape_listener(self):
        """Add global document keydown listener for Escape key."""
        if self._escape_handler is None:
            def handle_escape(event):
                if event.key == "Escape" and self._get_state('is_open'):
                    self._close_dropdown()

            # Create proxy and store reference for cleanup
            self._escape_handler = create_proxy(handle_escape)
            js.document.addEventListener('keydown', self._escape_handler)

    def _remove_escape_listener(self):
        """Remove global document keydown listener."""
        if self._escape_handler is not None:
            js.document.removeEventListener('keydown', self._escape_handler)
            self._escape_handler = None


    @property
    def selected_value(self):
        """Get selected value (single select)."""
        return self._get_state('selected_value')
    
    @property
    def selected_values(self):
        """Get selected values (multi select)."""
        return self._get_state('selected_values') or []
    
    @property
    def is_open(self):
        """Check if dropdown is open."""
        return self._get_state('is_open')
    
    def on_select(self, callback):
        """Register callback for item selection."""
        return self.on('select', callback)
    
    def on_deselect(self, callback):
        """Register callback for item deselection."""
        return self.on('deselect', callback)
    
    def on_change(self, callback):
        """Register callback for selection changes."""
        return self.on('change', callback)
    
    def on_open(self, callback):
        """Register callback for dropdown open."""
        return self.on('open', callback)
    
    def on_close(self, callback):
        """Register callback for dropdown close."""
        return self.on('close', callback)