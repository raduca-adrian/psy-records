"""
Designer-friendly styles for PyQt6 Designer
This module provides clean, reusable stylesheets that can be easily applied 
to widgets created in Qt Designer.
"""

# Color Palette
class Colors:
    # Light Theme Colors
    PRIMARY = "#0d6efd"
    PRIMARY_HOVER = "#0b5ed7"
    PRIMARY_PRESSED = "#0a58ca"
    
    SUCCESS = "#198754"
    SUCCESS_HOVER = "#157347"
    
    BACKGROUND = "#f8f9fa"
    SURFACE = "#ffffff"
    SURFACE_VARIANT = "#e8f4f8"
    
    TEXT_PRIMARY = "#212529"
    TEXT_SECONDARY = "#495057"
    TEXT_MUTED = "#6c757d"
    
    BORDER = "#6c757d"
    BORDER_LIGHT = "#dee2e6"
    BORDER_LIGHTER = "#e9ecef"
    
    # Dark Theme Colors
    DARK_PRIMARY = "#4dabf7"
    DARK_PRIMARY_HOVER = "#339af0"
    
    DARK_BACKGROUND = "#1a1a1a"
    DARK_SURFACE = "#2d2d2d"
    DARK_SURFACE_VARIANT = "#383838"
    
    DARK_TEXT_PRIMARY = "#f8f9fa"
    DARK_TEXT_SECONDARY = "#ced4da"
    
    DARK_BORDER = "#495057"

# Button Styles
BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {Colors.PRIMARY};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-height: 20px;
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {Colors.PRIMARY_HOVER};
}}
QPushButton:pressed {{
    background-color: {Colors.PRIMARY_PRESSED};
}}
QPushButton:disabled {{
    background-color: {Colors.BORDER_LIGHT};
    color: {Colors.TEXT_MUTED};
}}
"""

BUTTON_SUCCESS = f"""
QPushButton {{
    background-color: {Colors.SUCCESS};
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-height: 20px;
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {Colors.SUCCESS_HOVER};
}}
"""

BUTTON_SECONDARY = f"""
QPushButton {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER_LIGHT};
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-height: 20px;
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {Colors.SURFACE_VARIANT};
    border-color: {Colors.PRIMARY};
}}
"""

# Input Styles
INPUT_FIELD = f"""
QLineEdit {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER_LIGHT};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    min-height: 20px;
}}
QLineEdit:focus {{
    border-color: {Colors.PRIMARY};
    outline: none;
}}
QLineEdit:disabled {{
    background-color: {Colors.SURFACE_VARIANT};
    color: {Colors.TEXT_MUTED};
}}
"""

TEXT_AREA = f"""
QTextEdit {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER_LIGHT};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}}
QTextEdit:focus {{
    border-color: {Colors.PRIMARY};
}}
"""

COMBO_BOX = f"""
QComboBox {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    border: 2px solid {Colors.BORDER_LIGHT};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    min-height: 20px;
}}
QComboBox:hover {{
    border-color: {Colors.PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {Colors.TEXT_SECONDARY};
    margin-right: 5px;
}}
"""

# Table Styles
TABLE_WIDGET = f"""
QTableWidget {{
    background-color: {Colors.SURFACE};
    color: {Colors.TEXT_PRIMARY};
    gridline-color: {Colors.BORDER_LIGHT};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: 6px;
    font-size: 14px;
}}
QHeaderView::section {{
    background-color: {Colors.SURFACE_VARIANT};
    color: {Colors.TEXT_PRIMARY};
    padding: 12px 8px;
    border: 1px solid {Colors.BORDER_LIGHT};
    font-weight: bold;
    font-size: 14px;
}}
QTableWidget::item {{
    padding: 8px;
    border-bottom: 1px solid {Colors.BORDER_LIGHTER};
}}
QTableWidget::item:selected {{
    background-color: {Colors.PRIMARY};
    color: white;
}}
"""

# Frame Styles
CARD_FRAME = f"""
QFrame {{
    background-color: {Colors.SURFACE};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: 8px;
    padding: 16px;
}}
"""

HEADER_FRAME = f"""
QFrame {{
    background-color: {Colors.SURFACE_VARIANT};
    border: 1px solid {Colors.BORDER_LIGHT};
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}}
"""

# Label Styles
TITLE_LABEL = f"""
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 24px;
    font-weight: bold;
    padding: 8px 0px;
}}
"""

SUBTITLE_LABEL = f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 16px;
    font-weight: 600;
    padding: 4px 0px;
}}
"""

INFO_LABEL = f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 14px;
    padding: 2px 0px;
}}
"""

# Tab Widget Styles
TAB_WIDGET = f"""
QTabWidget::pane {{
    border: 1px solid {Colors.BORDER_LIGHT};
    background-color: {Colors.SURFACE};
    border-radius: 6px;
}}
QTabBar::tab {{
    background-color: {Colors.SURFACE_VARIANT};
    color: {Colors.TEXT_PRIMARY};
    padding: 12px 20px;
    margin-right: 2px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border: 1px solid {Colors.BORDER_LIGHT};
    font-size: 14px;
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background-color: {Colors.PRIMARY};
    color: white;
}}
QTabBar::tab:hover:!selected {{
    background-color: {Colors.SURFACE};
}}
"""

# Dialog Styles
DIALOG_MAIN = f"""
QDialog {{
    background-color: {Colors.BACKGROUND};
    color: {Colors.TEXT_PRIMARY};
}}
"""

# Dark Theme Styles
DARK_BUTTON_PRIMARY = f"""
QPushButton {{
    background-color: {Colors.DARK_PRIMARY};
    color: {Colors.DARK_TEXT_PRIMARY};
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: bold;
    min-height: 20px;
    font-size: 14px;
}}
QPushButton:hover {{
    background-color: {Colors.DARK_PRIMARY_HOVER};
}}
"""

DARK_INPUT_FIELD = f"""
QLineEdit {{
    background-color: {Colors.DARK_SURFACE};
    color: {Colors.DARK_TEXT_PRIMARY};
    border: 2px solid {Colors.DARK_BORDER};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
    min-height: 20px;
}}
QLineEdit:focus {{
    border-color: {Colors.DARK_PRIMARY};
}}
"""

# Style Application Helper
class StyleApplicator:
    """Helper class to apply styles to widgets created in Designer"""
    
    @staticmethod
    def apply_primary_button(button):
        button.setStyleSheet(BUTTON_PRIMARY)
    
    @staticmethod
    def apply_success_button(button):
        button.setStyleSheet(BUTTON_SUCCESS)
    
    @staticmethod
    def apply_secondary_button(button):
        button.setStyleSheet(BUTTON_SECONDARY)
    
    @staticmethod
    def apply_input_field(line_edit):
        line_edit.setStyleSheet(INPUT_FIELD)
    
    @staticmethod
    def apply_text_area(text_edit):
        text_edit.setStyleSheet(TEXT_AREA)
    
    @staticmethod
    def apply_combo_box(combo_box):
        combo_box.setStyleSheet(COMBO_BOX)
    
    @staticmethod
    def apply_table(table_widget):
        table_widget.setStyleSheet(TABLE_WIDGET)
    
    @staticmethod
    def apply_card_frame(frame):
        frame.setStyleSheet(CARD_FRAME)
    
    @staticmethod
    def apply_header_frame(frame):
        frame.setStyleSheet(HEADER_FRAME)
    
    @staticmethod
    def apply_title_label(label):
        label.setStyleSheet(TITLE_LABEL)
    
    @staticmethod
    def apply_subtitle_label(label):
        label.setStyleSheet(SUBTITLE_LABEL)
    
    @staticmethod
    def apply_info_label(label):
        label.setStyleSheet(INFO_LABEL)
    
    @staticmethod
    def apply_tab_widget(tab_widget):
        tab_widget.setStyleSheet(TAB_WIDGET)
    
    @staticmethod
    def apply_dialog_style(dialog):
        dialog.setStyleSheet(DIALOG_MAIN)
