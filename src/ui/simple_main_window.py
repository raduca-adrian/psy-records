"""
A minimal PyQt6 main window to run a simplified version of the app.
Keeps zero coupling to the complex application to allow quick iteration.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStatusBar,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QGroupBox,
    QSplitter,
    QTextEdit,
)


from .simple_add_patient_dialog import SimpleAddPatientDialog
from .simple_add_checkup_dialog import SimpleAddCheckupDialog
from .simple_add_session_dialog import SimpleAddSessionDialog


class SimpleMainWindow(QMainWindow):
    """Minimal, self-contained main window for rapid prototyping."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Psychological Records – Simple")
        self.setMinimumSize(800, 500)

        # Optional: use default app icon if one is set by the entry point
        if QIcon.hasThemeIcon("application-icon"):
            self.setWindowIcon(QIcon.fromTheme("application-icon"))

        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Patients", central)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setProperty("class", "h1")

        subtitle = QLabel("Manage patient records in a simplified flow.", central)
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        button_row = QHBoxLayout()
        add_btn = QPushButton("Add Patient", central)
        add_btn.clicked.connect(self.add_patient)
        refresh_btn = QPushButton("Refresh", central)
        refresh_btn.clicked.connect(self.refresh_patients)
        new_checkup_btn = QPushButton("New Checkup", central)
        new_checkup_btn.clicked.connect(self.add_checkup)
        new_session_btn = QPushButton("New Session", central)
        new_session_btn.clicked.connect(self.add_session)
        button_row.addWidget(add_btn)
        button_row.addWidget(refresh_btn)
        button_row.addWidget(new_checkup_btn)
        button_row.addWidget(new_session_btn)
        button_row.addStretch(1)

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "CNP"])
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.load_records_for_selected)

        # Right-side details area
        self.records_view = QTextEdit(central)
        self.records_view.setReadOnly(True)

        splitter = QSplitter(central)
        left_panel = QWidget(splitter)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addLayout(button_row)
        left_layout.addWidget(self.table)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.records_view)
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(splitter)
        layout.addStretch(1)

        self.setCentralWidget(central)

        status = QStatusBar(self)
        status.showMessage("Ready")
        self.setStatusBar(status)

        # Initial load if db is attached later
        self._initialized = False

    def attach_db_and_load(self) -> None:
        if getattr(self, "db", None) is None:
            return
        self._initialized = True
        self.refresh_patients()

    def refresh_patients(self) -> None:
        if getattr(self, "db", None) is None:
            return
        persons = self.db.get_all_persons()
        self.table.setRowCount(len(persons))
        for row_index, (pid, name, cnp, _created_at) in enumerate(persons):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(pid)))
            self.table.setItem(row_index, 1, QTableWidgetItem(name))
            self.table.setItem(row_index, 2, QTableWidgetItem(cnp))

        self.statusBar().showMessage(f"Loaded {len(persons)} patients", 1500)
        self.load_records_for_selected()

    def add_patient(self) -> None:
        if getattr(self, "db", None) is None:
            return
        dialog = SimpleAddPatientDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        name, cnp = dialog.get_values()
        if not self.db.add_person(name, cnp):
            self.statusBar().showMessage("Failed to add patient (duplicate CNP?)", 2000)
            return
        self.refresh_patients()
        self.statusBar().showMessage("Patient added", 1500)

    def _get_selected_person_id(self) -> int | None:
        selection = self.table.selectionModel().selectedRows()
        if not selection:
            return None
        row = selection[0].row()
        item = self.table.item(row, 0)
        try:
            return int(item.text()) if item else None
        except Exception:
            return None

    def load_records_for_selected(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.records_view.setPlainText("Select a patient to view records.")
            return
        record = self.db.get_person_complete_record(person_id)
        if not record:
            self.records_view.setPlainText("No records found.")
            return
        person = record.get("person")
        assessments = record.get("assessments", [])
        consultations = record.get("consultations", [])

        lines = []
        lines.append(f"Patient: {person[1]} (CNP: {person[2]})")
        lines.append("")
        lines.append("Checkups:")
        for a in assessments:
            lines.append(f"- {a[1]} | Dx: {a[5]} | Notes: {a[8] if len(a) > 8 else ''}")
        if not assessments:
            lines.append("- None")
        lines.append("")
        lines.append("Sessions:")
        for c in consultations:
            lines.append(f"- {c[1]} [{c[2]}] | Reco: {c[6]} | Notes: {c[9] if len(c) > 9 else ''}")
        if not consultations:
            lines.append("- None")
        self.records_view.setPlainText("\n".join(lines))

    def add_checkup(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage("Select a patient first", 2000)
            return
        dialog = SimpleAddCheckupDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        v = dialog.get_values()
        ok = self.db.add_assessment(
            person_id,
            v["date"],
            v["chief"],
            v["history"],
            v["exam"],
            v["diagnosis"],
            v["plan"],
            v["notes"],
        )
        if not ok:
            self.statusBar().showMessage("Failed to add checkup", 2000)
            return
        self.load_records_for_selected()
        self.statusBar().showMessage("Checkup added", 1500)

    def add_session(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage("Select a patient first", 2000)
            return
        dialog = SimpleAddSessionDialog(self)
        if dialog.exec() != dialog.DialogCode.Accepted:
            return
        v = dialog.get_values()
        ok = self.db.add_consultation(
            person_id,
            v["date"],
            v["type"],
            v["symptoms"],
            v["findings"],
            v["recommendations"],
            v["medications"],
            v["next_appointment"],
            v["notes"],
        )
        if not ok:
            self.statusBar().showMessage("Failed to add session", 2000)
            return
        self.load_records_for_selected()
        self.statusBar().showMessage("Session added", 1500)


