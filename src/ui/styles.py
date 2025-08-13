"""
Centralized styling system for the PyQt6 application.
This module provides reusable style constants and helper functions.
"""

from typing import Dict, Any

"""
Centralized styling system for the PyQt6 application.
This module provides reusable style constants and helper functions.
"""

from typing import Dict, Any
from enum import Enum

class ThemeMode(Enum):
    LIGHT = "light"
    DARK = "dark"

# Color palette with theme support
class Colors:
    # Theme-aware color system
    _current_theme = ThemeMode.LIGHT
    
    # Light theme colors
    _LIGHT_COLORS = {
        # Primary colors
        'PRIMARY': "#0d6efd",
        'PRIMARY_HOVER': "#0b5ed7",
        'PRIMARY_PRESSED': "#0a58ca",
        
        # Success colors
        'SUCCESS': "#198754",
        'SUCCESS_HOVER': "#157347",
        'SUCCESS_PRESSED': "#146c43",
        
        # Background colors
        'BACKGROUND': "#f8f9fa",
        'SURFACE': "#ffffff",
        'SURFACE_VARIANT': "#e8f4f8",
        
        # Text colors
        'TEXT_PRIMARY': "#212529",
        'TEXT_SECONDARY': "#495057",
        'TEXT_MUTED': "#6c757d",
        
        # Border colors
        'BORDER': "#6c757d",
        'BORDER_LIGHT': "#dee2e6",
        'BORDER_LIGHTER': "#e9ecef",
    }
    
    # Dark theme colors
    _DARK_COLORS = {
        # Primary colors (slightly adjusted for dark theme)
        'PRIMARY': "#4dabf7",
        'PRIMARY_HOVER': "#339af0",
        'PRIMARY_PRESSED': "#228be6",
        
        # Success colors
        'SUCCESS': "#51cf66",
        'SUCCESS_HOVER': "#40c057",
        'SUCCESS_PRESSED': "#37b24d",
        
        # Background colors
        'BACKGROUND': "#1a1a1a",
        'SURFACE': "#2d2d2d",
        'SURFACE_VARIANT': "#383838",
        
        # Text colors
        'TEXT_PRIMARY': "#f8f9fa",
        'TEXT_SECONDARY': "#ced4da",
        'TEXT_MUTED': "#adb5bd",
        
        # Border colors
        'BORDER': "#495057",
        'BORDER_LIGHT': "#343a40",
        'BORDER_LIGHTER': "#495057",
    }
    
    @classmethod
    def set_theme(cls, theme: ThemeMode):
        """Set the current theme"""
        cls._current_theme = theme
    
    @classmethod
    def get_theme(cls) -> ThemeMode:
        """Get the current theme"""
        return cls._current_theme
    
    @classmethod
    def _get_color(cls, color_name: str) -> str:
        """Get color value based on current theme"""
        if cls._current_theme == ThemeMode.DARK:
            return cls._DARK_COLORS.get(color_name, cls._LIGHT_COLORS.get(color_name, "#000000"))
        return cls._LIGHT_COLORS.get(color_name, "#000000")
    
    # Dynamic color properties
    @property
    def PRIMARY(cls) -> str:
        return cls._get_color('PRIMARY')
    
    @property 
    def PRIMARY_HOVER(cls) -> str:
        return cls._get_color('PRIMARY_HOVER')
    
    @property
    def PRIMARY_PRESSED(cls) -> str:
        return cls._get_color('PRIMARY_PRESSED')
    
    @property
    def SUCCESS(cls) -> str:
        return cls._get_color('SUCCESS')
    
    @property
    def SUCCESS_HOVER(cls) -> str:
        return cls._get_color('SUCCESS_HOVER')
    
    @property
    def SUCCESS_PRESSED(cls) -> str:
        return cls._get_color('SUCCESS_PRESSED')
    
    @property
    def BACKGROUND(cls) -> str:
        return cls._get_color('BACKGROUND')
    
    @property
    def SURFACE(cls) -> str:
        return cls._get_color('SURFACE')
    
    @property
    def SURFACE_VARIANT(cls) -> str:
        return cls._get_color('SURFACE_VARIANT')
    
    @property
    def TEXT_PRIMARY(cls) -> str:
        return cls._get_color('TEXT_PRIMARY')
    
    @property
    def TEXT_SECONDARY(cls) -> str:
        return cls._get_color('TEXT_SECONDARY')
    
    @property
    def TEXT_MUTED(cls) -> str:
        return cls._get_color('TEXT_MUTED')
    
    @property
    def BORDER(cls) -> str:
        return cls._get_color('BORDER')
    
    @property
    def BORDER_LIGHT(cls) -> str:
        return cls._get_color('BORDER_LIGHT')
    
    @property
    def BORDER_LIGHTER(cls) -> str:
        return cls._get_color('BORDER_LIGHTER')

# Create a global instance for easy access
colors = Colors()

# Typography
class Typography:
    FONT_FAMILY = "'Segoe UI', Arial, sans-serif"
    
    # Font sizes (relative units)
    FONT_SIZE_SMALL = "0.75em"    # 12px equivalent at 16px base
    FONT_SIZE_NORMAL = "1em"      # 16px equivalent at 16px base
    FONT_SIZE_LARGE = "1.25em"    # 20px equivalent at 16px base
    
    # Font weights
    FONT_WEIGHT_NORMAL = "500"
    FONT_WEIGHT_SEMIBOLD = "600"
    FONT_WEIGHT_BOLD = "700"

# Spacing (relative units)
class Spacing:
    XS = "0.375em"     # 6px equivalent at 16px base
    SM = "0.625em"     # 10px equivalent at 16px base
    MD = "1em"         # 16px equivalent at 16px base
    LG = "1.25em"      # 20px equivalent at 16px base
    XL = "1.5625em"    # 25px equivalent at 16px base
    XXL = "1.875em"    # 30px equivalent at 16px base
    XXXL = "2.1875em"  # 35px equivalent at 16px base

# Border radius (relative units)
class BorderRadius:
    SM = "0.5em"       # 8px equivalent at 16px base
    MD = "0.625em"     # 10px equivalent at 16px base

# UI Dimensions (relative units) - Balanced sizing for usability
class UIDimensions:
    # Widget sizes - Balanced to prevent overlap while maintaining reasonable size
    DIALOG_WIDTH_EM = "28em"        # 448px equivalent at 16px base - moderate size increase
    DIALOG_HEIGHT_EM = "22em"       # 352px equivalent at 16px base - reasonable vertical space
    COMBO_MAX_WIDTH_EM = "7em"      # 112px equivalent at 16px base - adequate for language names
    
    # Layout spacing - Balanced for readability without excessive spacing
    FORM_SPACING_PX = 12            # 0.75em equivalent - good vertical separation
    FORM_MARGIN_H_PX = 20          # 1.25em equivalent - balanced horizontal margins
    FORM_MARGIN_V_PX = 15          # 0.9375em equivalent - reasonable vertical margins
    
    # Additional spacing constants for consistent layouts
    BUTTON_SPACING_PX = 8          # Space between buttons
    SECTION_SPACING_PX = 16        # Space between form sections
    TAB_CONTENT_PADDING_PX = 12    # Padding inside tab content areas

# Shadows (Qt doesn't support box-shadow, so we'll remove these)
class Shadows:
    # Note: Qt StyleSheets don't support box-shadow property
    # These values are kept for documentation but not used
    FOCUS_BORDER = f"0.1875em solid {colors.PRIMARY}"  # Alternative to box-shadow

class StyleSheets:
    """Pre-defined stylesheet components with theme support"""
    
    @staticmethod
    def dialog() -> str:
        """Base dialog styling"""
        return f"""
            QDialog {{
                background-color: {colors.BACKGROUND};
                color: {colors.TEXT_PRIMARY};
                font-family: {Typography.FONT_FAMILY};
            }}
        """
    
    @staticmethod
    def input_field() -> str:
        """Standard input field styling with improved visibility"""
        return f"""
            QLineEdit {{
                padding: 0.75em 1em;
                border: 0.125em solid {colors.BORDER};
                border-radius: {BorderRadius.SM};
                font-size: {Typography.FONT_SIZE_NORMAL};
                background-color: {colors.SURFACE};
                color: {colors.TEXT_PRIMARY};
                selection-background-color: {colors.PRIMARY};
                selection-color: white;
                min-height: 1.5em;
                max-height: 3em;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
                margin: 0.375em 0em;
            }}
            QLineEdit:focus {{
                border-color: {colors.PRIMARY};
                border-width: 0.1875em;
                background-color: {colors.SURFACE};
                outline: none;
            }}
            QLineEdit::placeholder {{
                color: {colors.TEXT_MUTED};
                font-style: italic;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
            }}
            QTextEdit {{
                padding: 0.75em;
                border: 0.125em solid {colors.BORDER};
                border-radius: {BorderRadius.SM};
                font-size: {Typography.FONT_SIZE_NORMAL};
                background-color: {colors.SURFACE};
                color: {colors.TEXT_PRIMARY};
                selection-background-color: {colors.PRIMARY};
                selection-color: white;
                min-height: 4em;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
                margin: 0.375em 0em;
                line-height: 1.4;
            }}
            QTextEdit:focus {{
                border-color: {colors.PRIMARY};
                border-width: 0.1875em;
                background-color: {colors.SURFACE};
                outline: none;
            }}
        """
    
    @staticmethod
    def label() -> str:
        """Standard label styling with reduced size"""
        return f"""
            QLabel {{
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                color: {colors.TEXT_SECONDARY};
                font-size: {Typography.FONT_SIZE_NORMAL};
                padding: 0.25em 0em;
                margin: 0.125em 0em;
                min-height: 1.25em;
            }}
        """
    
    @staticmethod
    def primary_button() -> str:
        """Primary button styling with reduced size and Qt-compatible properties"""
        return f"""
            QPushButton {{
                background-color: {colors.PRIMARY};
                color: white;
                border: none;
                padding: 0.5em 1.25em;
                border-radius: {BorderRadius.SM};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: {Typography.FONT_SIZE_NORMAL};
                min-height: 1.25em;
                min-width: 6em;
                text-transform: uppercase;
            }}
            QPushButton:hover {{
                background-color: {colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {colors.PRIMARY_PRESSED};
            }}
        """
    
    @staticmethod
    def primary_button_wide() -> str:
        """Wide primary button styling for longer text"""
        base_style = StyleSheets.primary_button()
        # Override min-width for buttons with longer text
        return base_style.replace("min-width: 6em;", "min-width: 8.5em;")
    
    @staticmethod
    def success_button() -> str:
        """Success button styling with reduced size and Qt-compatible properties"""
        return f"""
            QPushButton {{
                background-color: {colors.SUCCESS};
                color: white;
                border: none;
                padding: 0.5em 1.25em;
                border-radius: {BorderRadius.SM};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: {Typography.FONT_SIZE_NORMAL};
                min-height: 1.25em;
                min-width: 6em;
                text-transform: uppercase;
            }}
            QPushButton:hover {{
                background-color: {colors.SUCCESS_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {colors.SUCCESS_PRESSED};
            }}
        """
    
    @staticmethod
    def combo_box() -> str:
        """Combo box styling with reduced size and Qt-compatible properties"""
        return f"""
            QComboBox {{
                padding: 0.625em 0.75em;
                border: 0.125em solid {colors.BORDER};
                border-radius: {BorderRadius.SM};
                font-size: {Typography.FONT_SIZE_NORMAL};
                background-color: {Colors.SURFACE};
                color: {Colors.TEXT_PRIMARY};
                min-height: 1.25em;
                max-height: 2.5em;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
                margin: 0.25em 0em;
            }}
            QComboBox:focus {{
                border-color: {Colors.PRIMARY};
                border-width: 0.1875em;
                background-color: {Colors.SURFACE};
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 1.5em;
                border-left: 0.125em solid {Colors.BORDER};
                border-top-right-radius: {BorderRadius.SM};
                border-bottom-right-radius: {BorderRadius.SM};
                background-color: {Colors.BORDER_LIGHTER};
            }}
            QComboBox::drop-down:hover {{
                background-color: {Colors.BORDER_LIGHT};
            }}
            QComboBox::down-arrow {{
                image: none;
                border: 0.125em solid {Colors.TEXT_PRIMARY};
                width: 0.375em;
                height: 0.375em;
                border-top: none;
                border-right: none;
                margin-top: -0.125em;
            }}
            QComboBox QAbstractItemView {{
                border: 0.125em solid {Colors.PRIMARY};
                background-color: {Colors.SURFACE};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                selection-color: white;
                font-size: {Typography.FONT_SIZE_NORMAL};
                padding: 0.25em;
                outline: none;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
            }}
            QComboBox QAbstractItemView::item {{
                padding: 0.5em 0.75em;
                color: {Colors.TEXT_PRIMARY};
                background-color: {Colors.SURFACE};
                border: none;
                min-height: 1.25em;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
            }}
            QComboBox QAbstractItemView::item:selected {{
                background-color: {Colors.PRIMARY};
                color: white;
                font-weight: {Typography.FONT_WEIGHT_BOLD};
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: #cce7ff;
                color: {Colors.TEXT_PRIMARY};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
            }}
        """
    
    @staticmethod
    def tab_widget() -> str:
        """Tab widget styling with improved spacing and visibility"""
        return f"""
            QTabWidget::pane {{
                border: 0.125em solid {Colors.BORDER_LIGHT};
                background-color: {Colors.SURFACE};
                border-radius: {BorderRadius.SM};
                margin-top: 0.625em;
                padding: 1em;
            }}
            QTabBar::tab {{
                background-color: {Colors.BORDER_LIGHTER};
                padding: 0.75em 1.5em;
                margin-right: 0.25em;
                border-top-left-radius: {BorderRadius.SM};
                border-top-right-radius: {BorderRadius.SM};
                color: {Colors.TEXT_SECONDARY};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: 0.875em;
                min-width: 6em;
                min-height: 1.25em;
            }}
            QTabBar::tab:selected {{
                background-color: {Colors.SURFACE};
                border-bottom: 0.1875em solid {Colors.PRIMARY};
                color: {Colors.PRIMARY};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: {Typography.FONT_SIZE_NORMAL};
            }}
            QTabBar::tab:hover {{
                background-color: {Colors.BORDER_LIGHT};
                color: {Colors.TEXT_PRIMARY};
            }}
            QTabWidget QScrollArea {{
                border: none;
                background-color: {Colors.SURFACE};
            }}
            QTabWidget QScrollArea QWidget {{
                background-color: {Colors.SURFACE};
            }}
        """
    
    @staticmethod
    def form_layout() -> str:
        """Form layout styling"""
        return f"""
            QFormLayout {{
                margin: {Spacing.XL};
                spacing: {Spacing.LG};
            }}
        """

class StyleHelper:
    """Helper class for applying styles to widgets"""
    
    @staticmethod
    def apply_title_style(widget, text_color: str = None, bg_color: str = None) -> str:
        """Generate title label styling"""
        text_color = text_color or "#2c3e50"
        bg_color = bg_color or Colors.SURFACE_VARIANT
        
        return f"""
            color: {text_color}; 
            margin: {Spacing.XL}; 
            padding: {Spacing.LG};
            background-color: {bg_color};
            border-radius: {BorderRadius.MD};
            border: 0.125em solid {Colors.PRIMARY};
        """
    
    @staticmethod
    def get_complete_dialog_style() -> str:
        """Get complete dialog stylesheet combining all components"""
        return "".join([
            StyleSheets.dialog(),
            StyleSheets.input_field(),
            StyleSheets.label(),
            StyleSheets.combo_box(),
            StyleSheets.tab_widget(),
            StyleSheets.form_layout()
        ])
    
    @staticmethod
    def apply_language_label_style() -> str:
        """Get language label specific styling"""
        return f"font-weight: {Typography.FONT_WEIGHT_SEMIBOLD}; color: {Colors.TEXT_SECONDARY}; font-size: {Typography.FONT_SIZE_SMALL};"

# Widget style appliers for easy use
class WidgetStyles:
    """Pre-configured style appliers for common widgets"""
    
    @staticmethod
    def apply_primary_button(button):
        """Apply primary button style to a button widget"""
        button.setStyleSheet(StyleSheets.primary_button())
    
    @staticmethod
    def apply_primary_button_wide(button):
        """Apply wide primary button style to a button widget"""
        button.setStyleSheet(StyleSheets.primary_button_wide())
    
    @staticmethod
    def apply_success_button(button):
        """Apply success button style to a button widget"""
        button.setStyleSheet(StyleSheets.success_button())
    
    @staticmethod
    def apply_title_label(label, text_color: str = None, bg_color: str = None):
        """Apply title style to a label widget"""
        label.setStyleSheet(StyleHelper.apply_title_style(text_color, bg_color))
    
    @staticmethod
    def apply_language_label(label):
        """Apply language label style"""
        label.setStyleSheet(StyleHelper.apply_language_label_style())
    
    @staticmethod
    def apply_dialog_style(dialog):
        """Apply complete dialog styling"""
        dialog.setStyleSheet(StyleHelper.get_complete_dialog_style())
    
    @staticmethod
    def apply_form_layout(layout):
        """Apply form layout spacing and margins using relative units"""
        layout.setSpacing(UIDimensions.FORM_SPACING_PX)
        layout.setContentsMargins(
            UIDimensions.FORM_MARGIN_H_PX, 
            UIDimensions.FORM_MARGIN_V_PX, 
            UIDimensions.FORM_MARGIN_H_PX, 
            UIDimensions.FORM_MARGIN_V_PX
        )
    
    @staticmethod
    def apply_dialog_dimensions(dialog):
        """Apply standardized dialog dimensions - Optimized for visibility"""
        # Note: setFixedSize requires pixel values, but we document the em equivalent
        dialog.setFixedSize(512, 416)  # Equivalent to 32em x 26em at 16px base - improved size
    
    @staticmethod
    def apply_combo_sizing(combo):
        """Apply standardized combo box sizing - Improved for longer text"""
        combo.setMaximumWidth(128)  # Equivalent to 8em at 16px base - better for language names
        
    @staticmethod
    def apply_section_spacing(layout):
        """Apply spacing between major sections"""
        layout.setSpacing(UIDimensions.SECTION_SPACING_PX)
        
    @staticmethod
    def apply_button_layout(layout):
        """Apply consistent spacing for button layouts"""
        layout.setSpacing(UIDimensions.BUTTON_SPACING_PX)
        
    @staticmethod
    def apply_tab_content_padding(widget):
        """Apply consistent padding to tab content areas"""
        widget.setContentsMargins(
            UIDimensions.TAB_CONTENT_PADDING_PX,
            UIDimensions.TAB_CONTENT_PADDING_PX,
            UIDimensions.TAB_CONTENT_PADDING_PX,
            UIDimensions.TAB_CONTENT_PADDING_PX
        )
