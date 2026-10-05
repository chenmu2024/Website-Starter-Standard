## What changed?

Describe the product, design, SEO/GEO, content, route/template, or technical changes.

## Design-system compliance

- [ ] I reviewed `DESIGN.md`.
- [ ] New UI reuses existing tokens/components.
- [ ] Any intentional design-language change was first reflected in `DESIGN.md`.
- [ ] No arbitrary gradients, glow, glassmorphism, shadows, radii, or colors were introduced.

## Responsive / accessibility

- [ ] Mobile checked.
- [ ] Tablet checked.
- [ ] Desktop checked.
- [ ] Keyboard/focus behavior checked.
- [ ] Important contrast and touch targets checked.

## SEO / GEO change gate

- [ ] I reviewed the applicable rules in `SEO-GEO-QUALITY-GATE.md`.
- [ ] Approved core keywords were preserved; any change is explicitly owner-approved.
- [ ] Metadata / heading hierarchy / canonical / robots behavior remain correct.
- [ ] New important routes are covered by crawlable internal linking and sitemap where applicable.
- [ ] Critical SEO content remains visible in raw HTML where required.
- [ ] Programmatic templates add real page-specific value; this change does not mass-create keyword/name swaps.
- [ ] Hreflang/canonical parity was checked if multilingual routes changed.
- [ ] Structured data remains truthful and valid if affected.
- [ ] No numeric SEO/keyword data was invented.

## L1 verification

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
