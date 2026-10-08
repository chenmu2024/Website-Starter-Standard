# UI Release Evidence (Per Project/Release)

> Copy into each project or release record and fill with **observed facts**. This template is deliberately unfilled. `NOT RUN` is not `PASS`; a report without evidence does not certify an implementation.

## Identity and baseline

- Project / repository:
- Branch / commit SHA:
- Production or preview URL:
- Review date and reviewer:
- Page/route(s), visitor mode (Operate / Read / Persuade / Experience):
- Approved keywords, core task and business invariants confirmed:
- Applicable `DESIGN.md` version or reference:
- Before/after screenshots or recording references, if actually captured:
- Baseline route/SEO data checked and where recorded:

## Verification ledger

Use `PASS`, `FAIL`, `NOT RUN`, or `NOT APPLICABLE`. For PASS/FAIL, include a reproducible command or browser observation, viewport, route and date.

| Area | Status | Evidence (file/URL/command/result) | Issue/owner |
|---|---|---|---|
| Core user task, valid input to result | NOT RUN | | |
| Empty, invalid, extreme, error/loading/success states | NOT RUN | | |
| Mobile ~360/390px | NOT RUN | | |
| Tablet ~768px | NOT RUN | | |
| Small laptop ~1024px | NOT RUN | | |
| Desktop ~1440px | NOT RUN | | |
| Keyboard/focus/labels/contrast | NOT RUN | | |
| Touch/custom interaction where relevant | NOT RUN | | |
| Spanish/Portuguese Unicode and overflow, if relevant | NOT RUN | | |
| Design tokens/components and content fidelity | NOT RUN | | |
| Build/type/lint/tests applicable | NOT RUN | | |
| Asset/link/navigation integrity | NOT RUN | | |
| LCP/INP/CLS lab measurements (label field separately) | NOT RUN | | |
| Source scanner `impeccable detect` (optional) | NOT RUN | | |
| Rendered-URL/browser scanner (optional) | NOT RUN | | |
| SEO/GEO nonregression (separate evidence file) | NOT RUN | | |
| Production deployment/user-task verification | NOT RUN | | |

## Optional tooling evidence

- Impeccable installed? (yes/no; by explicit approval only):
- Version + approved source/release:
- Hook installed/enabled? (default no):
- Scanner target/command/exit code (0 clean primary findings, 2 findings, 1 scan error):
- JSON/text output path or summary:
- False positives/brand-approved waivers with explanations:
- Browser/extension/Live used? If so where, permissions, capture evidence:
- Performance tool/environment, lab vs field data, tested device and viewport:
- Commands not executed and why:

## Findings and disposition

| ID | Severity P0/P1/P2/P3 | Route/component | Repro / evidence | Action / assignee | Status |
|---|---|---|---|---|---|
| | | | | | |

- P0 blockers unresolved:
- P1 blockers unresolved:
- P2 owner-approved deferrals:
- Known missing verification / constraints:
- Rollback plan if meaningful existing behavior changed:
- SEO/GEO release evidence link or artifact:

## Decision

- [ ] Core user tasks verified in real execution.
- [ ] Applicable P0/P1 defects are closed.
- [ ] Scope/keywords/routes/canonical/hreflang/analytics protected or explicitly owner-approved.
- [ ] Required visual/mobile/keyboard/production checks have evidence.
- [ ] `SEO-GEO-QUALITY-GATE.md` and required L1/L2 evidence remain satisfied where applicable.

**Decision:** PENDING (default) / ACCEPTED / BLOCKED

**Basis:** List actual results and any accepted limitations. Do not mark ACCEPTED while the main task/production verification or applicable blockers remain unverified.
