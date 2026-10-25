# Taste-inspired UI Design and Redesign Protocol

> Applies to new sites and redesigns built from this starter. Adapted selectively from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (v2 experimental), especially `design-taste-frontend`, `redesign-existing-projects`, and `image-to-code`. This is a project-owned policy, **not** an unreviewed import of third-party instructions.

## 1. Authority and scope

1. Explicit owner requirements, approved keywords, search intent, existing functionality, and `SEO-GEO-QUALITY-GATE.md` take precedence over aesthetic preferences.
2. `DESIGN.md` is the project-specific source of truth for tokens and component behavior. This protocol supplies a process and checks, not a universal palette or font.
3. Apply the full art-direction workflow to marketing/landing/editorial pages; apply **task-first, restrained** design to generators, calculators, converters, editors, games, and data-heavy workflows. Do not apply cinematic marketing-page rules to tool workspaces.
4. Do not blindly copy Taste Skill's categorical bans, random layout selection, exact hero word counts, mandatory dark mode, specific font libraries, GSAP requirements, or forced image generation. Choose based on actual user needs, localization, accessibility, performance, and available tools.
5. A Skill or generated design is reference material, not proof that a feature works, a page is accessible, or SEO is correct. Keep paid dependencies, new services, and recurring costs opt-in.

## 2. Design read before implementation

Document in the project's `DESIGN.md`:

- Page kind(s), audience, primary task, target locale(s), trust/brand constraints, conversion intent, and what must remain unchanged.
- One-sentence design read: `<page kind> for <audience>; <visual personality>; <task/brand constraints>`.
- Three **proposed** 1–10 controls: `DESIGN_VARIANCE` (structural novelty), `MOTION_INTENSITY` (animation), `VISUAL_DENSITY` (information per viewport). These are design shorthand, not acceptance metrics.
- 2–4 relevant design references, what is learned from each, what will not be copied, and a component/token map.
- First-screen priorities: what the user can **actually do** without scrolling, not just what marketing copy they can see.

Suggested starting points (tune per site rather than treating as mandates):

| Page kind | Variance | Motion | Density | Non-negotiable priority |
|---|---:|---:|---:|---|
| Calculator / generator / converter | 5 | 4 | 6 | Inputs + output path immediately clear |
| Game / clicker / simulator | 7 | 6 | 5 | Primary interaction visible and responsive |
| B2B finance / tax workflow | 4 | 3 | 6 | Trust, accuracy, labels, errors |
| Marketing landing | 7 | 6 | 4 | Message, authentic proof, CTA |
| Editorial / content hub | 6 | 4 | 4 | Reading, navigation, links |

## 2A. Conversion page structure (choose according to intent)

Use this for Persuade pages after classifying acquisition source, visitor, offer, primary action, objections, proof and mobile constraints in `DESIGN.md`.

| Page purpose | First-screen priority | Subsequent evidence/structure |
|---|---|---|
| Organic SEO tool | visible H1, usable core inputs, result/action path | useful steps, examples, constraints, distinct FAQ and relevant internal links |
| SaaS marketing | clear outcome and audience, authentic product preview, primary CTA | differentiated benefits, how-it-works, supported proof, objection handling, final CTA as needed |
| Paid-ad landing | credible consistency with ad promise and next step | real proof, friction reduction, necessary disclosures |
| Comparison/alternatives | visitor decision criteria and real product differences | sourced feature/price/limitation table, fair suitability explanation |
| Editorial/read | answer and readable information hierarchy | context, sources, navigation, genuinely useful links |

Rules:
1. Do **not** force a large animated brand hero, 6–12 FAQs, testimonial strip or repeated conversion CTA onto an Operate or Read page. Make page sections earn their place.
2. One primary CTA per decision region; supporting navigation stays available and functional. Every CTA must lead to a real destination.
3. Product capabilities, price, terms, guarantees, discounts, user numbers, case studies, logos, testimonials and competitor statistics require a source and checked date. Missing facts remain `UNVERIFIED` and should not appear as verified claims.
4. Use specific benefit copy only when the promise is demonstrable. Avoid manufactured numerical precision and fictional clients.
5. Verify mobile conversion/task journeys and existing SEO-leading keywords, URLs, canonical/hreflang and working controls. Claims of higher conversion require observed results, not just visual opinion.

**MOTION_INTENSITY describes the expressive role of motion, not the number of animations.** A lower illustrative value does not prohibit rich functional transitions if they remain accessible and performant. Prefer actual tested behavior over these starting numbers.

## 3. Anti-generic visual discipline

- Create hierarchy with content, type scale, whitespace, and meaningful grouping first; avoid reflexive purple glows, all-equal three-card grids, over-rounded nested cards, and heavy shadows **unless justified by the brand**.
- Use coherent design tokens: neutral surfaces, meaningful semantic state colors, one intentional primary accent family, documented radii and typography scales. Never override an established brand color simply because a Skill discourages it.
- Vary section composition only where it improves scanning or comprehension. Symmetry and dense tables are valid for tools; asymmetry is not a goal by itself.
- Choose fonts for language coverage (including Spanish/Portuguese diacritics), legibility, fallback behavior, licensing, and loading cost. No blanket font bans.
- Real data, screenshots, testimonials, prices, and brand logos require authentic sources. Never fabricate social proof or numeric metrics to make a design look complete.
- Respect conventional forms: persistent labels, correct focus order, keyboard access, readable placeholders, explicit validation/errors, and helpful empty/loading/disabled/success states.
- Use image assets when meaningful; provide reliable fallbacks, alt text, stable aspect ratios, and appropriate sizing. Do not introduce decorative image dependencies that slow a task-first tool.

## 4. Existing-site redesign: scan → diagnose → preserve → fix → verify

Before editing an existing site:

1. **Scan:** identify framework, package versions, styling/token sources, shared layouts, key routes, assets, interactive components, deployment approach.
2. **Baseline:** note current screenshots if browser access exists, primary user task, top SEO pages and keywords, nav/URLs/canonical/hreflang, analytics event names, form fields, brand/legal/consent copy, keyboard behavior, and performance if measurable.
3. **Diagnose:** list specific defects with file/route and observable evidence; distinguish visual defects, bugs, accessibility failures, missing states, performance hazards, and SEO risks. Prioritize user-blocking issues.
4. **Preserve by default:** do not silently change approved keywords, intent-page ownership, URL slugs, anchors, metadata, canonical/hreflang, primary nav labels, analytics events, input field names/order, brand wordmark, legal copy, or working tool logic.
5. **Fix minimally:** prefer typography, spacing, hierarchy, color consistency, states, and small layout changes before component rewrites; retain the existing framework and dependencies unless change is justified.
6. **Verify:** compare before/after appearance and behavior, check representative routes, confirm no core function or SEO output regressed, and log remaining uncertainty.

Document purposeful changes that affect protected items and obtain explicit owner approval first. For high-impact changes, use a reviewable commit/PR and record rollback guidance.

## 5. Image/reference → design → code (conditional)

Use when visual fidelity is central **and** real reference images or an image-generation/design tool are available. Not a prerequisite for routine CSS fixes or utility pages.

1. Capture the existing interface or acquire legitimate references; alternatively generate *section-specific* concept images for major marketing surfaces if the user wants new visuals.
2. Record a small design specification: viewport dimensions, type scale, spacing, grid, palette, imagery, component states, responsive collapse, and assets. A generated image is inspiration, not real text/data or accessible UI.
3. Implement actual semantic HTML/components using existing project tokens; map every shown control to functional behavior, never fake a working tool with a screenshot.
4. Compare rendered screenshots to the agreed reference at desktop **and mobile**; fix the biggest hierarchy, spacing, alignment, and typography mismatches before decorative details.
5. Verify real assets, layout stability, keyboard behavior, link targets, performance, and raw-HTML SEO content. If screenshot or image generation is unavailable, use written reference measurements and clearly report that visual comparison was not performed.

## 6. Motion/performance budget

- **Motion-first, performance-protected:** add purposeful, visually polished animation to tools, games and marketing surfaces whenever it improves the visitor's task or experience and performance permits. Avoid heavy scroll-jacking, unnecessary autoplay or focus-disrupting effects.
- Marketing pages may use expressive hero/product demos and feature-card storytelling. Animation needs a user benefit, but does not need separate owner approval. Optional showcase exports use `MOTION-SHOWCASE-PROTOCOL.md`.
- Prefer CSS `transform`/`opacity` for small motion; avoid re-rendering on every scroll/pointer frame, start costly effects only when helpful and visible, pause continuous offscreen loops, and respect `prefers-reduced-motion` with a visible static/no-JS fallback.
- Native CSS/SVG/Canvas/JavaScript/Web Animations API typically need no paid runtime API. Add Motion, GSAP, Three.js, new icon packs or assets only when licensing, task benefit, bundle size, operating cost and measured performance justify them.
- Measure or explicitly mark unverified mobile LCP, INP, CLS, JS transfer/long tasks, image/font loads, motion paint/CPU cost and core task responsiveness when relevant. Reference good Web Vitals: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1; never assert PASS without evidence. Reduce costly effects if measurements regress.

## 7. Visual acceptance and evidence

For every meaningful UI change, check:

- **Task first:** the tool entry/control/result is discoverable and works, including keyboard and touch. Marketing pages make the CTA and value proposition clear.
- **Consistency:** common navigation, tokens, typography, accent/radius rules, real content, forms and states remain coherent on adjacent page types.
- **Viewport coverage:** small mobile (~360px), typical mobile (~390px), tablet (~768px), small laptop (~1024px), wide desktop (~1440px); adjust for actual audience/device testing.
- **States:** initial, focus, hover, active, disabled, empty, loading, invalid/error, and success where applicable.
- **Regression:** approved keywords, heading structure, important raw HTML, route and navigation integrity, metadata/canonicals/hreflang, image links, structured data, core calculations and analytics remain intact.
- **Evidence:** record actual before/after route screenshots or visual observations, optional matched-reference overlays/SSIM/PSNR diagnostics, build/lint/type results, claim/CTA checks, interactive and reduced-motion states, performance data and outstanding issues. Mark missing measurements `NOT RUN`; never invent PASS.

Apply `IMPECCABLE-UI-QUALITY-GATE.md` for structured UX/a11y/responsive/i18n/edge-state/performance verification and record actual observations in `UI-RELEASE-EVIDENCE.md`. The Taste-inspired process guides visual direction; a detector rule is not authority to override brand or approved search architecture. Apply the existing `QA-CHECKLIST.md`, `SEO-GEO-QUALITY-GATE.md`, and `SEO-GEO-RELEASE-EVIDENCE.md` as the final release authority.

## Upstream references

- [Taste Skill project](https://github.com/Leonxlnx/taste-skill)
- [Taste Skill v2](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md)
- [Redesign Skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md)
- [Image-to-Code Skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/image-to-code-skill/SKILL.md)

Review upstream changes deliberately. The third-party default is experimental; do not silently auto-upgrade this protocol.
