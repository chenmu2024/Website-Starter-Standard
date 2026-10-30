# GEO trust, content accuracy and structured-data gate

> This is an engineering/release standard. It interprets third-party GEO score reports as potential issues to investigate, NOT as Google ranking criteria. Score 86/100, grade B and a target 90/100 are vendor-defined metrics; they cannot establish Google inclusion, traffic or revenue. Research/keyword selection remains in gefei-seo.

## 1. Decision principle: only enforce applicable checks

Judge each finding by page type, actual product behavior, factual importance, user risk, region and verifiable evidence. Label PASS, FAIL, NOT RUN or N/A (with explanation).

| Severity | Applicable examples | Release action |
|---|---|---|
| P0: block | False credentials, fabricated operator, materially false user-data assurances, exposed sensitive user data, broken core tool | Stop relevant release |
| P1: block where applicable | Incorrect payroll/tax or financial calculation, misleading legal rates, materially inaccurate privacy disclosure, fake structured-data claims | Fix before release |
| P2: improvement | Relevant real entity data missing, unclear formula assumptions, missing useful official source, hard-to-find trustworthy support information | Fix or document owner-accepted follow-up |
| P3: optional / N/A | llms.txt, arbitrary article author/date on calculator, invented sameAs, forcing a GEO score from B to A | Do not block release |

A high third-party score never overrides broken functionality, actual Google crawlability, privacy compliance, accessibility or site performance. Do not treat warnings as proof of a Google penalty.

## 2. Match schema to the REAL page type

- Homepage/brand: WebSite can describe the actual site. Organization is appropriate only if there is an actual truthful organization; a real solo operator may be represented by Person where appropriate. Never invent a legal entity, biography, qualifications, registration, address or staff.
- Interactive calculator/tool: where useful, WebApplication or SoftwareApplication can describe visible, functional capabilities. They are NOT a promise of Google rich results. Do not automatically add Article or BlogPosting to a calculator homepage.
- Editorial articles: byline/author, Article/BlogPosting and publication/modified dates may be relevant if these reflect real people, genuine editorial provenance and meaningful content changes.
- sameAs: include only verifiable, genuine relevant official profiles. No fabricated LinkedIn, social, GitHub or Wikipedia association.
- Logo, title, canonical URL, site name and operator should agree across visible pages, About/Contact and structured data; use stable absolute @id where entities are actually related.
- Keep structured data parsable and semantically truthful; separate JSON syntax validation, Schema.org semantic review and current Google rich-result eligibility testing. Not all Schema.org types trigger Google Search features.
- Do not force Schema markup on every URL. Organization identity is often best described on homepage or a relevant About page.

## 3. Make core tool outputs independently verifiable

For calculators, converters, generators or file tools, review applicable fields:

- Define inputs, units, currency, locale, assumptions, defaults, algorithm/formula, rounding/precision and limitations. Give a real example that a person can recalculate.
- Test representative normal cases, zero/negative/boundary inputs, invalid/empty inputs, localized number formatting, mobile results and error messages.
- For payroll/tax/labor/regulatory tools, verify country and effective dates, changing official rates/rules and source URLs. Distinguish generic user-defined calculations from legal entitlements. A disclaimer cannot compensate for an incorrect calculation.
- Plain arithmetic (for example percentage salary raise) does not need a fake external citation. Cite consequential outside facts, not arbitrary quoted text for score points.
- Do not add batch import, export, AI APIs or servers solely because a third-party scanner suggests more 'original' features; approved user tasks and business constraints take precedence.

## 4. Verify real trust, privacy and service information

- About: truthful brand/operator or maintained-by information where helpful; no fabricated identity or anonymous site pretending to be a regulated expert.
- Contact: a usable real channel where appropriate. Test reachability instead of inventing addresses.
- Privacy: review actual browser processing, submissions, network requests, analytics, advertising, cookies, third-party scripts, localStorage, uploaded files, server logs and data retention. Compare *actual implementation* with visible disclosures. Never claim '100% local/private' without checking code and network behavior.
- Terms: provide accurate terms, limitations and disclosures where required by local law, user submissions, payment/subscriptions or actual product risk. Merely lacking Terms is not automatically a Google SEO defect or universal legal requirement.
- Authorship: a real tutorial can benefit from clear authorship; a simple calculator doesn't automatically require an Author box. Do not fabricate authors or certifications.
- Freshness: dates should describe actual publication or significant updates. Never automatically bump the date daily just to get a scanner green mark.
- Sources: use authoritative, date-relevant links for factual rules and market claims. Do not invent references, awards, reviews, statistics or official affiliations.
- Where legal requirements are uncertain, mark for jurisdiction-specific human review rather than invent compliance guarantees.

## 5. Third-party GEO score triage

When an AI-search or GEO scanner reports issues:
1. Save scanner name, date, URL, visible issue and the tool's own scoring rubric if available.
2. Verify each issue against live visible page, raw HTML, actual JSON-LD, code, network behavior and applicable page type.
3. Record observation, source, severity, affected URL, appropriate minimal fix and exact validation method.
4. Explicitly mark inapplicable advice N/A. This includes llms.txt for Google, forced sameAs, author on a non-editorial tool and quotes without a genuine source.
5. Preserve approved keywords, existing high-traffic URLs, canonical logic, indexation and functional inputs. Do not introduce new paid dependencies.
6. Re-test real functionality, metadata, schema accuracy and privacy disclosures. Report NOT RUN for tests not performed.

Google Search generative-AI features do not require dedicated AI files such as llms.txt, special markup, citation-count targets or separate AI pages. E-E-A-T is a useful trust framework, not one standalone Google ranking score. Google may not show rich results even with valid markup.

## 6. Page-type review table

| Page type | Review priority | Usually N/A |
|---|---|---|
| Calculator / tool | formula, units, correctness, input privacy, WebApplication if appropriate, real site identity | Article authorship, quotes-per-page, daily modified dates |
| Help article | accurate sources, author when expected, real dates, article schema where appropriate | interactive-tool formula tests |
| Financial / labor / tax tool | official and dated rules, clear jurisdiction, tested computation, limitations, privacy | fabricated 'certified' or unsupported expertise |
| General landing page | user intent, truthful organization and product description, contact/policy links as applicable | irrelevant FAQ schema and forced citations |

## 7. Required evidence for release

Use the page-specific evidence table in SEO-GEO-RELEASE-EVIDENCE.md. For each applicable check report PASS/FAIL/NOT RUN/N/A plus:
- Actual route and affected component or JSON-LD node.
- Test command / screenshot / inspection details and date.
- Real input and expected output for formula tests.
- Relevant official source or stated unverified assumption.
- Actual privacy/network/storage inspection results.
- Severity, fix, regression check and any accepted exception.

An offline HTML scanner can help with syntax and missing links, but it cannot prove financial correctness, legal compliance, data-flow truthfulness, Google indexation or GEO ranking.

## Primary references

- Google generative AI search guidance: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Organization structured data: https://developers.google.com/search/docs/appearance/structured-data/organization
- Helpful people-first content, authorship and E-E-A-T: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Real publish/modified dates: https://developers.google.com/search/docs/appearance/publication-dates
- General structured-data guidelines: https://developers.google.com/search/docs/appearance/structured-data/sd-policies

These are sources for Google-related statements, not a guarantee of jurisdictional privacy or legal requirements.
