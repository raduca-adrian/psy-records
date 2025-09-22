from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QSplitter,
)


class ColumnContent(QWidget):
    def __init__(self, title: str, body: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        header = QHBoxLayout()
        self.title_label = QLabel(title, self)
        self.title_label.setProperty("class", "h2")
        close_btn = QPushButton("×", self)
        close_btn.setFixedWidth(28)
        close_btn.clicked.connect(self._close_self)
        header.addWidget(self.title_label)
        header.addStretch(1)
        header.addWidget(close_btn)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.text.setPlainText(body)

        layout.addLayout(header)
        layout.addWidget(self.text)

    def _close_self(self) -> None:
        parent_splitter = self.parent()
        # Remove self from splitter
        if isinstance(parent_splitter, QSplitter):
            index = parent_splitter.indexOf(self)
            if index >= 0:
                widget = parent_splitter.widget(index)
                parent_splitter.widget(index).setParent(None)
                del widget


class ColumnManager(QSplitter):
    """Manages a horizontal set of columns that can be added/removed at runtime."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setChildrenCollapsible(False)

    def add_text_column(self, title: str, body: str) -> None:
        column = ColumnContent(title, body, self)
        self.addWidget(column)
        # Stretch newer columns more modestly
        count = self.count()
        for i in range(count):
            self.setStretchFactor(i, 1 if i < count - 1 else 2)


