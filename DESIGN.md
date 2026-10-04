# PROJECT DESIGN SYSTEM

> This file must be customized for each new website before page-level UI implementation begins. Do not leave placeholders unresolved.

## 1. Product and visual positioning

- Product:
- Audience:
- Primary user task:
- Brand personality:
- Desired perception:
- Design direction:
- Design references (2–4):
- Why each reference is relevant:
- What must NOT be copied:

## 2. Visual theme & atmosphere

Describe the visual language in concrete terms: density, rhythm, level of decoration, use of imagery, light/dark balance, technical/editorial/playful tone, and how the design supports the actual user task.

## 3. Color system

### Core tokens

| Token | Value | Role |
|---|---|---|
| canvas | TBD | Page background |
| surface-1 | TBD | Primary elevated surface |
| surface-2 | TBD | Secondary surface |
| ink | TBD | Primary text |
| body | TBD | Body text |
| muted | TBD | Secondary text |
| hairline | TBD | Borders/dividers |
| primary | TBD | Primary action / brand accent |
| on-primary | TBD | Text/icons on primary |
| success | TBD | Success state |
| warning | TBD | Warning state |
| error | TBD | Error/destructive state |

### Rules

- Define where the accent color may and may not be used.
- Define gradient rules explicitly. Default: no decorative gradients unless justified.
- Define dark mode only if the product benefits from it.

## 4. Typography

### Font stack

- Display:
- Body:
- Monospace/technical:

### Type scale

| Token | Size | Weight | Line height | Tracking | Use |
|---|---:|---:|---:|---:|---|
| display-xl | TBD | TBD | TBD | TBD | Hero |
| display-lg | TBD | TBD | TBD | TBD | Section title |
| heading | TBD | TBD | TBD | TBD | Major heading |
| subheading | TBD | TBD | TBD | TBD | Card/tool heading |
| body-lg | TBD | TBD | TBD | TBD | Lead text |
| body | TBD | TBD | TBD | TBD | Default body |
| body-sm | TBD | TBD | TBD | TBD | Secondary copy |
| caption | TBD | TBD | TBD | TBD | Metadata |
| mono | TBD | TBD | TBD | TBD | Technical data |

## 5. Spacing system

Base unit: TBD

| Token | Value |
|---|---:|
| xs | TBD |
| sm | TBD |
| md | TBD |
| lg | TBD |
| xl | TBD |
| 2xl | TBD |
| section | TBD |

Define section rhythm, card padding, form gaps, dense tool-panel gaps, and mobile reductions.

## 6. Grid & layout

- Max content width:
- Reading width:
- Tool workspace width:
- Desktop gutters:
- Mobile gutters:
- Standard column patterns:
- Tool-page layout pattern:
- Content-page layout pattern:
- Marketing-page layout pattern:

## 7. Shape system

| Token | Radius | Use |
|---|---:|---|
| sm | TBD | Inputs / compact controls |
| md | TBD | Cards |
| lg | TBD | Major panels |
| full | 9999px | Pills only when appropriate |

## 8. Elevation & depth

Define exactly where borders, shadows, overlays, and surface contrast are allowed.

Default principle: use hierarchy, spacing, borders and surface contrast before adding shadows.

## 9. Components

Define visual and behavioral rules for:

- Header / navigation
- Primary button
- Secondary button
- Tertiary / text button
- Inputs
- Selects
- Sliders
- Tabs
- Chips / filters
- Tool control panel
- Result / output panel
- Cards
- Tables
- Alerts
- Tooltips
- Modals/drawers if needed
- Breadcrumbs
- Pagination
- Footer

For every interactive component define Default, Hover, Active, Focus, Disabled, Loading, Error as applicable.

## 10. Imagery & iconography

- Image style:
- Illustration style:
- Screenshot style:
- Icon family:
- Icon stroke/weight:
- Aspect-ratio rules:
- Placeholder/fallback rules:

Do not use irrelevant stock imagery or logos as decorative filler.

## 11. Motion

- Default transition duration:
- Easing:
- Allowed animation types:
- Prohibited animation types:
- Reduced-motion behavior:

## 12. Responsive behavior

| Breakpoint | Width | Behavior |
|---|---:|---|
| Mobile | TBD | TBD |
| Tablet | TBD | TBD |
| Desktop | TBD | TBD |
| Wide | TBD | TBD |

Explicitly document navigation collapse, tool panel stacking, card/grid changes, scrolling behavior, sticky elements, and touch targets.

## 13. Accessibility

- Minimum contrast targets
- Minimum touch target
- Focus treatment
- Keyboard behavior
- Form labels and error messaging
- Reduced motion
- Semantic heading and landmark requirements

## 14. Do / Don't

### Do

- TBD

### Don't

- Do not add decorative effects without a defined role.
- Do not create inconsistent one-off components.
- Do not copy a reference brand verbatim.
- Do not sacrifice task clarity for visual novelty.

## 15. AI implementation guide

Before implementing or changing UI, the coding agent must:

1. Read this file.
2. Reuse existing tokens/components.
3. Check whether the requested change conflicts with the system.
4. If the design language must change, update this file first.
5. Validate desktop and mobile behavior after implementation.
