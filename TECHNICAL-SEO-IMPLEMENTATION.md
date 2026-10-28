# Technical SEO implementation playbook

This is **Website-Starter-Standard engineering**, not an opportunity or keyword research procedure. Use the approved source described in `BUILD-INTAKE-CONTRACT.md` and the detailed `SEO-GEO-QUALITY-GATE.md`.

## Implementation defaults

- Prefer static pages / SSG or SSR for public SEO-critical text and crawlable `<a href>` links. Do not make the only keyword-relevant content depend on client JS hydration or gated interaction.
- React/Next.js: route metadata, canonical, robots, sitemaps and structured data must be rendered consistently; audit actual generated HTML instead of trusting configuration.
- Astro/static HTML: render unique per-route title/H1, important content and links in built HTML; JS islands may power the actual tool, not hide the page.
- JS-only browser tools may operate entirely locally; no paid backend, AI API, database or recurring service is needed by default. Do not silently add a dependency.
- Implement real 404 and redirect behavior at the target host; path case, trailing slash, canonical and sitemap should agree.
- One approved intent→one canonical page; avoid generated keyword-swapped routes and accidental orphan pages. Hreflang requires correct language/country equivalents and reciprocity.
- Schema/JSON-LD describes visible truthful content only; Google does not require special AI-only schema. `llms.txt` is optional and never a reason to degrade normal SEO.
- Use naturally effective native CSS/SVG/JS animation when it helps the user task and metrics permit; provide `prefers-reduced-motion`, no-JS/static fallback, no hidden critical copy, and do not run expensive offscreen loops.

## Engineering acceptance by area

| Area | Concrete evidence/check |
|---|---|
| Routing | Production important routes return 200; 404 routes return real 404; redirect chains and protected URL migration checked |
| HTML SEO | Generated raw HTML has unique title, H1, meta description, canonical, intended main content and crawlable links |
| Discoverability | Relevant important URLs accessible through hubs/navigation, in valid XML sitemap, not accidentally noindexed/robots-blocked |
| Page value | One complete user task works with real/invalid/edge-case inputs; each independent page adds distinct value |
| International | `pt-BR`, `es-MX` etc match real localized text; hreflang self + reciprocal return + canonical parity |
| Performance | Run Lighthouse/PSI or real lab tests when tools available; record LCP/INP/CLS results as measured/unmeasured, never fabricate PASS |
| UX/accessibility | Verify 360/390/768/1024/1440 approximate viewports when possible, keyboard/focus, touch, contrast, overflow and reduction of motion |
| Assets | Images load, reserved intrinsic dimensions, sensible lazy loading, readable alt text and performant fonts |
| Evidence | Record commands, test outputs, URLs, dates and NOT RUN/FAIL states; never call a successful build an SEO success |

## Offline audit (optional L1 helper)

```bash
python scripts/seo_static_audit.py --site-dir dist --base-url https://example.com --output seo-audit.json
python -m unittest discover -s tests -p "test_*.py"
```

The checker has no network, paid API or third-party dependencies. It analyzes only built HTML and simple internal links; it cannot verify JavaScript-rendered pages, live HTTP status, canonical targets on the network, actual Google indexing, ranking or Core Web Vitals. False positives require manual review.

## Mandatory workflow

1. **Intake**: establish source of approved keywords/intent and existing site baseline.
2. **Plan**: architecture, page list, design system and test plan; if adding pages, avoid keyword cannibalization.
3. **Implement**: use reusable components and project-level design tokens; preserve existing features and search-sensitive metadata.
4. **L1**: build/lint/unit checks plus route/internal link/title/canonical/sitemap/schema checks; capture actual command and result.
5. **L2**: UI quality gate, mobile, functional edge cases, technical crawl and production-domain checks before release.
6. **L3**: after real data exists, review GSC query/page changes, indexation, CWV and traffic anomalies; send newly discovered market/keyword opportunities back to gefei-seo, not self-authorize an expansion.

Stop a release on actual P0/P1 blockers. No tool/CI access means mark check `NOT RUN`, not `PASS`.
