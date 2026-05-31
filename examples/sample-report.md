# Maintainer Radar Report: example/critical-oss-project

Release status: **blocked**

Security-sensitive issues must be resolved before release.

## Issue Triage

| Priority | Issue | Reason | Action |
| --- | --- | --- | --- |
| P0 | [#41](https://github.com/example/critical-oss-project/issues/41) Possible token leak in debug logging | Security-sensitive issue or vulnerability language detected. | Move to private security triage, assign an owner, and prepare a fix plan. |
| P1 | [#44](https://github.com/example/critical-oss-project/issues/44) Regression: Windows path handling fails in release candidate | Release-blocking, regression, or breaking-change label is present. | Confirm release impact, reproduce, and decide whether to block the next tag. |
| P3 | [#45](https://github.com/example/critical-oss-project/issues/45) Document plugin lifecycle hooks | Documentation issue with no release-blocking signal. | Batch with other docs work or mark good-first-issue if scoped. |

## Pull Request Risk

| Risk | Score | PR | Reason | Action |
| --- | ---: | --- | --- | --- |
| critical | 100 | [#88](https://github.com/example/critical-oss-project/pull/88) Refactor auth token storage | 18 changed files, 750 changed lines, security-sensitive label, dependency-related change, review required, merge state blocked, failing or cancelled checks | Split or assign senior review; run focused security and regression checks before merge. |
| low | 2 | [#89](https://github.com/example/critical-oss-project/pull/89) Fix typo in quickstart | small PR with no high-risk labels or CI signals | Proceed with standard review once CI and ownership are clear. |

## Release Readiness

- Release candidate validation is incomplete.
- issue #41: Possible token leak in debug logging
- issue #44: Regression: Windows path handling fails in release candidate
- PR #88: Refactor auth token storage

## Label Context

- Issue #41: security, bug
- Issue #44: bug, regression, release-blocker
- Issue #45: documentation
- PR #88: security, dependencies
- PR #89: documentation

