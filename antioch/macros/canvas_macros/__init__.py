"""
Canvas Macros - Reusable interactive components for WebCanvas.

Canvas macros are similar to regular macros but designed to work within
a canvas drawing context instead of the DOM. They provide:
- Position and size management
- Mouse interaction handling
- State management
- Callback system
- Drawing abstraction

Base class: CanvasMacro
"""

from .base import CanvasMacro
from .button import CanvasButton

__all__ = [
    'CanvasMacro',
    'CanvasButton',
]
