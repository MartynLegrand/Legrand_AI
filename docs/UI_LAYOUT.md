# 🎨 Legrand 3D - UI Layout Reference

## Overview

This document describes the user interface layout and design of Legrand 3D.

## Main Layout

```
╔═══════════════════════════════════════════════════════════════════════╗
║  ⚡ Legrand 3D v1.0.0 MVP          🟢 Connected         🗑️ Clear    ║  ← Header (60px)
╠═══════════════╦═══════════════════════════════════╦═══════════════════╣
║               ║                                   ║                   ║
║               ║                                   ║  ⚙️ Properties    ║
║  🎨 Node      ║      🎬 3D Viewport              ║                   ║
║   Editor      ║                                   ║  Object Info      ║
║               ║   ┌─────────────────────────┐    ║  Name: Cube       ║
║ ┌─────────┐   ║   │                         │    ║  Type: MESH       ║
║ │Primitives│   ║   │      ┌────────┐        │    ║                   ║
║ └─────────┘   ║   │      │        │        │    ║  Transform        ║
║               ║   │      │  CUBE  │        │    ║  Location         ║
║  ⬜ Cube      ║   │      │        │        │    ║  X: [  0.0  ]    ║
║  🔵 Sphere    ║   │      └────────┘        │    ║  Y: [  0.0  ]    ║
║  🛢️ Cylinder  ║   │                         │    ║  Z: [  0.0  ]    ║
║  🔺 Cone      ║   │      Grid & Axes        │    ║                   ║
║  🍩 Torus     ║   └─────────────────────────┘    ║  Rotation         ║
║  ▭ Plane      ║                                   ║  X: [  0.0  ]    ║
║               ║   🖱️ Controls:                   ║  Y: [  0.0  ]    ║
║ Scene Objects ║   • Rotate: Left drag            ║  Z: [  0.0  ]    ║
║ (2 objects)   ║   • Pan: Right drag              ║                   ║
║  MESH Cube    ║   • Zoom: Scroll                 ║  Scale            ║
║  MESH Sphere  ║                                   ║  X: [  1.0  ]    ║
║               ║                                   ║  Y: [  1.0  ]    ║
║               ║                                   ║  Z: [  1.0  ]    ║
║               ║                                   ║                   ║
║               ║                                   ║ [ Apply Transform]║
╚═══════════════╩═══════════════════════════════════╩═══════════════════╝
  320px           flex: 1 (center area)              300px
```

## Component Breakdown

### 1. Header Component

**Dimensions**: Full width × 60px height

```
┌───────────────────────────────────────────────────────────────┐
│  ⚡ Legrand 3D  v1.0.0     🟢 Connected      🗑️ Clear Scene   │
│  └── Logo      └── Version  └── Status       └── Actions      │
└───────────────────────────────────────────────────────────────┘
```

**Elements**:
- **Logo**: "⚡ Legrand 3D" with gradient text
- **Version Badge**: "v1.0.0 MVP"
- **Status Indicator**: Green dot + "Connected" or Red dot + "Disconnected"
- **Clear Scene Button**: Removes all objects

**Colors**:
- Background: `#2d2d2d`
- Border: `#0078d4` (2px bottom)
- Logo: Linear gradient blue (`#0078d4` → `#00bcf2`)

### 2. Node Editor (Left Panel)

**Dimensions**: 320px width × full height

```
┌─────────────────────┐
│  🎨 Node Editor     │
│  Create and modify  │
├─────────────────────┤
│ [Primitives][Mods] │ ← Tabs
├─────────────────────┤
│                     │
│  ⬜ Cube   🔵 Sphere│ ← Primitive Grid
│                     │
│  🛢️ Cylinder 🔺 Cone│
│                     │
│  🍩 Torus   ▭ Plane │
│                     │
├─────────────────────┤
│ Scene Objects (2)   │ ← Object List
│                     │
│ [MESH] Cube        │
│ [MESH] Sphere      │
│                     │
└─────────────────────┘
```

#### Primitives Tab

**Grid Layout**: 2 columns × 3 rows

Each button:
- Icon (emoji)
- Label
- Hover effect (lift + blue border)
- Click creates object

#### Modifiers Tab

```
┌─────────────────────┐
│ Select Object:      │
│ [ Cube          ▼ ] │ ← Dropdown
├─────────────────────┤
│  🔲 Subdivision     │ ← Modifier buttons
│  ⬡ Bevel           │
│  📊 Array          │
├─────────────────────┤
│ Parameters          │
│                     │
│ Levels (Subdiv):    │
│ [      2      ]     │
│                     │
│ Width (Bevel):      │
│ [     0.1     ]     │
│                     │
│ Count (Array):      │
│ [      3      ]     │
└─────────────────────┘
```

**Colors**:
- Background: `#252525`
- Border: `#3e3e3e`
- Tab Active: `#0078d4`
- Button Hover: `#3e3e3e`

### 3. 3D Viewport (Center Panel)

**Dimensions**: Flexible (takes remaining space) × full height

```
┌─────────────────────────────────────┐
│  🎬 3D Viewport    [Loading...]     │ ← Header
├─────────────────────────────────────┤
│                                     │
│                                     │
│           ┌────────┐                │
│           │        │                │
│           │  CUBE  │                │ ← 3D Model
│           │        │                │
│           └────────┘                │
│                                     │
│     ─── Grid Lines ───              │ ← Grid Helper
│                                     │
│                                     │
├─────────────────────────────────────┤
│ 🖱️ Left drag: Rotate               │ ← Controls
│ 🖱️ Right drag: Pan                 │   Help Text
│ 🖱️ Scroll: Zoom                    │
└─────────────────────────────────────┘
```

**Scene Setup**:
- Background: Dark gray (`#1a1a1a`)
- Lighting: Ambient + Directional
- Grid: 10×10 units
- Axes: RGB (X=Red, Y=Green, Z=Blue)
- Camera: Perspective (FOV 75°)
- Position: (5, 5, 5) looking at origin

**When Empty**:
```
┌─────────────────────────────────────┐
│                                     │
│          🎨                         │
│                                     │
│    Welcome to Legrand 3D            │
│                                     │
│    Create a primitive object        │
│    to see the preview               │
│                                     │
└─────────────────────────────────────┘
```

**Colors**:
- Background: `#252525`
- Header: `#2d2d2d`
- Border: `#3e3e3e`
- Scene BG: `#1a1a1a`

### 4. Properties Panel (Right Panel)

**Dimensions**: 300px width × full height

```
┌─────────────────────┐
│  ⚙️ Properties      │
├─────────────────────┤
│                     │
│ OBJECT INFO         │
│ Name: Cube          │
│ Type: MESH          │
│                     │
├─────────────────────┤
│ TRANSFORM           │
│                     │
│ Location            │
│ [X]  [Y]  [Z]       │ ← 3 inputs
│ [0.0][0.0][0.0]     │
│                     │
│ Rotation            │
│ [X]  [Y]  [Z]       │
│ [0.0][0.0][0.0]     │
│                     │
│ Scale               │
│ [X]  [Y]  [Z]       │
│ [1.0][1.0][1.0]     │
│                     │
│ [Apply Transform]   │ ← Action button
│                     │
└─────────────────────┘
```

**When No Selection**:
```
┌─────────────────────┐
│  ⚙️ Properties      │
├─────────────────────┤
│                     │
│      📝             │
│                     │
│  Select an object   │
│  to view properties │
│                     │
│                     │
└─────────────────────┘
```

**Colors**:
- Background: `#252525`
- Section Headers: `#0078d4`
- Input Fields: `#1e1e1e`
- Border: `#3e3e3e`

## Color Palette

### Primary Colors
```
Background Dark:  #1e1e1e  ████
Background:       #252525  ████
Background Light: #2d2d2d  ████
Border:           #3e3e3e  ████
Text Primary:     #ffffff  ████
Text Secondary:   #cccccc  ████
Text Muted:       #888888  ████
Text Disabled:    #666666  ████
```

### Accent Colors
```
Primary Blue:     #0078d4  ████
Primary Blue Light:#00bcf2 ████
Success Green:    #10b981  ████
Error Red:        #ef4444  ████
Warning Orange:   #f59e0b  ████
```

### Status Colors
```
Connected:        #10b981  ████ (green)
Disconnected:     #ef4444  ████ (red)
Loading:          #0078d4  ████ (blue)
```

## Typography

### Font Family
```
Primary: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto'
Mono:    'Courier New', Consolas, Monaco, monospace
```

### Font Sizes
```
Logo:         24px (bold)
Heading:      18px (bold)
Subheading:   14px (medium)
Body:         12px (regular)
Caption:      11px (regular)
```

## Spacing

### Padding
```
Large:   20px
Medium:  16px
Small:   12px
XSmall:  8px
```

### Margins
```
Between Sections: 24px
Between Items:    12px
Between Elements: 8px
```

## Interactions

### Buttons

**States**:
```
Normal:  background: #0078d4
Hover:   background: #106ebe, transform: translateY(-2px)
Active:  background: #005a9e
Disabled: opacity: 0.5, cursor: not-allowed
```

### Inputs

**States**:
```
Normal:  border: #3e3e3e
Focus:   border: #0078d4, outline: none
Error:   border: #ef4444
```

### Cards/Panels

**Shadow**: None (flat design)
**Border**: 1px solid `#3e3e3e`
**Radius**: 4px (small), 8px (medium)

## Responsive Behavior

### Minimum Sizes
```
Node Editor:  320px width (fixed)
Viewport:     400px width (minimum)
Properties:   300px width (fixed)
Total Min:    1020px width
```

### Mobile (Future)
- Stack panels vertically
- Node Editor → full width
- Viewport → full width
- Properties → full width

## Animation & Transitions

### Standard Transitions
```css
transition: all 0.2s ease;
```

### Hover Effects
```css
transform: translateY(-2px);
box-shadow: 0 4px 8px rgba(0,0,0,0.2);
```

### Loading States
```css
animation: pulse 1.5s ease-in-out infinite;
```

## Accessibility

### Focus States
- Visible focus rings
- Keyboard navigation support
- Tab order: Header → Node Editor → Viewport → Properties

### Contrast Ratios
- Text on Dark BG: 15:1 (AAA)
- Interactive Elements: 7:1 (AA+)

### Screen Reader Labels
- All buttons have aria-labels
- Status indicators have text alternatives
- Form inputs have labels

## Icons

### System Icons
```
⚡ - Lightning (Logo)
🎨 - Palette (Node Editor)
🎬 - Clapper (Viewport)
⚙️ - Gear (Properties)
🗑️ - Trash (Clear)
🟢 - Green Circle (Connected)
🔴 - Red Circle (Disconnected)
```

### Primitive Icons
```
⬜ - Cube
🔵 - Sphere
🛢️ - Cylinder
🔺 - Cone
🍩 - Torus
▭ - Plane
```

### Modifier Icons
```
🔲 - Subdivision
⬡ - Bevel
📊 - Array
```

### Control Icons
```
🖱️ - Mouse
📝 - Notes
```

## Layout Measurements

### Exact Dimensions
```
Header Height:        60px
Node Editor Width:    320px
Properties Width:     300px
Viewport:             calc(100vw - 620px)
Panel Border:         1px
Total Height:         100vh
```

### Z-Index Layers
```
Header:        100
Modal/Dialog:  1000
Tooltip:       2000
Notification:  3000
```

---

This layout provides a clean, modern, and intuitive interface inspired by professional 3D software while maintaining simplicity and ease of use.
