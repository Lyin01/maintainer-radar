# Maintainer Workflows

Maintainer Radar supports three high-friction maintenance loops.

## Issue Triage

Run:

```bash
python -m maintainer_radar snapshot-github owner/name --output reports/github-snapshot.json
python -m maintainer_radar analyze reports/github-snapshot.json --output reports/triage.md
```

Use the report to:

- Move P0 issues to private security handling.
- Assign P1 bugs and release blockers.
- Ask for reproductions on under-specified issues.
- Batch docs and stale issues for lower-interruption work.

## Pull Request Review

The PR risk score helps maintainers decide where limited review attention belongs.

High-risk signals include:

- Security or dependency labels.
- Large changed-file or changed-line count.
- Failing checks.
- Merge conflicts or blocked merge state.
- Changes requested.
- Long-running open PRs.

## Release Readiness

Before tagging a release:

1. Generate a fresh snapshot.
2. Run the report.
3. Resolve P0 issues.
4. Decide whether P1 issues and high-risk PRs block the release.
5. Generate a Codex brief for focused review and test-gap suggestions.

## Codex Briefs

Run:

```bash
python -m maintainer_radar brief examples/github-snapshot.json --output reports/codex-brief.md
```

The brief asks Codex to identify blockers, review checklists, stale issue responses, and missing evidence. It is intentionally explicit that Codex is helping a human maintainer, not making final decisions.

## Application Evidence

Run:

```bash
python -m maintainer_radar apply-pack reports/github-snapshot.json --repository-url https://github.com/owner/name --output reports/application-pack.md
```

The pack gives maintainers a form-ready summary with 500-character checks, maintenance-load metrics, top risks, and a checklist of evidence still needed before applying.
