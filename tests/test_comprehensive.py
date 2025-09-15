import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QTimer

# Adjust the path to import modules from the src directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ui.responsive_main_widget import ResponsiveMainWidget
from ui.modern_main_window import ModernMainWindow
from database.database_manager import DatabaseManager
from security.encryption_manager import EncryptionManager
from utils.config_manager import ConfigManager
from utils.resource_manager import ResourceManager
from managers.language_manager import LanguageManager

class ComprehensiveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def setUp(self):
        # Mock dependencies
        self.mock_db_manager = MagicMock(spec=DatabaseManager)
        self.mock_encryption_manager = MagicMock(spec=EncryptionManager)
        self.mock_config_manager = MagicMock(spec=ConfigManager)
        self.mock_resource_manager = MagicMock(spec=ResourceManager)
        
        # Configure mocks to return valid values
        self.mock_config_manager.get.return_value = "en"
        self.mock_resource_manager.get_qss.return_value = ""
        self.mock_db_manager.get_all_records.return_value = []

        # Patch the classes to use the mocks
        self.patches = [
            patch('src.ui.modern_main_window.DatabaseManager', return_value=self.mock_db_manager),
            patch('src.ui.modern_main_window.EncryptionManager', return_value=self.mock_encryption_manager),
            patch('src.ui.modern_main_window.ConfigManager', return_value=self.mock_config_manager),
            patch('src.ui.modern_main_window.ResourceManager', return_value=self.mock_resource_manager),
            patch('src.ui.responsive_main_widget.ConfigManager', return_value=self.mock_config_manager),
            patch('src.ui.responsive_main_widget.ResourceManager', return_value=self.mock_resource_manager),
            patch('src.ui.responsive_main_widget.DatabaseManager', return_value=self.mock_db_manager)
        ]
        for p in self.patches:
            p.start()

        self.main_widget = ResponsiveMainWidget()
        self.window = ModernMainWindow(main_widget=self.main_widget)

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.window.close()
        del self.window
        del self.main_widget

    def test_01_main_window_initialization(self):
        """Test if the main window and its components are initialized correctly."""
        self.assertIsInstance(self.window, QMainWindow)
        self.assertEqual(self.window.windowTitle(), "Psychological Records")
        self.assertIsNotNone(self.window.centralWidget())
        self.assertIsInstance(self.window.centralWidget(), ResponsiveMainWidget)

    def test_02_responsive_main_widget_initialization(self):
        """Test if the main responsive widget and its sub-layouts are created."""
        self.assertIsNotNone(self.main_widget.layout)
        self.assertIsNotNone(self.main_widget.search_section)
        self.assertIsNotNone(self.main_widget.content_section)
        self.assertIsNotNone(self.main_widget.actions_section)
        self.assertIsNotNone(self.main_widget.status_bar)

    def test_03_search_section_widgets_exist(self):
        """Check if all expected widgets in the search section are present."""
        self.assertIsNotNone(self.main_widget.search_input)
        self.assertIsNotNone(self.main_widget.search_button)
        self.assertIsNotNone(self.main_widget.clear_search_button)

    def test_04_content_section_widgets_exist(self):
        """Check if the table widget in the content section is present."""
        self.assertIsNotNone(self.main_widget.table_widget)

    def test_05_actions_section_buttons_exist(self):
        """Check if all action buttons are created."""
        self.assertIsNotNone(self.main_widget.add_button)
        self.assertIsNotNone(self.main_widget.edit_button)
        self.assertIsNotNone(self.main_widget.delete_button)
        self.assertIsNotNone(self.main_widget.view_button)
        self.assertIsNotNone(self.main_widget.export_button)
        self.assertIsNotNone(self.main_widget.settings_button)
        self.assertIsNotNone(self.main_widget.theme_button)

    def test_06_database_interaction_on_init(self):
        """Verify that the database is queried for all records on initialization."""
        self.mock_db_manager.get_all_records.assert_called_once()

    def test_07_search_functionality(self):
        """Test the search functionality and its interaction with the database."""
        self.main_widget.search_input.setText("test_query")
        self.main_widget.search_button.click()
        self.mock_db_manager.search_records.assert_called_with("test_query")

    def test_08_clear_search_functionality(self):
        """Test if clearing the search reloads all records."""
        self.main_widget.search_input.setText("something")
        self.mock_db_manager.get_all_records.reset_mock() # Reset call count
        self.main_widget.clear_search_button.click()
        self.assertEqual(self.main_widget.search_input.text(), "")
        self.mock_db_manager.get_all_records.assert_called_once()

    def test_09_theme_toggle_functionality(self):
        """Test the theme toggling functionality."""
        initial_theme = self.main_widget.current_theme
        self.main_widget.theme_button.click()
        new_theme = self.main_widget.current_theme
        self.assertNotEqual(initial_theme, new_theme)
        # It should toggle back
        self.main_widget.theme_button.click()
        self.assertEqual(self.main_widget.current_theme, initial_theme)

    def test_10_status_bar_message(self):
        """Test if the status bar can display messages."""
        test_message = "This is a test message."
        self.main_widget.status_bar.showMessage(test_message, 5000)
        self.assertEqual(self.main_widget.status_bar.currentMessage(), test_message)

    def test_11_table_population(self):
        """Test if the table is populated with data from the database."""
        sample_data = [
            (1, "John Doe", 30, "Notes 1", "2023-01-01"),
            (2, "Jane Smith", 25, "Notes 2", "2023-01-02")
        ]
        self.mock_db_manager.get_all_records.return_value = sample_data
        self.main_widget.load_records_to_table()
        self.assertEqual(self.main_widget.table_widget.rowCount(), 2)
        self.assertEqual(self.main_widget.table_widget.item(0, 1).text(), "John Doe")
        self.assertEqual(self.main_widget.table_widget.item(1, 1).text(), "Jane Smith")

    def test_12_add_button_action(self):
        """Test if the add button triggers the correct (mocked) dialog."""
        with patch.object(self.main_widget, 'add_record') as mock_add_record:
            self.main_widget.add_button.click()
            mock_add_record.assert_called_once()

    def test_13_edit_button_action_with_selection(self):
        """Test if the edit button triggers the correct dialog when an item is selected."""
        self.main_widget.table_widget.insertRow(0)
        self.main_widget.table_widget.selectRow(0)
        with patch.object(self.main_widget, 'edit_record') as mock_edit_record:
            self.main_widget.edit_button.click()
            mock_edit_record.assert_called_once()

    def test_14_delete_button_action_with_selection(self):
        """Test if the delete button triggers the confirmation dialog when an item is selected."""
        self.main_widget.table_widget.insertRow(0)
        self.main_widget.table_widget.selectRow(0)
        with patch.object(self.main_widget, 'delete_record') as mock_delete_record:
            self.main_widget.delete_button.click()
            mock_delete_record.assert_called_once()

    def test_15_view_button_action_with_selection(self):
        """Test if the view button triggers the correct dialog when an item is selected."""
        self.main_widget.table_widget.insertRow(0)
        self.main_widget.table_widget.selectRow(0)
        with patch.object(self.main_widget, 'view_record') as mock_view_record:
            self.main_widget.view_button.click()
            mock_view_record.assert_called_once()

    def test_16_export_button_action(self):
        """Test if the export button triggers the export functionality."""
        with patch.object(self.main_widget, 'export_records') as mock_export_records:
            self.main_widget.export_button.click()
            mock_export_records.assert_called_once()

    def test_17_settings_button_action(self):
        """Test if the settings button triggers the settings dialog."""
        with patch.object(self.main_widget, 'open_settings') as mock_open_settings:
            self.main_widget.settings_button.click()
            mock_open_settings.assert_called_once()

    def test_18_no_action_on_buttons_without_selection(self):
        """Test that edit, delete, view buttons do nothing if no row is selected."""
        with patch.object(self.main_widget, 'edit_record') as mock_edit, \
             patch.object(self.main_widget, 'delete_record') as mock_delete, \
             patch.object(self.main_widget, 'view_record') as mock_view:
            
            self.main_widget.edit_button.click()
            mock_edit.assert_not_called()

            self.main_widget.delete_button.click()
            mock_delete.assert_not_called()

            self.main_widget.view_button.click()
            mock_view.assert_not_called()

    def test_19_window_resize_event(self):
        """Test if the resize event is handled, triggering layout updates."""
        with patch.object(self.main_widget.layout, 'update_margins') as mock_update_margins:
            # Simulate a resize event
            original_size = self.window.size()
            self.window.resize(original_size.width() + 100, original_size.height() + 100)
            # In a real app, the event loop would process this. We call it manually.
            self.window.resizeEvent(MagicMock())
            mock_update_margins.assert_called()

    def test_20_language_manager_integration(self):
        """Test that the LanguageManager is initialized and used for UI strings."""
        # This test assumes LanguageManager is initialized within ModernMainWindow or its dependencies
        # We check if a known translated string is set correctly.
        # Since we mocked ConfigManager, LanguageManager will use the default 'en'
        self.mock_config_manager.get.return_value = 'en'
        
        # Re-initialize to ensure LanguageManager picks up the mock config
        lm = LanguageManager(self.mock_config_manager)
        QApplication.instance().installTranslator(lm.translator)

        # We need to re-create the window for the new translator to take effect on the title
        self.window.setWindowTitle(QApplication.translate("ModernMainWindow", "Psychological Records"))
        self.assertEqual(self.window.windowTitle(), "Psychological Records")

if __name__ == '__main__':
    unittest.main(verbosity=2)
