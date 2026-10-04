# Website Starter Standard

A reusable baseline for AI-assisted website projects.

## Purpose

This starter prevents a common failure mode in AI-built websites: development begins before the visual system, SEO architecture, and QA rules are fixed, so later iterations become inconsistent and expensive.

## Mandatory workflow

1. Research user intent and keywords.
2. Analyze competitors and 2–4 high-quality design references.
3. Complete the project PRD.
4. Customize `DESIGN.md` for the specific project.
5. Define tokens and reusable components.
6. Implement the site.
7. Complete SEO/GEO and responsive work.
8. Run Visual QA and final QA.
9. Deploy and verify production.

## Files

- `AGENTS.md` — mandatory operating rules for coding/design agents.
- `DESIGN.md` — project-specific design-system template.
- `SEO-GEO.md` — search and answer-engine standards.
- `CLOUDFLARE.md` — Cloudflare deployment record and checks.
- `QA-CHECKLIST.md` — final acceptance checklist.

## Design references

`VoltAgent/awesome-design-md` can be used as a design-system reference database. Use it to learn design logic and combine appropriate patterns; do not simply clone one brand.

## Key rule

A website is not considered complete because it builds successfully. It is complete only after product, design-system, SEO/GEO, responsive, visual, and production checks pass.
