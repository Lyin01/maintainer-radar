# Release Playbook

Maintainer Radar treats release readiness as a maintainer decision with an automatable first pass.

## Local Release Check

```bash
python -m maintainer_radar snapshot-github owner/name --output reports/github-snapshot.json
python -m maintainer_radar analyze reports/github-snapshot.json --output reports/triage.md
python -m maintainer_radar gate reports/github-snapshot.json --output reports/gate.md
```

The `gate` command exits non-zero when the snapshot contains:

- a blocked release status
- a P0 security issue
- more P1 issues than allowed by `--max-p1-issues`
- more high-risk PRs than allowed by `--max-high-risk-prs`

Use `--warn-only` for scheduled reports where maintainers want an artifact without failing a workflow.

## GitHub Release Workflow

The included release workflow runs the gate before building artifacts for tags matching `v*.*.*`. If the gate fails, the release stops before packaging.

This is intentionally conservative. Maintainers can choose to:

- resolve the issue or PR
- raise the allowed threshold for a known release
- run the gate locally with `--warn-only` and document the release exception

## Human Review

The gate is not a substitute for release ownership. It is a visible checkpoint that makes release risk explicit before a tag becomes a public artifact.

