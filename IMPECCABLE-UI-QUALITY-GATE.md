# Impeccable-Inspired UI Quality Gate

> Project-owned, **mandatory review process** for AI-assisted websites. Selectively derived from [pbakaus/impeccable](https://github.com/pbakaus/impeccable), inspected 2026-10-08. **Impeccable itself, its CLI, hooks, browser extension, Live mode, binary downloads, and paid services are optional**. This document is not a claim that the detector was installed or ran.

## 0. Authority, boundaries, and rules of evidence

- Preserve explicit user requirements, approved core keywords, primary search intent/URL ownership, tool calculations, source content, legal/consent text, brand commitments, analytics event names, and existing functional controls. Do not silently rename or replace them for design reasons.
- `SEO-GEO-QUALITY-GATE.md` remains the authoritative SEO/GEO policy; `DESIGN.md` is the project's visual/token authority; `TASTE-UI-PROTOCOL.md` provides contextual art direction. This file supplies UI quality-control **process, failure triage, and evidence**.
- The Impeccable detector has documented 59 deterministic rules, but these are **heuristics**, not standards, SEO requirements, accessibility certification, or a complete functional test suite. An aesthetic finding can be legitimately waived with documented product/brand justification.
- Distinguish `PASS`, `FAIL`, `NOT RUN`, and `NOT APPLICABLE` for each applicable check. Do not infer a pass from a clean build, agent reasoning, or a detector exit code of 0.
- Favor no-cost inspections and existing project dependencies. Never add background monitoring, hosted services, browser extensions, global installation, automatic edit hooks, or paid APIs by default.

## 1. Classify each surface by visitor goal

Choose **per page/surface**, not once for the entire domain:

| Mode | Primary success | Examples | UI priority |
|---|---|---|---|
| **Operate** | Complete a task correctly | calculators, text generators, Minecraft tools, games, SaaS app views | inputs, states, result visibility, feedback, fast interactions |
| **Read** | Understand information | SEO articles, help, instructions, FAQs | information architecture, headings, readable text, evidence, navigation |
| **Persuade** | Make an informed choice/action | marketing home, product description, pricing | clear proposition, credible proof, relevant CTA |
| **Experience** | Explore/showcase the artifact | design portfolio, interactive gallery | artifact-first visual composition, purposeful motion |

A calculator website can contain an Operate tool page and a Read help article; do not turn the tool into an oversized cinematic marketing hero. Record mode, page kind, first-screen success and constraints in `DESIGN.md` or a route brief.

## 2. Required workflow for new or substantially changed UI

1. **Capture product truth:** target user, core job, user-visible copy, units/calculations, languages, known legal/trust constraints, owned keywords, important paths, success criteria. Existing facts must not be reinvented to fit a design style.
2. **Capture incumbent design:** inspect actual relevant files, framework/version, shared components, CSS tokens, screenshots if a browser is available, navigation, responsive layout, accessibility behavior, current functional states, analytics and SEO baselines.
3. **Diagnose before fixing:** collect observable failures; separate deterministic code issues, rendered-browser evidence, design criticism, UX/user-task concerns, SEO regressions, and subjective style choices.
4. **Prioritize:** fix broken operations, unreadable text, unreachable controls, accessibility barriers, broken responsive layouts, and serious regressions before decorative refinements. Tackle shared design-system defects at the token/component level.
5. **Implement minimal coherent changes:** prefer existing stack/tokens, support input/error/loading/empty/disabled/success states, preserve navigation/canonical routes and completed tool scope. Use Taste Skill for visual direction only when appropriate.
6. **Test full task paths:** use the tool from input through valid output; test invalid/empty/extreme inputs and mobile/keyboard/touch behavior; verify URLs and core content are unchanged unless approved.
7. **Verify in bounded rounds:** one batched desktop+mobile visual and functional inspection, address findings as a batch, then at most one final confirmation pass where practical. If blockers remain, record them explicitly rather than claiming completion.
8. **Record evidence:** use `UI-RELEASE-EVIDENCE.md` together with SEO/GEO release evidence; mark unexecuted checks as `NOT RUN`.

For small, non-visual content fixes, scope this process proportionately; still preserve SEO and functionality.

## 3. Five UI quality dimensions

### A. Accessibility and interaction

- Semantics/heading landmarks; reachable controls; keyboard navigation and visible focus; accessible names; form labels and correct error association.
- Actual text/input/control contrast, including against images and in supported themes; readable zoom/text resizing; touch targets usable; avoid keyboard traps.
- Prefer reduced-motion handling and avoid motion that blocks the task.
- Check real initial, loading, empty, invalid, error, disabled, active and success states as applicable. A detector cannot prove these scenarios work.

### B. Responsive and localization hardening

- Sample representative widths around 360, 390, 768, 1024 and 1440px (adjust for target users); include a small laptop, not just a large desktop.
- Long Spanish/Portuguese words, diacritics, very long generated nicknames, Unicode/emoji, copy/paste, truncation, wrapping and scrolling.
- Number formatting, decimal separators, currency and date rules; check domain-specific conversion/rounding behavior separately from aesthetics.
- Empty strings, invalid numbers, very large numbers, very long results, 100+ repeated items when relevant, offline/failed requests, API errors and timeouts if a network exists.
- Mouse, keyboard and touch paths; interrupted drag/scroll on custom controls where relevant.

### C. Visual consistency and design judgment

- `DESIGN.md` tokens govern color, type, spacing, radii, state colors, components, imagery and motion.
- Check hierarchy, first-screen task prominence, alignment, density, copy clarity, CTA consistency, legible outputs, real assets and broken images.
- Watch for gratuitous cards-in-cards, repeated equal-card grids, excessive glows, poorly justified animation, and stock-image filler.
- **Do not hard-ban** Inter, neutral palettes, purple, centered heroes, or standard form layouts. Intentional brand and usability decisions outrank anti-slop heuristics.
- A critique (human or LLM) is judgment with rationale, never a deterministic PASS.

### D. Measured performance and robustness

- Check LCP, INP and CLS with appropriate tools and label lab vs field evidence accurately. Reference good-threshold targets: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1, not assumed test results.
- Inspect JS/CSS bundles, render work, main-thread blocking, fonts, images, hydration, network load, CLS reservation and unnecessary third-party scripts.
- Optimize only demonstrated bottlenecks; compare before/after when possible. Add no animation package just to decorate a tool.
- Confirm offline/static fallbacks and responsive layout behavior when relevant. Avoid dependencies that create ongoing costs.

### E. Implementation integrity and regression

- Build/type/lint/unit tests (where present), route navigation, external links, images, accessibility and visible interactivity should not regress.
- Verify approved keywords, content, H1/H2, raw HTML visibility, title/description, canonical/hreflang, structured data, sitemap, robots, analytics and tool logic against the pre-change baseline.
- AI-generated visuals must not stand in for actual form fields or functioning tool controls.
- When a check is impossible, document the blocking environment/tool condition and do not claim that it passed.

## 4. Severity and acceptance

| Level | Meaning | Treatment |
|---|---|---|
| **P0 blocker** | Main tool broken, data loss, severe security/privacy or major site unavailability | Do not ship; fix or explicitly stop |
| **P1 blocker** | Core task obstructed, major accessibility/contrast failure, key responsive failure, critical SEO regression | Do not mark release accepted |
| **P2** | Meaningful but nonblocking workflow/design issue | Fix where feasible; document owner-approved deferral |
| **P3** | Cosmetic/subjective issue with no demonstrated task impact | Optional; avoid endless micro-polishing |

A clean Impeccable scan is only one piece of evidence. P0/P1 issues found by real interaction, code review or search/production QA remain blockers even if the scan exits 0.

## 5. Optional Impeccable tooling (explicit opt-in; not a dependency)

The **default** is to follow Sections 1–4 without installing anything. When a particular repository benefits from the tool and the owner approves:

1. Review the package, source/license, release version, runtime, installer behavior, permissions and any external binary/hook downloads. Pin a known reviewed release rather than relying on an unchecked auto-update.
2. In a trusted local checkout, install into the **project scope** with hooks disabled initially. Example syntax from upstream, verify version and platform before use:

   ```bash
   npx impeccable install --providers=codex --scope=project --no-hooks
   ```

   The `npx` installer requires Node.js 22.18+ in the reviewed upstream docs; the detector binary runs separately.
3. For manual scans, use an existing local source directory, for example:

   ```bash
   npx impeccable detect --json src/
   ```

   Exit code **0** = completed without primary findings; **2** = completed with primary findings; **1** = scanning failed for at least one requested target. A 1 is **not** a clean pass. Record exact command, scanner version, output and scope.
4. For rendered URLs, `npx impeccable detect https://example.com` additionally needs an installed compatible Chrome/Chromium/Edge browser. Browser evidence is a separate check from source scanning.
5. Optional AI actions (when installed in a compatible coding harness): `init`, `document`, `audit`, `critique`, `harden`, `adapt`, `optimize`, `polish`. Use commands only where relevant and preserve incumbent design and SEO.
6. **Hooks:** do not turn on edit-time Hook manifests by default. They can execute a downloaded local binary, insert messages into coding agents or interrupt writes. Review trusted repo, hook scope, privileges and ignore rules first, then obtain explicit opt-in.
7. **Live mode:** local checkout + trusted development server only; no production-site code edits, no weakening CSP. Review any shell validation scripts. No need for Live mode on every static tool site.
8. **Browser extension:** optional; inspect its host permissions and use only where appropriate. It is not necessary for baseline compliance.
9. If installed, document how to disable/uninstall, avoid committing ephemeral runtime files, and preserve project-owned design/source documents.

Impeccable's built-in aesthetic rules are not laws. Use narrowly justified waivers rather than blindly changing an established brand or suppressing all checks. Never silently rewrite the user's site because of a detector warning.

## 6. Required evidence and release gating

- Attach evidence or `NOT RUN` notes per route/task/viewport in `UI-RELEASE-EVIDENCE.md`; include error/edge cases, source vs browser scan distinction, scanner version when used, performance baseline, and fixed/remaining issues.
- Keep `SEO-GEO-RELEASE-EVIDENCE.md` for SEO-sensitive release assertions; neither document substitutes for production validation.
- New sites cannot be declared complete while applicable P0/P1 items remain open, or when the primary user task and production URL have not been checked.
- Do not declare tool-based checks as passing merely because the protocol was installed or linked.
- This starter repository contains **no installed Impeccable binary, Hook, extension, or automatic quality test**; downstream projects choose tools, run checks, and attach real results.

## Sources and maintenance

- [Impeccable repository](https://github.com/pbakaus/impeccable)
- [Skill source](https://github.com/pbakaus/impeccable/blob/main/skill/SKILL.src.md)
- [Detector/CLI usage](https://github.com/pbakaus/impeccable/blob/main/README.npm.md)
- [Audit](https://github.com/pbakaus/impeccable/blob/main/skill/reference/audit.md), [Harden](https://github.com/pbakaus/impeccable/blob/main/skill/reference/harden.md), [Optimize](https://github.com/pbakaus/impeccable/blob/main/skill/reference/optimize.md), [Polish](https://github.com/pbakaus/impeccable/blob/main/skill/reference/polish.md)

Third-party behavior, dependencies and command syntax may change. Re-review upstream before enabling external execution.
