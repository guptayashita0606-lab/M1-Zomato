---
name: Rosy Hearth
colors:
  surface: '#fcf9f8'
  surface-dim: '#dcd9d9'
  surface-bright: '#fcf9f8'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f2'
  surface-container: '#f0eded'
  surface-container-high: '#eae7e7'
  surface-container-highest: '#e4e2e1'
  on-surface: '#1b1c1c'
  on-surface-variant: '#5b403f'
  inverse-surface: '#303030'
  inverse-on-surface: '#f3f0f0'
  outline: '#8f6f6e'
  outline-variant: '#e4bebc'
  surface-tint: '#bb162c'
  primary: '#b7122a'
  on-primary: '#ffffff'
  primary-container: '#db313f'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb3b1'
  secondary: '#635d5d'
  on-secondary: '#ffffff'
  secondary-container: '#eae0e0'
  on-secondary-container: '#696363'
  tertiary: '#5c5c53'
  on-tertiary: '#ffffff'
  tertiary-container: '#75756b'
  on-tertiary-container: '#fffdf0'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad8'
  primary-fixed-dim: '#ffb3b1'
  on-primary-fixed: '#410007'
  on-primary-fixed-variant: '#92001c'
  secondary-fixed: '#eae0e0'
  secondary-fixed-dim: '#cdc4c4'
  on-secondary-fixed: '#1f1b1b'
  on-secondary-fixed-variant: '#4b4546'
  tertiary-fixed: '#e4e3d6'
  tertiary-fixed-dim: '#c8c7bb'
  on-tertiary-fixed: '#1b1c15'
  on-tertiary-fixed-variant: '#47473e'
  background: '#fcf9f8'
  on-background: '#1b1c1c'
  surface-variant: '#e4e2e1'
typography:
  display-xl:
    fontFamily: Epilogue
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Epilogue
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 34px
  headline-md:
    fontFamily: Epilogue
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 26px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 12px
  margin: 20px
---

## Brand & Style

This design system is built on the philosophy of "Culinary Joy and Celebration." It targets an audience that values convenience but seeks an emotional connection with their food choices—people who aren't just ordering a meal, but creating a moment. 

The visual style is a hybrid of **Minimalism** and **Tactile/Skeuomorphic** elements. It utilizes a soft, high-key color palette to create an airy, breathable environment, while employing subtle physical metaphors through soft shadows and layered surfaces. The emotional response is intended to be warm, inviting, and celebratory, moving away from the cold efficiency of typical logistics apps toward a "digital kitchen" aesthetic.

## Colors

The palette is centered around the core brand red, softened by a background of cream and pastel pink.

- **Primary:** A vibrant, high-energy red used for critical actions and brand recognition.
- **Secondary (Soft Pink):** Used for large surface areas to provide a gentle, feminine, and celebratory base.
- **Tertiary (Cream/Off-white):** Used for card backgrounds and container surfaces to ensure high readability and a "homey" feel.
- **Celebratory Tokens:** A secondary pink shade used for decorative flourishes, badges, and seasonal indicators.
- **Warm Tokens:** A golden-yellow accent used to denote quality, ratings, and "special" offers, evoking a sense of sunshine and freshness.

## Typography

This design system uses a typographic hierarchy that balances editorial flair with modern utility.

- **Headlines:** Utilizes **Epilogue**. Its geometric but distinctive terminals give it a slightly playful, "hand-crafted" quality that mimics rounded serifs without sacrificing modern legibility.
- **Body:** Utilizes **Plus Jakarta Sans**. Chosen for its friendly, open apertures and high x-height, making long descriptions easy to read.
- **Labels:** Utilizes **Be Vietnam Pro**. Its contemporary and clean structure ensures that even at tiny sizes, technical data like delivery times and prices remain clear.

## Layout & Spacing

This design system employs a **fluid grid** with an emphasis on "airy" breathing room. The layout relies on a 4-pixel base unit for all margins and paddings. 

For mobile-first implementations:
- **Margins:** 20px horizontal page margins.
- **Gutters:** 12px for internal card grids (e.g., product lists).
- **Rhythm:** Vertical spacing between major sections should be `lg` (24px) or `xl` (32px) to prevent the UI from feeling cluttered, maintaining the "soft" aesthetic.

## Elevation & Depth

Visual hierarchy is achieved through **Tonal Layers** and **Ambient Shadows**.

- **Surfaces:** Use the Tertiary (Cream) color for primary containers to separate them from the Secondary (Soft Pink) background.
- **Shadows:** Avoid pure black shadows. Use a "Warm Shadow" (Primary Red or a deep brown at 5-8% opacity) with a high blur radius (12px to 20px). This creates a soft "floating" effect rather than a harsh drop shadow.
- **Depth Levels:**
  - *Level 0 (Base):* Pink background.
  - *Level 1 (Cards):* White/Cream surfaces with 4px Y-offset shadows.
  - *Level 2 (Buttons/Modals):* Elevated surfaces with 8px Y-offset shadows and subtle 1px inner highlights.

## Shapes

The shape language is defined by extreme **Pill-shaped** roundness. This removes visual "aggression" from the interface.

- **Standard Containers:** Use `rounded-lg` (2rem).
- **Buttons & Chips:** Always use `rounded-full` (pill shape).
- **Images:** Product images should have a `rounded-xl` (3rem) or circular mask to maintain the "soft" aesthetic.
- **Interactive States:** On press, elements should slightly shrink (98% scale) to mimic a physical "squish."

## Components

- **Buttons:** Primary buttons use a solid Red fill with white text. Secondary buttons use a transparent background with a thin Red border or a soft Cream fill. All buttons are pill-shaped.
- **Cards:** Product cards use white backgrounds, high-rounded corners, and soft, tinted shadows. Images should bleed to the top edges of the card.
- **Chips/Filters:** Use a soft cream background with a 1px border. Selected states switch to a primary red border or fill.
- **Inputs:** Search bars should be pill-shaped with a soft "inner shadow" or a very light gray border to look recessed into the cream surface.
- **Celebratory Banners:** Use "Warm Glow" backgrounds with illustrated icons and Epilogue-bold typography.
- **Progress Indicators:** Use the "Celebratory" pink for progress bars or loading states to maintain the warm mood.