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
- Page kind(s) (marketing, content, generator, calculator, game, dashboard):
- Critical first-screen action and result path:
- Existing features/routes/keywords/brand attributes to preserve:
- One-sentence design read (page kind + audience + visual personality + task constraints):
- Visitor mode **per surface** (Operate / Read / Persuade / Experience), not just per website:
- Product truth (approved copy, claims, inputs/outputs, units and behavior) to preserve:
- First-screen task completion or conversion evidence:

### Intent, conversion and claim brief (complete where applicable)

- Acquisition channel / landing search intent (organic, ads, social, referral or direct):
- Primary goal and one clear action per page/surface; actual CTA destination or tool result:
- Evidence-supported value proposition and product screenshot/demo:
- Main visitor objections and how the page answers them:
- Source-backed offer/prices/trials/guarantees/performance claims/comparisons/customer proof with owner and checked date; unsupported items: `UNVERIFIED`.
- Chosen structure: tool-first / editorial / SaaS marketing / ad landing / comparison:
- Mobile first-screen user outcome, action and information hierarchy:
- Approved brand, keyword, route, analytics and working task invariants to retain:

Never turn a tool-first SEO page into a compulsory marketing funnel. `TASTE-UI-PROTOCOL.md` defines optional conversion sequences.

## 2. Visual theme & atmosphere

Describe the visual language in concrete terms: density, rhythm, level of decoration, use of imagery, light/dark balance, technical/editorial/playful tone, and how the design supports the actual user task.

### Contextual design controls (1–10; descriptive, not a scoring system)

- `DESIGN_VARIANCE` (layout novelty):
- `MOTION_INTENSITY` (animation):
- `VISUAL_DENSITY` (information density):
- Justification for these values and the user task:
- Tool-first viewport plan (which inputs/actions/results appear immediately):

Use `TASTE-UI-PROTOCOL.md` for page-type presets and redesign checks, and `IMPECCABLE-UI-QUALITY-GATE.md` for user-task, accessibility, edge-case and performance verification. A useful, accessible and fast tool beats a visually dramatic but obstructive landing page.

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
- Keep one intentional primary accent family and consistent neutral surfaces across page types; semantic success/warning/error colors remain distinct where necessary.
- Preserve existing brand colors during redesign unless a change is explicitly approved. No blanket ban on individual hues.

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

### Optional fallback design-token starting values

These are **not mandatory** site-wide standards or verified accessibility results. Approved branding, existing design tokens and actual user testing take priority. Resolve final chosen values in the project-specific tables above.

| Topic | Optional starting point | Considerations |
|---|---|---|
| Body | 16px; line height roughly 1.5–1.7 | Spanish/Portuguese, zoom |
| Spacing | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64px | density and mobile |
| Button height | roughly 40–48px | touch-target usability |
| Card radius | roughly 8–16px | nested geometry and brand |
| Main wide container | roughly 1120–1280px | wider tool workspace if needed |
| Reading line width | roughly 65–75ch | font and script dependent |
| Microinteraction | often 120–250ms | adjust to actual action and context |
| Icons | one coherent existing/licensed family | avoid new packages unnecessarily |

Do not import external blanket bans on Inter, Arial, gradients, rounded cards, italics or specific color families.

## 6. Grid & layout

- Max content width:
- Reading width:
- Tool workspace width:
- Desktop gutters:
- Mobile gutters:
- Standard column patterns:
- Tool-page layout pattern:
- First-screen hierarchy (main tool controls, result path, secondary copy):
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

For every interactive component define Default, Hover, Active, Focus, Disabled, Loading, Error and Success as applicable. Verify real events, not only screenshots.

### Operate and localization robustness

- Valid/invalid/empty/extreme values and numerical precision/rounding requirements:
- Unicode/diacritics/emoji and long-string overflow rules, especially for Spanish/Portuguese generators:
- Keyboard/tab order, accessible naming, text enlargement and touch/gesture fallbacks:
- Network failure, timeout and offline behavior if network requests exist:

## 10. Imagery & iconography

- Image style:
- Illustration style:
- Screenshot style:
- Icon family:
- Icon stroke/weight:
- Aspect-ratio rules:
- Placeholder/fallback rules:
- Reference-image/source provenance and implementation plan if using an image-to-code process:
- Desktop/mobile screenshot comparison plan, if browser tooling is available:

Do not use irrelevant stock imagery or logos as decorative filler.

## 11. Motion — motion-first, performance-protected

**Default:** proactively apply polished, purposeful animations to suitable elements on **all** page types, including calculators, generators, games and marketing sites, as long as they do not compromise the primary task, performance, SEO or accessibility. No fixed animation count and no repeated approval needed for routine microinteractions.

- Purpose of each significant animation (feedback, comprehension, continuity or story):
- Shared timing/easing/stagger/loop motion tokens:
- Allowed native implementation (CSS / SVG / Canvas / JS / Web Animations API):
- Trigger (input, page load, in-viewport) and offscreen/background pause:
- Static/no-JS visible and operable default state:
- `prefers-reduced-motion: reduce` final-state behavior:
- Rapid/repeated/interrupted interaction and keyboard/focus/touch tests:
- JS/package and performance budget; mobile downgrade plan:
- Real before/after LCP/INP/CLS and costly paint evidence, or `NOT RUN`:
- Special product showcase/MP4/GIF needed? (only if explicitly scoped; see `MOTION-SHOWCASE-PROTOCOL.md`):

Prefer efficient `transform`/`opacity` for small motion; large blur/filter/clip masks need profiling, not assumptions. Never hide core controls behind animations, introduce CLS or sacrifice responsiveness. No paid runtime animation API is needed.

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

1. Read this file and `TASTE-UI-PROTOCOL.md`.
2. Classify the affected surface (Operate / Read / Persuade / Experience), identify the relevant task or conversion journey, then state design direction and controls.
3. For redesigns: scan the existing repo, diagnose concrete defects, and record functionality/SEO/brand baselines before changing visual code.
4. Reuse existing tokens/components; preserve approved keywords, routes, canonical/hreflang, analytics, nav, legal copy, and working user tasks unless expressly approved.
5. If the design language must change, update this file first; keep the new design consistent across relevant pages.
6. For visually critical tasks with available references, optionally follow reference/image → design-spec → code → rendered desktop/mobile comparison; do not fake screenshots or missing verification.
7. Add purposeful animation where useful while preserving reduced-motion/static/no-JS fallbacks. Ensure meaningful empty/loading/error/focus states, accessible labels and authentic assets; use the optional showcase protocol only for complex media.
8. Validate real user-task behavior at mobile, tablet, and desktop viewports; check no SEO or performance regression.
9. Run the UI quality categories from `IMPECCABLE-UI-QUALITY-GATE.md` in scope: Operate/Read/Persuade/Experience intent, accessibility, responsive, localization/edge states, performance and regressions.
10. Record concrete before/after checks and any `NOT RUN` items in `UI-RELEASE-EVIDENCE.md` rather than claiming an untested pass; do not install an Impeccable CLI or Hook unless expressly approved.
