# SEO / GEO Release Evidence

> Implementation evidence only. Record research/approved keywords origin under `BUILD-INTAKE-CONTRACT.md` and `SEO-GEO-PROJECT-BRIEF.md`; no independent demand or revenue claim belongs here.

> Fill this for an SEO-sensitive release. Record evidence, not assumptions. Use N/A when a category truly does not apply.

## Release

- Project:
- Production URL:
- Branch/commit:
- Release date:
- Reviewer:

## 1. Build and deterministic checks

| Check | Command/tool | Result | Evidence / notes |
|---|---|---|---|
| Type/lint/build | | | |
| Required routes | | | |
| 404/redirect behavior | | | |
| Broken internal links | | | |
| Broken assets | | | |
| Sitemap coverage | | | |
| Canonical/robots parity | | | |
| Duplicate title/description/H1 | | | |
| Structured-data syntax | | | |
| hreflang parity | | | |
| Orphan pages | | | |

## 2. Raw HTML verification

Sample important indexable pages and record whether critical SEO content is present before client JS.

| Route | Title | H1/main answer | Canonical | Robots | Critical links | Schema |
|---|---|---|---|---|---|---|
| | | | | | | | |

## 3. Intent / content quality

- Approved keywords preserved:
- One canonical destination per primary intent:
- No new near-duplicate AI-query pages:
- Programmatic sample reviewed:
- AI-assisted/generated content adds original value:
- Direct answers are useful and not keyword-stuffed:
- Factual/changing claims have valid sources/check dates:

## 4. GEO / AI-search evidence

- Important answer blocks are self-contained:
- Original value present (tool/data/examples/screenshots/analysis):
- Entity naming consistent across copy/metadata/schema:
- No unsupported "AI visibility" claims:
- No unnecessary AI-only markup/files:
- Google-Extended/training crawler policy reviewed separately from Search:
- `llms.txt` present only if there is a real interoperability reason:

## 4A. Page-type trust / structured-data evidence

Follow `TRUST-AND-STRUCTURED-DATA-GATE.md`. Use PASS / FAIL / NOT RUN / N/A and supply reasons for N/A. Do not claim a release passed when applicable P0/P1 checks are unverified.

| Check | Page type / route | Actual test or URL evidence | Severity (or N/A) | Result and rationale |
|---|---|---|---|---|
| Site/operator identity, matching WebSite/Person/Organization/WebApplication schema | | | | |
| Authentic sameAs and editorial author/date fields if applicable | | | | |
| Formula, units, rounding, sample expected outputs and edge cases | | | | |
| Official sources/effective dates for regulatory/financial calculations | | | | |
| Browser/network/storage/analytics/ad data flows match Privacy copy | | | | |
| About/Contact/Privacy/Terms and applicable limitations/disclaimers | | | | |
| Syntax, semantic accuracy and Google schema eligibility checks separately | | | | |
| Vendor GEO issues triaged; optional items N/A or documented | | | | |

P0/P1 errors block affected release; P2 improvements can be documented as owner-approved follow-up. Optional P3/N/A items never independently block release.

## 5. Performance / UX / accessibility

Record actual tools/results when measured.

| Check | Environment | Result | Notes |
|---|---|---|---|
| Mobile layout | | | |
| Desktop layout | | | |
| LCP lab | | | |
| INP/interactivity lab | | | |
| CLS lab | | | |
| Keyboard/focus | | | |
| Touch targets | | | |
| Reduced motion | | | |

Do not label lab data as CrUX field data.

## 6. Production verification

- Production deploy completed:
- Production commit/version confirmed:
- robots.txt reachable:
- sitemap reachable:
- Canonicals use production host:
- Important routes return expected status:
- Social images/assets reachable:
- No obvious runtime/console failures:

## 7. Search Console / post-launch follow-up

Only fill when data exists.

- Sitemap submitted/accepted:
- Indexation checked:
- Query/page baseline exported:
- Generative-AI Search reporting reviewed:
- Multimodal/image-input reporting reviewed if relevant:
- CrUX field data available:
- Follow-up date:

## 8. Drift baseline

For important routes preserve:

- title/meta
- H1/headings
- canonical
- robots
- hreflang
- schema types
- main-content fingerprint/word count where useful
- critical internal links
- sitemap membership
- status/redirect target
- performance snapshot

Baseline location:

## 9. Findings and exceptions

For each unresolved exception record severity, owner, due date and verification method.

| Severity | Route/component | Finding | Why accepted now | Owner | Verification |
|---|---|---|---|---|---|
| | | | | | |
