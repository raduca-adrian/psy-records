# Bilingual Support (English & Romanian)

## Overview

The Psychological Records application now features complete bilingual support with:
- **English (en)** - Full UI translation
- **Română (ro)** - Full UI translation
- Language selection on first run
- Runtime language switching
- Persistent language preference

## Features

### 🌍 Language Selection on First Run

When you first launch the application, you'll see a language selection dialog:
- Bilingual welcome message
- Clear language options with flags (🇬🇧 English, 🇷🇴 Română)
- Easy-to-use interface
- Your selection is saved for future sessions

### 🔄 Runtime Language Switching

Switch languages anytime without restarting:
1. Click the language button in the status bar (🌍)
2. Select your preferred language
3. The UI updates immediately

The language button shows your current language:
- **English**: 🌍 English
- **Romanian**: 🌍 Română

### 💾 Persistent Language Preference

Your language choice is automatically saved and restored:
- Stored in application settings
- Persists across sessions
- No need to reconfigure

## Supported Languages

### English (en)
Complete translations for:
- All UI elements (buttons, labels, tabs)
- Form fields and placeholders
- Messages and notifications
- Tooltips and hints
- Status bar messages
- Error messages

### Română (ro)
Complete translations for:
- All UI elements (butoane, etichete, file)
- Câmpuri de formular și indicii
- Mesaje și notificări
- Sfaturi și indicații
- Mesaje din bara de stare
- Mesaje de eroare

## Usage

### For Users

#### Changing Language
1. Click the **🌍** button in the bottom-right status bar
2. Select your preferred language from the dialog
3. Click **OK**
4. The interface updates immediately

#### First-Time Setup
On first launch:
1. A bilingual dialog appears
2. Select your preferred language
3. Click **OK**
4. The application opens with your chosen language

### For Developers

#### Translation Architecture

**Language Manager** (`src/utils/language_manager.py`):
```python
from src.utils.language_manager import get_language_manager, get_text as _t

# Get language manager
lang_manager = get_language_manager()

# Get current language
current_lang = lang_manager.get_current_language()  # 'en' or 'ro'

# Change language
lang_manager.change_language('ro')

# Use translations
text = _t('app.title', 'Default Text')
```

**Translation Files**:
- `locales/en/translations.json` - English translations
- `locales/ro/translations.json` - Romanian translations

**Translation Keys Structure**:
```json
{
  "app": { "title": "..." },
  "tabs": { "patients": "...", "add_patient": "..." },
  "common": { "add": "...", "edit": "...", "delete": "..." },
  "patient_form": { "title": "...", "name_label": "..." },
  "checkup_form": { "title_add": "...", "date_label": "..." },
  "session_form": { "title_add": "...", "type_label": "..." },
  "language": { "selection_title": "...", "language_changed": "..." }
}
```

#### Adding New Translations

1. **Add English translation** (`locales/en/translations.json`):
```json
{
  "my_section": {
    "my_key": "My English Text"
  }
}
```

2. **Add Romanian translation** (`locales/ro/translations.json`):
```json
{
  "my_section": {
    "my_key": "Textul Meu în Română"
  }
}
```

3. **Use in code**:
```python
text = _t('my_section.my_key', 'Fallback Text')
```

#### Best Practices

1. **Always use translation keys**:
   ```python
   # ✓ Good
   title = _t('app.title', 'Psychological Records')
   
   # ✗ Bad
   title = "Psychological Records"
   ```

2. **Provide fallback text**:
   ```python
   # ✓ Good - has fallback
   text = _t('section.key', 'Default Text')
   
   # ⚠ Acceptable - uses key as fallback
   text = _t('section.key')
   ```

3. **Update UI on language change**:
   ```python
   def _reload_ui_text(self):
       """Update all visible text after language change."""
       self.setWindowTitle(_t('app.title'))
       self.my_button.setText(_t('common.save'))
       # ... update all text elements
   ```

4. **Use consistent key naming**:
   - `section.key` format
   - Lowercase with underscores
   - Descriptive names

## Translation Coverage

### Complete Translations For:

✅ **Application**
- Window title
- Status bar messages
- About information

✅ **Tabs**
- Patients tab
- Add Patient tab
- Checkup tab
- Session tab
- Tab tooltips

✅ **Forms**
- Patient form (add/edit)
- Checkup form (add/edit)
- Session form (add/edit)
- All field labels and placeholders

✅ **Common UI**
- Buttons (Add, Edit, Delete, Clear, Save, Cancel)
- Messages (Success, Error, Warning, Info)
- Actions (Export PDF, Refresh, etc.)

✅ **Theme Controls**
- Dark mode button
- Light mode button
- Theme activation messages

✅ **Language Controls**
- Language selection dialog
- Language change messages
- Language display names

## Technical Details

### Language Persistence

Language preference is stored using `QSettings`:
```python
QSettings('PsychologicalRecords', 'UnifiedApp')
```

Storage location:
- **Windows**: Registry (`HKEY_CURRENT_USER\Software\PsychologicalRecords\UnifiedApp`)
- **Linux**: `~/.config/PsychologicalRecords/UnifiedApp.conf`
- **macOS**: `~/Library/Preferences/com.PsychologicalRecords.UnifiedApp.plist`

### Language Loading Sequence

1. Application starts
2. Check if `language_configured` exists
3. If first run:
   - Show language selection dialog
   - Save choice
   - Set `language_configured = true`
4. If not first run:
   - Load saved language preference
   - Apply language

### Translation System

The translation system uses a centralized architecture:

```
┌─────────────────────────────────────┐
│      Application Startup            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      Language Manager               │
│  - Load preference from QSettings   │
│  - Initialize translator            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      App Translator                 │
│  - Load JSON translation files      │
│  - Provide _t() function            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│      UI Components                  │
│  - Use _t() for all text            │
│  - Update on language change        │
└─────────────────────────────────────┘
```

## Testing

Run the comprehensive language test suite:

```bash
python test_language_support.py
```

This tests:
- Language manager functionality
- English translations
- Romanian translations
- Language persistence
- Display names
- Translation coverage

## Future Enhancements

Potential additions:
- [ ] Additional languages (French, German, etc.)
- [ ] User-contributed translations
- [ ] Translation editor tool
- [ ] Context-aware translations
- [ ] Pluralization support
- [ ] Date/time format localization

## Support

For translation issues or suggestions:
1. Check translation files in `locales/`
2. Verify key naming matches pattern
3. Run language test suite
4. Report issues with specific keys

---

**Version**: 0.5.0  
**Languages**: English (en), Română (ro)  
**Status**: ✅ Production Ready

