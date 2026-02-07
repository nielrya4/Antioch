"""
Toolbar macro - A responsive horizontal menu bar with nested dropdowns.
Spans the width of its container and supports multi-level menu structures.
On mobile devices (viewport < 768px), displays as a hamburger menu.
"""
import js
from pyodide.ffi import create_proxy
from typing import Dict, Any, Callable, Optional, Union
from .base import Macro
from ..elements import Div, Span


class Toolbar(Macro):
    """
    A horizontal toolbar/menu bar with dropdown menus and nested submenus.

    Supports nested menu structures where each menu item can either:
    - Execute a callback (leaf node)
    - Open a submenu (nested dict)

    Example:
        menu_structure = {
            "File": {
                "Open": lambda: open_file(),
                "Save": {
                    "Save": lambda: save_file(),
                    "Save As": lambda: save_file_as()
                },
                "Exit": lambda: exit_app()
            },
            "Edit": {
                "Copy": lambda: copy(),
                "Paste": lambda: paste()
            }
        }
        toolbar = Toolbar(menu_structure)
    """

    def __init__(self, menu_structure: Dict[str, Any] = None,
                 toolbar_style: Optional[Dict[str, Any]] = None,
                 menu_item_style: Optional[Dict[str, Any]] = None,
                 dropdown_style: Optional[Dict[str, Any]] = None,
                 submenu_style: Optional[Dict[str, Any]] = None,
                 **kwargs):
        """
        Initialize a toolbar component.

        Args:
            menu_structure: Dictionary defining menu structure
                Keys are menu labels, values are either:
                - Callable: Direct action to execute
                - Dict: Submenu with more options
            toolbar_style: Custom styles for the toolbar bar
            menu_item_style: Custom styles for top-level menu items
            dropdown_style: Custom styles for dropdown menus
            submenu_style: Custom styles for submenu items
        """
        super().__init__(macro_type="toolbar", **kwargs)

        # Store menu structure
        self._set_state(
            menu_structure=menu_structure or {},
            active_menu=None,  # Currently open menu
            active_submenu=None,  # Currently open submenu
            is_mobile=False,  # Track if in mobile mode
            mobile_menu_open=False  # Track if mobile menu is open
        )

        # Store event handlers for cleanup
        self._click_outside_handler = None
        self._escape_handler = None
        self._resize_handler = None

        # Track all open mobile submenus for proper closing
        self._open_mobile_submenus = []

        # Mobile breakpoint (px)
        self._mobile_breakpoint = 768

        # Callback types
        self._add_callback_type('menu_click')
        self._add_callback_type('item_click')

        # Default styles
        default_toolbar_style = {
            "display": "flex",
            "width": "100%",
            "background_color": "#2c3e50",
            "padding": "0",
            "margin": "0",
            "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "font_family": "Arial, sans-serif",
            "user_select": "none",
            "position": "relative"  # For mobile menu positioning
        }

        default_menu_item_style = {
            "padding": "12px 20px",
            "color": "#ecf0f1",
            "cursor": "pointer",
            "position": "relative",
            "transition": "background-color 0.2s ease",
            "font_size": "14px",
            "border": "none",
            "background": "none",
            "outline": "none"
        }

        default_dropdown_style = {
            "position": "absolute",
            "top": "100%",
            "left": "0",
            "width": "200px",
            "background_color": "#ffffff",
            "border": "1px solid #bdc3c7",
            "border_radius": "0 0 4px 4px",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.15)",
            "z_index": "1000",
            "display": "none",
            "padding": "4px 0"
        }

        default_submenu_style = {
            "padding": "10px 20px",
            "color": "#2c3e50",
            "cursor": "pointer",
            "font_size": "14px",
            "border": "none",
            "background": "none",
            "text_align": "left",
            "width": "100%",
            "position": "relative",
            "transition": "background-color 0.2s ease",
            "outline": "none",
            "box_sizing": "border-box"
        }

        # Merge with user styles
        self._toolbar_style = self._merge_styles(default_toolbar_style, toolbar_style)
        self._menu_item_style = self._merge_styles(default_menu_item_style, menu_item_style)
        self._dropdown_style = self._merge_styles(default_dropdown_style, dropdown_style)
        self._submenu_style = self._merge_styles(default_submenu_style, submenu_style)

        # Initialize macro
        self._init_macro()

        # Set up resize listener for responsive behavior
        self._add_resize_listener()
        self._check_mobile_mode()

    def _create_elements(self):
        """Create the toolbar UI elements."""
        # Main toolbar container
        toolbar = self._register_element('toolbar', Div(style=self._toolbar_style))

        # Create hamburger button (hidden on desktop, visible on mobile)
        hamburger = self._create_hamburger()
        toolbar.add(hamburger)

        # Create desktop menu container (visible on desktop, hidden on mobile)
        desktop_menu = self._register_element('desktop_menu', Div(style={
            "display": "flex",
            "flex": "1"
        }))
        toolbar.add(desktop_menu)

        # Create mobile menu container (hidden by default, opens when hamburger clicked)
        mobile_menu = self._create_mobile_menu()
        toolbar.add(mobile_menu)

        # Create top-level menu items in desktop menu
        menu_structure = self._get_state('menu_structure')
        for menu_label, menu_content in menu_structure.items():
            menu_item = self._create_menu_item(menu_label, menu_content)
            desktop_menu.add(menu_item)

        return toolbar

    def _create_hamburger(self):
        """Create the hamburger menu button for mobile."""
        hamburger = self._register_element('hamburger', Div(style={
            "display": "none",  # Hidden by default (desktop)
            "padding": "12px 20px",
            "cursor": "pointer",
            "color": "#ecf0f1",
            "font_size": "20px",
            "transition": "background-color 0.3s ease"
        }))

        # Add three bars with transitions
        bar_style = {
            "width": "25px",
            "height": "3px",
            "background_color": "#ecf0f1",
            "margin": "4px 0",
            "border_radius": "2px",
            "transition": "background-color 0.3s ease"
        }

        hamburger.add(
            Div(style=bar_style),
            Div(style=bar_style),
            Div(style=bar_style)
        )

        # Add hover effects
        hamburger.on_mouseenter(lambda e, hb=hamburger: self._set_hamburger_hover(hb, True))
        hamburger.on_mouseleave(lambda e, hb=hamburger: self._set_hamburger_hover(hb, False))

        # Toggle mobile menu on click
        hamburger.on_click(lambda e: self._toggle_mobile_menu())

        return hamburger

    def _create_mobile_menu(self):
        """Create the mobile menu dropdown."""
        mobile_menu = self._register_element('mobile_menu', Div(style={
            "display": "none",  # Hidden by default
            "position": "absolute",
            "top": "100%",
            "left": "0",
            "width": "100%",
            "background_color": "#2c3e50",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.15)",
            "z_index": "999",
            "max_height": "80vh",
            "overflow_y": "auto"
        }))

        # Populate with menu items
        menu_structure = self._get_state('menu_structure')
        for menu_label, menu_content in menu_structure.items():
            menu_item = self._create_mobile_menu_item(menu_label, menu_content)
            mobile_menu.add(menu_item)

        return mobile_menu

    def _create_mobile_menu_item(self, label: str, content: Union[Callable, Dict]):
        """Create a mobile menu item."""
        container = Div(style={
            "border_bottom": "1px solid #34495e"
        })

        # Menu button
        menu_button = Div(label, style={
            "padding": "15px 20px",
            "color": "#ecf0f1",
            "cursor": "pointer",
            "font_size": "16px",
            "background": "none",
            "border": "none",
            "width": "100%",
            "text_align": "left",
            "transition": "background-color 0.3s ease"
        })

        # Add hover effects
        menu_button.on_mouseenter(lambda e, mb=menu_button: self._set_mobile_item_hover(mb, True))
        menu_button.on_mouseleave(lambda e, mb=menu_button: self._set_mobile_item_hover(mb, False))

        # Add button first (appears on top)
        container.add(menu_button)

        if callable(content):
            # Direct action - close any open submenus first
            def handle_direct_with_close(e, lbl, cb):
                self._close_all_mobile_submenus()
                self._handle_mobile_direct_click(lbl, cb)
            menu_button.on_click(lambda e, lbl=label, cb=content: handle_direct_with_close(e, lbl, cb))
        elif isinstance(content, dict):
            # Has submenu - create expandable section
            submenu = self._create_mobile_submenu(content)
            menu_button.on_click(lambda e, sm=submenu: self._toggle_mobile_submenu(sm))
            # Add submenu after button (appears below)
            container.add(submenu)

        return container

    def _create_mobile_submenu(self, submenu_content: Dict):
        """Create a mobile submenu (expandable)."""
        submenu = Div(style={
            "display": "none",  # Hidden by default
            "background_color": "#2c3e50",
            "padding": "0"
        })

        for item_label, item_content in submenu_content.items():
            if callable(item_content):
                # Leaf item
                item = Div(item_label, style={
                    "padding": "12px 20px 12px 40px",
                    "color": "#ecf0f1",
                    "cursor": "pointer",
                    "font_size": "14px",
                    "border_bottom": "1px solid #2c3e50",
                    "transition": "background-color 0.3s ease"
                })
                # Add hover effects
                item.on_mouseenter(lambda e, itm=item: self._set_mobile_item_hover(itm, True))
                item.on_mouseleave(lambda e, itm=item: self._set_mobile_item_hover(itm, False))
                item.on_click(lambda e, lbl=item_label, cb=item_content: self._handle_mobile_item_click(lbl, cb))
                submenu.add(item)
            elif isinstance(item_content, dict):
                # Nested submenu
                nested_label = Div(item_label, style={
                    "padding": "12px 20px 12px 40px",
                    "color": "#ecf0f1",
                    "cursor": "pointer",
                    "font_size": "14px",
                    "border_bottom": "1px solid #2c3e50",
                    "transition": "background-color 0.3s ease"
                })
                # Add hover effects
                nested_label.on_mouseenter(lambda e, nl=nested_label: self._set_mobile_item_hover(nl, True))
                nested_label.on_mouseleave(lambda e, nl=nested_label: self._set_mobile_item_hover(nl, False))

                nested_submenu = self._create_mobile_submenu(item_content)
                nested_submenu.style.padding_left = "20px"
                nested_label.on_click(lambda e, nsm=nested_submenu: self._toggle_mobile_submenu(nsm))
                submenu.add(nested_label, nested_submenu)

        return submenu

    def _toggle_mobile_menu(self):
        """Toggle the mobile menu visibility."""
        mobile_menu = self._get_element('mobile_menu')
        is_open = self._get_state('mobile_menu_open')

        if is_open:
            mobile_menu.style.display = "none"
            self._set_state(mobile_menu_open=False)
        else:
            mobile_menu.style.display = "block"
            self._set_state(mobile_menu_open=True)

    def _toggle_mobile_submenu(self, submenu: Div):
        """Toggle a mobile submenu."""
        # Check if this submenu is currently open (before we close anything)
        was_open = submenu in self._open_mobile_submenus

        # Close all open mobile submenus that are NOT ancestors of this submenu
        self._close_sibling_mobile_submenus(submenu)

        # If this submenu was not open, open it now
        if not was_open:
            submenu.style.display = "block"
            self._open_mobile_submenus.append(submenu)

    def _is_ancestor(self, potential_ancestor: Div, descendant: Div) -> bool:
        """Check if potential_ancestor contains descendant in the DOM tree."""
        try:
            return potential_ancestor._dom_element.contains(descendant._dom_element)
        except:
            return False

    def _close_sibling_mobile_submenus(self, submenu: Div):
        """Close all open mobile submenus except ancestors of the given submenu."""
        submenus_to_close = []
        for sm in self._open_mobile_submenus:
            # Don't close if it's an ancestor of the submenu we're opening
            if not self._is_ancestor(sm, submenu):
                submenus_to_close.append(sm)

        # Close the submenus and remove from tracking
        for sm in submenus_to_close:
            sm.style.display = "none"
            self._open_mobile_submenus.remove(sm)

    def _close_all_mobile_submenus(self):
        """Close all open mobile submenus."""
        for sm in self._open_mobile_submenus:
            sm.style.display = "none"
        self._open_mobile_submenus.clear()

    def _handle_mobile_direct_click(self, label: str, callback: Callable):
        """Handle click on mobile direct action."""
        try:
            callback()
            self._toggle_mobile_menu()  # Close menu after action
            self._trigger_callbacks('item_click', label, None)
        except Exception as e:
            print(f"Toolbar {self._id} mobile menu item '{label}' callback error: {e}")

    def _handle_mobile_item_click(self, label: str, callback: Callable):
        """Handle click on mobile submenu item."""
        try:
            callback()
            self._toggle_mobile_menu()  # Close menu after action
            self._trigger_callbacks('item_click', label, callback)
        except Exception as e:
            print(f"Toolbar {self._id} mobile item '{label}' callback error: {e}")

    def _check_mobile_mode(self):
        """Check viewport width and update mobile mode."""
        width = js.window.innerWidth
        is_mobile = width < self._mobile_breakpoint

        # Update state
        self._set_state(is_mobile=is_mobile)

        # Update visibility
        hamburger = self._get_element('hamburger')
        desktop_menu = self._get_element('desktop_menu')

        if hamburger and desktop_menu:
            if is_mobile:
                hamburger.style.display = "block"
                desktop_menu.style.display = "none"
            else:
                hamburger.style.display = "none"
                desktop_menu.style.display = "flex"
                # Close mobile menu if open
                mobile_menu = self._get_element('mobile_menu')
                if mobile_menu:
                    mobile_menu.style.display = "none"
                    self._set_state(mobile_menu_open=False)

    def _add_resize_listener(self):
        """Add window resize listener."""
        def handle_resize(event):
            self._check_mobile_mode()

        self._resize_handler = create_proxy(handle_resize)
        js.window.addEventListener('resize', self._resize_handler)

    def _remove_resize_listener(self):
        """Remove window resize listener."""
        if self._resize_handler is not None:
            js.window.removeEventListener('resize', self._resize_handler)
            self._resize_handler = None

    def _create_menu_item(self, label: str, content: Union[Callable, Dict]):
        """Create a top-level menu item with dropdown."""
        # Container for menu item + dropdown
        menu_container = Div(style={"position": "relative", "display": "inline-block"})

        # Menu button
        menu_button = Div(label, style=self._menu_item_style.copy())

        # Add hover effect
        menu_button.on_mouseenter(lambda e, btn=menu_button, lbl=label: self._set_menu_hover(btn, lbl, True))
        menu_button.on_mouseleave(lambda e, btn=menu_button, lbl=label: self._set_menu_hover(btn, lbl, False))

        # Check if this is a submenu or direct action
        if callable(content):
            # Direct action - just call the function
            menu_button.on_click(lambda e, lbl=label, cb=content: self._handle_direct_click(lbl, cb))
        elif isinstance(content, dict):
            # Has submenu - create dropdown
            dropdown = self._create_dropdown(content)
            menu_button.on_click(lambda e, lbl=label, dd=dropdown: self._toggle_menu(lbl, dd))
            menu_container.add(dropdown)

        menu_container.add(menu_button)

        # Store references to both container and button
        self._register_element(f'menu_{label}', menu_container)
        self._register_element(f'menu_button_{label}', menu_button)

        return menu_container

    def _create_dropdown(self, menu_content: Dict) -> Div:
        """Create a dropdown menu."""
        dropdown = Div(style=self._dropdown_style.copy())

        for item_label, item_content in menu_content.items():
            if callable(item_content):
                # Leaf item - create clickable menu item
                item = self._create_submenu_item(item_label, item_content)
                dropdown.add(item)
            elif isinstance(item_content, dict):
                # Nested submenu
                nested_container = self._create_nested_submenu(item_label, item_content)
                dropdown.add(nested_container)

        return dropdown

    def _create_submenu_item(self, label: str, callback: Callable) -> Div:
        """Create a clickable submenu item."""
        item = Div(label, style=self._submenu_style.copy())

        # Hover effects
        item.on_mouseenter(lambda e, itm=item: self._set_item_hover(itm, True))
        item.on_mouseleave(lambda e, itm=item: self._set_item_hover(itm, False))

        # Click handler
        item.on_click(lambda e, lbl=label, cb=callback: self._handle_item_click(lbl, cb))

        return item

    def _create_nested_submenu(self, label: str, submenu_content: Dict) -> Div:
        """Create a nested submenu (submenu within a submenu)."""
        container = Div(style={"position": "relative"})

        # Parent item with arrow indicator
        parent_style = self._submenu_style.copy()
        parent_style.update({
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center"
        })
        parent_item = Div(style=parent_style)
        parent_item.add(
            Span(label, style={"flex": "1"}),
            Span("▸", style={
                "color": "#95a5a6",
                "margin_left": "10px"
            })
        )

        # Hover effects
        parent_item.on_mouseenter(lambda e, itm=parent_item: self._set_item_hover(itm, True))
        parent_item.on_mouseleave(lambda e, itm=parent_item: self._set_item_hover(itm, False))

        # Create nested dropdown (positioned to the right)
        nested_dropdown = Div(style={
            "position": "absolute",
            "top": "0",
            "left": "100%",
            "width": "200px",
            "background_color": "#ffffff",
            "border": "1px solid #bdc3c7",
            "border_radius": "4px",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.15)",
            "z_index": "1001",
            "display": "none",
            "padding": "4px 0"
        })

        # Populate nested dropdown
        for nested_label, nested_content in submenu_content.items():
            if callable(nested_content):
                nested_item = self._create_submenu_item(nested_label, nested_content)
                nested_dropdown.add(nested_item)
            elif isinstance(nested_content, dict):
                # Support even deeper nesting
                deeper_nested = self._create_nested_submenu(nested_label, nested_content)
                nested_dropdown.add(deeper_nested)

        # Show/hide nested dropdown on hover
        parent_item.on_mouseenter(lambda e, dd=nested_dropdown: self._show_nested(dd))
        container.on_mouseleave(lambda e, dd=nested_dropdown: self._hide_nested(dd))

        container.add(parent_item, nested_dropdown)
        return container

    def _toggle_menu(self, menu_label: str, dropdown: Div):
        """Toggle a menu dropdown."""
        current_active = self._get_state('active_menu')

        if current_active == menu_label:
            # Close if already open
            self._close_all_menus()
        else:
            # Close any open menu and open this one
            self._close_all_menus()
            self._open_menu(menu_label, dropdown)

    def _open_menu(self, menu_label: str, dropdown: Div):
        """Open a menu dropdown."""
        self._set_state(active_menu=menu_label)
        dropdown.style.display = "block"

        # Highlight the active menu button
        menu_button = self._elements.get(f'menu_button_{menu_label}')
        if menu_button:
            menu_button.style.background_color = "#34495e"

        # Add click outside listener
        self._add_click_outside_listener()
        self._add_escape_listener()

        self._trigger_callbacks('menu_click', menu_label)

    def _close_all_menus(self):
        """Close all open menus."""
        active_menu = self._get_state('active_menu')
        if active_menu:
            menu_structure = self._get_state('menu_structure')
            for menu_label in menu_structure.keys():
                menu_container = self._elements.get(f'menu_{menu_label}')
                if menu_container:
                    # Find dropdown in container
                    for child in menu_container._dom_element.children:
                        if hasattr(child, 'style'):
                            # Check if it's a dropdown (has absolute positioning)
                            style_obj = js.window.getComputedStyle(child)
                            if style_obj.position == "absolute":
                                child.style.display = "none"

                # Reset menu button background
                menu_button = self._elements.get(f'menu_button_{menu_label}')
                if menu_button:
                    menu_button.style.background_color = "transparent"

        self._set_state(active_menu=None)
        self._remove_click_outside_listener()
        self._remove_escape_listener()

    def _show_nested(self, nested_dropdown: Div):
        """Show a nested submenu."""
        nested_dropdown.style.display = "block"

    def _hide_nested(self, nested_dropdown: Div):
        """Hide a nested submenu."""
        nested_dropdown.style.display = "none"

    def _handle_direct_click(self, label: str, callback: Callable):
        """Handle click on a direct action menu item."""
        try:
            # Close any open menus first
            self._close_all_menus()
            callback()
            self._trigger_callbacks('item_click', label, None)
        except Exception as e:
            print(f"Toolbar {self._id} menu item '{label}' callback error: {e}")

    def _handle_item_click(self, label: str, callback: Callable):
        """Handle click on a submenu item."""
        try:
            callback()
            self._close_all_menus()
            self._trigger_callbacks('item_click', label, callback)
        except Exception as e:
            print(f"Toolbar {self._id} item '{label}' callback error: {e}")

    def _set_menu_hover(self, menu_button: Div, label: str, is_hover: bool):
        """Set hover state for a menu button."""
        if is_hover:
            menu_button.style.background_color = "#34495e"
        else:
            # Reset unless menu is active
            active_menu = self._get_state('active_menu')
            if label != active_menu:
                menu_button.style.background_color = "transparent"

    def _set_item_hover(self, item: Div, is_hover: bool):
        """Set hover state for a submenu item."""
        if is_hover:
            item.style.background_color = "#ecf0f1"
        else:
            item.style.background_color = "transparent"

    def _set_hamburger_hover(self, hamburger: Div, is_hover: bool):
        """Set hover state for the hamburger button."""
        if is_hover:
            hamburger.style.background_color = "#34495e"
        else:
            hamburger.style.background_color = "transparent"

    def _set_mobile_item_hover(self, item: Div, is_hover: bool):
        """Set hover state for a mobile menu item."""
        if is_hover:
            item.style.background_color = "#34495e"
        else:
            item.style.background_color = "transparent"

    def _add_click_outside_listener(self):
        """Add global click listener to close menus when clicking outside."""
        if self._click_outside_handler is None:
            def handle_click_outside(event):
                toolbar_element = self._get_element('toolbar')
                if toolbar_element and toolbar_element._dom_element:
                    if not toolbar_element._dom_element.contains(event.target):
                        self._close_all_menus()
            self._click_outside_handler = create_proxy(handle_click_outside)
            js.document.addEventListener('click', self._click_outside_handler)

    def _remove_click_outside_listener(self):
        """Remove global click listener."""
        if self._click_outside_handler is not None:
            js.document.removeEventListener('click', self._click_outside_handler)
            self._click_outside_handler = None

    def _add_escape_listener(self):
        """Add escape key listener to close menus."""
        if self._escape_handler is None:
            def handle_escape(event):
                if event.key == "Escape":
                    self._close_all_menus()

            self._escape_handler = create_proxy(handle_escape)
            js.document.addEventListener('keydown', self._escape_handler)

    def _remove_escape_listener(self):
        """Remove escape key listener."""
        if self._escape_handler is not None:
            js.document.removeEventListener('keydown', self._escape_handler)
            self._escape_handler = None

    def update_menu(self, menu_structure: Dict[str, Any]):
        """
        Update the entire menu structure.

        Args:
            menu_structure: New menu structure dictionary
        """
        self._set_state(menu_structure=menu_structure)

        # Rebuild desktop menu
        desktop_menu = self._get_element('desktop_menu')
        if desktop_menu:
            desktop_menu._dom_element.innerHTML = ""
            for menu_label, menu_content in menu_structure.items():
                menu_item = self._create_menu_item(menu_label, menu_content)
                desktop_menu.add(menu_item)

        # Rebuild mobile menu
        mobile_menu = self._get_element('mobile_menu')
        if mobile_menu:
            mobile_menu._dom_element.innerHTML = ""
            for menu_label, menu_content in menu_structure.items():
                menu_item = self._create_mobile_menu_item(menu_label, menu_content)
                mobile_menu.add(menu_item)

        return self

    def on_menu_click(self, callback: Callable):
        """Register callback for when a menu is clicked/opened."""
        return self.on('menu_click', callback)

    def on_item_click(self, callback: Callable):
        """Register callback for when a menu item is clicked."""
        return self.on('item_click', callback)

    def destroy(self):
        """Clean up the toolbar."""
        self._remove_click_outside_listener()
        self._remove_escape_listener()
        self._remove_resize_listener()
        super().destroy()
