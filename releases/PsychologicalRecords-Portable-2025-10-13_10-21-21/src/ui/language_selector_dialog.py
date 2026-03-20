"""
Language selection dialog for first-time setup and language changes.
"""

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QButtonGroup,
    QRadioButton,
    QFrame,
)
from PyQt6.QtGui import QFont

from ..utils.material_theme import get_material_stylesheet


class LanguageSelectorDialog(QDialog):
    """Dialog for selecting application language."""

    def __init__(self, current_language: str = "en", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.selected_language = current_language
        self.setWindowTitle("Select Language / Selectați Limba")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        # Detect current theme
        settings = QSettings('PsychologicalRecords', 'UnifiedApp')
        self.current_theme = settings.value('theme', 'light')
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("Select Your Language", self)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setWeight(QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Bilingual message
        message = QLabel(
            "Welcome! Please select your preferred language.\n\n"
            "Bun venit! Vă rugăm să selectați limba preferată.",
            self
        )
        message.setWordWrap(True)
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(message)

        # Language selection frame
        lang_frame = QFrame(self)
        lang_frame.setFrameShape(QFrame.Shape.StyledPanel)
        lang_layout = QVBoxLayout(lang_frame)
        lang_layout.setSpacing(15)

        # Radio button group
        self.button_group = QButtonGroup(self)
        
        # English option
        self.english_radio = QRadioButton("🇬🇧  English", self)
        self.english_radio.setChecked(current_language == "en")
        english_font = QFont()
        english_font.setPointSize(12)
        self.english_radio.setFont(english_font)
        self.button_group.addButton(self.english_radio)
        lang_layout.addWidget(self.english_radio)

        # Romanian option
        self.romanian_radio = QRadioButton("🇷🇴  Română (Romanian)", self)
        self.romanian_radio.setChecked(current_language == "ro")
        romanian_font = QFont()
        romanian_font.setPointSize(12)
        self.romanian_radio.setFont(romanian_font)
        self.button_group.addButton(self.romanian_radio)
        lang_layout.addWidget(self.romanian_radio)

        layout.addWidget(lang_frame)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        cancel_btn = QPushButton("Cancel / Anulare", self)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("OK", self)
        ok_btn.setDefault(True)
        ok_btn.clicked.connect(self._on_ok)
        ok_btn.setProperty("class", "primary")
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)

        # Apply Material Design theme
        self._apply_theme()

    def _apply_theme(self) -> None:
        """Apply Material Design theme based on current preference."""
        stylesheet = get_material_stylesheet(self.current_theme)
        self.setStyleSheet(stylesheet)

    def _on_ok(self) -> None:
        """Handle OK button click."""
        if self.english_radio.isChecked():
            self.selected_language = "en"
        elif self.romanian_radio.isChecked():
            self.selected_language = "ro"
        self.accept()

    def get_selected_language(self) -> str:
        """Get the selected language code."""
        return self.selected_language


def select_language_on_startup(current_language: str = "en") -> str:
    """
    Show language selection dialog and return selected language.
    
    Args:
        current_language: Current language code
        
    Returns:
        Selected language code (en or ro)
    """
    dialog = LanguageSelectorDialog(current_language)
    if dialog.exec() == QDialog.DialogCode.Accepted:
        return dialog.get_selected_language()
    return current_language

