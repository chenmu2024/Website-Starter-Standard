# Website Starter Standard

A reusable baseline for AI-assisted website projects.

## Purpose

This starter prevents a common failure mode in AI-built websites: development begins before the product, keyword architecture, visual system, SEO/GEO architecture, and QA rules are fixed, so later iterations become inconsistent and expensive.

## Mandatory workflow

1. Research real user demand, search intent, keywords, competitors, and monetization.
2. Lock approved core keywords and map one primary intent to one canonical destination.
3. Analyze 2–4 high-quality design references.
4. Complete the project PRD and full information architecture.
5. Customize `DESIGN.md` for the project.
6. Complete `SEO-GEO-PROJECT-BRIEF.md` and the architecture in `SEO-GEO-QUALITY-GATE.md` before mass page production.
7. Define tokens and reusable components; apply the page-type-aware audit and UI workflow in `TASTE-UI-PROTOCOL.md`.
8. Implement the complete planned site, including programmatic/international rules where applicable.
9. Run L1 checks during development and collect concrete evidence in `SEO-GEO-RELEASE-EVIDENCE.md`.
10. Run the L2 release audit, Visual QA, and `QA-CHECKLIST.md` before launch.
11. Deploy and verify the real production site.
12. Record a production SEO baseline for later drift/regression checks; use L3 audits when real production data exists.

## Files

- `AGENTS.md` — mandatory operating rules for coding/design agents.
- `TASTE-UI-PROTOCOL.md` — selective Taste Skill-inspired visual audit, anti-generic design, reference-to-code workflow and UI regression gate.
- `DESIGN.md` — project-specific design-system template.
- `SEO-GEO.md` — concise search and answer-engine policy.
- `SEO-GEO-QUALITY-GATE.md` — detailed mandatory SEO/GEO, programmatic SEO, international SEO, audit, and launch gate.
- `SEO-GEO-PROJECT-BRIEF.md` — project-level keyword, intent, indexation, source, entity, schema, and AI-search plan.
- `SEO-GEO-RELEASE-EVIDENCE.md` — release proof template for route checks, raw HTML, schema, crawlability, performance, and production verification.
- `CLOUDFLARE.md` — Cloudflare deployment record and checks.
- `QA-CHECKLIST.md` — final acceptance checklist.
- `.github/PULL_REQUEST_TEMPLATE.md` — change-level compliance checklist.

## Design references

`VoltAgent/awesome-design-md` is a required design-reference source when applicable. Taste Skill's design-read, redesign audit, and conditional image-to-code methods are selectively adapted in `TASTE-UI-PROTOCOL.md` (not blindly installed). Learn and combine appropriate design logic; do not clone a single brand's visual identity. For tool-first websites, usability, crawlability, and performance outrank cinematic art direction.

## Current search / AI-search position

Google's generative-AI search features do not require special AI-only markup or a separate GEO stack. The standard therefore treats GEO as an extension of strong SEO: crawlable content, unique value, clear entities, primary-source evidence, useful page structure, and extractable answers. `llms.txt` may be used for interoperability with other systems, but it is not required for Google Search or Google's generative-AI search features.

## SEO/GEO reference model

`AgriciDaniel/claude-seo` is a useful open-source reference for technical SEO, GEO, programmatic SEO, international SEO, schema, auditing, and drift concepts. This starter distills applicable rules into `SEO-GEO-QUALITY-GATE.md`; downstream projects do not need the plugin installed unless explicitly useful.

Rules from third-party projects are not automatically treated as Google requirements. Primary-source documentation wins, and numeric keyword/SEO data must come from an identified data source.

## Owner defaults

- Approved keywords must not be silently changed.
- Prefer zero/freemium infrastructure until traffic or revenue validates paid services.
- Multilingual sites require market-specific keyword validation and international SEO QA.
- Build the complete agreed site rather than using unfinished "V1/V2 later" as a substitute for required scope.

## Key rule

A website is not complete because it builds successfully. It is complete only after product, design-system, SEO/GEO, programmatic/international rules where applicable, responsive, visual, production, and post-deployment verification pass.
