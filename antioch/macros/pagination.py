"""
Pagination macro - A reusable pagination component.
Uses unique IDs and safe event handling for multiple instances.
"""
from .base import Macro
from ..elements import Div, Button, Span


class Pagination(Macro):
    """
    A pagination component for navigating through pages of data.
    Perfect for large datasets, search results, and table navigation.
    """
    
    def __init__(self, total_items=0, items_per_page=10, current_page=1, 
                 max_visible_pages=7, show_first_last=True, show_prev_next=True,
                 show_page_info=True, button_style=None, container_style=None, **kwargs):
        """
        Initialize a pagination component.
        
        Args:
            total_items: Total number of items to paginate
            items_per_page: Number of items per page
            current_page: Currently active page (1-based)
            max_visible_pages: Maximum number of page buttons to show
            show_first_last: Whether to show first/last page buttons
            show_prev_next: Whether to show previous/next buttons
            show_page_info: Whether to show page info text
            button_style: Custom styles for buttons
            container_style: Custom styles for container
        """
        # Initialize base macro
        super().__init__(macro_type="pagination", **kwargs)
        
        # Calculate total pages
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page) if items_per_page > 0 else 1
        
        # Set up state
        self._set_state(
            total_items=total_items,
            items_per_page=items_per_page,
            current_page=max(1, min(current_page, total_pages)),
            total_pages=total_pages,
            max_visible_pages=max_visible_pages,
            show_first_last=show_first_last,
            show_prev_next=show_prev_next,
            show_page_info=show_page_info
        )
        
        # Add callback types
        self._add_callback_type('page_change')
        self._add_callback_type('items_per_page_change')
        
        # Default styles
        default_container_style = {
            "display": "flex",
            "align_items": "center",
            "justify_content": "center",
            "gap": "5px",
            "margin": "20px 0",
            "flex_wrap": "wrap"
        }
        
        default_button_style = {
            "padding": "8px 12px",
            "border": "1px solid #ddd",
            "background_color": "#fff",
            "color": "#333",
            "cursor": "pointer",
            "border_radius": "4px",
            "font_size": "14px",
            "min_width": "40px",
            "text_align": "center",
            "transition": "all 0.2s ease"
        }
        
        # Merge with user styles
        self._container_style = self._merge_styles(default_container_style, container_style)
        self._button_style = self._merge_styles(default_button_style, button_style)
        
        # Initialize macro
        self._init_macro()
    
    def _create_elements(self):
        """Create the pagination UI elements."""
        # Main container
        container = self._register_element('container', self._create_container(self._container_style))
        
        # Create pagination elements
        self._create_pagination_buttons(container)
        
        return container
    
    def _create_pagination_buttons(self, container):
        """Create pagination buttons."""
        current_page = self._get_state('current_page')
        total_pages = self._get_state('total_pages')
        show_first_last = self._get_state('show_first_last')
        show_prev_next = self._get_state('show_prev_next')
        show_page_info = self._get_state('show_page_info')
        
        # Page info
        if show_page_info:
            info_text = self._create_page_info()
            container.add(info_text)
        
        # First page button
        if show_first_last and total_pages > 1:
            first_btn = self._create_button("«", 1, current_page == 1)
            container.add(first_btn)
        
        # Previous button
        if show_prev_next and total_pages > 1:
            prev_btn = self._create_button("‹", max(1, current_page - 1), current_page == 1)
            container.add(prev_btn)
        
        # Page number buttons
        page_buttons = self._get_visible_page_range()
        for page_num in page_buttons:
            is_current = page_num == current_page
            page_btn = self._create_button(str(page_num), page_num, False, is_current)
            container.add(page_btn)
        
        # Next button
        if show_prev_next and total_pages > 1:
            next_btn = self._create_button("›", min(total_pages, current_page + 1), current_page == total_pages)
            container.add(next_btn)
        
        # Last page button
        if show_first_last and total_pages > 1:
            last_btn = self._create_button("»", total_pages, current_page == total_pages)
            container.add(last_btn)
    
    def _create_button(self, text, page_num, disabled=False, is_current=False):
        """Create a pagination button."""
        button_style = self._button_style.copy()
        
        if disabled:
            button_style.update({
                "opacity": "0.5",
                "cursor": "not-allowed",
                "background_color": "#f8f9fa"
            })
        elif is_current:
            button_style.update({
                "background_color": "#007bff",
                "color": "white",
                "border_color": "#007bff"
            })
        
        btn = Button(text, style=button_style)
        
        if not disabled:
            btn.on_click(lambda e, page=page_num: self._handle_page_click(page))
            
            if not is_current:
                btn.on_mouseenter(lambda e, b=btn: self._set_button_hover(b, True))
                btn.on_mouseleave(lambda e, b=btn: self._set_button_hover(b, False))
        
        return btn
    
    def _set_button_hover(self, button, is_hover):
        """Set button hover state."""
        if is_hover:
            button.style.background_color = "#e9ecef"
            button.style.border_color = "#adb5bd"
        else:
            button.style.background_color = "#fff"
            button.style.border_color = "#ddd"
    
    def _create_page_info(self):
        """Create page information text."""
        current_page = self._get_state('current_page')
        total_pages = self._get_state('total_pages')
        total_items = self._get_state('total_items')
        items_per_page = self._get_state('items_per_page')
        
        start_item = (current_page - 1) * items_per_page + 1
        end_item = min(current_page * items_per_page, total_items)
        
        info_text = f"Showing {start_item}-{end_item} of {total_items} items (Page {current_page} of {total_pages})"
        
        return Span(info_text, style={
            "margin_right": "15px",
            "font_size": "14px",
            "color": "#666"
        })
    
    def _get_visible_page_range(self):
        """Get the range of page numbers to display."""
        current_page = self._get_state('current_page')
        total_pages = self._get_state('total_pages')
        max_visible = self._get_state('max_visible_pages')
        
        if total_pages <= max_visible:
            return list(range(1, total_pages + 1))
        
        # Calculate start and end of visible range
        half_visible = max_visible // 2
        start = max(1, current_page - half_visible)
        end = min(total_pages, start + max_visible - 1)
        
        # Adjust start if we're near the end
        if end - start + 1 < max_visible:
            start = max(1, end - max_visible + 1)
        
        return list(range(start, end + 1))
    
    def _handle_page_click(self, page_num):
        """Handle page button click."""
        old_page = self._get_state('current_page')
        if page_num != old_page and 1 <= page_num <= self._get_state('total_pages'):
            self._set_state(current_page=page_num)
            self._update_pagination()
            self._trigger_callbacks('page_change', page_num, old_page)
    
    def _update_pagination(self):
        """Update pagination display."""
        container = self._get_element('container')
        if container:
            # Clear existing buttons
            container._dom_element.innerHTML = ""
            # Recreate pagination
            self._create_pagination_buttons(container)
    
    def set_page(self, page_num):
        """Set current page."""
        total_pages = self._get_state('total_pages')
        if 1 <= page_num <= total_pages:
            old_page = self._get_state('current_page')
            self._set_state(current_page=page_num)
            self._update_pagination()
            self._trigger_callbacks('page_change', page_num, old_page)
        return self
    
    def next_page(self):
        """Go to next page."""
        current_page = self._get_state('current_page')
        total_pages = self._get_state('total_pages')
        if current_page < total_pages:
            return self.set_page(current_page + 1)
        return self
    
    def prev_page(self):
        """Go to previous page."""
        current_page = self._get_state('current_page')
        if current_page > 1:
            return self.set_page(current_page - 1)
        return self
    
    def first_page(self):
        """Go to first page."""
        return self.set_page(1)
    
    def last_page(self):
        """Go to last page."""
        total_pages = self._get_state('total_pages')
        return self.set_page(total_pages)
    
    def set_total_items(self, total_items):
        """Update total items count."""
        items_per_page = self._get_state('items_per_page')
        new_total_pages = max(1, (total_items + items_per_page - 1) // items_per_page) if items_per_page > 0 else 1
        
        current_page = self._get_state('current_page')
        new_current_page = min(current_page, new_total_pages)
        
        self._set_state(
            total_items=total_items,
            total_pages=new_total_pages,
            current_page=new_current_page
        )
        
        self._update_pagination()
        return self
    
    def set_items_per_page(self, items_per_page):
        """Update items per page."""
        if items_per_page > 0:
            total_items = self._get_state('total_items')
            new_total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            
            current_page = self._get_state('current_page')
            new_current_page = min(current_page, new_total_pages)
            
            old_items_per_page = self._get_state('items_per_page')
            
            self._set_state(
                items_per_page=items_per_page,
                total_pages=new_total_pages,
                current_page=new_current_page
            )
            
            self._update_pagination()
            self._trigger_callbacks('items_per_page_change', items_per_page, old_items_per_page)
        
        return self
    
    def get_page_data_range(self):
        """Get the data range for current page."""
        current_page = self._get_state('current_page')
        items_per_page = self._get_state('items_per_page')
        total_items = self._get_state('total_items')
        
        start_index = (current_page - 1) * items_per_page
        end_index = min(start_index + items_per_page, total_items)
        
        return {
            'start_index': start_index,
            'end_index': end_index,
            'start_item': start_index + 1,
            'end_item': end_index,
            'page': current_page,
            'total_pages': self._get_state('total_pages'),
            'items_per_page': items_per_page,
            'total_items': total_items
        }
    
    @property
    def current_page(self):
        """Get current page number."""
        return self._get_state('current_page')
    
    @property
    def total_pages(self):
        """Get total number of pages."""
        return self._get_state('total_pages')
    
    @property
    def total_items(self):
        """Get total number of items."""
        return self._get_state('total_items')
    
    @property
    def items_per_page(self):
        """Get items per page."""
        return self._get_state('items_per_page')
    
    @property
    def has_next(self):
        """Check if there's a next page."""
        return self.current_page < self.total_pages
    
    @property
    def has_prev(self):
        """Check if there's a previous page."""
        return self.current_page > 1
    
    def on_page_change(self, callback):
        """Register callback for page changes."""
        return self.on('page_change', callback)
    
    def on_items_per_page_change(self, callback):
        """Register callback for items per page changes."""
        return self.on('items_per_page_change', callback)