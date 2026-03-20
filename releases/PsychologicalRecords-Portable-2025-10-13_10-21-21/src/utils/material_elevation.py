"""
Material Design elevation system using QGraphicsDropShadowEffect.
"""

from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


def apply_elevation(widget: QWidget, level: int = 2, dark_mode: bool = False) -> None:
    """
    Apply Material Design elevation effect to a widget.
    
    Args:
        widget: The widget to apply elevation to
        level: Elevation level (0-24), higher = more shadow
        dark_mode: Whether to use dark mode shadow colors
    """
    if level == 0:
        widget.setGraphicsEffect(None)
        return
    
    shadow = QGraphicsDropShadowEffect()
    
    # Shadow parameters based on elevation level
    # Material Design elevation spec
    if level <= 1:
        blur = 3
        offset = 1
        opacity = 0.12 if dark_mode else 0.24
    elif level <= 3:
        blur = 6
        offset = 2
        opacity = 0.16 if dark_mode else 0.32
    elif level <= 6:
        blur = 10
        offset = 4
        opacity = 0.19 if dark_mode else 0.38
    elif level <= 8:
        blur = 14
        offset = 5
        opacity = 0.22 if dark_mode else 0.40
    elif level <= 12:
        blur = 20
        offset = 8
        opacity = 0.24 if dark_mode else 0.42
    elif level <= 16:
        blur = 24
        offset = 10
        opacity = 0.27 if dark_mode else 0.44
    else:
        blur = 32
        offset = 14
        opacity = 0.30 if dark_mode else 0.46
    
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(offset)
    
    # Shadow color
    shadow_color = QColor(0, 0, 0, int(255 * opacity))
    shadow.setColor(shadow_color)
    
    widget.setGraphicsEffect(shadow)


def apply_card_elevation(widget: QWidget, dark_mode: bool = False) -> None:
    """Apply standard card elevation (level 2)."""
    apply_elevation(widget, 2, dark_mode)


def apply_raised_elevation(widget: QWidget, dark_mode: bool = False) -> None:
    """Apply raised component elevation (level 8)."""
    apply_elevation(widget, 8, dark_mode)


def apply_dialog_elevation(widget: QWidget, dark_mode: bool = False) -> None:
    """Apply dialog elevation (level 24)."""
    apply_elevation(widget, 24, dark_mode)


def remove_elevation(widget: QWidget) -> None:
    """Remove elevation effect from a widget."""
    widget.setGraphicsEffect(None)

