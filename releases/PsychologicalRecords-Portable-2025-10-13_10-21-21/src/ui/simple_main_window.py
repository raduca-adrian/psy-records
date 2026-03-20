"""
A minimal PyQt6 main window to run a simplified version of the app.
Keeps zero coupling to the complex application to allow quick iteration.
"""

import os
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


from .add_patient_dialog import AddPatientDialog
from .add_checkup_dialog import AddCheckupDialog
from .add_session_dialog import AddSessionDialog
from .edit_checkup_dialog import EditCheckupDialog
from .edit_session_dialog import EditSessionDialog
from .select_record_dialog import SelectRecordDialog
from ..utils.pdf_generator import generate_psychological_report
from ..utils.language_manager import get_language_manager, get_text as _t


class SimpleMainWindow(QMainWindow):
    """Minimal, self-contained main window for rapid prototyping."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.language_manager = get_language_manager()
        self.setWindowTitle(_t('app.title', 'Psychological Records – Simple'))
        self.setMinimumSize(800, 500)

        # Optional: use default app icon if one is set by the entry point
        if QIcon.hasThemeIcon("application-icon"):
            self.setWindowIcon(QIcon.fromTheme("application-icon"))

        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel(_t('main_window.psychological_records', 'Patients'), central)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title.setProperty("class", "h1")

        subtitle = QLabel(_t('main_window.about_text', 'Manage patient records in a simplified flow.'), central)
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        button_row = QHBoxLayout()
        add_btn = QPushButton(_t('menu.add_person', 'Add Patient'), central)
        add_btn.clicked.connect(self.add_patient)
        refresh_btn = QPushButton(_t('menu.refresh', 'Refresh'), central)
        refresh_btn.clicked.connect(self.refresh_patients)
        new_checkup_btn = QPushButton(_t('psychological_records.new_assessment', 'New Checkup'), central)
        new_checkup_btn.clicked.connect(self.add_checkup)
        new_session_btn = QPushButton(_t('psychological_records.new_session', 'New Session'), central)
        new_session_btn.clicked.connect(self.add_session)
        edit_checkup_btn = QPushButton(_t('psychological_records.edit', 'Edit Checkup'), central)
        edit_checkup_btn.clicked.connect(self.edit_checkup)
        edit_session_btn = QPushButton(_t('psychological_records.edit', 'Edit Session'), central)
        edit_session_btn.clicked.connect(self.edit_session)
        export_pdf_btn = QPushButton(_t('psychological_records.generate_report', 'Export PDF'), central)
        export_pdf_btn.clicked.connect(self.export_pdf)
        button_row.addWidget(add_btn)
        button_row.addWidget(refresh_btn)
        button_row.addWidget(new_checkup_btn)
        button_row.addWidget(new_session_btn)
        button_row.addWidget(edit_checkup_btn)
        button_row.addWidget(edit_session_btn)
        button_row.addWidget(export_pdf_btn)
        button_row.addStretch(1)

        self.table = QTableWidget(0, 3, central)
        self.table.setHorizontalHeaderLabels([
            _t('main_window.id', 'ID'),
            _t('main_window.name', 'Name'),
            _t('main_window.cnp', 'CNP'),
        ])
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
        dialog = AddPatientDialog(self)
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
            self.records_view.setPlainText(_t('main_window.select_person_records', 'Select a patient to view records.'))
            return
        record = self.db.get_person_complete_record(person_id)
        if not record:
            self.records_view.setPlainText(_t('psychological_records.no_data_found', 'No records found.'))
            return
        person = record.get("person")
        assessments = record.get("assessments", [])
        consultations = record.get("consultations", [])

        lines = []
        lines.append(f"{_t('pdf.client_name', 'Client Name:')} {person[1]} ({_t('pdf.cnp','CNP')}: {person[2]})")
        lines.append("")
        lines.append(_t('pdf.psychological_assessments', 'Checkups:'))
        for a in assessments:
            lines.append(f"- {a[1]} | Dx: {a[5]} | Notes: {a[8] if len(a) > 8 else ''}")
        if not assessments:
            lines.append("- None")
        lines.append("")
        lines.append(_t('pdf.therapy_sessions', 'Sessions:'))
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
            self.statusBar().showMessage(_t('main_window.select_person_records', 'Select a patient first'), 2000)
            return
        dialog = AddCheckupDialog(self)
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
            self.statusBar().showMessage(_t('common.error', 'Failed to add checkup'), 2000)
            return
        self.load_records_for_selected()
        self.statusBar().showMessage("Checkup added", 1500)

    def add_session(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage(_t('main_window.select_person_records', 'Select a patient first'), 2000)
            return
        dialog = AddSessionDialog(self)
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
            self.statusBar().showMessage(_t('common.error', 'Failed to add session'), 2000)
            return
        self.load_records_for_selected()
        self.statusBar().showMessage("Session added", 1500)

    def edit_checkup(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage(_t('main_window.select_person_records', 'Select a patient first'), 2000)
            return
        assessments = self.db.get_assessments_for_person(person_id)
        items = [(a[0], f"{a[1]} - {a[5] or 'No diagnosis'}") for a in assessments]
        dlg = SelectRecordDialog("Select Checkup", items, self)
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        rec_id = dlg.get_selected_id()
        if rec_id is None:
            return
        current = next((a for a in assessments if a[0] == rec_id), None)
        if not current:
            return
        edit = EditCheckupDialog(current, self)
        if edit.exec() != edit.DialogCode.Accepted:
            return
        v = edit.get_values()
        self.db.update_assessment(
            v["assessment_id"],
            v["date"],
            v["chief"],
            v["history"],
            v["exam"],
            v["diagnosis"],
            v["plan"],
            v["notes"],
        )
        self.load_records_for_selected()
        self.statusBar().showMessage("Checkup updated", 1500)

    def edit_session(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage("Select a patient first", 2000)
            return
        consultations = self.db.get_consultations_for_person(person_id)
        items = [(c[0], f"{c[1]} - {c[2]}") for c in consultations]
        dlg = SelectRecordDialog("Select Session", items, self)
        if dlg.exec() != dlg.DialogCode.Accepted:
            return
        rec_id = dlg.get_selected_id()
        if rec_id is None:
            return
        current = next((c for c in consultations if c[0] == rec_id), None)
        if not current:
            return
        edit = EditSessionDialog(current, self)
        if edit.exec() != edit.DialogCode.Accepted:
            return
        v = edit.get_values()
        self.db.update_consultation(
            v["consultation_id"],
            v["date"],
            v["type"],
            v["symptoms"],
            v["findings"],
            v["recommendations"],
            v["medications"],
            v["next_appointment"],
            v["notes"],
        )
        self.load_records_for_selected()
        self.statusBar().showMessage("Session updated", 1500)

    def export_pdf(self) -> None:
        if getattr(self, "db", None) is None:
            return
        person_id = self._get_selected_person_id()
        if person_id is None:
            self.statusBar().showMessage("Select a patient first", 2000)
            return
        record = self.db.get_person_complete_record(person_id)
        if not record:
            self.statusBar().showMessage(_t('psychological_records.no_data_found', 'No data to export'), 2000)
            return
        person = record.get("person")
        assessments = record.get("assessments", [])
        consultations = record.get("consultations", [])
        out_dir = "data"
        os.makedirs(out_dir, exist_ok=True)
        safe_name = (person[1] or "patient").replace(" ", "_")
        path = os.path.join(out_dir, f"Report_{safe_name}.pdf")
        try:
            generate_psychological_report(person, assessments, consultations, path)
            self.statusBar().showMessage(_t('psychological_records.report_generated', 'Exported') + f" → {path}", 3000)
        except Exception:
            self.statusBar().showMessage(_t('psychological_records.report_failed', 'Failed to export PDF'), 3000)


