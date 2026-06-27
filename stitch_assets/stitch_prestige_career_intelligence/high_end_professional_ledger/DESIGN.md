---
name: High-End Professional Ledger
colors:
  surface: '#fff8f0'
  surface-dim: '#e1d9cc'
  surface-bright: '#fff8f0'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fbf3e5'
  surface-container: '#f5eddf'
  surface-container-high: '#efe7da'
  surface-container-highest: '#eae1d4'
  on-surface: '#1f1b13'
  on-surface-variant: '#4d4635'
  inverse-surface: '#343027'
  inverse-on-surface: '#f8f0e2'
  outline: '#7f7663'
  outline-variant: '#d0c5af'
  surface-tint: '#735c00'
  primary: '#735c00'
  on-primary: '#ffffff'
  primary-container: '#d4af37'
  on-primary-container: '#554300'
  inverse-primary: '#e9c349'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#415ba4'
  on-tertiary: '#ffffff'
  tertiary-container: '#97b0ff'
  on-tertiary-container: '#254188'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffe088'
  primary-fixed-dim: '#e9c349'
  on-primary-fixed: '#241a00'
  on-primary-fixed-variant: '#574500'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#dbe1ff'
  tertiary-fixed-dim: '#b4c5ff'
  on-tertiary-fixed: '#00174b'
  on-tertiary-fixed-variant: '#27438a'
  background: '#fff8f0'
  on-background: '#1f1b13'
  surface-variant: '#eae1d4'
typography:
  display-lg:
    fontFamily: Playfair Display
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Playfair Display
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Playfair Display
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Hanken Grotesk
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Hanken Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-caps:
    fontFamily: Hanken Grotesk
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.15em
  label-md:
    fontFamily: Hanken Grotesk
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1440px
  gutter: 32px
  margin-desktop: 80px
  margin-tablet: 40px
  margin-mobile: 24px
---

## Brand & Style

The brand personality is authoritative, exclusive, and meticulously curated. Drawing inspiration from heritage luxury houses, this design system treats job analysis not as a utility, but as a high-stakes editorial experience. It targets C-suite executives and elite talent acquisition specialists who value precision and prestige.

The design style is **Minimalist Luxury**. It balances the starkness of high-fashion editorial layouts with the tactile warmth of physical atelier stationary. The emotional response should be one of calm confidence—spacious, quiet, and profoundly intentional. Every pixel must feel considered, avoiding unnecessary ornamentation in favor of perfect proportions and exquisite typography.

## Colors

The palette is anchored by the "Cream/Off-white" background, providing a softer, more sophisticated canvas than pure white. 

- **Primary (Brushed Gold):** Used sparingly for key actions, status indicators, and subtle decorative accents. It represents value and excellence.
- **Secondary (Deep Charcoal):** Used for structural elements, headers, and primary navigation to ground the lighter background.
- **Surface:** The charcoal is also used for "Dark Mode" containers or heavy-contrast cards within the light layout.
- **Text:** A specific Deep Grey is used for body copy to maintain readability while appearing more refined than absolute black.

## Typography

The typographic hierarchy relies on the tension between the classicism of **Playfair Display** and the contemporary precision of **Hanken Grotesk**. 

Headlines should utilize the serif's high contrast to evoke a sense of heritage. For large display text, slight negative letter-spacing adds a modern, "tight" editorial feel. Functional UI elements, labels, and long-form data analysis utilize Hanken Grotesk for its exceptional legibility and neutral tone. Use `label-caps` for section headers and categories to emulate the branding seen on luxury packaging.

## Layout & Spacing

This design system employs a **Fixed Grid** philosophy for desktop to maintain the "editorial ledger" feel, ensuring content never feels over-stretched. 

- **Desktop (1440px+):** 12-column grid with generous 80px side margins and 32px gutters. This "breathable" space is critical for the luxury aesthetic.
- **Tablet:** 8-column grid with 40px margins.
- **Mobile:** 4-column grid with 24px margins.

Vertical rhythm follows a strict 8px baseline. Use exaggerated white space between major sections (e.g., 120px or 160px) to signify the transition between different analytical modules.

## Elevation & Depth

Depth is conveyed through **Tonal Layers** and **Refined Outlines** rather than aggressive shadows. 

1.  **Base Layer:** The Cream background (#FDFCF8).
2.  **Raised Surfaces:** Use extremely subtle, 1px borders in `neutral_muted` or a very faint tint of gold to define card boundaries.
3.  **Shadows:** When necessary for floating elements (like modals), use "Ambient Shadows"—diffused, low-opacity (5-10%) shadows with a slight warm tint to match the gold/cream palette.
4.  **Interactive Depth:** On hover, elements should not "pop" toward the user. Instead, use a subtle color shift or a thin gold underline to indicate focus, maintaining the flat, paper-like elegance of the UI.

## Shapes

The shape language is **Soft** but disciplined. Avoid large radii or bubbly "app-like" corners. 

- Standard components (buttons, input fields) use a 4px (0.25rem) corner radius. 
- Larger containers and cards use a maximum of 8px (0.5rem). 
- This subtle rounding softens the high-contrast layout without sacrificing the professional, architectural structure of the design.

## Components

### Buttons
- **Primary:** Deep Charcoal background with Cream text. On hover, a 1px Gold bottom border or Gold text transition.
- **Secondary:** Transparent background with a 1px Deep Charcoal border. 
- **Ghost:** Gold text only, using the `label-caps` style for an ultra-refined look.

### Input Fields
- Underline style preferred over boxed inputs to mimic luxury stationary. 
- Use Hanken Grotesk for input text. 
- Focus state: The underline transitions from Deep Grey to Gold.

### Cards
- Cream background with a 1px `neutral_muted` border. 
- No shadows by default. 
- Header areas within cards should use the `label-caps` typography.

### Data Visualization
- Charts should use a monochromatic palette of Charcoal, Grey, and Gold. 
- Lines should be thin (1px to 1.5px) to maintain the minimalist aesthetic.

### Chips & Tags
- Rectangular with minimal rounding (2px). 
- Backgrounds should be very pale gold or light grey with dark text to ensure they don't distract from the primary content.