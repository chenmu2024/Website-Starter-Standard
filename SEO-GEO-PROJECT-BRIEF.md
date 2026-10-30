# SEO / GEO Project Brief

> Complete this file for each website before mass page production. It converts **owner-approved `gefei-seo` research handoff** into a project-specific technical search architecture. See `BUILD-INTAKE-CONTRACT.md`. Do not use this engineering brief to invent keyword demand.

## 1. Project identity

- Project / brand:
- Production domain:
- Primary language:
- Target countries/regions:
- Product type:
- Primary user task:
- Monetization:
- Cost constraints:
- Primary site purpose/focus:

## 2. Approved keyword source

- Research origin (repo/commit or signed document):
- Research decision (GO/TEST/HOLD/REJECT) and approved scope:
- Owner approval/date:
- Unverified research inputs and safeguards:

Copy the **exact owner-approved** keyword set and source data from the research handoff. Engineering can select URL implementation details, but never silently revise the target keyword, market, intent or product scope.

| Keyword | Language/market | Volume | KD | CPC | Data source | Checked date | Owner-approved? |
|---|---|---:|---:|---:|---|---|---|
| | | | | | | | |

Rules:
- Do not silently replace approved keywords.
- Unknown metrics stay unknown; do not infer them.
- Market-specific variants require their own validation.

## 3. Intent ownership / canonical map

One primary intent should have one canonical destination.

| Primary intent | Approved keyword(s) | Canonical route | Page type | Index? | Parent hub | Notes |
|---|---|---|---|---|---|---|
| | | | | | | |

Record intentional overlaps and why they are not cannibalization.

## 4. Route and indexation policy

| Route/template | Purpose | Canonical rule | robots rule | Sitemap? | hreflang? | Programmatic? |
|---|---|---|---|---|---|---|
| | | | | | | |

Parameters/facets:
- Allowed crawlable parameters:
- Blocked/noindex parameter patterns:
- Redirect rules:
- Legacy URL rules:

## 5. Internal-link architecture

Define hubs/spokes and required crawl paths.

- Primary hub:
- Secondary hubs:
- Critical child pages:
- Related-tool/content rules:
- Breadcrumb model:
- Orphan-page prevention rule:
- Pages intentionally not promoted from core authority pages:

## 6. GEO / AI-search answer plan

For each important page, define what should be directly extractable without creating duplicate AI-only content.

| Route | Direct answer/definition | Original value | Evidence/source need | Useful table/example/tool | Freshness sensitivity |
|---|---|---|---|---|---|
| | | | | | |

Google-specific rule:
- Normal SEO foundations apply to Google's generative-AI Search features.
- Do not create special AI-only markup/pages solely for Google AI visibility.
- `llms.txt` is optional interoperability metadata, not a Google requirement.

## 7. Evidence / source registry

Use this for factual or changing claims.

| Claim/topic | Primary source | What it supports | Checked date | Refresh cadence/trigger | Fallback if unavailable |
|---|---|---|---|---|---|
| | | | | | |

Never cite a source that does not actually support the visible claim.

## 8. Entity map

| Entity | Type | Canonical name | Stable URL/@id | Alternate names | Source of truth |
|---|---|---|---|---|---|
| Brand/site | Organization/WebSite | | | | |
| | | | | | |

Keep entity naming consistent in visible content, metadata and JSON-LD.

## 8A. Trust, tool formulas, privacy and transparency

Use `TRUST-AND-STRUCTURED-DATA-GATE.md` based on actual page type and risk; do not chase third-party GEO scores.

- Applicable page types and trust requirements (tools / landing / editorial / financial or legal):
- Real site brand and operator (Person / Organization if actually applicable):
- Appropriate schema and verified profiles; N/A reasons for irrelevant types:
- Calculator inputs, units, rounding, formula, expected sample and edge cases (or N/A):
- Changing factual rules, official sources and jurisdiction/effective date (or N/A):
- Actual browser/server/storage/file/ads/analytics requests and privacy disclosure plan:
- About/Contact/Privacy/Terms/disclaimer applicability and owner:
- Real authorship and significant modification-date strategy for editorial pages (or N/A):
- Third-party GEO findings, if any, to classify; never score target:

## 9. Structured-data plan

| Route/template | Schema type | Visible content represented | Google feature eligibility checked? | Validation method |
|---|---|---|---|---|
| | | | | |

Do not add schema as a generic GEO hack.

## 10. International SEO plan

If not multilingual/multi-region, mark N/A.

- URL strategy:
- Language/region codes:
- x-default policy:
- Canonical/hreflang rules:
- Keyword validation per market:
- Localization requirements beyond translation:

## 11. Programmatic SEO plan

If not programmatic, mark N/A.

- Data source:
- Unique page-level value:
- Template variables that change substance:
- Slug/collision rule:
- Batch size:
- Sample audit rule:
- Stop/rollback condition:
- Sitemap inclusion gate:

## 12. Media / multimodal plan

- Original screenshots/charts/images:
- Caption/context rules:
- Image alt/fallback rules:
- OG/social image plan:
- Search Console multimodal review needed after launch?:

## 13. Search / AI crawler policy

Keep Search visibility separate from training/product permissions.

- Googlebot Search policy:
- Bing/Search crawler policy:
- Google-Extended policy and business reason:
- Other AI crawler policy and business reason:
- robots.txt owner:

## 14. Release verification plan

- L1 commands/checks:
- Raw-HTML checks:
- Crawl/link checks:
- Schema validation:
- Mobile/visual checks:
- Performance checks:
- Production verification:
- Search Console follow-up:
- Baseline location:

## 15. Owner sign-off

- Approved keyword set:
- Approved intent map:
- Approved indexation policy:
- Approved international/programmatic plan:
- Approved crawler/training policy:
- Date:
