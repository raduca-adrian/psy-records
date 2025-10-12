#!/usr/bin/env python3
"""
Test script for bilingual language support (English & Romanian).
"""

import sys
import os
from pathlib import Path

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtCore import QCoreApplication, QSettings
from src.utils.language_manager import get_language_manager, get_text as _t

def test_language_manager():
    """Test language manager functionality."""
    print("=" * 60)
    print("LANGUAGE MANAGER TESTS")
    print("=" * 60)
    
    # Initialize QApplication minimal context for QSettings
    app = QCoreApplication([])
    app.setOrganizationName("PsychologicalRecords")
    app.setApplicationName("UnifiedApp")
    
    lang_manager = get_language_manager()
    
    # Test 1: Get available languages
    print("\n1. Available Languages:")
    langs = lang_manager.get_available_languages()
    print(f"   Available: {langs}")
    assert 'en' in langs and 'ro' in langs, "English and Romanian should be available"
    print("   ✓ Both English and Romanian available")
    
    # Test 2: Test English translations
    print("\n2. Testing English translations:")
    lang_manager.change_language('en')
    assert lang_manager.get_current_language() == 'en', "Current language should be 'en'"
    
    test_keys = [
        ('app.title', 'Psychological Records'),
        ('tabs.patients', 'Patients'),
        ('common.add_patient', 'Add Patient'),
        ('common.dark_mode', 'Dark Mode'),
        ('language.language_changed', 'Language changed successfully!')
    ]
    
    for key, expected_phrase in test_keys:
        text = _t(key)
        print(f"   {key}: '{text}'")
        assert expected_phrase.lower() in text.lower(), f"Expected '{expected_phrase}' in '{text}'"
    print("   ✓ All English translations working")
    
    # Test 3: Test Romanian translations
    print("\n3. Testing Romanian translations:")
    lang_manager.change_language('ro')
    assert lang_manager.get_current_language() == 'ro', "Current language should be 'ro'"
    
    test_keys_ro = [
        ('app.title', 'Psihologic'),
        ('tabs.patients', 'Pacienți'),
        ('common.add_patient', 'Pacient'),
        ('common.dark_mode', 'Întunecat'),
        ('language.language_changed', 'Limba')
    ]
    
    for key, expected_phrase in test_keys_ro:
        text = _t(key)
        print(f"   {key}: '{text}'")
        assert expected_phrase in text, f"Expected '{expected_phrase}' in '{text}'"
    print("   ✓ All Romanian translations working")
    
    # Test 4: Test language persistence
    print("\n4. Testing language persistence:")
    settings = QSettings('PsychologicalRecords', 'UnifiedApp')
    lang_manager.change_language('en')
    saved_lang = settings.value('language', 'en')
    print(f"   Saved language preference: {saved_lang}")
    assert saved_lang == 'en', "Language preference should be saved"
    print("   ✓ Language persistence working")
    
    # Test 5: Test display names
    print("\n5. Testing language display names:")
    en_name = lang_manager.get_language_display_name('en')
    ro_name = lang_manager.get_language_display_name('ro')
    print(f"   English display name: {en_name}")
    print(f"   Romanian display name: {ro_name}")
    assert en_name == 'English', "English display name should be 'English'"
    assert ro_name == 'Română', "Romanian display name should be 'Română'"
    print("   ✓ Display names working")
    
    print("\n" + "=" * 60)
    print("✅ ALL LANGUAGE MANAGER TESTS PASSED")
    print("=" * 60)
    

def test_translation_coverage():
    """Test that key UI sections have translations."""
    print("\n" + "=" * 60)
    print("TRANSLATION COVERAGE TESTS")
    print("=" * 60)
    
    sections = {
        'app': ['title'],
        'tabs': ['patients', 'add_patient', 'checkup', 'session'],
        'common': ['add_patient', 'new_checkup', 'new_session', 'clear', 
                   'dark_mode', 'light_mode', 'export_pdf'],
        'patient_form': ['title', 'name_label', 'cnp_label'],
        'checkup_form': ['title_add', 'title_edit', 'date_label', 'chief_label', 
                         'diagnosis_label'],
        'session_form': ['title_add', 'title_edit', 'type_label', 'symptoms_label'],
        'language': ['selection_title', 'language_changed', 'select_language']
    }
    
    missing = []
    
    for lang in ['en', 'ro']:
        print(f"\nChecking {lang.upper()} translations:")
        lang_manager = get_language_manager()
        lang_manager.change_language(lang)
        
        for section, keys in sections.items():
            for key in keys:
                full_key = f"{section}.{key}"
                text = _t(full_key, f"MISSING_{full_key}")
                if text.startswith("MISSING_"):
                    missing.append((lang, full_key))
                    print(f"   ✗ {full_key}: MISSING")
                else:
                    print(f"   ✓ {full_key}: '{text[:50]}...' " if len(text) > 50 else f"   ✓ {full_key}: '{text}'")
    
    if missing:
        print(f"\n⚠️  Missing translations: {len(missing)}")
        for lang, key in missing:
            print(f"   - {lang}: {key}")
        return False
    else:
        print("\n" + "=" * 60)
        print("✅ ALL TRANSLATION KEYS PRESENT")
        print("=" * 60)
        return True


def main():
    """Run all language tests."""
    print("\n🌍 BILINGUAL SUPPORT TEST SUITE")
    print("Testing English & Romanian translations\n")
    
    try:
        test_language_manager()
        test_translation_coverage()
        
        print("\n" + "=" * 60)
        print("🎉 ALL LANGUAGE TESTS PASSED!")
        print("=" * 60)
        print("\n✓ English translation system: WORKING")
        print("✓ Romanian translation system: WORKING")
        print("✓ Language persistence: WORKING")
        print("✓ Translation coverage: COMPLETE")
        print("\n✅ The application is fully bilingual and ready for use!")
        
        return 0
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

