"""
Centralized styling system for the PyQt6 application.
This module provides reusable style constants and helper functions.
"""

from typing import Dict, Any

# Color palette
class Colors:
    # Primary colors
    PRIMARY = "#0d6efd"
    PRIMARY_HOVER = "#0b5ed7"
    PRIMARY_PRESSED = "#0a58ca"
    
    # Success colors
    SUCCESS = "#198754"
    SUCCESS_HOVER = "#157347"
    SUCCESS_PRESSED = "#146c43"
    
    # Background colors
    BACKGROUND = "#f8f9fa"
    SURFACE = "#ffffff"
    SURFACE_VARIANT = "#e8f4f8"
    
    # Text colors
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#495057"
    TEXT_MUTED = "#6c757d"
    
    # Border colors
    BORDER = "#6c757d"
    BORDER_LIGHT = "#dee2e6"
    BORDER_LIGHTER = "#e9ecef"

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

# UI Dimensions (relative units) - Reduced sizes
class UIDimensions:
    # Widget sizes - Reduced to prevent overlap
    DIALOG_WIDTH_EM = "30em"        # 480px equivalent at 16px base (was 37.5em)
    DIALOG_HEIGHT_EM = "25em"       # 400px equivalent at 16px base (was 34.375em)
    COMBO_MAX_WIDTH_EM = "7.5em"    # 120px equivalent at 16px base (was 9.375em)
    
    # Layout spacing - Reduced for compact layout
    FORM_SPACING_PX = 12            # 0.75em equivalent - using px for QLayout methods
    FORM_MARGIN_H_PX = 20          # 1.25em equivalent - using px for QLayout methods  
    FORM_MARGIN_V_PX = 15          # 0.9375em equivalent - using px for QLayout methods

# Shadows (Qt doesn't support box-shadow, so we'll remove these)
class Shadows:
    # Note: Qt StyleSheets don't support box-shadow property
    # These values are kept for documentation but not used
    FOCUS_BORDER = f"0.1875em solid {Colors.PRIMARY}"  # Alternative to box-shadow

class StyleSheets:
    """Pre-defined stylesheet components"""
    
    @staticmethod
    def dialog() -> str:
        """Base dialog styling"""
        return f"""
            QDialog {{
                background-color: {Colors.BACKGROUND};
                color: {Colors.TEXT_PRIMARY};
                font-family: {Typography.FONT_FAMILY};
            }}
        """
    
    @staticmethod
    def input_field() -> str:
        """Standard input field styling with reduced size"""
        return f"""
            QLineEdit {{
                padding: 0.625em 0.75em;
                border: 0.125em solid {Colors.BORDER};
                border-radius: {BorderRadius.SM};
                font-size: {Typography.FONT_SIZE_NORMAL};
                background-color: {Colors.SURFACE};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.PRIMARY};
                selection-color: white;
                min-height: 1.25em;
                max-height: 2.5em;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
                margin: 0.25em 0em;
            }}
            QLineEdit:focus {{
                border-color: {Colors.PRIMARY};
                border-width: 0.1875em;
                background-color: {Colors.SURFACE};
            }}
            QLineEdit::placeholder {{
                color: {Colors.TEXT_MUTED};
                font-style: italic;
                font-weight: {Typography.FONT_WEIGHT_NORMAL};
            }}
        """
    
    @staticmethod
    def label() -> str:
        """Standard label styling with reduced size"""
        return f"""
            QLabel {{
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                color: {Colors.TEXT_SECONDARY};
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
                background-color: {Colors.PRIMARY};
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
                background-color: {Colors.PRIMARY_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.PRIMARY_PRESSED};
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
                background-color: {Colors.SUCCESS};
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
                background-color: {Colors.SUCCESS_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.SUCCESS_PRESSED};
            }}
        """
    
    @staticmethod
    def combo_box() -> str:
        """Combo box styling with reduced size and Qt-compatible properties"""
        return f"""
            QComboBox {{
                padding: 0.625em 0.75em;
                border: 0.125em solid {Colors.BORDER};
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
        """Tab widget styling with reduced size"""
        return f"""
            QTabWidget::pane {{
                border: 0.125em solid {Colors.BORDER_LIGHT};
                background-color: {Colors.SURFACE};
                border-radius: {BorderRadius.SM};
                margin-top: 0.5em;
                padding: 0.75em;
            }}
            QTabBar::tab {{
                background-color: {Colors.BORDER_LIGHTER};
                padding: 0.625em 1.25em;
                margin-right: 0.1875em;
                border-top-left-radius: {BorderRadius.SM};
                border-top-right-radius: {BorderRadius.SM};
                color: {Colors.TEXT_SECONDARY};
                font-weight: {Typography.FONT_WEIGHT_BOLD};
                font-size: 0.875em;
                min-width: 5em;
                min-height: 1em;
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
        """Apply standardized dialog dimensions - Reduced size"""
        # Note: setFixedSize requires pixel values, but we document the em equivalent
        dialog.setFixedSize(480, 400)  # Equivalent to 30em x 25em at 16px base
    
    @staticmethod
    def apply_combo_sizing(combo):
        """Apply standardized combo box sizing - Reduced size"""
        combo.setMaximumWidth(120)  # Equivalent to 7.5em at 16px base
