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


class AddPatientDialog(QDialog):
    """Dialog for adding a new patient (name + CNP)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Add Patient")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Name", self))
        self.name_edit = QLineEdit(self)
        layout.addWidget(self.name_edit)

        layout.addWidget(QLabel("CNP", self))
        self.cnp_edit = QLineEdit(self)
        self.cnp_edit.setMaxLength(32)
        layout.addWidget(self.cnp_edit)

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Cancel", self)
        ok_btn = QPushButton("Add", self)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self._on_ok)
        buttons.addStretch(1)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)
        layout.addLayout(buttons)

    def _on_ok(self) -> None:
        name = self.name_edit.text().strip()
        cnp = self.cnp_edit.text().strip()
        if not name or not cnp:
            QMessageBox.warning(self, "Required", "Name and CNP are required.")
            return
        self.accept()

    def get_values(self) -> tuple[str, str]:
        return self.name_edit.text().strip(), self.cnp_edit.text().strip()



