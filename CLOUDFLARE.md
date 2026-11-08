# Cloudflare Pages / Workers deployment & production acceptance standard

This is a per-project release **execution** gate, not SEO opportunity research. It applies to Cloudflare Pages or Workers when used; adapt framework-specific details in the project. Deployment evidence is separate from source tests, Google/Bing indexing and real AI citations.

## 1. Record project configuration

- Repository and immutable source commit:
- Production branch and deployment ID:
- Production custom domain and preferred scheme/host:
- Preview branch/URL (if available):
- Framework and exact build command:
- Artifact output directory and runtime version:
- Public build identity file and SHA:
- Redirects, 404, asset headers, CSP and cache rules:
- Required environmental variables; **never paste secrets into evidence**:
- Rollback method and known-good deployment:
- Operator approval for domain purchase and production deployment:

Do not claim production deploy is authorized merely because code has been merged. Avoid new paid infrastructure without explicit owner approval.

## 2. Independent deployment states

1. CODE READY — changed commit, diff and intended behavior reviewed.
2. CI PASS — build, tests, SEO policy, calculation contract (if applicable), UI/browser/exports as scoped.
3. PREVIEW DEPLOYED — preview URL resolves; required pages available; preview indexing prevention verified.
4. PRODUCTION DEPLOYED — custom-domain deployment matches the intended immutable commit.
5. LIVE HTTP VERIFIED — real URLs, asset loading, canonical/robots/sitemap/404, mobile task and console checks.
6. ACCOUNT/SEARCH VERIFIED — Cloudflare zone AI/WAF settings from actual dashboard/API evidence; GSC/Bing property, sitemap acceptance, indexing and AI citations are separate follow-up evidence.

Do not collapse these into one binary "website finished" claim. See RELEASE-STATE-CONTRACT.md.

## 3. Preview vs production indexation

- Production HTML must contain the correct canonical and desired robots metadata; production indexable pages must not accidentally have noindex or sitewide Disallow.
- Cloudflare Pages preview deployments normally include an X-Robots-Tag: noindex response header by default (official Pages preview documentation). Inspect actual HTTP headers: do not infer correct behavior from a checked box.
- For a nonstandard custom preview domain/Worker, explicitly configure equivalent noindex headers and verify that no runtime rule strips them.
- Preview may have canonical to production or omit it by policy, but must not create competing indexable duplicates. Use domain-specific rules rather than copy production indexing blindly.
- A production pages.dev alias can also serve public indexable content if not handled separately. Decide its behavior and verify redirects or noindex without accidentally blocking the production custom domain.
- Ensure non-HTML static assets/URLs relevant to preview are handled as needed. Validate canonical, sitemap, redirects and status on the actual host, not just the built files.

Official: https://developers.cloudflare.com/pages/configuration/preview-deployments/

## 4. Cloudflare AI Crawler / WAF account review

Use the zone's Security > Settings > Bot traffic > AI Crawler and Agent access policies, if available. Record:
- Search, Agents, Training and each Personal Agent action as actually saved;
- Bot Preference Sync current setting and whether Cloudflare is prepending robots.txt directives;
- Any zone-wide bot blocking, WAF challenge, managed rule or Access rule affecting public tool pages;
- Screenshot or authorized API evidence with date, zone and reviewer; redact tokens/account secrets.

Search discoverability and AI training permissions are independent decisions. No universal requirement to permit training; the business owner selects policy. If Search and Agents are intended to be allowed, confirm settings and real request behavior.

A request that merely sets a named crawler User-Agent is NOT verification that a provider's authenticated crawler has access. Mark real verified-crawler access NOT RUN unless appropriate logs/security analytics support it.

Official: https://developers.cloudflare.com/bots/additional-configurations/block-ai-bots/

## 5. Read-only production HTTP check

Publish a small generated file at /build-info.json **from the actual CI/deploy SHA**:

    {"commit":"<full Git commit SHA>"}

Generate it from the CI environment; never hardcode a successful or arbitrary SHA. Avoid exposing internal secrets in that file. The deployment must render it from the same artifact as the app.

From a trusted CI/terminal after the intended deployment:

    python tools/verify_deployment.py --url https://example.com --route /important-tool/ --expected-sha <full-git-commit> --preview-url https://pr-preview.pages.dev --output evidence/http-release.json

The checker is HTTP read-only and deliberately limits response bytes. It verifies production homepage 200, raw HTML title/canonical/noindex, robots.txt and sitemap XML, named important URLs, true HTTP 404, preview noindex and deployed SHA parity. It fails if any mandatory check fails or deployed commit was not independently supplied. If no preview exists, mark that part NOT_APPLICABLE with reason.

IMPORTANT limits: no Cloudflare account login, no real bot identification, no GSC indexing, no CWV field data, no end-to-end JS execution, no proof of printed physical scale. In production, run a browser UI smoke check as a separate job.

No target host/network available => NOT RUN, not PASS. A CDN cache can still present stale HTML; confirm the production SHA and appropriate cache policy before announcing a live change.

## 6. Runtime browser and rollback gate

- Verify at least one genuinely executed end-to-end user task on the production host; for a calculator compare representative expected result, error case and visible/export output.
- Verify actual responsive pages in Chromium, Firefox and WebKit where automated tooling is available. Record exact viewport and environment; WebKit on Linux is not an iPhone screen-reader test.
- Confirm no horizontal document overflow at narrow mobile sizes due to inherited min-width, data table, visual media or hidden elements.
- Check 404/redirect/HTTPS, cache invalidation, Content Security Policy errors and third-party scripts affecting privacy disclosures.
- Define rollback trigger: wrong formula, noindex on production, wrong canonical host, broken core tool, inaccessible assets, unexpected CDN deployment or severe accessibility regression.
- Re-run production parity/HTTP checks after rollback; a past success result is not evidence of the current deployed commit.

## 7. Post-launch signals (NOT a technical release blocker)

Complete Google Search Console and Bing Webmaster Tools property verification, then submit the canonical sitemap. Track actual indexing, queries, click/exposure trends, CWV field data when available, referral sources and URL-specific AI citations with model/date/query/source. Do not manufacture a traffic score from a successful HTTP request.

## Release evidence checklist

| Gate | Status | Evidence link / commit / observation |
|---|---|---|
| Build and tests | NOT RUN | |
| Preview noindex header / HTML | NOT RUN | |
| Production deployment ID and intended commit | NOT RUN | |
| Production HTTP / canonical / robots / sitemap / 404 | NOT RUN | |
| Production browser main user task | NOT RUN | |
| Cloudflare AI policy and WAF account review | NOT RUN | |
| GSC/Bing site property / actual indexing | NOT RUN | |
| AI citation and referral evidence | NOT RUN | |

Use PASS, FAIL, NOT RUN and NOT APPLICABLE with reasons; never mark partial checks as fully completed.
