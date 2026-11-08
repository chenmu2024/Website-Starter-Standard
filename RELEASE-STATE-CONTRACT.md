# Release State Contract — prevent false completion claims

Required for new sites, major SEO changes, data-sensitive tools and any deployment where preview and production can differ.

A successful Git commit, PR merge, Cloudflare preview deployment or HTTP 200 does **not** establish that the next state has passed. Every statement of "complete" must name its scope and evidence.

| State | Allowed claim | Required proof | Never infer |
|---|---|---|---|
| IMPLEMENTED | Code written to a named branch/commit | Diff, actual checked source | Tests passed |
| CI_VERIFIED | Appropriate automated checks passed on that commit | Workflow URL, test totals and exclusions | Production site updated |
| PREVIEW_VERIFIED | Correct preview artifact deployed; preview noindex | Deployment URL/ID, HTTP headers, browser check | Production indexed |
| PRODUCTION_VERIFIED | Production custom-domain artifact matches intended SHA and works | Deploy ID, build-info SHA, live HTTP + task tests | Google/Bing indexed |
| SEARCH_VERIFIED | Property, sitemap and search reports actually checked | GSC/Bing evidence, date range, query/page | AI citations / revenue |
| AI_REFERRAL_VERIFIED | Particular query/model/time linked a real page, or referral measured | Query, cited URL, date, identifiable source | Repeatable rankings or future traffic |
| PHYSICAL_VERIFIED | Printed/real-world measurement accepted by an actual reviewer | Measured paper/stock/fixture, equipment, tolerance, date | Browser emulation is a physical test |

For independent layers (SEARCH, AI, PHYSICAL) report state per dimension. A site can be PRODUCTION_VERIFIED while indexing is still NOT RUN; never say all layers completed.

## Evidence fields for every gate

- project/repository, environment (local/preview/production/real workshop);
- immutable commit SHA and relevant deployment ID if any;
- target URL / route list / expected behaviors;
- command and executed runtime (browser/OS/viewport or hardware);
- observed result: PASS / FAIL / NOT RUN / NOT_APPLICABLE;
- execution time and evidence artifact URL/file;
- unresolved P0/P1 findings, owner, rollback or remediation;
- do not mark PASS when only a plan/script/template exists.

Do not rewrite NOT RUN as PASS just because the check "could have run", was previously successful, or an AI agent says it completed.

## CI and production workflow

1. Lock research-approved scope and baseline: route, SEO metadata, core calculations, UI, analytics, cost.
2. Implement small changes on branch and run L1 deterministic checks.
3. Run appropriate L2 full build/calculation/browser/performance/SEO tests.
4. Publish preview if enabled and verify preview noindex and functional state.
5. Review diff/PR, inspect current GitHub Actions on exact head SHA.
6. Merge only after relevant P0/P1 tests pass; deploy to Cloudflare per owner-authorized project policy.
7. Verify real production SHA and HTTP/task behavior, capture evidence.
8. Only then start Search Console/Bing/AI citation monitoring as distinct ongoing operations.

If a test unexpectedly fails after a previous pass, identify and repair root cause, including stale test assertions and inherited CSS rules. Do not remove tests or relax release gates solely to reach green CI. If a gate is impossible due to tool/account/hardware limitations, document NOT RUN and do not claim it passed.

See CALCULATION-QUALITY-GATE.md, CLOUDFLARE.md, QA-CHECKLIST.md, SEO-GEO-RELEASE-EVIDENCE.md and UI-RELEASE-EVIDENCE.md.
