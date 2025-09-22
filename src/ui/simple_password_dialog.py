from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QWidget,
)


class SimplePasswordDialog(QDialog):
    """Prompt for database password; supports initialize or unlock modes."""

    def __init__(self, initializing: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.initializing = initializing
        self.setWindowTitle("Set Database Password" if initializing else "Unlock Database")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        prompt = QLabel(
            "Create a new password for the database." if initializing else "Enter the database password.",
            self,
        )
        layout.addWidget(prompt)

        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Password")
        layout.addWidget(self.password_edit)

        self.confirm_edit = None
        if initializing:
            self.confirm_edit = QLineEdit(self)
            self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_edit.setPlaceholderText("Confirm password")
            layout.addWidget(self.confirm_edit)

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Cancel", self)
        ok_btn = QPushButton("OK", self)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self._on_ok)
        buttons.addStretch(1)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)
        layout.addLayout(buttons)

    def _on_ok(self) -> None:
        password = self.password_edit.text().strip()
        if not password:
            QMessageBox.warning(self, "Required", "Password is required.")
            return
        if self.initializing and self.confirm_edit:
            if password != self.confirm_edit.text().strip():
                QMessageBox.warning(self, "Mismatch", "Passwords do not match.")
                return
        self.accept()

    def get_password(self) -> str:
        return self.password_edit.text().strip()


