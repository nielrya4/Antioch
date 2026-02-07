"""
Tabs macro - A reusable tabbed interface component.
Uses unique IDs and safe event handling for multiple instances.
"""
import uuid
from .base import Macro
from ..elements import Div, Button, Span


class Tab:
    """Represents a single tab with content."""
    
    def __init__(self, title, content=None, tab_id=None, disabled=False):
        """
        Initialize a tab.
        
        Args:
            title: Display title for the tab
            content: Content for the tab (string or Element)
            tab_id: Unique identifier (generated if not provided)
            disabled: Whether the tab is disabled
        """
        self.title = title
        self.content = content or ""
        self.tab_id = tab_id or str(uuid.uuid4())[:8]
        self.disabled = disabled
        self.tab_button = None
        self.tab_content = None
        self.is_active = False


class Tabs(Macro):
    """A tabbed interface component with dynamic tab management."""
    
    def __init__(self, tabs=None, active_tab=0, tab_position="top",
                 tabs_style=None, content_style=None, container_style=None, **kwargs):
        """
        Initialize a tabs component.
        
        Args:
            tabs: List of Tab objects or dictionaries with tab data
            active_tab: Index or ID of initially active tab
            tab_position: Position of tabs ("top", "bottom", "left", "right")
            tabs_style: Custom styles for tabs container
            content_style: Custom styles for content area
            container_style: Custom styles for main container
        """
        # Initialize base macro
        super().__init__(macro_type="tabs", **kwargs)
        
        # Set up tabs-specific state
        self._set_state(
            tabs=[],
            active_tab_id=None,
            tab_position=tab_position,
            initial_tabs=tabs,
            initial_active_tab=active_tab
        )
        
        # Add callback types
        self._add_callback_type('change')
        self._add_callback_type('tab_added')
        self._add_callback_type('tab_removed')
        
        # Default styles
        default_container_style = {
            "border": "1px solid #ddd",
            "border_radius": "8px",
            "background_color": "#fff"
        }
        
        default_tabs_style = {
            "display": "flex",
            "background_color": "#f8f9fa",
            "border_bottom": "1px solid #ddd",
            "border_radius": "8px 8px 0 0"
        }
        
        default_content_style = {
            "padding": "20px",
            "min_height": "200px"
        }
        
        # Merge with user styles using base class method
        self._container_style = self._merge_styles(default_container_style, container_style)
        self._tabs_style = self._merge_styles(default_tabs_style, tabs_style)
        self._content_style = self._merge_styles(default_content_style, content_style)
        
        # Adjust styles based on tab position
        self._adjust_styles_for_position()
        
        # Initialize macro
        self._init_macro()
        
        # Add initial tabs after creation
        if tabs:
            for tab_data in tabs:
                if isinstance(tab_data, Tab):
                    self.add_tab(tab_data)
                elif isinstance(tab_data, dict):
                    self.add_tab(Tab(**tab_data))
                else:
                    # Assume it's a title string
                    self.add_tab(Tab(str(tab_data)))
        
        # Set active tab
        tabs_list = self._get_state('tabs')
        if tabs_list:
            if isinstance(active_tab, int) and 0 <= active_tab < len(tabs_list):
                self.set_active_tab(tabs_list[active_tab].tab_id)
            elif isinstance(active_tab, str):
                self.set_active_tab(active_tab)
            else:
                self.set_active_tab(tabs_list[0].tab_id)
    
    def _adjust_styles_for_position(self):
        """Adjust styles based on tab position."""
        tab_position = self._get_state('tab_position')
        if tab_position == "bottom":
            self._tabs_style["border_bottom"] = "none"
            self._tabs_style["border_top"] = "1px solid #ddd"
            self._tabs_style["border_radius"] = "0 0 8px 8px"
        elif tab_position == "left":
            self._tabs_style["flex_direction"] = "column"
            self._tabs_style["border_bottom"] = "none"
            self._tabs_style["border_right"] = "1px solid #ddd"
            self._tabs_style["border_radius"] = "8px 0 0 8px"
            self._tabs_style["min_width"] = "150px"
        elif tab_position == "right":
            self._tabs_style["flex_direction"] = "column"
            self._tabs_style["border_bottom"] = "none"
            self._tabs_style["border_left"] = "1px solid #ddd"
            self._tabs_style["border_radius"] = "0 8px 8px 0"
            self._tabs_style["min_width"] = "150px"
    
    def _create_elements(self):
        """Create the tabs UI elements."""
        # Main container using base class helper
        container = self._create_container(self._container_style)
        
        # Tabs container
        tabs_container = self._register_element('tabs_container', Div(style=self._tabs_style))
        
        # Content container
        content_container = self._register_element('content_container', Div(style=self._content_style))
        
        # Arrange containers based on position
        tab_position = self._get_state('tab_position')
        if tab_position == "top":
            container.add(tabs_container, content_container)
        elif tab_position == "bottom":
            container.add(content_container, tabs_container)
        elif tab_position in ["left", "right"]:
            # Use flexbox for side-by-side layout
            container.style.display = "flex"
            if tab_position == "left":
                container.add(tabs_container, content_container)
            else:
                container.add(content_container, tabs_container)
            content_container.style.flex = "1"
        
        return container
    
    def _create_tab_button(self, tab):
        """Create a tab button element."""
        button_style = {
            "background": "none",
            "border": "none",
            "padding": "12px 20px",
            "cursor": "pointer",
            "font_size": "14px",
            "color": "#666",
            "transition": "all 0.3s ease",
            "border_bottom": "2px solid transparent"
        }
        
        tab_position = self._get_state('tab_position')
        if tab_position in ["left", "right"]:
            button_style["border_bottom"] = "none"
            button_style["border_right"] = "2px solid transparent" if tab_position == "left" else "none"
            button_style["border_left"] = "2px solid transparent" if tab_position == "right" else "none"
            button_style["text_align"] = "left"
            button_style["width"] = "100%"
        
        if tab.disabled:
            button_style["cursor"] = "not-allowed"
            button_style["opacity"] = "0.5"
        
        button = Button(tab.title, style=button_style)
        button.set_attribute("data-tab-id", tab.tab_id)
        
        if not tab.disabled:
            button.on_click(lambda e, tid=tab.tab_id: self.set_active_tab(tid))
            button.on_mouseenter(lambda e, b=button: self._set_tab_hover(b, True))
            button.on_mouseleave(lambda e, b=button: self._set_tab_hover(b, False))
        
        return button
    
    def _create_tab_content(self, tab):
        """Create a tab content element."""
        content_div = Div(style={
            "display": "none",
            "width": "100%"
        })
        content_div.set_attribute("data-tab-id", tab.tab_id)
        
        # Add content
        if tab.content:
            if isinstance(tab.content, str):
                from ..elements import P
                content_div.add(P(tab.content))
            else:
                content_div.add(tab.content)
        
        return content_div
    
    def _set_tab_hover(self, button, is_hover):
        """Set tab button hover state."""
        if is_hover:
            button.style.background_color = "#e9ecef"
            button.style.color = "#495057"
        else:
            # Only reset if not active
            tab_id = button.get_attribute("data-tab-id")
            active_tab_id = self._get_state('active_tab_id')
            if tab_id != active_tab_id:
                button.style.background_color = "transparent"
                button.style.color = "#666"
    
    def _update_tab_styles(self):
        """Update tab button styles based on active state."""
        tabs_list = self._get_state('tabs')
        active_tab_id = self._get_state('active_tab_id')
        tab_position = self._get_state('tab_position')
        for tab in tabs_list:
            if tab.tab_button:
                if tab.tab_id == active_tab_id:
                    # Active styles
                    tab.tab_button.style.background_color = "#fff"
                    tab.tab_button.style.color = "#007bff"
                    
                    if tab_position == "top":
                        tab.tab_button.style.border_bottom = "2px solid #007bff"
                    elif tab_position == "bottom":
                        tab.tab_button.style.border_top = "2px solid #007bff"
                    elif tab_position == "left":
                        tab.tab_button.style.border_right = "2px solid #007bff"
                    elif tab_position == "right":
                        tab.tab_button.style.border_left = "2px solid #007bff"
                else:
                    # Inactive styles
                    tab.tab_button.style.background_color = "transparent"
                    tab.tab_button.style.color = "#666"
                    tab.tab_button.style.border_bottom = "2px solid transparent"
                    tab.tab_button.style.border_top = "2px solid transparent"
                    tab.tab_button.style.border_left = "2px solid transparent"
                    tab.tab_button.style.border_right = "2px solid transparent"
    
    
    def add_tab(self, tab):
        """Add a new tab."""
        if isinstance(tab, dict):
            tab = Tab(**tab)
        elif not isinstance(tab, Tab):
            raise TypeError("tab must be a Tab instance or dictionary")
        
        # Check for duplicate IDs
        if any(t.tab_id == tab.tab_id for t in self.tabs):
            tab.tab_id = str(uuid.uuid4())[:8]
        
        # Create UI elements
        tab.tab_button = self._create_tab_button(tab)
        tab.tab_content = self._create_tab_content(tab)
        
        # Add to containers
        tabs_container = self._get_element('tabs_container')
        content_container = self._get_element('content_container')
        tabs_container.add(tab.tab_button)
        content_container.add(tab.tab_content)
        
        # Add to tabs list
        tabs_list = self._get_state('tabs')
        tabs_list.append(tab)
        self._set_state(tabs=tabs_list)
        
        # If this is the first tab, make it active
        if len(tabs_list) == 1:
            self.set_active_tab(tab.tab_id)
        
        self._trigger_callbacks('tab_added', tab)
        return self
    
    def remove_tab(self, tab_id):
        """Remove a tab by ID."""
        tab = self.get_tab(tab_id)
        if not tab:
            return self
        
        # Remove UI elements
        if tab.tab_button:
            tab.tab_button.remove()
        if tab.tab_content:
            tab.tab_content.remove()
        
        # Remove from tabs list
        tabs_list = self._get_state('tabs')
        updated_tabs = [t for t in tabs_list if t.tab_id != tab_id]
        self._set_state(tabs=updated_tabs)
        
        # If removing active tab, switch to another tab
        active_tab_id = self._get_state('active_tab_id')
        if active_tab_id == tab_id:
            if updated_tabs:
                self.set_active_tab(updated_tabs[0].tab_id)
            else:
                self._set_state(active_tab_id=None)
        
        self._trigger_callbacks('tab_removed', tab)
        return self
    
    def get_tab(self, tab_id):
        """Get a tab by ID."""
        tabs_list = self._get_state('tabs')
        return next((tab for tab in tabs_list if tab.tab_id == tab_id), None)
    
    def set_active_tab(self, tab_id):
        """Set the active tab by ID."""
        tab = self.get_tab(tab_id)
        if not tab or tab.disabled:
            return self
        
        old_tab_id = self._get_state('active_tab_id')
        
        # Hide all tab content
        tabs_list = self._get_state('tabs')
        for t in tabs_list:
            if t.tab_content:
                t.tab_content.style.display = "none"
                t.is_active = False
        
        # Show selected tab content
        if tab.tab_content:
            tab.tab_content.style.display = "block"
            tab.is_active = True
        
        self._set_state(active_tab_id=tab_id)
        self._update_tab_styles()
        
        # Trigger change callback
        if old_tab_id != tab_id:
            self._trigger_callbacks('change', tab, old_tab_id)
        
        return self
    
    def get_active_tab(self):
        """Get the currently active tab."""
        active_tab_id = self._get_state('active_tab_id')
        return self.get_tab(active_tab_id) if active_tab_id else None
    
    def set_tab_content(self, tab_id, content):
        """Set content for a specific tab."""
        tab = self.get_tab(tab_id)
        if tab and tab.tab_content:
            tab.content = content
            tab.tab_content._dom_element.innerHTML = ""
            
            if isinstance(content, str):
                from ..elements import P
                tab.tab_content.add(P(content))
            else:
                tab.tab_content.add(content)
        return self
    
    def disable_tab(self, tab_id):
        """Disable a tab."""
        tab = self.get_tab(tab_id)
        if tab:
            tab.disabled = True
            if tab.tab_button:
                tab.tab_button.style.opacity = "0.5"
                tab.tab_button.style.cursor = "not-allowed"
            
            # If disabling active tab, switch to another
            active_tab_id = self._get_state('active_tab_id')
            if active_tab_id == tab_id:
                tabs_list = self._get_state('tabs')
                active_tabs = [t for t in tabs_list if not t.disabled and t.tab_id != tab_id]
                if active_tabs:
                    self.set_active_tab(active_tabs[0].tab_id)
        return self
    
    def enable_tab(self, tab_id):
        """Enable a tab."""
        tab = self.get_tab(tab_id)
        if tab:
            tab.disabled = False
            if tab.tab_button:
                tab.tab_button.style.opacity = "1"
                tab.tab_button.style.cursor = "pointer"
        return self
    
    def on_change(self, callback):
        """Register callback for tab change.
        
        Args:
            callback: Function that takes (tabs_instance, new_tab, old_tab_id)
        """
        return self.on('change', callback)
    
    def on_tab_added(self, callback):
        """Register callback for tab added."""
        return self.on('tab_added', callback)
    
    def on_tab_removed(self, callback):
        """Register callback for tab removed."""
        return self.on('tab_removed', callback)
    
    # element property is inherited from base class
    
    @property
    def tabs(self):
        """Get current tabs list for backward compatibility."""
        return self._get_state('tabs')
    
    @property
    def active_tab_id(self):
        """Get current active tab ID for backward compatibility."""
        return self._get_state('active_tab_id')
    
    @property
    def tab_position(self):
        """Get current tab position for backward compatibility."""
        return self._get_state('tab_position')