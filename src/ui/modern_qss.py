"""
Modern QSS (Qt Style Sheets) system for the Psychological Records application.
Provides responsive design, modern styling, and consistent theming.
"""

from PyQt6.QtCore import QObject, pyqtSignal, QSize
from PyQt6.QtWidgets import QApplication
from src.utils.theme_manager import get_theme_manager, ThemeMode
import os

class ResponsiveStyleManager(QObject):
    """Manages responsive styling based on window size and theme."""
    
    style_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_theme_manager()
        self.current_size_class = "medium"
        self.theme_manager.register_theme_change_callback(self.on_theme_changed)
    
    def get_size_class(self, width, height):
        """Determine size class based on window dimensions."""
        if width < 800 or height < 600:
            return "small"
        elif width < 1200 or height < 800:
            return "medium"
        else:
            return "large"
    
    def update_size_class(self, width, height):
        """Update current size class and emit signal if changed."""
        new_size_class = self.get_size_class(width, height)
        if new_size_class != self.current_size_class:
            self.current_size_class = new_size_class
            self.style_changed.emit()
    
    def on_theme_changed(self, theme_mode):
        """Handle theme changes."""
        self.style_changed.emit()
    
    def get_current_stylesheet(self):
        """Get the complete stylesheet for current theme and size."""
        theme_mode = self.theme_manager.get_current_theme()
        return ModernQSS.get_complete_stylesheet(theme_mode, self.current_size_class)

class ModernQSS:
    """Modern QSS stylesheets with responsive design support."""
    
    @staticmethod
    def get_colors(theme_mode: ThemeMode):
        """Get color palette for the specified theme."""
        if theme_mode == ThemeMode.DARK:
            return {
                # Background colors
                'bg_primary': '#1e1e1e',
                'bg_secondary': '#2d2d2d',
                'bg_tertiary': '#3d3d3d',
                'bg_surface': '#404040',
                'bg_elevated': '#4a4a4a',
                
                # Text colors
                'text_primary': '#ffffff',
                'text_secondary': '#e0e0e0',
                'text_tertiary': '#b0b0b0',
                'text_disabled': '#808080',
                
                # Accent colors
                'accent_primary': '#0078d4',
                'accent_hover': '#106ebe',
                'accent_pressed': '#005a9e',
                'accent_light': '#40e0d0',
                
                # Status colors
                'success': '#16c60c',
                'warning': '#ffb900',
                'error': '#d13438',
                'info': '#0078d4',
                
                # Border colors
                'border_primary': '#5a5a5a',
                'border_secondary': '#404040',
                'border_focus': '#0078d4',
                
                # Shadow colors
                'shadow': 'rgba(0, 0, 0, 0.4)',
                'shadow_light': 'rgba(0, 0, 0, 0.2)',
            }
        else:  # Light theme
            return {
                # Background colors
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'bg_tertiary': '#e9ecef',
                'bg_surface': '#ffffff',
                'bg_elevated': '#ffffff',
                
                # Text colors
                'text_primary': '#212529',
                'text_secondary': '#495057',
                'text_tertiary': '#6c757d',
                'text_disabled': '#adb5bd',
                
                # Accent colors
                'accent_primary': '#0d6efd',
                'accent_hover': '#0b5ed7',
                'accent_pressed': '#0a58ca',
                'accent_light': '#cfe2ff',
                
                # Status colors
                'success': '#198754',
                'warning': '#fd7e14',
                'error': '#dc3545',
                'info': '#0dcaf0',
                
                # Border colors
                'border_primary': '#dee2e6',
                'border_secondary': '#e9ecef',
                'border_focus': '#0d6efd',
                
                # Shadow colors
                'shadow': 'rgba(0, 0, 0, 0.15)',
                'shadow_light': 'rgba(0, 0, 0, 0.075)',
            }
    
    @staticmethod
    def get_spacing(size_class):
        """Get spacing values for the specified size class."""
        if size_class == "small":
            return {
                'xs': '4px', 'sm': '8px', 'md': '12px', 
                'lg': '16px', 'xl': '20px', 'xxl': '24px'
            }
        elif size_class == "medium":
            return {
                'xs': '6px', 'sm': '12px', 'md': '16px', 
                'lg': '20px', 'xl': '24px', 'xxl': '32px'
            }
        else:  # large
            return {
                'xs': '8px', 'sm': '16px', 'md': '20px', 
                'lg': '24px', 'xl': '32px', 'xxl': '40px'
            }
    
    @staticmethod
    def get_typography(size_class):
        """Get typography settings for the specified size class."""
        if size_class == "small":
            return {
                'font_size_xs': '10px', 'font_size_sm': '12px', 'font_size_base': '14px',
                'font_size_lg': '16px', 'font_size_xl': '18px', 'font_size_xxl': '20px',
                'line_height': '1.4', 'font_family': '"Segoe UI", system-ui, sans-serif'
            }
        elif size_class == "medium":
            return {
                'font_size_xs': '12px', 'font_size_sm': '14px', 'font_size_base': '16px',
                'font_size_lg': '18px', 'font_size_xl': '20px', 'font_size_xxl': '24px',
                'line_height': '1.5', 'font_family': '"Segoe UI", system-ui, sans-serif'
            }
        else:  # large
            return {
                'font_size_xs': '14px', 'font_size_sm': '16px', 'font_size_base': '18px',
                'font_size_lg': '20px', 'font_size_xl': '24px', 'font_size_xxl': '28px',
                'line_height': '1.6', 'font_family': '"Segoe UI", system-ui, sans-serif'
            }
    
    @staticmethod
    def get_component_styles(colors, spacing, typography):
        """Get component-specific styles."""
        return f"""
        /* ==== MAIN WINDOW ==== */
        QMainWindow {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            font-family: {typography['font_family']};
            font-size: {typography['font_size_base']};
            line-height: {typography['line_height']};
        }}
        
        /* ==== CENTRAL WIDGET ==== */
        QWidget {{
            background-color: transparent;
            color: {colors['text_primary']};
        }}
        
        /* ==== LABELS ==== */
        QLabel {{
            color: {colors['text_primary']};
            font-size: {typography['font_size_base']};
            padding: {spacing['xs']};
        }}
        
        QLabel[class="title"] {{
            font-size: {typography['font_size_xxl']};
            font-weight: 700;
            color: {colors['text_primary']};
            padding: {spacing['lg']};
            background-color: {colors['bg_elevated']};
            border-radius: 8px;
            border: 2px solid {colors['accent_primary']};
        }}
        
        QLabel[class="subtitle"] {{
            font-size: {typography['font_size_lg']};
            font-weight: 600;
            color: {colors['text_secondary']};
            padding: {spacing['md']};
        }}
        
        QLabel[class="caption"] {{
            font-size: {typography['font_size_sm']};
            color: {colors['text_tertiary']};
            padding: {spacing['sm']};
        }}
        
        /* ==== BUTTONS ==== */
        QPushButton {{
            background-color: {colors['accent_primary']};
            color: white;
            border: none;
            border-radius: 6px;
            padding: {spacing['md']} {spacing['lg']};
            font-weight: 600;
            font-size: {typography['font_size_base']};
            min-height: 32px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {colors['accent_hover']};
            transform: translateY(-1px);
        }}
        
        QPushButton:pressed {{
            background-color: {colors['accent_pressed']};
            transform: translateY(0px);
        }}
        
        QPushButton:disabled {{
            background-color: {colors['text_disabled']};
            color: {colors['text_tertiary']};
        }}
        
        QPushButton[class="secondary"] {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
        }}
        
        QPushButton[class="secondary"]:hover {{
            background-color: {colors['bg_surface']};
            border-color: {colors['accent_primary']};
        }}
        
        QPushButton[class="success"] {{
            background-color: {colors['success']};
        }}
        
        QPushButton[class="warning"] {{
            background-color: {colors['warning']};
        }}
        
        QPushButton[class="danger"] {{
            background-color: {colors['error']};
        }}
        
        QPushButton[class="icon"] {{
            min-width: 40px;
            max-width: 40px;
            min-height: 40px;
            max-height: 40px;
            border-radius: 20px;
            padding: {spacing['sm']};
        }}
        
        /* ==== INPUT FIELDS ==== */
        QLineEdit {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
            border-radius: 6px;
            padding: {spacing['md']};
            font-size: {typography['font_size_base']};
            min-height: 20px;
        }}
        
        QLineEdit:focus {{
            border-color: {colors['border_focus']};
            background-color: {colors['bg_elevated']};
        }}
        
        QLineEdit:disabled {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_disabled']};
        }}
        
        QTextEdit {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
            border-radius: 6px;
            padding: {spacing['md']};
            font-size: {typography['font_size_base']};
            line-height: {typography['line_height']};
        }}
        
        QTextEdit:focus {{
            border-color: {colors['border_focus']};
        }}
        
        /* ==== TABLES ==== */
        QTableWidget {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            gridline-color: {colors['border_secondary']};
            border: 2px solid {colors['border_primary']};
            border-radius: 8px;
            selection-background-color: {colors['accent_light']};
            alternate-background-color: {colors['bg_secondary']};
        }}
        
        QTableWidget::item {{
            padding: {spacing['md']};
            border-bottom: 1px solid {colors['border_secondary']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['accent_primary']};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {colors['accent_primary']};
            color: white;
            padding: {spacing['lg']} {spacing['md']};
            border: none;
            border-right: 1px solid {colors['border_primary']};
            font-weight: 700;
            font-size: {typography['font_size_sm']};
            min-height: 40px;
        }}
        
        QHeaderView::section:hover {{
            background-color: {colors['accent_hover']};
        }}
        
        /* ==== TABS ==== */
        QTabWidget::pane {{
            border: 2px solid {colors['border_primary']};
            background-color: {colors['bg_surface']};
            border-radius: 8px;
            margin-top: {spacing['md']};
        }}
        
        QTabBar::tab {{
            background-color: {colors['bg_tertiary']};
            color: {colors['text_secondary']};
            padding: {spacing['md']} {spacing['xl']};
            margin-right: {spacing['xs']};
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: 600;
            min-width: 100px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border-bottom: 3px solid {colors['accent_primary']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {colors['bg_surface']};
            color: {colors['accent_primary']};
        }}
        
        /* ==== COMBO BOXES ==== */
        QComboBox {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
            border-radius: 6px;
            padding: {spacing['md']};
            min-height: 20px;
            min-width: 120px;
        }}
        
        QComboBox:focus {{
            border-color: {colors['border_focus']};
        }}
        
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border-left: 2px solid {colors['border_primary']};
            border-top-right-radius: 6px;
            border-bottom-right-radius: 6px;
            background-color: {colors['bg_tertiary']};
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border: 3px solid {colors['text_primary']};
            width: 0px;
            height: 0px;
            border-top: 6px solid {colors['text_primary']};
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: none;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
            selection-background-color: {colors['accent_primary']};
            selection-color: white;
        }}
        
        /* ==== FRAMES AND CONTAINERS ==== */
        QFrame {{
            background-color: {colors['bg_surface']};
            border: 1px solid {colors['border_primary']};
            border-radius: 8px;
            padding: {spacing['lg']};
        }}
        
        QFrame[class="card"] {{
            background-color: {colors['bg_elevated']};
            border: none;
            border-radius: 12px;
            padding: {spacing['xl']};
        }}
        
        QFrame[class="header"] {{
            background-color: {colors['bg_secondary']};
            border-bottom: 2px solid {colors['accent_primary']};
            border-radius: 0px;
            padding: {spacing['lg']};
        }}
        
        /* ==== MENU BAR ==== */
        QMenuBar {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border_primary']};
            padding: {spacing['sm']};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: {spacing['md']} {spacing['lg']};
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['accent_primary']};
            color: white;
        }}
        
        QMenu {{
            background-color: {colors['bg_surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_primary']};
            border-radius: 6px;
            padding: {spacing['sm']};
        }}
        
        QMenu::item {{
            padding: {spacing['md']} {spacing['lg']};
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {colors['accent_primary']};
            color: white;
        }}
        
        /* ==== STATUS BAR ==== */
        QStatusBar {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_secondary']};
            border-top: 1px solid {colors['border_primary']};
            padding: {spacing['sm']} {spacing['lg']};
        }}
        
        /* ==== SCROLL BARS ==== */
        QScrollBar:vertical {{
            background-color: {colors['bg_tertiary']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['text_tertiary']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['accent_primary']};
        }}
        
        QScrollBar::add-line, QScrollBar::sub-line {{
            border: none;
            background: none;
        }}
        
        /* ==== TOOLTIPS ==== */
        QToolTip {{
            background-color: {colors['bg_elevated']};
            color: {colors['text_primary']};
            border: 1px solid {colors['border_primary']};
            border-radius: 4px;
            padding: {spacing['sm']} {spacing['md']};
            font-size: {typography['font_size_sm']};
        }}
        
        /* ==== DIALOGS ==== */
        QDialog {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
        }}
        
        /* ==== RESPONSIVE MODIFIERS ==== */
        """
    
    @staticmethod
    def get_complete_stylesheet(theme_mode: ThemeMode, size_class: str = "medium"):
        """Get the complete stylesheet for the given theme and size class."""
        colors = ModernQSS.get_colors(theme_mode)
        spacing = ModernQSS.get_spacing(size_class)
        typography = ModernQSS.get_typography(size_class)
        
        return ModernQSS.get_component_styles(colors, spacing, typography)

# Global style manager instance
_style_manager = None

def get_style_manager():
    """Get the global style manager instance."""
    global _style_manager
    if _style_manager is None:
        _style_manager = ResponsiveStyleManager()
    return _style_manager
