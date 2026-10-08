# Website Project Agent Rules

These rules are mandatory for every website created from this starter.

## 1. Required build order

Do not start page-level UI implementation until the following are complete:

1. User intent, site goal, monetization model, and cost constraints understood; for new opportunities and major pivots, complete the evidence-first business decision in `OPC-BUSINESS-GATE.md` and record observed evidence in `OPC-BUSINESS-EVIDENCE.md`.
2. Keyword research reviewed and explicitly approved keywords locked.
3. Search intent mapped to canonical destinations; no unresolved cannibalization plan.
4. Competitor/reference analysis completed.
5. Full project PRD and information architecture completed.
6. Project-specific `DESIGN.md` completed, including a page-type design read and the task-first controls from `TASTE-UI-PROTOCOL.md`.
7. `SEO-GEO-PROJECT-BRIEF.md` completed with keyword/intent ownership, indexation, sources, entities, schema, and international rules.
8. Applicable SEO/GEO, programmatic SEO, and international architecture from `SEO-GEO-QUALITY-GATE.md` defined.
9. Design tokens and reusable base components defined.

Then implement the complete planned site, responsive behavior, SEO/GEO, QA, deployment, and production verification.

## 2. DESIGN.md is mandatory

Every project MUST have a project-specific `DESIGN.md` before UI development begins.

The design system must be derived from product context, target users, search intent, brand positioning, and 2–4 high-quality references. `VoltAgent/awesome-design-md` is a required reference source during design research when applicable, but no site may directly clone a single brand's visual identity.

The design system must define at minimum: visual theme, semantic colors, typography, spacing, grid/layout, radii, core components and states, elevation, responsive behavior, media/icon rules, motion, accessibility, design guardrails, and AI implementation notes.

Read `TASTE-UI-PROTOCOL.md` and `IMPECCABLE-UI-QUALITY-GATE.md` before UI creation or redesign. Its Taste Skill-derived principles are selective, contextual guidance, **not** a mandate to install a Skill, generate images for every change, add heavy motion, enforce specific fonts, or replace the site's existing stack.

## 3. Design-system enforcement

- All pages and components must follow `DESIGN.md`.
- Do not introduce arbitrary colors, radii, spacing, shadows, gradients, glow, blur, glassmorphism, or typography.
- Reuse existing tokens/components first.
- If the visual language must change, update `DESIGN.md` first, then implementation.
- Marketing, tool, content, and utility pages may differ in density but must share one recognizable system.
- Avoid generic AI-SaaS aesthetics unless the product genuinely requires them.
- Apply the `TASTE-UI-PROTOCOL.md` sequence: design read → context-sensitive visual system → implement → multi-viewport visual/user-task review.
- For existing sites, follow scan → diagnose → preserve → fix → verify. Do not silently alter approved keywords, routes, analytics events, form field names/order, brand, navigation labels, legal text, or working calculations.
- For generators, converters, calculators, and games, the core interaction and results path take priority over cinematic heroes, scroll effects, and decorative marketing sections.
- Image-to-code is optional when fidelity matters and real source images/tools exist; never ship fake controls or claim a screenshot was compared unless it was.

## 3A. UI quality gate and verification evidence

- Apply the **review process** in `IMPECCABLE-UI-QUALITY-GATE.md` to meaningful new or modified UI; Impeccable software installation itself is **not** mandatory.
- Classify the visitor goal **per surface**: Operate (tool/workspace), Read (article/help), Persuade (marketing), Experience (showcase). A tool's landing page and its interactive workspace may have different priorities.
- For relevant changes, inspect accessibility, functional states, narrow viewports, keyboard/touch, actual long/invalid inputs, Spanish/Portuguese localization and text overflow, visual cohesion, and real measured performance when available.
- Diagnose before editing; record observed issues and severity. Treat P0/P1 blocking defects as release blockers; a clean heuristic detector output does **not** override a broken user task or SEO regression.
- Record test evidence in `UI-RELEASE-EVIDENCE.md` for a release, with `PASS`, `FAIL`, `NOT RUN`, or `NOT APPLICABLE`. Never claim scanner, browser, Lighthouse, responsive or manual checks ran when they did not.
- Optional CLI, downloaded binaries, provider hooks, extension permissions, and Live mode require explicit opt-in after reviewing version, cost, security, and edit behavior. Never silently install, update, enable or invoke an edit-blocking Hook.
- Validate in a bounded batch rather than looping indefinitely on cosmetic details. Follow existing protected keywords, URLs, canonical/hreflang, analytics, calculations and brand constraints.

## 4. SEO / GEO quality gate is mandatory

Read and apply `SEO-GEO-QUALITY-GATE.md` before changing routes, templates, metadata, structured data, multilingual architecture, programmatic pages, or indexation behavior.

- Preserve explicitly approved core keywords. Do not silently replace, merge, translate, or rewrite them.
- Never fabricate keyword metrics, SERP data, traffic, backlinks, citations, or indexation status.
- Map one primary intent to one canonical destination.
- Maintain crawlable initial content, heading hierarchy, canonical URLs, robots directives, sitemap coverage, internal linking, valid structured data, and real 404 behavior.
- Programmatic pages must provide standalone value and meaningful differentiation; do not mass-publish name/keyword swaps.
- Multilingual sites must pass canonical/hreflang and localization checks.
- GEO work must improve extractability, evidence, clarity, originality, and usefulness; it must not create near-duplicate "AI keyword" pages.
- Do not add AI-only files/markup solely because a GEO checklist says so. Google states that its generative-AI Search features use normal Search foundations and do not require special AI markup.
- `Google-Extended` is a model-training/product control, not a Google Search indexing/ranking control. Do not confuse crawler/training permissions with search visibility.
- Treat third-party thresholds as internal heuristics, not search-engine rules.

## 4B. Commercial opportunity gate (OPC-inspired)

- Read `OPC-BUSINESS-GATE.md` for new projects, significant expansions, business pivots and periodic post-launch business review.
- On new opportunities, complete the project-specific `OPC-BUSINESS-EVIDENCE.md` **before material development**, with sourced and dated search demand, SERP, comparable traffic, business model and validation plan. Unknown data stays `UNVERIFIED`; neither Google Trends relative values nor CPC imply proven demand/revenue.
- Use the evidence-first six-dimension priority screen and owner-reviewed GO / TEST / HOLD / STOP. Never auto-build or auto-delete based on the heuristic score.
- For existing sites, do not block urgent SEO/UI/function fixes pending a new commercial evaluation; never silently change already-approved keywords, primary routes, content, brand or the agreed full project scope.
- Before declaring commercial success, collect real GSC/user/revenue/cost data. Prefer free sources and require explicit approval for paid APIs or fixed recurring charges.
- The `easychen/opc-methodology` project is an attributed conceptual reference. Do not copy or redistribute its CC BY-NC-SA Skill content for commercial use.

## 5. Audit levels

- L1 change/commit audit after SEO-sensitive changes.
- L2 release audit before production launch/major release, with evidence recorded in `SEO-GEO-RELEASE-EVIDENCE.md`.
- L3 periodic full audit only when production data or a major review justifies it.

Do not spend full-audit model/API cost on every trivial commit. Prefer deterministic checks for status codes, counts, duplicate ratios, schema syntax, arithmetic, and route coverage.

## 6. Performance and accessibility

- Mobile-first behavior must be validated, not assumed.
- Avoid unnecessary dependencies and heavy client-side JavaScript.
- Prefer SSG/SSR for public SEO content; do not let CSR hide the only copy of indexable content.
- Optimize images and fonts.
- Preserve keyboard navigation, visible focus, semantic HTML, usable touch targets, readable contrast, and reduced-motion behavior.

## 7. Cost discipline

Unless meaningful traffic or revenue is already validated, prefer zero/freemium infrastructure:

- Static or edge hosting where practical.
- Free-tier databases/services where practical.
- No paid SEO API, crawler, fixed monthly server, or other recurring cost without explicit approval.

## 8. Visual QA is mandatory

A website is not complete until Visual QA checks hero/first-screen hierarchy, tool clarity, desktop/tablet/mobile layouts, typography/spacing/components, CTA hierarchy, contrast, imagery, generic-template smell, unnecessary effects, real user-task efficiency, and SEO content readability.

Use the redesign and evidence matrix in `TASTE-UI-PROTOCOL.md` plus the UX/a11y/i18n/performance quality dimensions in `IMPECCABLE-UI-QUALITY-GATE.md`: include observed screenshots/comparisons where tools permit, interaction states, mobile and small-laptop behavior, and explicit `not run` notes instead of assumed passes.

## 9. Final project QA

Before calling the site complete, verify:

- No broken primary navigation or route 404s.
- Main tools work end-to-end.
- All planned important pages exist.
- Responsive layouts work at representative widths.
- `SEO-GEO-QUALITY-GATE.md` launch acceptance passes.
- Applicable UI quality gates in `IMPECCABLE-UI-QUALITY-GATE.md` pass, with P0/P1 blockers closed and actual checks recorded in `UI-RELEASE-EVIDENCE.md`.
- Internal links and images/assets work.
- No obvious console/build/runtime errors.
- Production build succeeds.
- Cloudflare deployment settings are documented when used.
- Production URL is checked after deployment.
- The final site still follows `DESIGN.md`.
- A post-launch SEO baseline is recorded for important routes.

## 10. Complete-scope rule

Do not use a thin "V1 now, required pages/features later" approach as a substitute for the agreed complete build. Staged implementation is acceptable internally, but all agreed required scope and acceptance gates must be completed before declaring the project finished.

## 11. Default new-site rule

When starting a new website for this owner, treat this repository as the canonical website baseline. Do not wait for reminders about approved keywords, `DESIGN.md`, `awesome-design-md`, `SEO-GEO-QUALITY-GATE.md`, programmatic SEO, international SEO, Cloudflare, mobile QA, cost discipline, complete-scope delivery, or final visual/production QA. Apply them automatically unless explicitly overridden for that project.
