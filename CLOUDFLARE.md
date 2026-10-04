# Cloudflare Deployment Standard

Use this file when the project is deployed on Cloudflare Pages or Workers.

## Record per project

- Production domain:
- GitHub repository:
- Production branch:
- Framework preset:
- Build command:
- Output directory:
- Node/runtime version if relevant:
- Required environment variables:
- Custom redirects/headers:

## Deployment rules

- GitHub `main` should represent the intended production state unless the project explicitly uses another branch.
- Do not add paid infrastructure unless explicitly approved.
- Prefer static generation/edge delivery for public SEO pages when practical.
- Verify production routes after deploy; do not treat a successful build as proof that the site works.

## Post-deploy checks

- Homepage 200
- Primary tools 200 and functional
- Important SEO routes 200
- Sitemap accessible
- robots.txt accessible
- Canonical points to production domain
- Static assets/images load
- No mixed-content or obvious CSP errors
- Mobile layout usable
