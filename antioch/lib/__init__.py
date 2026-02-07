"""
External library integration utilities for Antioch.

This module provides utilities for dynamic script/stylesheet loading.
Libraries are loaded by their respective modules when imported.
"""

# Import loader utilities for external use
from .loader import (
    inject_script,
    inject_stylesheet,
    is_script_loaded,
    is_stylesheet_loaded,
    is_global_defined
)

__all__ = [
    'inject_script',
    'inject_stylesheet',
    'is_script_loaded',
    'is_stylesheet_loaded',
    'is_global_defined'
]
