# Visual Regression Baseline Policy

## Purpose

A visual snapshot is an approved rendering baseline, not an incidental screenshot. It must be generated and compared in the same operating-system and browser environment. The downstream P1 workflow uses **GitHub Actions `ubuntu-24.04`**, `npm ci` from the committed lockfile, and the Chromium revision installed by that locked Playwright package.

## Required baseline workflow

1. Copy the P1 Playwright files and `templates/github-actions/website-browser-quality.yml` as described in `DOWNSTREAM-ADOPTION.md`.
2. Commit `package.json` and `package-lock.json`; do not use an unpinned global Playwright installation.
3. Set `QA_VISUAL_ROUTES_JSON` to the exact approved routes. Keep `QA_VISUAL_UPDATE='0'` for ordinary CI.
4. To create or intentionally refresh baselines, temporarily set `QA_VISUAL_UPDATE='1'` in the downstream workflow and trigger that workflow on the branch whose rendering is being approved. The workflow uses the same Ubuntu runner, locked Playwright package, installed Chromium and application build as its normal comparison job. Its explicit `--update-snapshots` step writes candidates to `tests/e2e/__screenshots__/`.
5. Download the `website-p1-release-evidence` artifact, including `visual-environment.txt` (runner image, Node, Playwright, Chromium version and route list). Inspect every route/viewport image for content, layout, font, clipping, loading and dynamic-data correctness. A generated image is only a candidate; it is not approved merely because the command succeeded.
6. Commit only the inspected snapshot files to the downstream repository. Set `QA_VISUAL_UPDATE='0'` again and rerun CI. The ordinary workflow now compares against the committed baselines and never updates them.
7. Keep the Playwright dependency and lockfile unchanged when comparing against those baselines. If the approved runner OS, browser revision, font set or rendering environment intentionally changes, regenerate and review a new baseline set as a separate change.

## Local Windows use

Windows screenshots are useful for local preview and visual investigation, but they are **not CI-approved baselines** for the Ubuntu workflow. Do not commit Windows-generated images as the expected output for Linux CI. A developer without access to the matching CI environment may review local screenshots, but must leave the automated visual gate `NOT RUN` until the CI-generated candidates have been inspected and committed.

## Route identity and snapshot names

Snapshot names include a readable route slug plus a SHA-256 prefix of the original route. This prevents collisions such as `/foo/bar/` versus `/foo-bar/`, and `/` versus `/home/`, while remaining deterministic across operating systems.

## Safety rules

- Visual baseline generation is opt-in; ordinary CI must not pass `--update-snapshots`.
- Do not update snapshots automatically after a mismatch.
- Mask only genuinely nondeterministic regions using `data-visual-mask`; do not mask broken layout or meaningful content.
- Record the route list, Playwright version, browser and runner environment with the release evidence.
- A visual snapshot does not replace interaction, accessibility, responsive, export, SEO, production or real-device checks.
