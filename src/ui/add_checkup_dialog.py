from PyQt6.QtCore import Qt, QDate
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
)


class AddCheckupDialog(QDialog):
    """Dialog to create a medical assessment (checkup)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New Checkup")
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Date", self))
        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        layout.addWidget(QLabel("Chief complaint", self))
        self.chief_edit = QLineEdit(self)
        layout.addWidget(self.chief_edit)

        layout.addWidget(QLabel("Medical history", self))
        self.hist_edit = QTextEdit(self)
        layout.addWidget(self.hist_edit)

        layout.addWidget(QLabel("Examination", self))
        self.exam_edit = QTextEdit(self)
        layout.addWidget(self.exam_edit)

        layout.addWidget(QLabel("Diagnosis", self))
        self.diag_edit = QTextEdit(self)
        layout.addWidget(self.diag_edit)

        layout.addWidget(QLabel("Treatment plan", self))
        self.plan_edit = QTextEdit(self)
        layout.addWidget(self.plan_edit)

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
        return {
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "chief": self.chief_edit.text().strip(),
            "history": self.hist_edit.toPlainText().strip(),
            "exam": self.exam_edit.toPlainText().strip(),
            "diagnosis": self.diag_edit.toPlainText().strip(),
            "plan": self.plan_edit.toPlainText().strip(),
            "notes": self.notes_edit.toPlainText().strip(),
        }



