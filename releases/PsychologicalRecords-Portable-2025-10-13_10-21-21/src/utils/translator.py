"""
Translation utility for the Psychological Records Application.
Supports Romanian and English languages.
"""

import json
import os
from typing import Dict, Any

class Translator:
    def __init__(self, locale: str = 'en'):
        self.locale = locale
        self.translations: Dict[str, Any] = {}
        self.load_translations()
    
    def load_translations(self):
        """Load translations for the current locale."""
        locale_path = os.path.join(os.path.dirname(__file__), '..', '..', 'locales', self.locale, 'translations.json')
        locale_path = os.path.abspath(locale_path)
        
        try:
            with open(locale_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print(f"Translation file not found for locale: {self.locale}")
            # Fallback to English if available
            if self.locale != 'en':
                self.locale = 'en'
                self.load_translations()
        except json.JSONDecodeError:
            print(f"Invalid JSON in translation file for locale: {self.locale}")
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text for a given key."""
        keys = key.split('.')
        current = self.translations
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default or key
        
        return current if isinstance(current, str) else (default or key)
    
    def change_locale(self, new_locale: str):
        """Change the current locale and reload translations."""
        self.locale = new_locale
        self.load_translations()
    
    def get_available_locales(self) -> list:
        """Get list of available locales."""
        locales_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'locales')
        locales_dir = os.path.abspath(locales_dir)
        
        locales = []
        if os.path.exists(locales_dir):
            for item in os.listdir(locales_dir):
                locale_path = os.path.join(locales_dir, item)
                if os.path.isdir(locale_path) and os.path.exists(os.path.join(locale_path, 'translations.json')):
                    locales.append(item)
        
        return locales


# Global translator instance
_translator = None

def get_translator() -> Translator:
    """Get the global translator instance."""
    global _translator
    if _translator is None:
        _translator = Translator()
    return _translator

def set_locale(locale: str):
    """Set the global locale."""
    global _translator
    if _translator is None:
        _translator = Translator(locale)
    else:
        _translator.change_locale(locale)

def _(key: str, default: str = None) -> str:
    """Shorthand function for getting translated text."""
    return get_translator().get_text(key, default)
