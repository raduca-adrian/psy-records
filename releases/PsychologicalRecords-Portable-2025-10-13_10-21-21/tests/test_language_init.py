#!/usr/bin/env python3
"""Test language initialization synchronization"""

from src.utils.language_manager import get_language_manager
from src.utils.app_translator import get_translator

print('Testing language manager initialization...')
print()

# Initialize language manager
lm = get_language_manager()
print()

# Check both systems
translator = get_translator()

print(f'Language Manager current language: {lm.get_current_language()}')
print(f'App translator locale: {translator.locale}')
print(f'Translation test: {translator.get_text("login.title")}')
