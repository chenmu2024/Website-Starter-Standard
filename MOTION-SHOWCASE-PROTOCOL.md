# Motion and Product Showcase Protocol

> Project-owned guidance derived selectively from [elayadesign/ai-design-skills](https://github.com/elayadesign/ai-design-skills) (MIT). **Motion-first, performance-protected:** ordinary web animation is encouraged by default where beneficial; complex showcase production and exports are opt-in.

## 1. Priority and scope

Authority: explicit owner requirements > approved SEO keywords, routes, product logic and legal/trust constraints > project `DESIGN.md` > UI/SEO release gates > this protocol > external style examples.

**Routine animation is encouraged without additional approval** for buttons, hover/active/focus feedback, form validation, tool previews, result transitions, meaningful loading/progress, feature cards, appropriate hero demonstrations, charts, visualizations and games. Do not impose an animation-count quota.

**Full showcase workflow is conditional:** use this for Figma-to-motion reconstruction, complex animated product demos, reusable promotional loops, or explicitly requested GIF/MP4 exports. Animated websites do not automatically require a showcase export. No forced Figma, paid API, animation framework, new server, background job, or database.

## 2. Choose motion by visitor intent

| Intent | Good motion | Avoid |
|---|---|---|
| Operate (tool, calculator, editor, game) | immediate feedback, result refresh, input status, functional visual transitions, meaningful play animation | obscured inputs, delayed results, decorative looping |
| Read (articles, help, FAQs) | disclosure, navigation, helpful progress cues where warranted | hiding reading text until scroll, disruptive parallax |
| Persuade (SaaS marketing, ad pages) | honest product demonstration, feature-card storytelling, CTA feedback, smooth section composition | fabricated results/proof, distracting sales animation |
| Experience (gallery, simulator, presentation) | richer Canvas/SVG motion, coherent sequences, interactive exploration | unnecessary CPU drain, unbounded autoplay or inaccessible motion |

Movement should explain state, create continuity, make a product understandable or contribute to the intended experience. Static is permissible when movement adds no value.

## 3. Motion design specification

Before complex effects, document the affected element, desired user benefit, starting/intermediate/rest states, duration/easing from `DESIGN.md`, start trigger (user/load/viewport), one-shot versus loop, interrupt/repeat behavior and static/reduced-motion fallback.

Use **CSS, SVG, Canvas, JavaScript, Web Animations API** first. Prefer transforms/opacity for small feedback, but profile full-screen filters, large blur, clipping/masks, shadows and layout-moving properties; none is automatically fast on every device. Add a licensed Motion/GSAP/other library only where there is an actual need, a compatible license, and acceptable bundle/performance effects. Client-side animation itself requires no paid runtime API or server.

- Core form controls, main tool output and crawlable content must be available without animation and without JavaScript motion initialization. Avoid default CSS that hides essential content until an observer fires.
- Use `prefers-reduced-motion: reduce` to show a readable, functional resting state without nonessential motion.
- Keep keyboard focus stable and accessible, avoid layout shifts and unresponsive inputs, preserve touch interactions and avoid repetitive flashes.
- For continuous effects, pause when offscreen or on hidden document tabs where suitable; limit battery/CPU impact.
- Measure important mobile flows and actual LCP/INP/CLS when feasible. Simplify or disable high-cost animations rather than degrading core performance or accessibility.

## 4. High-fidelity reconstruction (only when there is a real source)

1. Distinguish **functional web feature** (live semantic HTML/actual controls) from **showcase-only exported artwork** (layered images and type allowed for visual fidelity).
2. Identify approved reference: original Figma node/file, owned screenshot or appropriately licensed imagery. Figma API is optional, may require authentication/provider rate limits; never reveal secrets.
3. Identify static background, masks, layer order, nested clipping, joined app frame vs separate cards, type and shadow behavior. Keep the approved design unchanged unless redesign requested.
4. Build and capture the final/rest **still frame before any motion**. Capture original and implementation at the same viewport/device scale/browser/font/theme/state. Fix structural differences first.
5. Optional image overlays, diff maps, SSIM and PSNR are diagnostics, not universal pass thresholds. Compare text legibility and real interaction separately. Report missing assets or insufficient source access explicitly.
6. Give each visual a concise real story: a chart inspects a point, a list receives an item, a converter displays an output, or a calendar selects a slot. Return to a clear final/rest state; exported loops should close without visible seams.

## 5. Website animation versus showcase timeline

**Website:** run user-triggered or in-viewport effects when beneficial; pause continuous effects when out of view; content and controls must work while animating. The full showcase pipeline is **not** needed for normal web animations.

**Showcase:** when requested, plan static beginning, staggered reveal, visual stories, return to rest and seamless repeat. Animated layers must respect the reference's clipping, depth and background. Avoid inventing statistics to create visually interesting motion.

## 6. Optional local media export

Only when a GIF/MP4 is requested or explicitly included in scope:
1. Establish rights, destination, format, exact content, aspect ratio, resolution, FPS, duration, file-size budget and readable small-screen result.
2. Where tools permit, use a controlled Playwright clock to capture deterministic browser frames; use local FFmpeg to encode H.264 MP4 or optimized GIF/WebP. No recurring API/backend required.
3. Inspect a contact sheet of start/load/story/rest, overflow, clipping, state-reset errors, loop seam and misleading animated claims.
4. Record real output filename, dimensions, FPS, duration, codec, bytes and commands. If source, browser or encoder is unavailable, record `NOT RUN`, never invent successful artifacts.

Do not automatically install Playwright/FFmpeg or run external executables without checking the environment and project's dependency policy. A Figma integration, if used, is a separate data-source/authentication decision, not an animation runtime requirement.

## 7. Verification and release evidence

Report actual route, tested viewports, animation and task states, repeated/interrupt interactions, focus/touch, reduced-motion, no-JS fallback, offscreen pause and performance before/after when measured. Optional visual-source comparisons and requested exports have their own evidence. Use `UI-RELEASE-EVIDENCE.md`: `PASS`, `FAIL`, `NOT RUN`, `NOT APPLICABLE`. Task, SEO, accessibility and significant performance regressions are blocking even when an animation looks attractive.

## Attribution

Selective principles from [landing-page-design](https://github.com/elayadesign/ai-design-skills/blob/main/skills/landing-page-design/SKILL.md) and [design-to-motion](https://github.com/elayadesign/ai-design-skills/blob/main/skills/design-to-motion/SKILL.md), MIT. Third-party presets are not automatically installed, updated, or given higher priority than existing project rules.
