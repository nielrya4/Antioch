"""
Antioch Macros - A collection of reusable UI components built on Antioch.

This package provides high-level, reusable UI components that handle their own
state management and event handling safely for multiple instances.

Available Components:
- Counter: Increment/decrement counter with limits and validation
- Modal: Modal dialogs with overlay and customizable content
- Form: Form builder with field validation and data management
- Tabs: Tabbed interface with dynamic tab management
- ProgressBar: Progress indicators with animations and customization
- Alert: Alert notifications with different types and dismissible functionality
- Accordion: Collapsible content panels with expand/collapse animations
- Pagination: Complete pagination system for large datasets
- Dropdown: Dropdown menus with search, multi-select, and item management
- Toast: Toast notification system with auto-dismiss and positioning
- Slider: Range slider component with value display and tick marks
- Map: Interactive map component with markers, shapes, and tile layers
- WebCanvas: Programmatic canvas drawing API for graphics and animations
- Toolbar: Horizontal menu bar with nested dropdowns and submenus
- FileSelect: File browser for selecting files from the virtual filesystem
- FileUpload: Upload files from computer to the virtual filesystem
- DownloadLink: Download link for URLs, data strings, or VFS files
- Window: Draggable, resizable window with minimize/maximize/close
- WindowManager: Manages all windows with taskbar and window management

Base Classes for Creating Custom Macros:
- Macro: Base class with common functionality (ID management, callbacks, styling)
- SimpleMacro: Simplified base class for basic macros with just content

All components use unique identifiers and safe event handling to ensure
multiple instances work independently on the same page.
"""

from .base import Macro, SimpleMacro
from .counter import Counter
from .modal import Modal
from .form import Form, FormField, RequiredValidator, EmailValidator, MinLengthValidator, CustomValidator
from .tabs import Tabs, Tab
from .datatable import DataTable, Column, ColumnType
from .chartjs import ChartJS
from .progressbar import ProgressBar
from .alert import Alert
from .accordion import Accordion, AccordionPanel
from .pagination import Pagination
from .dropdown import Dropdown, DropdownItem
from .toast import Toast, ToastManager, show_toast, info_toast, success_toast, warning_toast, error_toast, clear_all_toasts
from .slider import Slider
from .map import Map
from .webcanvas import WebCanvas
from .toolbar import Toolbar
from .file_select import FileSelect
from .file_upload import FileUpload
from .download_link import DownloadLink
from .window import Window
from .window_manager import WindowManager

__all__ = [
    # Base classes for custom macros
    'Macro',
    'SimpleMacro',

    # Core components
    'Counter',
    'Modal',
    'Form',
    'Tabs',
    'DataTable',
    'ChartJS',
    'ProgressBar',
    'Alert',
    'Accordion',
    'Pagination',
    'Dropdown',
    'Toast',
    'Slider',
    'Map',
    'WebCanvas',
    'Toolbar',
    'FileSelect',
    'FileUpload',
    'DownloadLink',
    'Window',
    'WindowManager',

    # Form-related classes
    'FormField',
    'RequiredValidator',
    'EmailValidator', 
    'MinLengthValidator',
    'CustomValidator',
    
    # Tab-related classes
    'Tab',
    
    # Accordion-related classes
    'AccordionPanel',
    
    # Dropdown-related classes
    'DropdownItem',

    # DataTable-related classes
    'Column',
    'ColumnType',

    # Toast-related classes
    'ToastManager',
    'show_toast',
    'info_toast',
    'success_toast', 
    'warning_toast',
    'error_toast',
    'clear_all_toasts'
]

# Version info
__version__ = '1.0.0'
__author__ = 'Antioch Team'
__description__ = 'Reusable UI components for Antioch DOM library'