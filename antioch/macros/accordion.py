"""
Accordion macro - A reusable collapsible content component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Button, Span, H3


class AccordionPanel:
    """Represents a single accordion panel."""
    
    def __init__(self, title, content, panel_id=None, expanded=False):
        """
        Initialize an accordion panel.
        
        Args:
            title: Panel title/header text
            content: Panel content (string or Element)
            panel_id: Unique identifier (generated if not provided)
            expanded: Whether panel starts expanded
        """
        import uuid
        self.title = title
        self.content = content
        self.panel_id = panel_id or str(uuid.uuid4())[:8]
        self.expanded = expanded
        self.header_element = None
        self.content_element = None
        self.container = None


class Accordion(Macro):
    """
    An accordion component with collapsible panels.
    Perfect for FAQs, documentation, settings panels, and organized content display.
    """
    
    def __init__(self, panels=None, allow_multiple=False, default_expanded=None,
                 header_style=None, content_style=None, container_style=None, **kwargs):
        """
        Initialize an accordion component.
        
        Args:
            panels: List of AccordionPanel objects or dicts with panel data
            allow_multiple: Whether multiple panels can be expanded simultaneously
            default_expanded: Index or list of indices to expand by default
            header_style: Custom styles for panel headers
            content_style: Custom styles for panel content
            container_style: Custom styles for accordion container
        """
        # Initialize base macro
        super().__init__(macro_type="accordion", **kwargs)
        
        # Process initial panels
        processed_panels = []
        if panels:
            for panel_data in panels:
                if isinstance(panel_data, AccordionPanel):
                    processed_panels.append(panel_data)
                elif isinstance(panel_data, dict):
                    processed_panels.append(AccordionPanel(**panel_data))
                else:
                    # Assume it's a title string
                    processed_panels.append(AccordionPanel(str(panel_data)))
        
        # Set up state
        self._set_state(
            panels=processed_panels,
            allow_multiple=allow_multiple,
            default_expanded=default_expanded
        )
        
        # Add callback types
        self._add_callback_type('panel_expand')
        self._add_callback_type('panel_collapse')
        self._add_callback_type('change')
        
        # Default styles
        default_container_style = {
            "border": "1px solid #ddd",
            "border_radius": "6px",
            "overflow": "hidden",
            "box_shadow": "0 1px 3px rgba(0,0,0,0.1)"
        }
        
        default_header_style = {
            "background_color": "#f8f9fa",
            "border": "none",
            "padding": "15px 20px",
            "width": "100%",
            "text_align": "left",
            "cursor": "pointer",
            "font_size": "16px",
            "font_weight": "600",
            "color": "#333",
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "transition": "background-color 0.2s ease"
        }
        
        default_content_style = {
            "padding": "20px",
            "border_top": "1px solid #eee",
            "background_color": "#fff",
            "line_height": "1.6"
        }
        
        # Merge with user styles
        self._container_style = self._merge_styles(default_container_style, container_style)
        self._header_style = self._merge_styles(default_header_style, header_style)
        self._content_style = self._merge_styles(default_content_style, content_style)
        
        # Initialize macro
        self._init_macro()
        
        # Set default expanded panels
        self._set_default_expanded()
    
    def _create_elements(self):
        """Create the accordion UI elements."""
        # Main container
        container = self._register_element('container', self._create_container(self._container_style))
        
        # Create panels
        panels = self._get_state('panels')
        for i, panel in enumerate(panels):
            panel_container = self._create_panel(panel, i)
            container.add(panel_container)
        
        return container
    
    def _create_panel(self, panel, index):
        """Create a single accordion panel."""
        # Panel container
        panel_container = Div(style={
            "border_bottom": "1px solid #eee" if index < len(self._get_state('panels')) - 1 else "none"
        })
        panel.container = panel_container
        
        # Panel header/button
        header_btn = Button(style=self._header_style.copy())
        
        # Header content
        header_content = Div(style={
            "display": "flex",
            "justify_content": "space-between",
            "align_items": "center",
            "width": "100%"
        })
        
        # Title
        title_span = Span(panel.title, style={"flex": "1", "text_align": "left"})
        
        # Expand/collapse icon
        icon_span = Span("▼", style={
            "font_size": "12px",
            "transition": "transform 0.2s ease",
            "transform": "rotate(-90deg)" if not panel.expanded else "rotate(0deg)"
        })
        
        header_content.add(title_span, icon_span)
        header_btn.add(header_content)
        
        # Store references
        panel.header_element = header_btn
        panel.icon_element = icon_span
        
        # Header click handler
        header_btn.on_click(lambda e, p=panel: self._toggle_panel(p))
        
        # Header hover effects
        header_btn.on_mouseenter(lambda e, btn=header_btn: self._set_header_hover(btn, True))
        header_btn.on_mouseleave(lambda e, btn=header_btn: self._set_header_hover(btn, False))
        
        # Panel content
        content_div = Div(style={
            **self._content_style,
            "display": "block" if panel.expanded else "none",
            "transition": "all 0.3s ease"
        })
        
        # Add content
        if panel.content:
            if isinstance(panel.content, str):
                from ..elements import P
                content_div.add(P(panel.content))
            else:
                content_div.add(panel.content)
        
        panel.content_element = content_div
        
        panel_container.add(header_btn, content_div)
        return panel_container
    
    def _set_header_hover(self, header_btn, is_hover):
        """Set header hover state."""
        if is_hover:
            header_btn.style.background_color = "#e9ecef"
        else:
            header_btn.style.background_color = "#f8f9fa"
    
    def _toggle_panel(self, panel):
        """Toggle a panel's expanded state."""
        if panel.expanded:
            self._collapse_panel(panel)
        else:
            self._expand_panel(panel)
    
    def _expand_panel(self, panel):
        """Expand a panel."""
        # If not allowing multiple, collapse others first
        if not self._get_state('allow_multiple'):
            panels = self._get_state('panels')
            for other_panel in panels:
                if other_panel != panel and other_panel.expanded:
                    self._collapse_panel(other_panel, trigger_callbacks=False)
        
        panel.expanded = True
        
        # Update UI
        if panel.content_element:
            panel.content_element.style.display = "block"
        
        if panel.icon_element:
            panel.icon_element.style.transform = "rotate(0deg)"
        
        # Trigger callbacks
        self._trigger_callbacks('panel_expand', panel)
        self._trigger_callbacks('change', panel, 'expand')
    
    def _collapse_panel(self, panel, trigger_callbacks=True):
        """Collapse a panel."""
        panel.expanded = False
        
        # Update UI
        if panel.content_element:
            panel.content_element.style.display = "none"
        
        if panel.icon_element:
            panel.icon_element.style.transform = "rotate(-90deg)"
        
        # Trigger callbacks
        if trigger_callbacks:
            self._trigger_callbacks('panel_collapse', panel)
            self._trigger_callbacks('change', panel, 'collapse')
    
    def _set_default_expanded(self):
        """Set default expanded panels."""
        default_expanded = self._get_state('default_expanded')
        panels = self._get_state('panels')
        
        if default_expanded is not None:
            if isinstance(default_expanded, int):
                # Single index
                if 0 <= default_expanded < len(panels):
                    self._expand_panel(panels[default_expanded])
            elif isinstance(default_expanded, (list, tuple)):
                # Multiple indices
                for index in default_expanded:
                    if 0 <= index < len(panels):
                        panels[index].expanded = True
                        # Update UI if elements exist
                        panel = panels[index]
                        if panel.content_element:
                            panel.content_element.style.display = "block"
                        if panel.icon_element:
                            panel.icon_element.style.transform = "rotate(0deg)"
    
    def add_panel(self, title, content, expanded=False):
        """Add a new panel to the accordion."""
        panel = AccordionPanel(title, content, expanded=expanded)
        
        panels = self._get_state('panels')
        panels.append(panel)
        self._set_state(panels=panels)
        
        # Add to UI
        container = self._get_element('container')
        if container:
            panel_container = self._create_panel(panel, len(panels) - 1)
            container.add(panel_container)
        
        return panel
    
    def remove_panel(self, panel_id_or_index):
        """Remove a panel by ID or index."""
        panels = self._get_state('panels')
        
        if isinstance(panel_id_or_index, int):
            # Remove by index
            if 0 <= panel_id_or_index < len(panels):
                panel = panels.pop(panel_id_or_index)
                if panel.container:
                    panel.container.remove()
        else:
            # Remove by ID
            for i, panel in enumerate(panels):
                if panel.panel_id == panel_id_or_index:
                    panels.pop(i)
                    if panel.container:
                        panel.container.remove()
                    break
        
        self._set_state(panels=panels)
        return self
    
    def expand_panel(self, panel_id_or_index):
        """Expand a specific panel."""
        panel = self._get_panel(panel_id_or_index)
        if panel and not panel.expanded:
            self._expand_panel(panel)
        return self
    
    def collapse_panel(self, panel_id_or_index):
        """Collapse a specific panel."""
        panel = self._get_panel(panel_id_or_index)
        if panel and panel.expanded:
            self._collapse_panel(panel)
        return self
    
    def expand_all(self):
        """Expand all panels (only if allow_multiple is True)."""
        if self._get_state('allow_multiple'):
            panels = self._get_state('panels')
            for panel in panels:
                if not panel.expanded:
                    self._expand_panel(panel)
        return self
    
    def collapse_all(self):
        """Collapse all panels."""
        panels = self._get_state('panels')
        for panel in panels:
            if panel.expanded:
                self._collapse_panel(panel)
        return self
    
    def _get_panel(self, panel_id_or_index):
        """Get a panel by ID or index."""
        panels = self._get_state('panels')
        
        if isinstance(panel_id_or_index, int):
            if 0 <= panel_id_or_index < len(panels):
                return panels[panel_id_or_index]
        else:
            for panel in panels:
                if panel.panel_id == panel_id_or_index:
                    return panel
        return None
    
    def get_expanded_panels(self):
        """Get list of currently expanded panels."""
        panels = self._get_state('panels')
        return [panel for panel in panels if panel.expanded]
    
    def set_panel_content(self, panel_id_or_index, content):
        """Update content of a specific panel."""
        panel = self._get_panel(panel_id_or_index)
        if panel:
            panel.content = content
            if panel.content_element:
                panel.content_element._dom_element.innerHTML = ""
                if isinstance(content, str):
                    from ..elements import P
                    panel.content_element.add(P(content))
                else:
                    panel.content_element.add(content)
        return self
    
    @property
    def panels(self):
        """Get current panels list."""
        return self._get_state('panels')
    
    @property
    def expanded_count(self):
        """Get number of expanded panels."""
        return len(self.get_expanded_panels())
    
    def on_panel_expand(self, callback):
        """Register callback for panel expand events."""
        return self.on('panel_expand', callback)
    
    def on_panel_collapse(self, callback):
        """Register callback for panel collapse events."""
        return self.on('panel_collapse', callback)
    
    def on_change(self, callback):
        """Register callback for any panel state changes."""
        return self.on('change', callback)