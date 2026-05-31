# Codex Maintenance Brief: example/critical-oss-project

You are helping a human open-source maintainer. Treat this as decision support, not an automatic merge or close instruction.

## Repository Context

- Repository: example/critical-oss-project
- Default branch: main
- Release status: blocked
- Release summary: Security-sensitive issues must be resolved before release.

## Highest Priority Issues

- P0 #41: Possible token leak in debug logging
  Reason: Security-sensitive issue or vulnerability language detected.
  Maintainer action: Move to private security triage, assign an owner, and prepare a fix plan.
- P1 #44: Regression: Windows path handling fails in release candidate
  Reason: Release-blocking, regression, or breaking-change label is present.
  Maintainer action: Confirm release impact, reproduce, and decide whether to block the next tag.
- P3 #45: Document plugin lifecycle hooks
  Reason: Documentation issue with no release-blocking signal.
  Maintainer action: Batch with other docs work or mark good-first-issue if scoped.

## Highest Risk Pull Requests

- CRITICAL #88: Refactor auth token storage (score 100)
  Risk signals: 18 changed files, 750 changed lines, security-sensitive label, dependency-related change, review required, merge state blocked, failing or cancelled checks
  Maintainer action: Split or assign senior review; run focused security and regression checks before merge.
- LOW #89: Fix typo in quickstart (score 2)
  Risk signals: small PR with no high-risk labels or CI signals
  Maintainer action: Proceed with standard review once CI and ownership are clear.

## Requested Codex Work

1. Check whether any P0/P1 issue or high-risk PR should block the next release.
2. For each high-risk PR, propose a focused review checklist and possible test gaps.
3. For stale or under-specified issues, draft concise maintainer responses.
4. Do not invent facts beyond the snapshot. Call out missing evidence explicitly.

