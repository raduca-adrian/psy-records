"""
Material Design theme system with light and dark mode support.
"""

from typing import Literal, Dict, Any
from dataclasses import dataclass


@dataclass
class MaterialColors:
    """Material Design color palette."""
    # Primary colors
    primary: str
    primary_dark: str
    primary_light: str
    
    # Accent colors
    accent: str
    accent_dark: str
    accent_light: str
    
    # Background colors
    background: str
    surface: str
    card: str
    
    # Text colors
    text_primary: str
    text_secondary: str
    text_disabled: str
    text_hint: str
    
    # Border and divider colors
    border: str
    divider: str
    
    # State colors
    hover: str
    selected: str
    focus: str
    
    # Status colors
    error: str
    warning: str
    success: str
    info: str


# Light theme colors
LIGHT_THEME = MaterialColors(
    primary="#2196F3",
    primary_dark="#1976D2",
    primary_light="#BBDEFB",
    
    accent="#4CAF50",
    accent_dark="#388E3C",
    accent_light="#C8E6C9",
    
    background="#FAFAFA",
    surface="#FFFFFF",
    card="#FFFFFF",
    
    text_primary="#212121",
    text_secondary="#757575",
    text_disabled="#BDBDBD",
    text_hint="#9E9E9E",
    
    border="#E0E0E0",
    divider="#EEEEEE",
    
    hover="#F5F5F5",
    selected="#E3F2FD",
    focus="#2196F3",
    
    error="#F44336",
    warning="#FF9800",
    success="#4CAF50",
    info="#2196F3",
)


# Dark theme colors
DARK_THEME = MaterialColors(
    primary="#64B5F6",
    primary_dark="#42A5F5",
    primary_light="#90CAF9",
    
    accent="#81C784",
    accent_dark="#66BB6A",
    accent_light="#A5D6A7",
    
    background="#121212",
    surface="#1E1E1E",
    card="#2C2C2C",
    
    text_primary="#FFFFFF",
    text_secondary="#B0B0B0",
    text_disabled="#6B6B6B",
    text_hint="#808080",
    
    border="#404040",
    divider="#333333",
    
    hover="#2C2C2C",
    selected="#1A3A52",
    focus="#64B5F6",
    
    error="#EF5350",
    warning="#FFA726",
    success="#66BB6A",
    info="#42A5F5",
)


def get_material_stylesheet(theme: Literal["light", "dark"] = "light") -> str:
    """Generate Material Design stylesheet for the given theme."""
    colors = DARK_THEME if theme == "dark" else LIGHT_THEME
    
    return f"""
    /* ===== MAIN WINDOW ===== */
    QMainWindow {{
        background-color: {colors.background};
    }}
    
    /* ===== TAB WIDGET ===== */
    QTabWidget::pane {{
        border: none;
        background-color: {colors.surface};
        border-radius: 4px;
    }}
    
    QTabBar::tab {{
        background-color: {colors.card};
        color: {colors.text_secondary};
        padding: 12px 24px;
        margin-right: 4px;
        border: none;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        font-weight: 500;
        font-size: 14px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {colors.surface};
        color: {colors.primary};
        border-bottom: 3px solid {colors.primary};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {colors.hover};
        color: {colors.text_primary};
    }}
    
    /* ===== LABELS ===== */
    QLabel {{
        color: {colors.text_primary};
        background-color: transparent;
    }}
    
    QLabel[class="h1"] {{
        font-size: 28px;
        font-weight: 600;
        color: {colors.text_primary};
        padding: 8px 0;
        letter-spacing: 0.5px;
    }}
    
    QLabel[class="h2"] {{
        font-size: 22px;
        font-weight: 600;
        color: {colors.text_primary};
        padding: 6px 0;
    }}
    
    QLabel[class="h3"] {{
        font-size: 18px;
        font-weight: 600;
        color: {colors.text_primary};
        padding: 4px 0;
    }}
    
    QLabel[class="subtitle"] {{
        color: {colors.text_secondary};
        font-size: 14px;
    }}
    
    /* ===== BUTTONS ===== */
    QPushButton {{
        background-color: {colors.primary};
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        font-weight: 500;
        font-size: 14px;
        min-width: 88px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    QPushButton:hover {{
        background-color: {colors.primary_dark};
    }}
    
    QPushButton:pressed {{
        background-color: {colors.primary_dark};
        padding: 11px 19px 9px 21px;
    }}
    
    QPushButton:disabled {{
        background-color: {colors.text_disabled};
        color: {colors.text_hint};
    }}
    
    QPushButton[class="primary"] {{
        background-color: {colors.accent};
    }}
    
    QPushButton[class="primary"]:hover {{
        background-color: {colors.accent_dark};
    }}
    
    QPushButton[class="primary"]:pressed {{
        background-color: {colors.accent_dark};
    }}
    
    QPushButton[class="secondary"] {{
        background-color: transparent;
        color: {colors.primary};
        border: 2px solid {colors.primary};
    }}
    
    QPushButton[class="secondary"]:hover {{
        background-color: {colors.hover};
    }}
    
    QPushButton[class="text"] {{
        background-color: transparent;
        color: {colors.primary};
        border: none;
        min-width: 64px;
    }}
    
    QPushButton[class="text"]:hover {{
        background-color: {colors.hover};
    }}
    
    /* ===== INPUT FIELDS ===== */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        padding: 12px;
        border: 1px solid {colors.border};
        border-radius: 4px;
        background-color: {colors.surface};
        color: {colors.text_primary};
        font-size: 14px;
        selection-background-color: {colors.selected};
        selection-color: {colors.text_primary};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {colors.focus};
        padding: 11px;
    }}
    
    QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
        background-color: {colors.hover};
        color: {colors.text_disabled};
    }}
    
    /* ===== DATE EDIT ===== */
    QDateEdit {{
        padding: 10px 12px;
        border: 1px solid {colors.border};
        border-radius: 4px;
        background-color: {colors.surface};
        color: {colors.text_primary};
        font-size: 14px;
    }}
    
    QDateEdit:focus {{
        border: 2px solid {colors.focus};
        padding: 9px 11px;
    }}
    
    QDateEdit::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QDateEdit::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {colors.text_secondary};
        width: 0;
        height: 0;
    }}
    
    /* ===== COMBO BOX ===== */
    QComboBox {{
        padding: 10px 12px;
        border: 1px solid {colors.border};
        border-radius: 4px;
        background-color: {colors.surface};
        color: {colors.text_primary};
        font-size: 14px;
    }}
    
    QComboBox:focus {{
        border: 2px solid {colors.focus};
        padding: 9px 11px;
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 30px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 6px solid {colors.text_secondary};
        width: 0;
        height: 0;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        selection-background-color: {colors.selected};
        selection-color: {colors.text_primary};
        color: {colors.text_primary};
        outline: none;
    }}
    
    /* ===== TABLE WIDGET ===== */
    QTableWidget {{
        border: 1px solid {colors.border};
        border-radius: 4px;
        background-color: {colors.surface};
        gridline-color: {colors.divider};
        color: {colors.text_primary};
        outline: none;
    }}
    
    QTableWidget::item {{
        padding: 8px;
        border: none;
    }}
    
    QTableWidget::item:selected {{
        background-color: {colors.selected};
        color: {colors.text_primary};
    }}
    
    QTableWidget::item:hover {{
        background-color: {colors.hover};
    }}
    
    QHeaderView::section {{
        background-color: {colors.card};
        padding: 12px 8px;
        border: none;
        border-bottom: 2px solid {colors.primary};
        font-weight: 600;
        font-size: 13px;
        color: {colors.text_primary};
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* ===== FRAME ===== */
    QFrame[frameShape="4"] {{
        background-color: {colors.card};
        border: 1px solid {colors.border};
        border-radius: 8px;
        padding: 20px;
    }}
    
    QFrame[class="elevated"] {{
        background-color: {colors.card};
        border: none;
        border-radius: 8px;
        padding: 20px;
    }}
    
    /* ===== LIST WIDGET ===== */
    QListWidget {{
        border: 1px solid {colors.border};
        border-radius: 4px;
        background-color: {colors.surface};
        color: {colors.text_primary};
        outline: none;
    }}
    
    QListWidget::item {{
        padding: 12px 16px;
        border-bottom: 1px solid {colors.divider};
    }}
    
    QListWidget::item:last {{
        border-bottom: none;
    }}
    
    QListWidget::item:selected {{
        background-color: {colors.selected};
        color: {colors.text_primary};
    }}
    
    QListWidget::item:hover {{
        background-color: {colors.hover};
    }}
    
    /* ===== STATUS BAR ===== */
    QStatusBar {{
        background-color: {colors.card};
        border-top: 1px solid {colors.border};
        color: {colors.text_secondary};
        font-size: 13px;
        padding: 4px 8px;
    }}
    
    QStatusBar::item {{
        border: none;
    }}
    
    /* ===== SCROLL AREA ===== */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    
    /* ===== SCROLL BAR ===== */
    QScrollBar:vertical {{
        background-color: {colors.background};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors.text_disabled};
        border-radius: 6px;
        min-height: 30px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors.text_hint};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
    
    QScrollBar:horizontal {{
        background-color: {colors.background};
        height: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {colors.text_disabled};
        border-radius: 6px;
        min-width: 30px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {colors.text_hint};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}
    
    /* ===== SPLITTER ===== */
    QSplitter::handle {{
        background-color: {colors.divider};
    }}
    
    QSplitter::handle:horizontal {{
        width: 2px;
    }}
    
    QSplitter::handle:vertical {{
        height: 2px;
    }}
    
    QSplitter::handle:hover {{
        background-color: {colors.primary};
    }}
    
    /* ===== MESSAGE BOX ===== */
    QMessageBox {{
        background-color: {colors.surface};
    }}
    
    QMessageBox QLabel {{
        color: {colors.text_primary};
        font-size: 14px;
    }}
    
    /* ===== DIALOG ===== */
    QDialog {{
        background-color: {colors.surface};
    }}
    
    /* ===== MENU ===== */
    QMenu {{
        background-color: {colors.surface};
        border: 1px solid {colors.border};
        border-radius: 4px;
        padding: 4px;
    }}
    
    QMenu::item {{
        padding: 8px 20px;
        border-radius: 2px;
        color: {colors.text_primary};
    }}
    
    QMenu::item:selected {{
        background-color: {colors.hover};
    }}
    
    /* ===== TOOL TIP ===== */
    QToolTip {{
        background-color: {colors.card};
        color: {colors.text_primary};
        border: 1px solid {colors.border};
        border-radius: 4px;
        padding: 8px;
        font-size: 13px;
    }}
    """


def get_theme_toggle_button_style(theme: Literal["light", "dark"] = "light") -> str:
    """Get style for the theme toggle button."""
    colors = DARK_THEME if theme == "dark" else LIGHT_THEME
    return f"""
        QPushButton#themeToggle {{
            background-color: {colors.card};
            color: {colors.text_primary};
            border: 2px solid {colors.border};
            border-radius: 20px;
            padding: 8px 16px;
            font-weight: 500;
            font-size: 13px;
            min-width: 100px;
        }}
        
        QPushButton#themeToggle:hover {{
            background-color: {colors.hover};
            border-color: {colors.primary};
        }}
        
        QPushButton#themeToggle:pressed {{
            background-color: {colors.selected};
        }}
    """

