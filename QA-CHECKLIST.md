# Website Final QA Checklist

## Product
- [ ] Core user task works end-to-end.
- [ ] Main outputs/results are useful and understandable.
- [ ] Empty/error/loading states exist where necessary.
- [ ] All agreed important pages/features are present; required scope is not deferred behind an unfinished V1.

## Design system
- [ ] `DESIGN.md` is project-specific and complete.
- [ ] Pages use shared tokens/components.
- [ ] No unjustified gradients/glow/glass/shadows.
- [ ] No generic AI-template look.

## Responsive
- [ ] Small mobile checked.
- [ ] Large mobile checked.
- [ ] Tablet checked.
- [ ] Desktop checked.
- [ ] Wide desktop checked.
- [ ] No horizontal overflow except intentional scrollers.

## SEO / GEO — governance
- [ ] Approved core keywords were preserved exactly unless owner-approved changes are documented.
- [ ] Numeric Volume/KD/CPC/SERP/traffic claims have an identified data source.
- [ ] Intent-to-canonical-page mapping is complete.
- [ ] No obvious cannibalization or near-duplicate intent pages.
- [ ] `SEO-GEO-QUALITY-GATE.md` was reviewed.

## SEO / GEO — technical
- [ ] Titles/descriptions complete and intent-aligned.
- [ ] H1/H2/H3 structure correct.
- [ ] Canonicals correct and consistent with final URLs.
- [ ] Robots directives correct.
- [ ] Sitemap includes canonical indexable URLs only.
- [ ] Important primary content exists in raw HTML where required.
- [ ] Internal links are crawlable and tested.
- [ ] No important orphan pages.
- [ ] Structured data is truthful, valid, and currently applicable.
- [ ] Missing URLs return real 404 behavior.
- [ ] Redirects do not create avoidable chains.
- [ ] No accidental noindex/robots blocking.

## Programmatic SEO
- [ ] Each generated page has standalone value, not only a swapped keyword/name.
- [ ] Template/content differentiation was sampled across sibling pages.
- [ ] Low-value/duplicate variants are consolidated or excluded from indexation.
- [ ] Generated slugs are deterministic and collision-safe.
- [ ] Generated pages enter the correct hubs/internal links/sitemaps only after passing quality review.
- [ ] Large page batches comply with the review/stop heuristics in `SEO-GEO-QUALITY-GATE.md`.

## International SEO (if applicable)
- [ ] Target-market keywords were validated rather than mechanically translated.
- [ ] Language/region codes are intentional.
- [ ] Canonical and hreflang URLs align.
- [ ] Hreflang self-references and return relationships are complete.
- [ ] `x-default` is used only where a real fallback exists.
- [ ] Localized pages differ where market context requires it.

## GEO / answer readiness
- [ ] Important pages answer/define the core topic early where appropriate.
- [ ] Factual blocks can be understood without surrounding fluff.
- [ ] Tables/examples/questions are used only where useful.
- [ ] Tool assumptions, units, formulas, and limitations are explicit.
- [ ] Changing/factual claims use reliable sources where needed.
- [ ] No near-duplicate pages were created solely for AI-query variants.

## Content / media
- [ ] No placeholder copy.
- [ ] No fabricated statistics, citations, reviews, testimonials, or credentials.
- [ ] No repetitive thin sections.
- [ ] Images are relevant and load.
- [ ] No broken external assets.
- [ ] Image dimensions/aspect ratio prevent obvious layout shift.
- [ ] Alt text is meaningful and not keyword-stuffed.
- [ ] Calls to action match user intent.

## Performance / accessibility
- [ ] Images optimized.
- [ ] Fonts minimized/optimized.
- [ ] LCP/INP/CLS checked at least with an appropriate lab tool; field data labeled separately when available.
- [ ] Keyboard navigation works.
- [ ] Focus visible.
- [ ] Contrast acceptable.
- [ ] Touch targets usable.
- [ ] Reduced-motion respected where applicable.

## Technical / production
- [ ] Production build succeeds.
- [ ] No primary-route 404s.
- [ ] No obvious console/runtime errors.
- [ ] Environment variables documented.
- [ ] Cloudflare configuration documented when used.
- [ ] Real production URL was checked after deployment.
- [ ] robots.txt and sitemap are reachable in production.

## Audit / drift
- [ ] Applicable L1 checks passed for SEO-sensitive changes.
- [ ] L2 release audit passed before launch/major release.
- [ ] A production baseline was recorded for important routes after acceptance.
- [ ] L3 full audit is performed when production data or a major review justifies it.

## Final visual review
- [ ] Hero is clear within seconds.
- [ ] Tool controls are obvious.
- [ ] Results are visually dominant when they should be.
- [ ] Mobile hierarchy remains strong.
- [ ] The site has a distinct brand language.
- [ ] The site still matches `DESIGN.md`.
