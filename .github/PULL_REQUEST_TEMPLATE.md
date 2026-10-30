## What changed?

Describe the product, design, SEO/GEO, content, route/template, or technical changes.

## Design-system compliance

- [ ] I reviewed `DESIGN.md`.
- [ ] New UI reuses existing tokens/components.
- [ ] Any intentional design-language change was first reflected in `DESIGN.md`.
- [ ] No arbitrary gradients, glow, glassmorphism, shadows, radii, or colors were introduced.
- [ ] I applied the page-type and redesign requirements in `TASTE-UI-PROTOCOL.md` when UI changed.
- [ ] Tool-first interactions were not displaced by decorative heroes, and existing brand/functional/SEO invariants remain intact.

- [ ] Where applicable, Persuade/ad/comparison entry promises, primary CTA and source-backed commercial proof were verified.
- [ ] Useful motion was considered/added without harming task speed, accessibility, SEO or performance; static/reduced-motion states were preserved.
- [ ] If UI changed, I reviewed `IMPECCABLE-UI-QUALITY-GATE.md` and classified each relevant surface (Operate/Read/Persuade/Experience).
- [ ] Optional CLI/Hook/Live integrations were not silently installed/enabled; any deliberate tooling choice and reviewed version are documented.

## Responsive / accessibility

- [ ] Mobile checked.
- [ ] Tablet checked.
- [ ] Desktop checked.
- [ ] Keyboard/focus behavior checked.
- [ ] Important contrast and touch targets checked.
- [ ] Visual checks covered mobile, tablet, small laptop, and desktop where tooling was available; skipped checks are marked `not run`.

- [ ] When an approved reference exists, a matched-viewport rendered comparison was performed or correctly marked `NOT RUN`.

## UI quality evidence

- [ ] Real primary task, meaningful empty/invalid/error states, keyboard/touch, long text/i18n and target viewports were checked where applicable.

- [ ] Motion start/end/interruption, reduced-motion and no-JS/static fallback were tested where applicable; optional MP4/GIF only when expressly scoped.
- [ ] Applicable P0/P1 UI blockers were fixed before declaring the release ready.
- [ ] `UI-RELEASE-EVIDENCE.md` (or equivalent linked PR evidence) records actual executed checks, reproducible results and explicit `NOT RUN` items; Impeccable detector findings are not treated as proof of full quality.

## Research intake / scope protection

- [ ] If new site/major feature/pivot: I linked the approved gefei-seo handoff (repo/commit or document), or explicitly documented owner-approved exception.
- [ ] Approved target keywords, primary intents, markets, monetization goals and required product features remain unchanged unless owner-approved.
- [ ] The intended route map follows `BUILD-INTAKE-CONTRACT.md`; research-unknown items are not claimed verified.
- [ ] Existing-site technical/UI repairs did not start a speculative keyword or product pivot.
- [ ] No paid recurring APIs/servers/services were silently introduced.


## Trust / third-party GEO report (when applicable)

- [ ] Reviewed `TRUST-AND-STRUCTURED-DATA-GATE.md`; any scanner finding judged by real page type, impact and observed evidence, not an arbitrary score.
- [ ] No fabricated operator, author, organization, `sameAs`, freshness dates, awards or testimonials.
- [ ] Relevant formulas, sample outputs, date-/country-sensitive rules, privacy/network/storage/ads behavior verified or NOT RUN/N/A.
- [ ] Truthful About/Contact/Privacy and applicable Terms are reviewed. Inapplicable `llms.txt`, author markup and forced citations marked N/A.

## SEO / GEO change gate

- [ ] I reviewed the applicable rules in `SEO-GEO-QUALITY-GATE.md` and the project brief.
- [ ] Approved core keywords were preserved; any change is explicitly owner-approved.
- [ ] Metadata / heading hierarchy / canonical / robots behavior remain correct.
- [ ] New important routes are covered by crawlable internal linking and sitemap where applicable.
- [ ] Critical SEO content remains visible in raw HTML where required.
- [ ] Programmatic templates add real page-specific value; this change does not mass-create keyword/name swaps.
- [ ] Hreflang/canonical parity was checked if multilingual routes changed.
- [ ] Structured data remains truthful and valid if affected.
- [ ] No numeric SEO/keyword/AI-visibility data was invented.
- [ ] Factual/time-sensitive claims have sources and freshness handling where needed.
- [ ] No special AI-only markup/files or crawler rules were added without a documented reason.

## L1 verification

Attach or summarize concrete evidence in `SEO-GEO-RELEASE-EVIDENCE.md` or the PR description.

- [ ] Build/type/lint checks relevant to this project pass.
- [ ] Changed important routes do not return unintended 404/redirect behavior.
- [ ] Broken links/assets introduced by this change were checked.
- [ ] SEO-sensitive regressions were checked against the previous accepted state where possible.

## Production readiness

- [ ] Build succeeds.
- [ ] Main user task works end-to-end.
- [ ] Images/assets load.
- [ ] Relevant items in `QA-CHECKLIST.md` were verified.
- [ ] If this is a release, the L2 release audit and production verification are complete.
