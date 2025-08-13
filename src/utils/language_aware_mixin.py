"""
Language support mixin for PyQt6 dialogs and windows.
Provides automatic language change handling and text updates.
"""

from abc import ABC, abstractmethod
from src.utils.language_manager import get_language_manager, get_text

class LanguageAwareMixin(ABC):
    """
    Mixin class to add language awareness to PyQt6 widgets.
    
    Classes that inherit from this mixin should:
    1. Call self.setup_language_support() in their __init__ method
    2. Implement the abstract update_ui_texts() method
    3. Use self.get_text() for all translatable strings
    """
    
    def setup_language_support(self):
        """Initialize language support for this widget."""
        self.language_manager = get_language_manager()
        self.language_manager.register_language_change_callback(self.on_language_updated)
    
    def cleanup_language_support(self):
        """Clean up language support (call in closeEvent or destructor)."""
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
    
    def on_language_updated(self, locale: str):
        """Called when language changes anywhere in the application."""
        self.update_ui_texts()
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for the given key."""
        return get_text(key, default or key)
    
    @abstractmethod
    def update_ui_texts(self):
        """Update all translatable UI elements. Must be implemented by subclasses."""
        pass

class LanguageAwareDialog:
    """
    Base class for dialogs that support automatic language updates.
    
    Usage:
        class MyDialog(QDialog, LanguageAwareDialog):
            def __init__(self):
                super().__init__()
                self.setup_language_support()
                self.init_ui()
            
            def update_ui_texts(self):
                self.setWindowTitle(self.get_text('my_dialog.title'))
                # Update other UI elements...
            
            def closeEvent(self, event):
                self.cleanup_language_support()
                super().closeEvent(event)
    """
    
    def setup_language_support(self):
        """Initialize language support for this dialog."""
        self.language_manager = get_language_manager()
        self.language_manager.register_language_change_callback(self.on_language_updated)
    
    def cleanup_language_support(self):
        """Clean up language support."""
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
    
    def on_language_updated(self, locale: str):
        """Called when language changes anywhere in the application."""
        try:
            self.update_ui_texts()
        except Exception as e:
            print(f"Error updating UI texts in {self.__class__.__name__}: {e}")
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for the given key."""
        return get_text(key, default or key)
    
    def update_ui_texts(self):
        """Update all translatable UI elements. Should be overridden by subclasses."""
        pass

class LanguageAwareMainWindow:
    """
    Base class for main windows that support automatic language updates.
    
    Usage similar to LanguageAwareDialog but for QMainWindow subclasses.
    """
    
    def setup_language_support(self):
        """Initialize language support for this main window."""
        self.language_manager = get_language_manager()
        self.language_manager.register_language_change_callback(self.on_language_updated)
    
    def cleanup_language_support(self):
        """Clean up language support."""
        if hasattr(self, 'language_manager'):
            self.language_manager.unregister_language_change_callback(self.on_language_updated)
    
    def on_language_updated(self, locale: str):
        """Called when language changes anywhere in the application."""
        try:
            self.update_ui_texts()
        except Exception as e:
            print(f"Error updating UI texts in {self.__class__.__name__}: {e}")
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for the given key."""
        return get_text(key, default or key)
    
    def update_ui_texts(self):
        """Update all translatable UI elements. Should be overridden by subclasses."""
        pass
