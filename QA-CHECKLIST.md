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
- [ ] `TASTE-UI-PROTOCOL.md` was applied for the page type; design read, variance/motion/density choices, and first-screen task hierarchy are justified.
- [ ] Visitor mode (Operate / Read / Persuade / Experience) was set for each affected surface; tool/task views keep actual controls and results prominent.
- [ ] `IMPECCABLE-UI-QUALITY-GATE.md` was reviewed; false-positive aesthetic preferences have not overridden brand/user intent.
- [ ] Important fonts/color accents/radii/spacing are consistent; existing brand identity is preserved unless owner-approved.
- [ ] For redesigns, a concrete scan/diagnosis and before/after functionality + visual + SEO baseline was reviewed.
- [ ] No needlessly repeated generic card grids, nested containers or stock-image filler; justified exceptions are documented.

## Responsive
- [ ] Small mobile checked.
- [ ] Large mobile checked.
- [ ] Tablet checked.
- [ ] Desktop checked.
- [ ] Wide desktop checked.
- [ ] No horizontal overflow except intentional scrollers.
- [ ] Representative widths around 360/390/768/1024/1440px were visually checked where browser access exists, or skipped checks are marked `not run`.
- [ ] Tool controls and results path remain discoverable on small laptop and mobile viewports.
- [ ] Long localized text, Unicode/diacritics, text zoom, and any custom touch/drag controls were tested where applicable.

## SEO / GEO — governance
- [ ] Approved core keywords were preserved exactly unless owner-approved changes are documented.
- [ ] Numeric Volume/KD/CPC/SERP/traffic claims have an identified data source.
- [ ] Intent-to-canonical-page mapping is complete.
- [ ] No obvious cannibalization or near-duplicate intent pages.
- [ ] `SEO-GEO-PROJECT-BRIEF.md` is complete for this project.
- [ ] `SEO-GEO-QUALITY-GATE.md` was reviewed.
- [ ] Time-sensitive factual claims have a source/check-date/refresh rule where appropriate.

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

## GEO / AI-search readiness
- [ ] Important pages answer/define the core topic early where appropriate.
- [ ] Factual blocks can be understood without surrounding fluff.
- [ ] Tables/examples/questions are used only where useful.
- [ ] Tool assumptions, units, formulas, and limitations are explicit.
- [ ] Changing/factual claims use reliable sources where needed.
- [ ] No near-duplicate pages were created solely for AI-query variants.
- [ ] Important entities/names are consistent across page copy, metadata and schema.
- [ ] No special AI-only markup/files were added without a documented interoperability need.
- [ ] Training-crawler decisions are documented separately from Search crawl/index rules.
- [ ] AI-assisted/generated content adds original value and does not exist merely at scale.

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
- [ ] Dynamic effects justify their performance cost; existing dependencies and lighter CSS alternatives were considered before adding a motion library.
- [ ] Measurements are recorded when run; unmeasured Web Vitals are explicitly labeled as unverified, not passed.
- [ ] Form labels, accessible errors and complete empty/loading/invalid/disabled/success state behavior were exercised where applicable.
- [ ] P0/P1 interaction, accessibility, layout, SEO or functionality blockers are closed before release acceptance.

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
- [ ] `SEO-GEO-RELEASE-EVIDENCE.md` contains concrete evidence for this release.
- [ ] `UI-RELEASE-EVIDENCE.md` contains actual UI checks, scope, viewport and failures or explicit `NOT RUN` (do not invent pass results).
- [ ] If Impeccable CLI was used, its exact version, command, exit status (0/1/2), findings and waivers were documented; if unused, that fact is not a failure.
- [ ] A production baseline was recorded for important routes after acceptance.
- [ ] L3 full audit is performed when production data or a major review justifies it.
- [ ] Search Console AI/multimodal reporting is reviewed when the site has enough relevant data.

## Final visual review
- [ ] Hero is clear within seconds.
- [ ] Tool controls are obvious.
- [ ] Results are visually dominant when they should be.
- [ ] Mobile hierarchy remains strong.
- [ ] The site has a distinct brand language.
- [ ] The site still matches `DESIGN.md`.
- [ ] Existing functional controls and core calculations behave as before any visual redesign; keyboard, touch, and loading/error/empty states checked.
- [ ] Browser before/after screenshots or written visual evidence are recorded when available; unavailable captures are labeled `not run`.
- [ ] If image-to-code was used: major desktop/mobile discrepancies were reviewed, UI controls are implemented (not fake images), and assets are real.
