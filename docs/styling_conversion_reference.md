# Styling Conversion Reference: Pixels to Relative Units

## Overview
The PyQt6 application styling system has been converted from fixed pixel values to relative `em` units for better scalability and maintainability.

## Base Font Size
- Base font size: 16px (1em = 16px at default sizing)

## Typography Conversion
| Component | Before (px) | After (em) | Calculation |
|-----------|-------------|------------|-------------|
| Small font | 12px | 0.75em | 12 ÷ 16 = 0.75 |
| Normal font | 16px | 1em | 16 ÷ 16 = 1 |
| Large font | 20px | 1.25em | 20 ÷ 16 = 1.25 |

## Spacing Conversion
| Size | Before (px) | After (em) | Calculation |
|------|-------------|------------|-------------|
| XS | 6px | 0.375em | 6 ÷ 16 = 0.375 |
| SM | 10px | 0.625em | 10 ÷ 16 = 0.625 |
| MD | 16px | 1em | 16 ÷ 16 = 1 |
| LG | 20px | 1.25em | 20 ÷ 16 = 1.25 |
| XL | 25px | 1.5625em | 25 ÷ 16 = 1.5625 |
| XXL | 30px | 1.875em | 30 ÷ 16 = 1.875 |
| XXXL | 35px | 2.1875em | 35 ÷ 16 = 2.1875 |

## Border Conversion
| Size | Before (px) | After (em) | Calculation |
|------|-------------|------------|-------------|
| Border width | 3px | 0.1875em | 3 ÷ 16 = 0.1875 |
| Border radius SM | 8px | 0.5em | 8 ÷ 16 = 0.5 |
| Border radius MD | 10px | 0.625em | 10 ÷ 16 = 0.625 |

## Widget-Specific Conversions

### Input Fields
- Padding: `18px 20px` → `1.125em 1.25em`
- Min height: `30px` → `1.875em`
- Max height: `60px` → `3.75em`

### Buttons
- Padding: `16px 32px` → `1em 2em`
- Min height: `30px` → `1.875em`
- Min width: `150px` → `9.375em`
- Letter spacing: `1px` → `0.0625em`
- Transform Y: `2px` → `0.125em`

### Combo Boxes
- Dropdown width: `32px` → `2em`
- Item min height: `35px` → `2.1875em`
- Arrow dimensions: `10px` → `0.625em`

### Tabs
- Tab padding: `18px` → `1.125em`
- Tab margin: `5px` → `0.3125em`
- Tab font size: `15px` → `0.9375em`
- Tab min width: `130px` → `8.125em`
- Tab min height: `25px` → `1.5625em`
- Border bottom: `4px` → `0.25em`

## Benefits of Relative Units

1. **Scalability**: Components scale proportionally with system/browser font size changes
2. **Accessibility**: Better support for users who need larger text
3. **Consistency**: All sizing is relative to the base font size
4. **Maintenance**: Easier to adjust overall sizing by changing base font size
5. **Responsive Design**: Better adaptation to different screen densities

## Usage Notes

- All measurements are now relative to the current font size (em units)
- The base font size can be adjusted globally to scale the entire interface
- Pixel values are only retained for non-scalable elements like shadows and specific color codes
- The conversion maintains the visual appearance while adding scalability
