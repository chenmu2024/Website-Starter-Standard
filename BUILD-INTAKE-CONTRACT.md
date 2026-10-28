# Build Intake Contract — gefei-seo → Website-Starter-Standard

**Purpose:** convert approved *what/why/keywords* research into protected engineering inputs. This is the **only required bridge**; research and engineering must not become competing sources of truth.

## Ownership

| geFei Research repo (decides) | Website Starter (implements and tests) |
|---|---|
| Target user and market/language | Product architecture and user flows |
| Real non-brand query and keyword/intent evidence | Concrete routes, SSG/SSR, metadata, canonical, sitemap, hreflang |
| Page-level SERP opportunity and differentiation | UI/UX, design tokens, responsive behavior, accessibility |
| Monetization hypothesis, approved fixed cost cap | Core tool correctness, mobile performance, animations, error states |
| GO/TEST/HOLD/REJECT and owner-approved scope | Unit/e2e/visual checks, technical SEO audits, deployment and monitoring |

Research source: https://github.com/chenmu2024/gefei-seo/blob/main/contracts/RESEARCH-TO-BUILD.md

## Intake fields

- **Source**: research repo path / immutable commit SHA (or owner-supplied signed research document).
- **Decision**: GO / TEST / HOLD / REJECT; scope of authorization and approver/date.
- **Target market**: country, local language, key user job, monetization mode.
- **Approved keywords**: exact strings and one intent→canonical destination; known/unknown Volume/KD/CPC with source/checked date.
- **Why it can compete**: grounded SERP URLs, differentiation and disconfirming facts; engineering does not redo these estimates.
- **Must-have feature output**: precise user inputs/outputs, validated constraints, distinctive functionality.
- **Cost and policy boundaries**: domain-only default recurring cost, no unapproved paid AI/API/server/database; copyright, privacy and local regulations.
- **Protected existing assets**: URLs, titles, canonical behavior, rankings baseline, functional logic and current branding.
- **Evidence/launch goals**: measurable post-launch Google queries, user task success, conversion/revenue; unknowns explicitly `UNVERIFIED`.

## Acceptance and escalation

1. **GO + approved** → engineering may implement exactly the agreed scope.
2. **TEST + approved** → implement only the named smallest test. A TEST is not permission to build the full production site.
3. **HOLD / REJECT / unapproved** → do not begin speculative full-site construction; ask for decision or return missing evidence to geFei research.
4. **Existing approved site maintenance / bug, indexation, or UI fixes** → no fresh commercial research required; inspect code and protected assets, fix within existing authorized scope.
5. **Direct user override** → if owner explicitly requests work despite missing research, record it as an approved exception and state unknown SEO outcomes. No hidden guessing.
6. **Technical infeasibility or changing keyword/URL/market** → report exact conflict and request owner decision instead of silently substituting requirements.

## Release implementation

After approval, fill `SEO-GEO-PROJECT-BRIEF.md` with copied keyword/source/intents. Derive UI from `DESIGN.md` and `TASTE-UI-PROTOCOL.md`. Implement/verify technical SEO with `SEO-GEO-QUALITY-GATE.md` and `TECHNICAL-SEO-IMPLEMENTATION.md`; capture real execution status in `SEO-GEO-RELEASE-EVIDENCE.md` and `UI-RELEASE-EVIDENCE.md`; release only when `QA-CHECKLIST.md` passes applicable critical gates.

**No rankings are guaranteed.** Passing an engineering gate proves a check ran, not search engine inclusion or traffic.
