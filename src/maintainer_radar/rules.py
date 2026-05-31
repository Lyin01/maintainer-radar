from __future__ import annotations

from datetime import datetime, timezone

from .config import RadarConfig
from .models import (
    AnalysisReport,
    Issue,
    IssueFinding,
    PullRequest,
    PullRequestFinding,
    ReleaseFinding,
    RepositorySnapshot,
)


def _days_old(created_at: datetime | None, now: datetime) -> int:
    if created_at is None:
        return 0
    return max((now - created_at).days, 0)


def _has(labels: tuple[str, ...], candidates: tuple[str, ...]) -> bool:
    return bool(set(labels).intersection(candidates))


def _mentions_security(text: str) -> bool:
    haystack = text.lower()
    return any(token in haystack for token in ("cve", "vulnerability", "exploit", "token leak", "rce"))


def classify_issue(issue: Issue, config: RadarConfig, now: datetime) -> IssueFinding:
    labels = issue.labels
    age = _days_old(issue.created_at, now)

    if _has(labels, config.labels.security) or _mentions_security(issue.title):
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P0",
            reason="Security-sensitive issue or vulnerability language detected.",
            recommended_action="Move to private security triage, assign an owner, and prepare a fix plan.",
            labels=labels,
            url=issue.url,
        )

    if _has(labels, config.labels.release_blocker):
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P1",
            reason="Release-blocking, regression, or breaking-change label is present.",
            recommended_action="Confirm release impact, reproduce, and decide whether to block the next tag.",
            labels=labels,
            url=issue.url,
        )

    if _has(labels, config.labels.needs_reproduction):
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P2",
            reason="Needs reproduction before engineering work is actionable.",
            recommended_action="Ask for a minimal reproduction, version, platform, and expected behavior.",
            labels=labels,
            url=issue.url,
        )

    if _has(labels, config.labels.bug) and (issue.comments >= 5 or age >= 14):
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P1",
            reason="Bug report has maintainer/community activity or has aged past two weeks.",
            recommended_action="Reproduce, identify owner, and decide whether a patch or workaround is needed.",
            labels=labels,
            url=issue.url,
        )

    if age >= config.thresholds.stale_issue_days:
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P3",
            reason=f"Issue is older than {config.thresholds.stale_issue_days} days without higher-risk signals.",
            recommended_action="Close if obsolete, ask for confirmation, or move to backlog.",
            labels=labels,
            url=issue.url,
        )

    if _has(labels, config.labels.documentation):
        return IssueFinding(
            number=issue.number,
            title=issue.title,
            priority="P3",
            reason="Documentation issue with no release-blocking signal.",
            recommended_action="Batch with other docs work or mark good-first-issue if scoped.",
            labels=labels,
            url=issue.url,
        )

    return IssueFinding(
        number=issue.number,
        title=issue.title,
        priority="P2",
        reason="Open issue without immediate security or release-blocking signal.",
        recommended_action="Triage labels, clarify expected behavior, and decide owner/backlog status.",
        labels=labels,
        url=issue.url,
    )


def _check_penalty(checks: tuple[str, ...]) -> tuple[int, str | None]:
    if not checks:
        return 0, None
    if any(check in {"failure", "failed", "error", "cancelled", "timed_out"} for check in checks):
        return 20, "failing or cancelled checks"
    if any(check in {"pending", "queued", "in_progress"} for check in checks):
        return 6, "pending checks"
    return 0, None


def classify_pull_request(pr: PullRequest, config: RadarConfig, now: datetime) -> PullRequestFinding:
    labels = pr.labels
    age = _days_old(pr.created_at, now)
    lines_changed = pr.additions + pr.deletions
    score = 0
    reasons: list[str] = []

    if pr.draft:
        reasons.append("draft PR")
    if pr.changed_files >= config.thresholds.large_pr_files:
        score += 18
        reasons.append(f"{pr.changed_files} changed files")
    else:
        score += min(pr.changed_files * 2, 12)

    if lines_changed >= config.thresholds.large_pr_lines:
        score += 20
        reasons.append(f"{lines_changed} changed lines")
    else:
        score += min(lines_changed // 80, 10)

    if _has(labels, config.labels.security):
        score += 35
        reasons.append("security-sensitive label")
    if _has(labels, config.labels.release_blocker):
        score += 25
        reasons.append("release-blocking label")
    if _has(labels, config.labels.dependency):
        score += 10
        reasons.append("dependency-related change")

    if pr.review_decision == "CHANGES_REQUESTED":
        score += 20
        reasons.append("changes requested")
    elif pr.review_decision == "REVIEW_REQUIRED":
        score += 8
        reasons.append("review required")

    if pr.merge_state in {"BLOCKED", "DIRTY", "UNKNOWN"}:
        score += 15
        reasons.append(f"merge state {pr.merge_state.lower()}")

    check_score, check_reason = _check_penalty(pr.checks)
    score += check_score
    if check_reason:
        reasons.append(check_reason)

    if age >= config.thresholds.stale_pr_days:
        score += 10
        reasons.append(f"open for {age} days")

    score = max(0, min(score, 100))
    if score >= 75:
        risk = "critical"
        action = "Split or assign senior review; run focused security and regression checks before merge."
    elif score >= 50:
        risk = "high"
        action = "Request targeted review, verify CI, and ask Codex for a risk-focused review brief."
    elif score >= 25:
        risk = "medium"
        action = "Review normally, paying attention to the listed risk signals."
    else:
        risk = "low"
        action = "Proceed with standard review once CI and ownership are clear."

    return PullRequestFinding(
        number=pr.number,
        title=pr.title,
        risk=risk,
        score=score,
        reason=", ".join(reasons) if reasons else "small PR with no high-risk labels or CI signals",
        recommended_action=action,
        labels=labels,
        url=pr.url,
    )


def assess_release(snapshot: RepositorySnapshot, issues: tuple[IssueFinding, ...], prs: tuple[PullRequestFinding, ...]) -> ReleaseFinding:
    blockers: list[str] = list(snapshot.release.blockers)
    blockers.extend(f"issue #{issue.number}: {issue.title}" for issue in issues if issue.priority in {"P0", "P1"})
    blockers.extend(f"PR #{pr.number}: {pr.title}" for pr in prs if pr.risk in {"critical", "high"})

    if any(issue.priority == "P0" for issue in issues):
        status = "blocked"
        summary = "Security-sensitive issues must be resolved before release."
    elif blockers:
        status = "needs-review"
        summary = "Release has open blocker or high-risk review signals."
    else:
        status = "ready"
        summary = "No P0/P1 issues or high-risk PRs detected in the snapshot."

    return ReleaseFinding(status=status, summary=summary, blockers=tuple(blockers))


def analyze_snapshot(snapshot: RepositorySnapshot, config: RadarConfig, now: datetime | None = None) -> AnalysisReport:
    if now is None:
        now = datetime.now(timezone.utc)

    issue_findings = tuple(
        sorted(
            (classify_issue(issue, config, now) for issue in snapshot.issues if issue.state == "open"),
            key=lambda finding: (finding.priority, finding.number),
        )
    )
    pr_findings = tuple(
        sorted(
            (classify_pull_request(pr, config, now) for pr in snapshot.pull_requests if pr.state == "open"),
            key=lambda finding: (-finding.score, finding.number),
        )
    )
    release = assess_release(snapshot, issue_findings, pr_findings)
    return AnalysisReport(
        repository=snapshot.repository,
        issues=issue_findings,
        pull_requests=pr_findings,
        release=release,
    )

