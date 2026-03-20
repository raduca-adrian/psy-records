"""
Centralized language settings manager for the PyQt6 application.
Handles language persistence, loading, and application-wide updates.
"""

import os
import json
from typing import Optional, Callable, List
from .app_translator import get_translator, set_language, get_available_locales

class LanguageManager:
    """Manages language settings across the entire application"""
    
    SETTINGS_FILE = 'settings.json'
    DEFAULT_LANGUAGE = 'en'
    
    def __init__(self):
        self._language_change_callbacks: List[Callable] = []
        self._current_language = self.DEFAULT_LANGUAGE
        
        # Load language preference and update global translator
        self.load_language_preference()
    
    def load_language_preference(self) -> str:
        """Load saved language preference from settings file."""
        try:
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    saved_locale = settings.get('language', self.DEFAULT_LANGUAGE)
                    self._current_language = saved_locale
                    # Ensure the global translator is updated
                    set_language(saved_locale)
                    return saved_locale
        except Exception as e:
            print(f"Failed to load language preference: {e}")
        
        # Fallback to default
        self._current_language = self.DEFAULT_LANGUAGE
        set_language(self.DEFAULT_LANGUAGE)
        return self.DEFAULT_LANGUAGE
    
    def save_language_preference(self, locale: str) -> bool:
        """Save language preference to settings file."""
        try:
            settings = {}
            if os.path.exists(self.SETTINGS_FILE):
                with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
            
            settings['language'] = locale
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to save language preference: {e}")
            return False
    
    def change_language(self, locale: str) -> bool:
        """Change the application language and notify all registered components."""
        if locale not in get_available_locales():
            print(f"Unsupported language: {locale}")
            return False
        
        # Update the global translator
        set_language(locale)
        self._current_language = locale
        
        # Save to settings
        self.save_language_preference(locale)
        
        # Notify all registered components
        for callback in self._language_change_callbacks:
            try:
                callback(locale)
            except Exception as e:
                print(f"Error in language change callback: {e}")
        
        return True
    
    def register_language_change_callback(self, callback: Callable[[str], None]):
        """Register a callback to be called when language changes."""
        if callback not in self._language_change_callbacks:
            self._language_change_callbacks.append(callback)
    
    def unregister_language_change_callback(self, callback: Callable[[str], None]):
        """Unregister a language change callback."""
        if callback in self._language_change_callbacks:
            self._language_change_callbacks.remove(callback)
    
    def get_current_language(self) -> str:
        """Get the current language code."""
        return self._current_language
    
    def get_available_languages(self) -> List[str]:
        """Get list of available language codes."""
        return get_available_locales()
    
    def get_language_display_name(self, locale: str) -> str:
        """Get display name for a language code."""
        language_names = {
            'en': 'English',
            'ro': 'Română'
        }
        return language_names.get(locale, locale)

# Global language manager instance
_language_manager = None

def get_language_manager() -> LanguageManager:
    """Get the global language manager instance."""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager

def get_text(key: str, default: str = None) -> str:
    """Convenience function to get translated text."""
    from .app_translator import get_text as translator_get_text
    return translator_get_text(key, default or key)
