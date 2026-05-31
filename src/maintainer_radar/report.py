from __future__ import annotations

import json
from dataclasses import asdict

from .models import AnalysisReport


def _labels(labels: tuple[str, ...]) -> str:
    return ", ".join(labels) if labels else "none"


def to_markdown(report: AnalysisReport) -> str:
    lines: list[str] = [
        f"# Maintainer Radar Report: {report.repository.name}",
        "",
        f"Release status: **{report.release.status}**",
        "",
        report.release.summary,
        "",
        "## Issue Triage",
        "",
    ]

    if report.issues:
        lines.append("| Priority | Issue | Reason | Action |")
        lines.append("| --- | --- | --- | --- |")
        for issue in report.issues:
            issue_ref = f"[#{issue.number}]({issue.url})" if issue.url else f"#{issue.number}"
            lines.append(
                f"| {issue.priority} | {issue_ref} {issue.title} | {issue.reason} | {issue.recommended_action} |"
            )
    else:
        lines.append("No open issues found in the snapshot.")

    lines.extend(["", "## Pull Request Risk", ""])
    if report.pull_requests:
        lines.append("| Risk | Score | PR | Reason | Action |")
        lines.append("| --- | ---: | --- | --- | --- |")
        for pr in report.pull_requests:
            pr_ref = f"[#{pr.number}]({pr.url})" if pr.url else f"#{pr.number}"
            lines.append(
                f"| {pr.risk} | {pr.score} | {pr_ref} {pr.title} | {pr.reason} | {pr.recommended_action} |"
            )
    else:
        lines.append("No open pull requests found in the snapshot.")

    lines.extend(["", "## Release Readiness", ""])
    if report.release.blockers:
        for blocker in report.release.blockers:
            lines.append(f"- {blocker}")
    else:
        lines.append("- No blockers detected.")

    lines.extend(["", "## Label Context", ""])
    for issue in report.issues[:5]:
        lines.append(f"- Issue #{issue.number}: {_labels(issue.labels)}")
    for pr in report.pull_requests[:5]:
        lines.append(f"- PR #{pr.number}: {_labels(pr.labels)}")

    return "\n".join(lines) + "\n"


def to_json(report: AnalysisReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=True)


def to_codex_brief(report: AnalysisReport) -> str:
    top_issues = report.issues[:5]
    top_prs = report.pull_requests[:5]

    lines: list[str] = [
        f"# Codex Maintenance Brief: {report.repository.name}",
        "",
        "You are helping a human open-source maintainer. Treat this as decision support, not an automatic merge or close instruction.",
        "",
        "## Repository Context",
        "",
        f"- Repository: {report.repository.name}",
        f"- Default branch: {report.repository.default_branch}",
        f"- Release status: {report.release.status}",
        f"- Release summary: {report.release.summary}",
        "",
        "## Highest Priority Issues",
        "",
    ]

    if top_issues:
        for issue in top_issues:
            issue_ref = f"#{issue.number}"
            lines.append(f"- {issue.priority} {issue_ref}: {issue.title}")
            lines.append(f"  Reason: {issue.reason}")
            lines.append(f"  Maintainer action: {issue.recommended_action}")
    else:
        lines.append("- No open issues in this snapshot.")

    lines.extend(["", "## Highest Risk Pull Requests", ""])
    if top_prs:
        for pr in top_prs:
            pr_ref = f"#{pr.number}"
            lines.append(f"- {pr.risk.upper()} {pr_ref}: {pr.title} (score {pr.score})")
            lines.append(f"  Risk signals: {pr.reason}")
            lines.append(f"  Maintainer action: {pr.recommended_action}")
    else:
        lines.append("- No open pull requests in this snapshot.")

    lines.extend(
        [
            "",
            "## Requested Codex Work",
            "",
            "1. Check whether any P0/P1 issue or high-risk PR should block the next release.",
            "2. For each high-risk PR, propose a focused review checklist and possible test gaps.",
            "3. For stale or under-specified issues, draft concise maintainer responses.",
            "4. Do not invent facts beyond the snapshot. Call out missing evidence explicitly.",
        ]
    )

    return "\n".join(lines) + "\n"

