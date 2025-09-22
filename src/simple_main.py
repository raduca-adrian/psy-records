"""
Entry point for the simplified application.
Independent of the full secure/login/theme stack so it starts instantly.
"""

from __future__ import annotations

import os
import sys

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygon
from PyQt6.QtWidgets import QApplication, QMessageBox

from .ui.simple_main_window import SimpleMainWindow
from .core.database import DatabaseManager
from .ui.simple_password_dialog import SimplePasswordDialog


def _create_basic_app_icon(app: QApplication) -> None:
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    painter.setBrush(QColor(52, 152, 219))
    painter.setPen(QColor(41, 128, 185))

    points = [
        (32, 5),
        (50, 15),
        (50, 40),
        (32, 58),
        (14, 40),
        (14, 15),
    ]
    polygon = QPolygon([QPoint(x, y) for x, y in points])
    painter.drawPolygon(polygon)
    painter.end()

    app.setWindowIcon(QIcon(pixmap))


def main() -> int:
    # Basic HiDPI settings to avoid blurry text
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("Psychological Records – Simple")
    app.setOrganizationName("Psychological Practice Management")
    app.setApplicationVersion("0.1.0")

    _create_basic_app_icon(app)

    # Database unlock/initialize flow
    db = DatabaseManager()
    initializing = not os.path.exists(db.encrypted_db_path)
    pwd_dialog = SimplePasswordDialog(initializing)
    if pwd_dialog.exec() != pwd_dialog.DialogCode.Accepted:
        return 0
    password = pwd_dialog.get_password()

    if initializing:
        if not db.initialize_database(password):
            QMessageBox.critical(None, "Database Error", "Failed to initialize database.")
            return 1

    if not db.connect(password):
        QMessageBox.critical(None, "Database Error", "Invalid password or database error.")
        return 1

    # Ensure an initial user exists for completeness (optional, but harmless)
    try:
        if not db.user_exists("admin"):
            db.create_user("admin", password)
    except Exception:
        pass

    window = SimpleMainWindow()
    window.db = db
    window.attach_db_and_load()
    window.show()
    result = app.exec()
    db.close()
    return result


if __name__ == "__main__":
    sys.exit(main())


