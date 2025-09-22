from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QWidget,
)


class SimpleSelectRecordDialog(QDialog):
    """Select a record to edit; displays a list of titles mapped to IDs."""

    def __init__(self, title: str, items: list[tuple[int, str]], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self._id_by_row: list[int] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        layout.addWidget(QLabel("Select a record:", self))
        self.list_widget = QListWidget(self)
        for rec_id, label in items:
            self.list_widget.addItem(label)
            self._id_by_row.append(rec_id)
        layout.addWidget(self.list_widget)

        buttons = QHBoxLayout()
        cancel_btn = QPushButton("Cancel", self)
        ok_btn = QPushButton("Edit", self)
        cancel_btn.clicked.connect(self.reject)
        ok_btn.clicked.connect(self.accept)
        buttons.addStretch(1)
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)
        layout.addLayout(buttons)

    def get_selected_id(self) -> int | None:
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self._id_by_row):
            return None
        return self._id_by_row[row]
