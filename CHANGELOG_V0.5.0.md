# Changelog - Version 0.5.0

## 🌍 Bilingual Support Release

**Release Date**: October 12, 2025  
**Focus**: Complete bilingual support (English & Romanian)

---

## 🎯 Major Features

### ✨ Full Bilingual Support

**English & Romanian Languages**:
- ✅ Complete UI translation for both languages
- ✅ All buttons, labels, and forms translated
- ✅ All messages and notifications translated
- ✅ All tooltips and hints translated

**Language Selection**:
- 🆕 Language selection dialog on first run
- 🆕 Bilingual welcome message
- 🆕 Visual language picker with flags (🇬🇧 🇷🇴)
- 🆕 Runtime language switching
- 🆕 Persistent language preference

**Language Controls**:
- 🆕 Language button in status bar (🌍)
- 🆕 Quick access to language switcher
- 🆕 Immediate UI update on language change
- 🆕 No restart required

---

## 📋 New Components

### Language Selector Dialog
**File**: `src/ui/language_selector_dialog.py`
- Modern, user-friendly language selection
- Bilingual labels (English/Romanian)
- Radio button selection
- Material Design styling

### Enhanced Language Manager
**File**: `src/utils/language_manager.py`
- Improved persistence handling
- Language change callbacks
- Display name management
- QSettings integration

---

## 🔄 Enhanced Components

### Unified Main Window
**File**: `src/ui/unified_main_window.py`
- Added language switcher button
- Added `change_language()` method
- Added `_reload_ui_text()` method
- Updated all UI strings to use translations
- Dynamic tab title updates
- Dynamic tooltip updates

### Application Startup
**File**: `src/simple_main.py`
- First-run language detection
- Language selection integration
- Persistent preference loading
- Version updated to 0.5.0

---

## 📝 Translation Files

### English Translations
**File**: `locales/en/translations.json`
- Added 350+ translation keys
- Complete coverage of all UI elements
- Organized by section
- Added new sections:
  - `tabs` - Tab labels and tooltips
  - `patient_form` - Patient form strings
  - `checkup_form` - Checkup form strings
  - `session_form` - Session form strings
  - `language` - Language selection strings

### Romanian Translations
**File**: `locales/ro/translations.json`
- Added 350+ translation keys
- Complete Romanian localization
- Professional medical terminology
- Matches English structure exactly

---

## 🎨 UI/UX Improvements

### Status Bar
- Added language button with flag icon
- Shows current language name
- Click to change language
- Positioned before theme toggle

### Theme Toggle
- Updated to use translations
- Dynamic text based on language
- Localized tooltips

### Tabs
- Translated tab titles with icons
- Translated tab tooltips
- Language-aware accessibility messages

### Forms
- Translated all field labels
- Translated all placeholders
- Translated all buttons
- Translated all validation messages

---

## 🔧 Technical Changes

### Translation Architecture
```
Language Manager → App Translator → UI Components
      ↓                  ↓                ↓
   QSettings      JSON Files        _t() calls
```

### Key Components:
1. **Language Manager** - Centralized language control
2. **App Translator** - Translation file loader
3. **_t() Function** - Translation helper
4. **QSettings** - Persistent storage

### Translation Key Format:
```
section.key
```

Examples:
- `app.title`
- `tabs.patients`
- `common.add_patient`
- `patient_form.name_label`

---

## 🧪 Testing

### New Test Suite
**File**: `test_language_support.py`
- Language manager tests
- English translation tests
- Romanian translation tests
- Persistence tests
- Coverage tests

### Test Results:
```
✓ Available languages detected
✓ English translations verified
✓ Romanian translations verified
✓ Language persistence working
✓ Display names correct
✓ Complete translation coverage
```

---

## 📚 Documentation

### New Documentation
1. **BILINGUAL_SUPPORT.md**
   - Complete bilingual feature guide
   - Usage instructions
   - Developer guide
   - Translation workflow

2. **Updated Files**:
   - README.md (language feature mentioned)
   - KEYBOARD_SHORTCUTS.md (language shortcuts)
   - UNIFIED_APP_SUMMARY.md (v0.5.0 info)

---

## 🔢 Statistics

### Translation Coverage:
- **Total keys**: 350+
- **English**: 100% complete
- **Romanian**: 100% complete
- **Sections**: 11

### Files Changed:
- New files: 2
- Modified files: 5
- Translation files: 2
- Test files: 1
- Documentation: 2

### Code Quality:
- All tests passing ✅
- Language tests passing ✅
- No linter errors ✅
- UTF-8 encoding verified ✅

---

## 🚀 Upgrade Guide

### For Users:
1. Update to v0.5.0
2. On first launch, select your language
3. Use the 🌍 button to change language anytime

### For Developers:
1. Pull latest changes
2. Review `BILINGUAL_SUPPORT.md`
3. Update any hardcoded strings to use `_t()`
4. Test both languages
5. Run `test_language_support.py`

---

## 🐛 Bug Fixes

- Fixed hardcoded strings in UI
- Fixed theme button text updates
- Fixed tab tooltip translations
- Fixed status message translations

---

## 🔮 Future Plans

### v0.6.0 (Planned):
- [ ] Additional languages (French, German)
- [ ] PDF report translations
- [ ] Date format localization
- [ ] Number format localization
- [ ] User manual translations

---

## 📦 Installation

```bash
# Update from repository
git pull origin main

# Install dependencies (if any new)
pip install -r requirements.txt

# Run tests
python test_language_support.py

# Launch application
python -m src.simple_main
```

---

## 🙏 Acknowledgments

Special thanks to:
- Romanian medical terminology resources
- PyQt6 internationalization framework
- Material Design guidelines

---

## 📄 License

Same as project license.

---

**Full Changelog**: v0.4.0...v0.5.0  
**Contributors**: 1  
**Commits**: 15+  
**Files Changed**: 12  
**Lines Added**: 2,500+

