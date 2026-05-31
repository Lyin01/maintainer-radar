# Maintainer Radar

Maintainer Radar is a local-first CLI that turns GitHub issue, pull request, and release metadata into a maintainer work queue: issue priority, PR review risk, release blockers, and a Codex-ready brief that a human maintainer can review before using any AI assistant.

It is designed for open-source maintainers who need help with exactly the work highlighted by the Codex for Open Source application: pull request review, issue triage, release management, security coverage, and repeatable maintenance automation.

## What It Does

- Ranks issues into P0-P3 triage buckets using labels, age, comments, security language, and release-blocker signals.
- Scores pull requests by review risk using size, labels, draft state, merge state, review decision, and CI signals.
- Produces release readiness notes so maintainers can spot blockers before tagging a release.
- Exports a concise Codex brief with repository context, top risks, and concrete review tasks.
- Runs locally with deterministic rules first; optional AI usage can be added without sending secrets by default.

## Quick Start

```bash
python -m pip install -e .
python -m maintainer_radar analyze examples/github-snapshot.json --output reports/triage.md
python -m maintainer_radar brief examples/github-snapshot.json --output reports/codex-brief.md
```

Generate a starter config:

```bash
python -m maintainer_radar init-config --output .maintainer-radar.toml
```

Fetch a live GitHub snapshot:

```bash
python -m maintainer_radar snapshot-github owner/name --output reports/github-snapshot.json
python -m maintainer_radar analyze reports/github-snapshot.json --output reports/triage.md
python -m maintainer_radar apply-pack reports/github-snapshot.json --repository-url https://github.com/owner/name --output reports/application-pack.md
```

## Input Format

Maintainer Radar accepts a JSON snapshot with `repository`, `issues`, `pull_requests`, and optional `release` sections. The example in [examples/github-snapshot.json](examples/github-snapshot.json) shows the supported shape.

You can build the same data from GitHub CLI output and combine it into one file:

```bash
gh issue list --state open --limit 200 --json number,title,labels,state,createdAt,updatedAt,comments,assignees,url
gh pr list --state open --limit 100 --json number,title,labels,isDraft,additions,deletions,changedFiles,reviewDecision,mergeStateStatus,statusCheckRollup,createdAt,updatedAt,url
```

## Why This Repository Is Application-Ready

The Codex for Open Source form asks for a public GitHub username, a public repository URL, maintainer role, why the repository qualifies, and how API credits will support maintainer workflows. This repository includes:

- Working maintainer automation with tests and sample outputs.
- CI, CodeQL, release workflow, issue templates, PR template, security policy, governance, and contribution docs.
- A scheduled maintenance report workflow that fetches GitHub data and exports review artifacts.
- Committed sample output in [examples/sample-report.md](examples/sample-report.md), [examples/sample-codex-brief.md](examples/sample-codex-brief.md), and [examples/sample-application-pack.md](examples/sample-application-pack.md).
- Application readiness output with character counts and missing-evidence checks for the Codex for Open Source form.
- A prepared application dossier in [docs/codex-for-open-source-application.md](docs/codex-for-open-source-application.md).
- A public launch checklist in [docs/publication-checklist.md](docs/publication-checklist.md).

Important: a brand-new repository still needs honest adoption evidence. Use the application dossier to add real GitHub stars, downloads, dependent repositories, early users, or ecosystem importance after publishing.

## Maintainer Safety

Maintainer Radar is intentionally local-first. The default workflow does not call external AI APIs, upload private reports, or process secrets. If a maintainer later adds AI summarization, the project policy is to send only public issue/PR metadata and to keep all generated output as maintainer-reviewed suggestions.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the next milestones: live GitHub API ingestion, dependency-risk signals, release note drafting, and optional OpenAI-powered clustering behind explicit configuration.
