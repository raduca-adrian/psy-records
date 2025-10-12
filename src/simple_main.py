"""
Entry point for the simplified application.
Independent of the full secure/login/theme stack so it starts instantly.
"""

from __future__ import annotations

import os
import sys

from PyQt6.QtCore import Qt, QPoint, QSettings
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap, QPolygon
from PyQt6.QtWidgets import QApplication, QMessageBox

from .ui.unified_main_window import UnifiedMainWindow
from .core.database import DatabaseManager
from .ui.password_dialog import PasswordDialog
from .ui.language_selector_dialog import select_language_on_startup
from .utils.language_manager import get_language_manager


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
    app.setApplicationName("Psychological Records")
    app.setOrganizationName("Psychological Practice Management")
    app.setApplicationVersion("0.5.0")

    _create_basic_app_icon(app)
    
    # Language selection on first run or if not set
    settings = QSettings('PsychologicalRecords', 'UnifiedApp')
    lang_manager = get_language_manager()
    
    # Check if language has been set before
    if not settings.contains('language_configured'):
        # First run - show language selector
        current_lang = lang_manager.get_current_language()
        selected_lang = select_language_on_startup(current_lang)
        lang_manager.change_language(selected_lang)
        settings.setValue('language_configured', True)
    else:
        # Load saved language preference
        lang_manager.load_language_preference()

    # Database unlock/initialize flow
    db = DatabaseManager()
    initializing = not os.path.exists(db.encrypted_db_path)
    pwd_dialog = PasswordDialog(initializing)
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

    window = UnifiedMainWindow()
    window.db = db
    window.attach_db_and_load()
    window.show()
    result = app.exec()
    db.close()
    return result


if __name__ == "__main__":
    sys.exit(main())


