from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QDateEdit,
    QWidget,
    QComboBox,
)
from PyQt6.QtCore import QDate


class SimpleAddSessionDialog(QDialog):
    """Dialog to create a consultation/session."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Session")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Date", self))
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Type", self))
        self.type_combo = QComboBox(self)
        self.type_combo.addItems(["Follow-up", "Initial", "Telemedicine", "Emergency"]) 
        layout.addWidget(self.type_combo)

        layout.addWidget(QLabel("Symptoms", self))
        self.symptoms_edit = QTextEdit(self)
        layout.addWidget(self.symptoms_edit)

        layout.addWidget(QLabel("Findings", self))
        self.findings_edit = QTextEdit(self)
        layout.addWidget(self.findings_edit)

        layout.addWidget(QLabel("Recommendations", self))
        self.reco_edit = QTextEdit(self)
        layout.addWidget(self.reco_edit)

        layout.addWidget(QLabel("Medications", self))
        self.meds_edit = QTextEdit(self)
        layout.addWidget(self.meds_edit)

        layout.addWidget(QLabel("Next appointment (optional)", self))
        self.next_date_edit = QDateEdit(self)
        self.next_date_edit.setCalendarPopup(True)
        self.next_date_edit.setSpecialValueText("None")
        self.next_date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.next_date_edit)

        layout.addWidget(QLabel("Notes", self))
        self.notes_edit = QTextEdit(self)
        layout.addWidget(self.notes_edit)

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Cancel", self)
        ok_btn = QPushButton("Add", self)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept)
        buttons.addStretch(1)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)
        layout.addLayout(buttons)

    def get_values(self) -> dict:
        next_appointment = self.next_date_edit.date().toString("yyyy-MM-dd")
        return {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "type": self.type_combo.currentText(),
            "symptoms": self.symptoms_edit.toPlainText().strip(),
            "findings": self.findings_edit.toPlainText().strip(),
            "recommendations": self.reco_edit.toPlainText().strip(),
            "medications": self.meds_edit.toPlainText().strip(),
            "next_appointment": next_appointment,
            "notes": self.notes_edit.toPlainText().strip(),
        }


