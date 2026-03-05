# Unified Single Window Application

## Overview

The Psychological Records application has been redesigned as a **unified single window application**. All functionality that was previously spread across multiple dialog windows is now integrated into a single, tabbed interface.

## Key Features

### 1. **Single Window Interface**
- All functionality accessible from one main window
- No more popup dialogs for adding/editing records
- Seamless navigation between different sections

### 2. **Tabbed Navigation**
The application consists of four main tabs:

#### 📋 Patients Tab
- View all patients in a table
- Select a patient to view their complete records
- Quick access to patient actions
- Export PDF reports

#### ➕ Add Patient Tab
- Simple form to add new patients
- Fields: Name, CNP (Personal Numeric Code)
- Clear and Save buttons
- Automatically returns to Patients tab after saving

#### 🩺 Checkup Tab
- Add new medical checkups/assessments
- Edit existing checkups
- Fields include:
  - Date
  - Chief Complaint
  - Medical History
  - Examination
  - Diagnosis
  - Treatment Plan
  - Notes

#### 💬 Session Tab
- Add new therapy sessions/consultations
- Edit existing sessions
- Fields include:
  - Date
  - Session Type (Follow-up, Initial, Telemedicine, Emergency)
  - Symptoms
  - Findings
  - Recommendations
  - Medications
  - Next Appointment
  - Notes

### 3. **Integrated Workflow**

#### Adding Records
1. Select a patient from the Patients tab
2. Click "New Checkup" or "New Session"
3. Fill out the form in the respective tab
4. Click "Add" to save
5. Automatically returns to Patients tab

#### Editing Records
1. Select a patient from the Patients tab
2. Click "Edit Checkup" or "Edit Session"
3. Select the record to edit from the list
4. Modify the form fields
5. Click "Update" to save
6. Automatically returns to Patients tab

#### Viewing Records
- Select any patient from the table
- Records appear in the right panel instantly
- Shows all checkups and sessions for that patient

## Technical Architecture

### File Structure
```
src/
├── simple_main.py              # Entry point
└── ui/
    ├── unified_main_window.py  # Main unified window (NEW)
    ├── password_dialog.py      # Database password dialog
    └── [legacy dialog files]   # Old dialog-based files
```

### Main Components

#### `UnifiedMainWindow` Class
The core of the application, containing:
- Tab management
- Patient list and viewer
- Embedded forms for all operations
- Database integration
- PDF export functionality

#### Key Methods
- `refresh_patients()` - Reload patient list
- `start_add_checkup()` - Switch to add checkup mode
- `start_edit_checkup()` - Switch to edit checkup mode
- `start_add_session()` - Switch to add session mode
- `start_edit_session()` - Switch to edit session mode
- `save_checkup()` - Save or update checkup
- `save_session()` - Save or update session
- `export_pdf()` - Generate PDF report

## Running the Application

### Method 1: Using the run script
```bash
python run_unified.py
```

### Method 2: Running as module
```bash
python -m src.simple_main
```

### Method 3: Using the original run script
```bash
python run.py
```

## Keyboard Shortcuts

The unified application includes convenient keyboard shortcuts for faster navigation:

### Tab Navigation
- **Ctrl+1** - Switch to Patients tab
- **Ctrl+2** - Switch to Add Patient tab
- **Ctrl+3** - Switch to Checkup tab
- **Ctrl+4** - Switch to Session tab

### Quick Actions
- **Ctrl+N** - New Patient (switch to Add Patient tab)
- **Ctrl+R** - Refresh patient list
- **Ctrl+E** - Export PDF for selected patient
- **F5** - Refresh patient list (alternative)

### Tips
- Use Tab key to navigate between form fields
- Use Enter to activate the focused button
- Use Esc to cancel dialogs (e.g., message boxes)

## Benefits of Unified Window Design

### User Experience
- **Faster Navigation**: No need to open/close multiple windows
- **Context Preservation**: See patient info while filling forms
- **Less Clicking**: Direct tab switching instead of menu navigation
- **Better Overview**: All functionality visible at a glance

### Development Benefits
- **Simpler State Management**: Single window state
- **Easier Testing**: All components in one place
- **Better Integration**: Direct communication between components
- **Reduced Complexity**: No dialog lifecycle management

## Comparison: Old vs New

### Old Dialog-Based Approach
```
Main Window → Click "Add Patient" → Dialog Opens
            → Fill Form → Click Save → Dialog Closes
            → Back to Main Window
```

### New Unified Approach
```
Main Window → Switch to "Add Patient" Tab
            → Fill Form → Click Save
            → Auto-switch to Patients Tab
```

## Migration Notes

The old dialog-based files are still present but no longer used:
- `simple_add_patient_dialog.py` (deleted)
- `simple_add_checkup_dialog.py` (deleted)
- `simple_add_session_dialog.py` (deleted)
- `simple_edit_checkup_dialog.py` (deleted)
- `simple_edit_session_dialog.py` (deleted)
- `simple_select_record_dialog.py` (deleted)

These have been replaced by embedded panels within `unified_main_window.py`.

## Future Enhancements

Possible improvements for the unified window:
1. **Keyboard Shortcuts**: Add shortcuts for tab switching (Ctrl+1, Ctrl+2, etc.)
2. **Form Validation**: Real-time validation with visual feedback
3. **Auto-save**: Save draft data to prevent loss
4. **Search/Filter**: Quick patient search in the Patients tab
5. **Breadcrumbs**: Show current patient context in all tabs
6. **Side Panel**: Optional collapsible side panel for quick actions
7. **Dashboard Tab**: Statistics and recent activity overview

## Version History

- **v0.2.0** (Current): Unified single window application
- **v0.1.0**: Original dialog-based application

## Support

For issues or questions, please refer to the main project documentation.

