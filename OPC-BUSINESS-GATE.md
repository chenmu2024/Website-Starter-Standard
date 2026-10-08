# Opportunity, business, and operating evidence gate

A project-specific commercial decision process for solo-built websites, inspired by [easychen/opc-methodology](https://github.com/easychen/opc-methodology).
This is an **original checklist**, not the third-party Skill text or a commercial redistribution of it.

## Applies to

- **New opportunity / new website**: evaluate before allocating material build time.
- **Existing website**: record existing approved keywords as frozen. Review real results before deciding to expand, pause or retire. Never turn a profitability review into an unrequested keyword/route rewrite.
- **Small SEO/UI/bug fix**: do not block necessary repairs with a new full feasibility study.
- **Previously approved full-scope build**: preserve the owner's agreed complete site scope; validation determines whether to start, not whether to silently defer required pages to "V2".

## Stage A — market and niche (evidence, not intuition)

Document:
1. **Exactly approved keywords**, country/language, intended query and canonical page. Do not alter keyword spellings, case or language without approval.
2. Keyword provider, collection date, **absolute monthly volume**, KD, CPC with country and dataset. Unknown is `UNVERIFIED`, never zero. Trends 0–100 is relative interest, **not** volume.
3. SERP top-10 inspection: search intent alignment, brand dominance, true competing page types, estimated weaknesses and overlapping intents.
4. A comparable reference site estimated at roughly 10k–100k visits/month **with verified provider/date**; alternatively, a newly popular game with evidence within the last seven days. Neither substitutes for the nonzero volume check.
5. Owner's durable strengths: reusable code/design, distribution, language-market knowledge, original datasets, and zero-cost delivery feasibility.
6. Real customer pain and distribution path; "high CPC" alone does not prove willingness to pay.

**Default decision policy (owner heuristics, not Google rules):**
- If absolute search volume is unverified or zero, mark **HOLD / REJECT**, not a build-ready lead.
- KD > 40, unattractive SERP, thin SERP differences or source inconsistency → **HOLD** pending owner review, not a falsely guaranteed win.
- Verify all country-specific markets separately; avoid summing near-duplicate queries or unsupported volumes.
- Prefer non-paid APIs, free static/edge hosting and direct browser computation. Recurring charges require explicit approval.

## Stage B — six-dimensional business evidence

Use the following **internal**, non-predictive rubric. For each score **0–5**, attach an observed source/date and one-sentence rationale; if absent score `UNVERIFIED` and do not total a partially evidenced score.

| Dimension | What to examine |
|---|---|
| Customer pain | Cost, frequency, urgency of the problem; direct signals or verified customer reports |
| Leverage | Code, content and AI reuse without linear human service |
| Timing | A real new distribution, product, policy, or competitive opening |
| Resource fit | Existing expertise, domains, reusable tools and verified channel access |
| Standardizable delivery | Can value be delivered safely and consistently to more users? |
| Cashflow | Realistic income mechanism and speed to first verified revenue |

An illustrative **review** threshold is 22/30, with customer pain and cashflow each >=3. This is an internal priority sorting aid, not a probability, revenue forecast or automatic "GO". Unknown scores are never set to average.

## Stage C — business model and falsifiable MVP experiment

- User segment and concrete job/problem to solve
- Distinct value and alternative solutions
- Acquisition method: SEO / community / distribution / owned channel
- Monetization: ads, affiliate, subscriptions, downloads or B2B contracts; identify when billing is actually available
- Cost structure, provider dependencies, privacy/safety/regulatory risk
- Single **riskiest assumption** and cheapest way to test it
- Time-boxed success criterion and explicit human **GO / TEST / HOLD / STOP** decision

For pure SEO/ad tools, launch success is **not** just passing a build. Observe whether Google indexes useful routes, users operate the main tool, and revenue becomes measurable. For SaaS, ad impressions or keyword CPC are not substitutes for qualified leads or paid conversion.

## Stage D — conversion path and post-launch dashboard

Map the entire flow:

```text
intentful query / share → landing → successful user task → next meaningful action → measured revenue / retained user
```

Measure only with real sources:
- GSC query/page/country: impressions, clicks, CTR, average position, indexation
- Technical: availability, Core Web Vitals and important route/tool errors
- Product: action completion, engagement (when privacy-safe data exists)
- Economics: verified page/ad/affiliate/subscription revenue, explicit cash cost and operator time
- Distribution and backlinks: real referring sources and quality, not raw comment counts

**Recurring operating decisions (heuristics, not automatic punishment):**
- **KEEP / EXPAND**: evidence of acquisition and value, achievable operations and improving revenue
- **FIX**: known indexation, SERP intent mismatch, tool failure, monetization blockage or poor UX
- **TEST**: meaningful impressions or qualified leads but still too little outcome data
- **HOLD**: costs exceed the agreed cap, data is missing, or low potential relative to alternatives
- **STOP**: after documented recovery experiments, no evidence of viable demand/conversion and meaningful opportunity cost

Never recommend deletion of a live site or changing approved keywords from this rubric without the owner's explicit decision. Indexing is often delayed; age alone is not a stop-loss rule.

## Approval contract

Complete the project-specific **`OPC-BUSINESS-EVIDENCE.md`** when evaluating a new opportunity or a major business pivot. Reference it in PRs/briefs. SEO, GEO, design, and UI rules in the other standard files remain independently mandatory. A commercial "GO" never waives the functional, legal, accessibility or release quality gates.

## Guardrails

- Separate `Observed`, `Inferred`, and `Not yet verified` claims.
- Cite the actual source and check date; do not invent Semrush/Ahrefs data or claim paid access.
- Distinguish keyword demand, user pain, business model and realized revenue.
- When using another author's ideas, preserve attribution and licensing boundaries.
- Integrating this checklist adds no paid API, no background process and no dependency on an external commercial Skill.
