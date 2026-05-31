# Publication Checklist

Use this checklist to turn the local repository into a public GitHub project.

## Before Publishing

- [x] Replace GitHub username placeholders with `Lyin01`.
- [ ] Run `python -m unittest discover -s tests`.
- [ ] Run the sample CLI commands from the README.
- [ ] Generate `reports/application-pack.md` and review missing evidence.
- [ ] Run `python -m maintainer_radar gate reports/github-snapshot.json --warn-only --output reports/gate.md`.
- [ ] Review `docs/codex-for-open-source-application.md` and keep claims honest.
- [ ] Choose a package name if publishing to PyPI later.

## Publish To GitHub

```bash
git init
git add .
git commit -m "Initial Maintainer Radar release"
git branch -M main
gh repo create Lyin01/maintainer-radar --public --source . --remote origin --push
```

Or publish with a fine-grained token:

```powershell
$env:GITHUB_TOKEN = "github_pat_..."
.\scripts\publish-github.ps1
```

For an organization repository, pass `-Org YOUR_ORG`.

If GitHub CLI is unavailable, create a public empty repository on GitHub and run:

```bash
git remote add origin https://github.com/Lyin01/maintainer-radar.git
git push -u origin main
```

## After Publishing

- [ ] Confirm CI passes on GitHub.
- [ ] Enable GitHub security advisories.
- [ ] Enable Dependabot alerts.
- [ ] Create `v0.1.0` release notes with sample report output.
- [ ] Run the Maintenance Report workflow and download the application pack artifact.
- [ ] Confirm the release quality gate behaves as expected for known blockers.
- [ ] Add real adoption or ecosystem evidence to the application dossier.
- [ ] Submit the Codex for Open Source form.
