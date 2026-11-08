# Adopt P0 quality gates in a downstream website

This repository is a shared standard, not a magic global GitHub Actions runner. Changes here do not automatically rewrite or enable CI in WoodLayout, Quilt Calculator, Math Works, CSV-QBO or other sites. Each site must adopt the templates and provide real project-specific commands.

## A. One-time project integration

1. Preserve project-specific scope, locked keyword/intent/route map and current working calculation behavior.
2. Copy these files into the downstream repository:
   - tools/seo_audit.py
   - tools/validate_calculation_cases.py for any numerical calculator/converter/worksheet generator
   - tools/verify_deployment.py
   - templates/github-actions/website-quality.yml -> .github/workflows/website-quality.yml
   - templates/github-actions/website-post-deploy.yml -> .github/workflows/website-post-deploy.yml
   - templates/indexation-policy.preview.json -> tests/indexation-policy.preview.json
   - templates/indexation-policy.production.json -> tests/indexation-policy.production.json
3. Configure SITE_DIR, BASE_URL, PRODUCT_KIND, BUILD_COMMAND, CORE_TEST_COMMAND and BROWSER_TEST_COMMAND in the downstream CI. A calculator additionally configures CALC_RUNTIME_COMMAND and publishes tests/golden-cases.json based on actual independent calculations.
4. Fill required_routes and indexable_routes for that website, not the sample homepage only. The production list is explicit; a valid Sitemap is not permission to index every random built HTML route.
5. For Cloudflare Pages branch previews, preview_noindex_via=header is permitted in the offline preview policy only if the post-deployment X-Robots-Tag noindex is actually verified. Otherwise choose preview_noindex_via=meta and generate raw preview meta directives for all HTML.
6. Use branch protection or required status checks for the quality job once it is proven stable. The shared standard cannot configure repository branch protection automatically.

## B. Avoid CI that only checks a template

- BUILD_COMMAND must perform an actual production or preview build and leave SITE_DIR with index.html.
- CORE_TEST_COMMAND must execute real application tests.
- BROWSER_TEST_COMMAND must run a real browser suite against the generated build or suitable preview server. Provide browser dependencies in the command or separate steps. A screenshot file without an executed test is NOT a browser pass.
- In calculator mode, CALC_RUNTIME_COMMAND must call the actual runtime engine, write release-evidence/calculation-observed.json and not reuse the expected-output code. The quality gate fails without the file.
- A non-calculator site uses PRODUCT_KIND=static, but still needs meaningful functional and browser tests.
- The sample tests in Website-Starter-Standard validate only the validator scripts themselves; they do not certify downstream websites.

## C. Build identity parity on Cloudflare

The live probe requires a deployed /build-info.json with a JSON object of the form:

    {"commit":"FULL_GIT_COMMIT_SHA"}

Generate this at build time from the actual deployed source commit. For Cloudflare Pages CI, CF_PAGES_COMMIT_SHA can supply it; for GitHub Actions, GITHUB_SHA is available (be careful: pull_request workflow SHA may be a synthetic merge commit rather than branch HEAD). Never publish a sample or manually typed made-up SHA.

For a Python-based build script:

    import json, os
    from pathlib import Path
    sha = os.getenv("CF_PAGES_COMMIT_SHA") or os.getenv("GITHUB_SHA")
    if not sha:
        raise RuntimeError("Deployment commit SHA unavailable")
    Path("dist/build-info.json").write_text(json.dumps({"commit": sha}), encoding="utf8")

Run the same site build on Cloudflare, not a different unpublished CI artifact. Check the intended merge SHA against the actual production build identity before marking the production site verified.

## D. Production follow-up

After Cloudflare confirms the authorized deployment:
- Manually launch the copied website-post-deploy.yml workflow with real production URL, intended SHA, preview URL (when applicable) and one critical route.
- Download its JSON HTTP evidence and separately verify actual browser functionality, UX/accessibility, Cloudflare AI/WAF account settings and any needed real physical printing or material tests.
- Complete GSC and Bing property/sitemap verification as independent post-launch tasks.
- Record explicit NOT RUN or NOT APPLICABLE for unavailable evidence; do not label crawler User-Agent spoofing as a real verified bot visit.

## E. Local checks on this standard itself

    python -m unittest discover -s tests -v

To review the canonical offline scanner without a policy:

    python tools/seo_audit.py --site-dir dist --base-url https://example.com --output report.json --fail-on error

For a site-specific preview/production policy, add --policy-json tests/indexation-policy.production.json (or the preview policy). The old scripts/seo_static_audit.py remains a compatibility adapter, not a separate implementation.

The new release probe makes real HTTP requests only when actually invoked in an environment with network access. It does not log into Cloudflare, buy domains, deploy sites, change WAF policies or use paid APIs.
