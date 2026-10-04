# Website Project Agent Rules

These rules are mandatory for every website created from this starter.

## 1. Required build order

Do not start page-level UI implementation until the following are complete:

1. User intent, site goal, and monetization model understood.
2. Keyword plan and search intent mapped.
3. Competitor/reference analysis completed.
4. Full project PRD completed.
5. Project-specific `DESIGN.md` completed.
6. Design tokens and reusable base components defined.

Then implement pages, SEO/GEO, responsive behavior, QA, and deployment.

## 2. DESIGN.md is mandatory

Every project MUST have a project-specific `DESIGN.md` before UI development begins.

The design system must be derived from the product context, target users, search intent, brand positioning, and 2–4 high-quality references. `VoltAgent/awesome-design-md` is a required reference source during the design-research step when applicable, but no site may directly clone a single brand's visual identity.

The design system must define at minimum:

- Visual theme and atmosphere
- Color tokens and semantic color roles
- Typography hierarchy
- Spacing scale
- Grid, containers, and layout rules
- Border radius scale
- Buttons, inputs, cards, tabs, navigation, tables and other core components
- Hover, active, focus, loading, error, disabled states
- Elevation/shadow rules
- Responsive breakpoints and mobile behavior
- Image, illustration, icon, and media rules
- Motion and animation rules
- Accessibility and contrast requirements
- Do / Don't design guardrails
- AI implementation notes

## 3. Design-system enforcement

All pages and components must follow `DESIGN.md`.

- Do not introduce arbitrary colors, radii, spacing, shadows, gradients, glow, blur, glassmorphism, or typography.
- Do not create one-off visual systems for individual pages.
- New UI must reuse existing tokens and components first.
- If the visual language must change, update `DESIGN.md` first, then update implementation.
- Marketing pages, tool pages, content pages, and utility pages may have different densities, but must remain recognizably part of the same design system.
- Avoid generic AI-SaaS aesthetics unless the product genuinely requires them.

## 4. SEO / GEO constraints

- Preserve explicitly approved core keywords. Do not silently replace or rewrite them.
- Each important search intent must map to a clear page or section.
- Maintain clean heading hierarchy, canonical URLs, metadata, structured data where appropriate, sitemap coverage, internal linking, and indexability.
- Content must answer the query directly before expanding into supporting context.
- Avoid thin doorway pages and near-duplicate pages.
- Optimize for both conventional search and answer engines by using concise definitions, tables, FAQs, examples, and clearly attributable facts where useful.

## 5. Performance and accessibility

- Mobile-first behavior must be validated, not assumed.
- Avoid unnecessary dependencies and heavy client-side JavaScript.
- Optimize images and fonts.
- Preserve keyboard navigation, visible focus states, semantic HTML, usable touch targets, and readable contrast.
- Respect reduced-motion preferences for non-essential animation.

## 6. Cost discipline

Unless a project has already validated meaningful traffic or revenue, prefer zero/freemium infrastructure:

- Static or edge hosting where practical
- Free-tier databases/services where practical
- No paid API or fixed monthly server cost without explicit approval

## 7. Visual QA is mandatory

A website is not complete until Visual QA has checked:

- Hero and first-screen hierarchy
- Tool interaction clarity
- Desktop, tablet, and mobile layouts
- Typography consistency
- Spacing consistency
- Component consistency
- CTA hierarchy
- Contrast and readability
- Cross-page visual consistency
- AI-template smell / generic decoration
- Unnecessary gradients, glow, glassmorphism, or shadows
- Empty, broken, stretched, or irrelevant imagery
- Real user-task efficiency
- SEO content readability

## 8. Final project QA

Before calling the site complete, verify:

- No broken navigation or 404s from primary routes
- Main tools work end-to-end
- All planned important pages exist
- Responsive layouts work at representative widths
- Metadata, canonical, robots, and sitemap are correct
- Internal links work
- Images load
- No obvious console/build errors
- Production build succeeds
- Cloudflare deployment settings are documented when Cloudflare is used
- The final site still follows `DESIGN.md`

## 9. Default new-site rule

When starting a new website for this owner, treat this repository as the canonical website baseline. Do not wait for the owner to remind you about `DESIGN.md`, `awesome-design-md`, SEO/GEO, Cloudflare, mobile QA, cost discipline, or final visual QA. Apply these requirements automatically unless the owner explicitly overrides a rule for that specific project.
