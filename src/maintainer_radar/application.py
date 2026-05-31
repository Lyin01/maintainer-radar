from __future__ import annotations

from .models import AnalysisReport, RepositorySnapshot


QUALIFICATION_DRAFT = (
    "Maintainer Radar helps OSS maintainers rank issues/PRs, spot release blockers, and produce actionable Codex "
    "briefs from GitHub metadata. It targets active projects with growing maintainer load and is built with tests, CI, "
    "security policy, governance, examples, and public docs so maintainers can safely automate triage and release work."
)

API_CREDIT_DRAFT = (
    "We will use API credits to generate review briefs for high-risk PRs, deduplicate and cluster issues, draft release "
    "notes, and run security-focused Codex reviews on dependency and auth-related changes. Outputs stay "
    "maintainer-reviewed suggestions; secrets, private advisories, and private repository content are excluded from prompts."
)

OPTIONAL_NOTE_DRAFT = (
    "The project is designed to make Codex useful to many maintainers, not only one repo: deterministic local scoring "
    "first, optional AI briefs, auditable config, CI, security policy, and examples. Credits would accelerate real-world "
    "validation with early OSS users and public maintenance playbooks."
)


def character_count(text: str) -> int:
    return len(text.strip())


def _fit_status(text: str, limit: int = 500) -> str:
    count = character_count(text)
    return "ok" if count <= limit else f"too long by {count - limit}"


def _risk_counts(report: AnalysisReport) -> tuple[int, int, int]:
    p0_or_p1 = sum(1 for issue in report.issues if issue.priority in {"P0", "P1"})
    high_prs = sum(1 for pr in report.pull_requests if pr.risk in {"critical", "high"})
    release_blockers = len(report.release.blockers)
    return p0_or_p1, high_prs, release_blockers


def _checklist_line(done: bool, label: str, detail: str) -> str:
    marker = "x" if done else " "
    return f"- [{marker}] {label}: {detail}"


def build_application_pack(
    snapshot: RepositorySnapshot,
    report: AnalysisReport,
    *,
    role: str = "Primary maintainer",
    repository_url: str | None = None,
) -> str:
    repo_url = repository_url or snapshot.repository.url or "https://github.com/YOUR_GITHUB_USERNAME/maintainer-radar"
    p0_or_p1, high_prs, release_blockers = _risk_counts(report)
    open_issues = len(snapshot.issues)
    open_prs = len(snapshot.pull_requests)

    has_public_url = repo_url.startswith("https://github.com/") and "YOUR_GITHUB_USERNAME" not in repo_url
    has_maintenance_load = bool(open_issues or open_prs)
    has_codex_workflow = bool(report.issues or report.pull_requests)

    lines = [
        f"# Codex For Open Source Application Pack: {snapshot.repository.name}",
        "",
        "This pack is generated from a Maintainer Radar snapshot. Keep the usage claims honest before submitting.",
        "",
        "## Form Fields",
        "",
        f"- GitHub repository URL: `{repo_url}`",
        f"- Maintainer role: {role}",
        "- Interested in: Codex Security; API credits for my project",
        "- OpenAI Organization ID: `<fill in from platform.openai.com>`",
        "",
        "## Draft Answers",
        "",
        "### Why does this repository qualify?",
        "",
        QUALIFICATION_DRAFT,
        "",
        f"Character count: {character_count(QUALIFICATION_DRAFT)} / 500 ({_fit_status(QUALIFICATION_DRAFT)})",
        "",
        "### How will you use API credits for your project?",
        "",
        API_CREDIT_DRAFT,
        "",
        f"Character count: {character_count(API_CREDIT_DRAFT)} / 500 ({_fit_status(API_CREDIT_DRAFT)})",
        "",
        "### Anything else we should know?",
        "",
        OPTIONAL_NOTE_DRAFT,
        "",
        f"Character count: {character_count(OPTIONAL_NOTE_DRAFT)} / 500 ({_fit_status(OPTIONAL_NOTE_DRAFT)})",
        "",
        "## Evidence From Snapshot",
        "",
        f"- Repository: {snapshot.repository.name}",
        f"- Default branch: {snapshot.repository.default_branch}",
        f"- Open issues in snapshot: {open_issues}",
        f"- Open pull requests in snapshot: {open_prs}",
        f"- P0/P1 issues detected: {p0_or_p1}",
        f"- High-risk pull requests detected: {high_prs}",
        f"- Release blockers detected: {release_blockers}",
        f"- Release status: {report.release.status}",
        "",
        "## Top Maintenance Signals",
        "",
    ]

    if report.issues:
        for issue in report.issues[:5]:
            lines.append(f"- {issue.priority} issue #{issue.number}: {issue.title}")
    else:
        lines.append("- No open issues in this snapshot.")

    if report.pull_requests:
        for pr in report.pull_requests[:5]:
            lines.append(f"- {pr.risk} PR #{pr.number}: {pr.title} (score {pr.score})")
    else:
        lines.append("- No open pull requests in this snapshot.")

    lines.extend(
        [
            "",
            "## Readiness Checklist",
            "",
            _checklist_line(has_public_url, "Public GitHub repository URL", repo_url),
            _checklist_line(has_maintenance_load, "Active maintenance signal", f"{open_issues} issues, {open_prs} PRs"),
            _checklist_line(has_codex_workflow, "Codex maintainer workflow evidence", "triage and review brief generated"),
            _checklist_line(True, "Local-first safety posture", "default workflow does not call external AI APIs"),
            _checklist_line(True, "Automation evidence", "CI, CodeQL, scheduled report, and sample outputs are included"),
            _checklist_line(False, "External adoption evidence", "add real stars, downloads, dependent repos, or early users"),
            _checklist_line(False, "Public release evidence", "publish a v0.1.0 release after pushing to GitHub"),
            "",
            "## Submission Notes",
            "",
            "- Replace placeholders before submission.",
            "- Add real usage and ecosystem evidence; do not invent stars, downloads, or adopters.",
            "- Attach or link generated triage and Codex brief reports when explaining API credit use.",
        ]
    )

    return "\n".join(lines) + "\n"

