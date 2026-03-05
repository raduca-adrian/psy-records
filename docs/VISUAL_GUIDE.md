# Visual Guide - Unified Psychological Records Application

## Application Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│ Psychological Records                                        [_][□][X] │
├─────────────────────────────────────────────────────────────────────┤
│ [📋 Patients] [➕ Add Patient] [🩺 Checkup] [💬 Session]          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Currently displayed content depends on selected tab...              │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│ Ready                                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Tab 1: Patients View

```
┌─────────────────────────────────────────────────────────────────────┐
│ Patients                                                              │
│ Manage patient records                                               │
│                                                                       │
│ [Refresh] [Export PDF]                                               │
│                                                                       │
│ ┌─────────────┬──────────────┬─────────┐  ┌────────────────────────┐│
│ │ ID │ Name   │ CNP          │          │  │ Selected Patient:      ││
│ ├────┼────────┼──────────────┤          │  │                        ││
│ │ 1  │John Doe│1234567890123 │          │  │ Actions:               ││
│ │ 2  │Jane..  │9876543210987 │          │  │ [New Checkup]          ││
│ │    │        │              │          │  │ [New Session]          ││
│ │    │        │              │          │  │ [Edit Checkup]         ││
│ │    │        │              │          │  │ [Edit Session]         ││
│ │    │        │              │          │  │                        ││
│ │    │        │              │          │  │ Records:               ││
│ │    │        │              │          │  │ Client Name: John Doe  ││
│ │    │        │              │          │  │ CNP: 1234567890123     ││
│ │    │        │              │          │  │                        ││
│ │    │        │              │          │  │ Checkups:              ││
│ │    │        │              │          │  │ - 2024-01-15 | Dx: ... ││
│ │    │        │              │          │  │                        ││
│ └────┴────────┴──────────────┘          │  │ Sessions:              ││
│                                          │  │ - 2024-01-20 [F...  ] ││
│                                          │  │                        ││
│                                          │  └────────────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

## Tab 2: Add Patient

```
┌─────────────────────────────────────────────────────────────────────┐
│ Add New Patient                                                       │
│                                                                       │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ Name *                                                         │   │
│ │ [Enter patient full name_________________                   ] │   │
│ │                                                                │   │
│ │ CNP *                                                          │   │
│ │ [Enter CNP (Personal Numeric Code)_______                   ] │   │
│ │                                                                │   │
│ │ [Clear] [Add Patient]                                          │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Tab 3: Checkup

```
┌─────────────────────────────────────────────────────────────────────┐
│ Add New Checkup                                                       │
│ Patient: John Doe (CNP: 1234567890123)                               │
│                                                                       │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ Date *                                                         │   │
│ │ [2024-10-12 ▼]                                                 │   │
│ │                                                                │   │
│ │ Chief Complaint *                                              │   │
│ │ [_____________________________                               ] │   │
│ │                                                                │   │
│ │ Medical History                                                │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Examination                                                    │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Diagnosis *                                                    │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Treatment Plan                                                 │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Notes                                                          │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ [Clear] [Add Checkup]                                          │   │
│ └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Tab 4: Session

```
┌─────────────────────────────────────────────────────────────────────┐
│ Add New Session                                                       │
│ Patient: John Doe (CNP: 1234567890123)                               │
│                                                                       │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ Date *                                                         │   │
│ │ [2024-10-12 ▼]                                                 │   │
│ │                                                                │   │
│ │ Type *                                                         │   │
│ │ [Follow-up              ▼]                                     │   │
│ │                                                                │   │
│ │ Symptoms                                                       │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Findings                                                       │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Recommendations                                                │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Medications                                                    │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ Next Appointment (optional)                                    │   │
│ │ [2024-10-12 ▼]                                                 │   │
│ │                                                                │   │
│ │ Notes                                                          │   │
│ │ [                                                            ] │   │
│ │ [                                                            ] │   │
│ │                                                                │   │
│ │ [Clear] [Add Session]                                          │   │
│ └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Color Scheme

### Primary Colors
- **Primary Blue**: `#2196F3` - Buttons, selected tabs, links
- **Dark Blue**: `#1976D2` - Button hover states
- **Light Blue**: `#E3F2FD` - Selected table rows

### Accent Colors
- **Green**: `#4CAF50` - Primary action buttons (Add, Save)
- **Dark Green**: `#45a049` - Primary button hover

### Neutral Colors
- **Background**: `#f5f5f5` - Main window background
- **White**: `#ffffff` - Tab content, form backgrounds
- **Light Gray**: `#e0e0e0` - Borders, inactive tabs
- **Medium Gray**: `#cccccc` - Input borders
- **Dark Gray**: `#333333` - Primary text
- **Medium Text**: `#555555` - Secondary text

## Typography

- **Headers (h1)**: 24px bold
- **Subheaders (h3)**: 16px semi-bold
- **Body Text**: 13px regular
- **Buttons**: 13px medium weight

## Spacing

- **Window Padding**: 24px
- **Form Spacing**: 16px between sections
- **Button Padding**: 8px vertical, 16px horizontal
- **Input Padding**: 8px all around
- **Tab Padding**: 10px vertical, 20px horizontal

## Interactive Elements

### Buttons
- Rounded corners (4px)
- Smooth hover transitions
- Color change on hover
- Pressed state for feedback

### Input Fields
- Border changes on focus (from 1px to 2px)
- Blue focus border
- Placeholder text for guidance

### Table
- Alternating row colors on hover
- Blue highlight on selection
- Clear column headers with bottom border

### Tabs
- Visual indicator for active tab
- Smooth hover effects
- Icons + text labels

## Workflow Indicators

1. **Patient Context** - Always shown when working with records
2. **Form State** - "Add" vs "Edit" clearly indicated
3. **Status Messages** - Bottom status bar for feedback
4. **Required Fields** - Marked with asterisk (*)

## Accessibility Features

- High contrast text
- Clear focus indicators
- Keyboard navigation support
- Meaningful tab order
- Error messages in message boxes
- Tooltips (can be added)

---

**Design Philosophy**: Clean, modern, professional interface that prioritizes usability and efficiency while maintaining a polished appearance suitable for medical/psychological practice management.

