# International SEO automated checks

The offline SEO auditor validates only the HTML and sitemap files in a built artifact. It does not crawl remote domains, inspect HTTP Link headers, run JavaScript, or prove Search Console indexing.

## What is now checked

When alternate language links exist in built HTML:

- hreflang code syntax (language, optional script, region and variant subtags; plus x-default);
- duplicate hreflang codes on one page;
- absolute URL form;
- whether same-origin target routes exist in the build;
- whether the target page uses the expected self-canonical;
- whether each page declares a self-reference;
- whether same-origin language variants return-link to the source language;
- whether html[lang] language prefix agrees with the page's self hreflang code.

External alternate URLs are reported as EXTERNAL_UNVERIFIED because the offline build cannot inspect another domain. This is not automatically an error: multi-domain international sites may be valid, but their other properties need a separate crawl or live check.

## Explicit language-group contract

The auditor cannot infer which pages are intended to be translations of one another. For a known international family, add an explicit group to the site's production policy:

    {
      "mode": "production",
      "required_routes": ["/", "/es/", "/pt-br/"],
      "indexable_routes": ["/", "/es/", "/pt-br/"],
      "hreflang_groups": [
        {
          "routes": {
            "en": "/",
            "es-ES": "/es/",
            "pt-BR": "/pt-br/",
            "x-default": "/"
          }
        }
      ]
    }

The routes object maps each hreflang language code to its same-site URL path. Every listed variant must exist, and every variant must contain every mapping in that group, including its own self-reference. x-default may point to the same fallback URL as a language-specific variant.

Run the normal static audit with:

    python tools/seo_audit.py --site-dir dist --base-url https://example.com --policy-json tests/indexation-policy.production.json --output release-evidence/seo.json --fail-on error

A missing or wrong group entry is an ERROR under the explicit policy. Do not add a group just to silence warnings; only group genuine alternate versions that serve the same content/intent in different languages or regions.

## Limitations and human review

- Locale URLs and canonical destinations must match the approved route map. A correct hreflang tag cannot compensate for a wrong page, thin machine-translated copy or mismatched search intent.
- The static tool checks return links only among pages present in the same built site. For cross-domain language families, verify all domains and reciprocal links with a live crawl.
- It does not validate translation quality, localized keyword research, currency/legal localization, market-specific content, Content-Language headers, redirects, or actual indexation.
- It does not crawl every alternate href remotely and does not check hreflang declared only in HTTP headers.
- If the site is genuinely single-language or does not have equivalent alternate pages, omit hreflang_groups; do not manufacture language links.
- Review localized title/description/H1, language-region choice, canonical, sitemap, x-default and reciprocal links as one coherent route family.
