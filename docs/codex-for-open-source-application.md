# Codex For Open Source Application Dossier

This document is a fill-in application pack for Maintainer Radar. Replace placeholders with real public evidence after the repository is published.

Official form fields confirmed on 2026-06-01:

- GitHub username: public profile required.
- GitHub repository URL: public repository required.
- Maintainer role: primary or core maintainer.
- Qualification statement: maximum 500 characters.
- Interest: Codex Security and/or API credits.
- OpenAI Organization ID.
- API credit use statement: maximum 500 characters.
- Optional note: maximum 500 characters.

## Repository URL

`https://github.com/YOUR_GITHUB_USERNAME/maintainer-radar`

## Maintainer Role

Primary maintainer.

## Why This Repository Qualifies

Draft under 500 characters:

Maintainer Radar helps OSS maintainers rank issues/PRs, spot release blockers, and produce actionable Codex briefs from GitHub metadata. It targets active projects with growing maintainer load and is built with tests, CI, security policy, governance, examples, and public docs so maintainers can safely automate triage and release work.

Before submitting, add one or more real evidence points:

- GitHub stars: `__`
- Forks: `__`
- Monthly package downloads: `__`
- Early adopter repositories: `__`
- Maintainer workload evidence: `__ open issues`, `__ open PRs`, `__ releases/month`
- Ecosystem importance: `__`

## Interested In

- Codex Security
- API credits for my project

## API Credit Use

Draft under 500 characters:

We will use API credits to generate review briefs for high-risk PRs, deduplicate and cluster issues, draft release notes, and run security-focused Codex reviews on dependency and auth-related changes. Outputs stay maintainer-reviewed suggestions; secrets, private advisories, and private repository content are excluded from prompts.

## Anything Else

Draft under 500 characters:

The project is designed to make Codex useful to many maintainers, not only one repo: deterministic local scoring first, optional AI briefs, auditable config, CI, security policy, and examples. Credits would accelerate real-world validation with early OSS users and public maintenance playbooks.

## Evidence Checklist

- [ ] Public GitHub repository exists.
- [ ] README shows quickstart and maintainer value.
- [ ] CI is green on `main`.
- [ ] Security policy is visible.
- [ ] Issues and PR templates are enabled.
- [ ] At least one release is tagged.
- [ ] Example report and Codex brief are committed or attached to release notes.
- [ ] Real usage/adoption/importance signals are added above.

## Generate A Fresh Application Pack

After publishing the repository, generate a fresh snapshot and application pack:

```bash
python -m maintainer_radar snapshot-github YOUR_GITHUB_USERNAME/maintainer-radar --output reports/github-snapshot.json
python -m maintainer_radar apply-pack reports/github-snapshot.json --repository-url https://github.com/YOUR_GITHUB_USERNAME/maintainer-radar --output reports/application-pack.md
```

Use the generated pack to verify character counts and identify missing evidence before submitting.
