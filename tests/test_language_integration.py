#!/usr/bin/env python3
"""Test script to verify psychological records window language integration"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils.language_manager import get_language_manager
from src.utils.app_translator import get_translator

def test_language_integration():
    print("Testing language integration for psychological records...")
    print()
    
    # Test 1: Language manager initialization
    print("Test 1: Language Manager Initialization")
    lm = get_language_manager()
    current_lang = lm.get_current_language()
    print(f"Current language: {current_lang}")
    
    # Test 2: Translation keys for psychological records
    print("\nTest 2: Psychological Records Translation Keys")
    translator = get_translator()
    
    test_keys = [
        "psychological_records.title",
        "psychological_records.new_assessment", 
        "psychological_records.new_session",
        "psychological_records.generate_report",
        "psychological_records.assessments_tab",
        "psychological_records.sessions_tab",
        "psychological_records.date",
        "psychological_records.actions",
        "common.edit",
        "common.delete",
        "main_window.refresh"
    ]
    
    print(f"Testing translation keys in language '{current_lang}':")
    for key in test_keys:
        translation = translator.get_text(key)
        print(f"  {key}: {translation}")
    
    # Test 3: Language switching
    print("\nTest 3: Language Switching")
    original_lang = current_lang
    target_lang = 'en' if current_lang == 'ro' else 'ro'
    
    print(f"Switching from {original_lang} to {target_lang}...")
    success = lm.change_language(target_lang)
    
    if success:
        print("Language change successful!")
        new_translator = get_translator()
        print(f"Sample translation after change: '{new_translator.get_text('psychological_records.title')}'")
        
        # Switch back
        lm.change_language(original_lang)
        print(f"Switched back to {original_lang}")
    else:
        print("Language change failed!")
    
    print("\n✅ Language integration test completed!")

if __name__ == "__main__":
    test_language_integration()
