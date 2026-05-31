# GitHub Ingestion

Maintainer Radar can create a snapshot directly from a public GitHub repository.

```bash
python -m maintainer_radar snapshot-github owner/name --output reports/github-snapshot.json
python -m maintainer_radar analyze reports/github-snapshot.json --output reports/triage.md
python -m maintainer_radar brief reports/github-snapshot.json --output reports/codex-brief.md
python -m maintainer_radar apply-pack reports/github-snapshot.json --repository-url https://github.com/owner/name --output reports/application-pack.md
python -m maintainer_radar gate reports/github-snapshot.json --output reports/gate.md
```

For higher rate limits or private repositories, set a token before running:

```bash
$env:GITHUB_TOKEN = "github_pat_..."
python -m maintainer_radar snapshot-github owner/name --output reports/github-snapshot.json
```

The snapshot command reads:

- repository name, default branch, description, and URL
- open issues and labels
- open pull requests, labels, draft status, size, merge state, and timestamps
- latest release metadata when available

It does not post comments, close issues, approve PRs, merge code, or call AI APIs.

## Scheduled Reports

The repository includes `.github/workflows/maintenance-report.yml`, which can run weekly or by manual dispatch. It generates:

- `reports/github-snapshot.json`
- `reports/triage.md`
- `reports/codex-brief.md`
- `reports/application-pack.md`
- `reports/gate.md`

Those reports are uploaded as a GitHub Actions artifact for maintainer review.
