"""
Global translator instance for the application.
Ensures consistent language selection across all screens.
"""

from .translator import Translator

# Global translator instance
_translator_instance = None

def get_translator():
    """Get the global translator instance."""
    global _translator_instance
    if _translator_instance is None:
        _translator_instance = Translator('en')  # Default to English
    return _translator_instance

def set_language(locale: str):
    """Set the language for the entire application."""
    translator = get_translator()
    translator.change_locale(locale)
    
def get_text(key: str, default: str = None) -> str:
    """Get translated text using the global translator."""
    return get_translator().get_text(key, default)

def get_available_locales():
    """Get list of available locales."""
    return ['en', 'ro']
