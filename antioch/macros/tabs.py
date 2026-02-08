"""
Tabs macro - A reusable tabbed interface component.
Uses a single content container whose contents are replaced
when a different tab is activated.
"""

import uuid
from .base import Macro
from ..elements import Div, Button


class Tab:
    """Represents a single tab with content."""

    def __init__(self, title, content=None, tab_id=None, disabled=False):
        self.title = title
        self.content = content or ""
        self.tab_id = tab_id or str(uuid.uuid4())[:8]
        self.disabled = disabled
        self.tab_button = None
        self.is_active = False


class Tabs(Macro):
    """A tabbed interface component with dynamic tab management."""

    def __init__(
        self,
        tabs=None,
        active_tab=0,
        tab_position="top",
        tabs_style=None,
        content_style=None,
        container_style=None,
        **kwargs,
    ):
        super().__init__(macro_type="tabs", **kwargs)

        self._set_state(
            tabs=[],
            active_tab_id=None,
            tab_position=tab_position,
            initial_tabs=tabs,
            initial_active_tab=active_tab,
        )

        self._add_callback_type("change")
        self._add_callback_type("tab_added")
        self._add_callback_type("tab_removed")

        default_container_style = {
            "border": "1px solid #ddd",
            "border_radius": "8px",
            "background_color": "#fff",
        }

        default_tabs_style = {
            "display": "flex",
            "background_color": "#f8f9fa",
            "border_bottom": "1px solid #ddd",
            "border_radius": "8px 8px 0 0",
        }

        default_content_style = {
            "padding": "20px",
            "min_height": "200px",
        }

        self._container_style = self._merge_styles(
            default_container_style, container_style
        )
        self._tabs_style = self._merge_styles(default_tabs_style, tabs_style)
        self._content_style = self._merge_styles(
            default_content_style, content_style
        )

        self._adjust_styles_for_position()
        self._init_macro()

        if tabs:
            for tab_data in tabs:
                if isinstance(tab_data, Tab):
                    self.add_tab(tab_data)
                elif isinstance(tab_data, dict):
                    self.add_tab(Tab(**tab_data))
                else:
                    self.add_tab(Tab(str(tab_data)))

        tabs_list = self._get_state("tabs")
        if tabs_list:
            if isinstance(active_tab, int) and 0 <= active_tab < len(tabs_list):
                self.set_active_tab(tabs_list[active_tab].tab_id)
            elif isinstance(active_tab, str):
                self.set_active_tab(active_tab)
            else:
                self.set_active_tab(tabs_list[0].tab_id)

    # ------------------------------------------------------------------ styling

    def _adjust_styles_for_position(self):
        tab_position = self._get_state("tab_position")

        if tab_position == "bottom":
            self._tabs_style["border_bottom"] = "none"
            self._tabs_style["border_top"] = "1px solid #ddd"
            self._tabs_style["border_radius"] = "0 0 8px 8px"

        elif tab_position == "left":
            self._tabs_style.update(
                {
                    "flex_direction": "column",
                    "border_bottom": "none",
                    "border_right": "1px solid #ddd",
                    "border_radius": "8px 0 0 8px",
                    "min_width": "150px",
                }
            )

        elif tab_position == "right":
            self._tabs_style.update(
                {
                    "flex_direction": "column",
                    "border_bottom": "none",
                    "border_left": "1px solid #ddd",
                    "border_radius": "0 8px 8px 0",
                    "min_width": "150px",
                }
            )

    # ------------------------------------------------------------------ elements

    def _create_elements(self):
        container = self._create_container(self._container_style)

        tabs_container = self._register_element(
            "tabs_container", Div(style=self._tabs_style)
        )

        content_container = self._register_element(
            "content_container", Div(style=self._content_style)
        )

        pos = self._get_state("tab_position")

        if pos == "top":
            container.add(tabs_container, content_container)
        elif pos == "bottom":
            container.add(content_container, tabs_container)
        else:
            container.style.display = "flex"
            if pos == "left":
                container.add(tabs_container, content_container)
            else:
                container.add(content_container, tabs_container)
            content_container.style.flex = "1"

        return container

    def _create_tab_button(self, tab):
        style = {
            "background": "none",
            "border": "none",
            "padding": "12px 20px",
            "cursor": "pointer",
            "font_size": "14px",
            "color": "#666",
            "transition": "all 0.3s ease",
            "border_bottom": "2px solid transparent",
        }

        pos = self._get_state("tab_position")
        if pos in ("left", "right"):
            style["border_bottom"] = "none"
            style["text_align"] = "left"
            style["width"] = "100%"
            if pos == "left":
                style["border_right"] = "2px solid transparent"
            else:
                style["border_left"] = "2px solid transparent"

        if tab.disabled:
            style["cursor"] = "not-allowed"
            style["opacity"] = "0.5"

        button = Button(tab.title, style=style)
        button.set_attribute("data-tab-id", tab.tab_id)

        if not tab.disabled:
            button.on_click(lambda e, tid=tab.tab_id: self.set_active_tab(tid))
            button.on_mouseenter(lambda e, b=button: self._set_tab_hover(b, True))
            button.on_mouseleave(lambda e, b=button: self._set_tab_hover(b, False))

        return button

    # ------------------------------------------------------------------ behavior

    def _set_tab_hover(self, button, is_hover):
        tab_id = button.get_attribute("data-tab-id")
        if is_hover:
            button.style.background_color = "#e9ecef"
            button.style.color = "#495057"
        elif tab_id != self._get_state("active_tab_id"):
            button.style.background_color = "transparent"
            button.style.color = "#666"

    def _update_tab_styles(self):
        active_id = self._get_state("active_tab_id")
        pos = self._get_state("tab_position")

        for tab in self._get_state("tabs"):
            btn = tab.tab_button
            if not btn:
                continue

            if tab.tab_id == active_id:
                btn.style.background_color = "#fff"
                btn.style.color = "#007bff"

                if pos == "top":
                    btn.style.border_bottom = "2px solid #007bff"
                elif pos == "bottom":
                    btn.style.border_top = "2px solid #007bff"
                elif pos == "left":
                    btn.style.border_right = "2px solid #007bff"
                elif pos == "right":
                    btn.style.border_left = "2px solid #007bff"
            else:
                btn.style.background_color = "transparent"
                btn.style.color = "#666"
                btn.style.border_bottom = "2px solid transparent"
                btn.style.border_top = "2px solid transparent"
                btn.style.border_left = "2px solid transparent"
                btn.style.border_right = "2px solid transparent"

    # ------------------------------------------------------------------ public API

    def add_tab(self, tab):
        if isinstance(tab, dict):
            tab = Tab(**tab)
        elif not isinstance(tab, Tab):
            raise TypeError("tab must be a Tab instance or dictionary")

        if any(t.tab_id == tab.tab_id for t in self.tabs):
            tab.tab_id = str(uuid.uuid4())[:8]

        tab.tab_button = self._create_tab_button(tab)
        self._get_element("tabs_container").add(tab.tab_button)

        tabs = self._get_state("tabs")
        tabs.append(tab)
        self._set_state(tabs=tabs)

        if len(tabs) == 1:
            self.set_active_tab(tab.tab_id)

        self._trigger_callbacks("tab_added", tab)
        return self

    def remove_tab(self, tab_id):
        tab = self.get_tab(tab_id)
        if not tab:
            return self

        if tab.tab_button:
            tab.tab_button.remove()

        tabs = [t for t in self.tabs if t.tab_id != tab_id]
        self._set_state(tabs=tabs)

        if self._get_state("active_tab_id") == tab_id:
            if tabs:
                self.set_active_tab(tabs[0].tab_id)
            else:
                self._get_element("content_container")._dom_element.innerHTML = ""
                self._set_state(active_tab_id=None)

        self._trigger_callbacks("tab_removed", tab)
        return self

    def set_active_tab(self, tab_id):
        tab = self.get_tab(tab_id)
        if not tab or tab.disabled:
            return self

        old_id = self._get_state("active_tab_id")

        for t in self.tabs:
            t.is_active = False
        tab.is_active = True

        self._set_state(active_tab_id=tab_id)
        self._update_tab_styles()

        container = self._get_element("content_container")
        container._dom_element.innerHTML = ""

        if tab.content:
            if isinstance(tab.content, str):
                from ..elements import P

                container.add(P(tab.content))
            else:
                container.add(tab.content)
                # If content is a Macro with ensure_initialized, call it
                if hasattr(tab.content, 'ensure_initialized'):
                    tab.content.ensure_initialized()

        if old_id != tab_id:
            self._trigger_callbacks("change", tab, old_id)

        return self

    def set_tab_content(self, tab_id, content):
        tab = self.get_tab(tab_id)
        if not tab:
            return self

        tab.content = content

        if tab.tab_id == self._get_state("active_tab_id"):
            container = self._get_element("content_container")
            container._dom_element.innerHTML = ""

            if isinstance(content, str):
                from ..elements import P

                container.add(P(content))
            else:
                container.add(content)
                # If content is a Macro with ensure_initialized, call it
                if hasattr(content, 'ensure_initialized'):
                    content.ensure_initialized()

        return self

    def get_tab(self, tab_id):
        return next((t for t in self.tabs if t.tab_id == tab_id), None)

    def get_active_tab(self):
        return self.get_tab(self._get_state("active_tab_id"))

    def on_change(self, callback):
        return self.on("change", callback)

    def on_tab_added(self, callback):
        return self.on("tab_added", callback)

    def on_tab_removed(self, callback):
        return self.on("tab_removed", callback)

    @property
    def tabs(self):
        return self._get_state("tabs")

    @property
    def active_tab_id(self):
        return self._get_state("active_tab_id")

    @property
    def tab_position(self):
        return self._get_state("tab_position")
