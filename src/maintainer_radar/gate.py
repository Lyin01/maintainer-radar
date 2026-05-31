from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from .models import AnalysisReport


@dataclass(frozen=True)
class GateResult:
    passed: bool
    status: str
    failures: tuple[str, ...]
    warnings: tuple[str, ...]


def evaluate_gate(
    report: AnalysisReport,
    *,
    max_p1_issues: int = 0,
    max_high_risk_prs: int = 0,
) -> GateResult:
    failures: list[str] = []
    warnings: list[str] = []

    p0_issues = [issue for issue in report.issues if issue.priority == "P0"]
    p1_issues = [issue for issue in report.issues if issue.priority == "P1"]
    high_risk_prs = [pr for pr in report.pull_requests if pr.risk in {"critical", "high"}]

    if report.release.status == "blocked":
        failures.append("release status is blocked")
    elif report.release.status == "needs-review":
        warnings.append("release status needs maintainer review")

    if p0_issues:
        failures.append(f"{len(p0_issues)} P0 issue(s) require security triage")

    if len(p1_issues) > max_p1_issues:
        failures.append(f"{len(p1_issues)} P1 issue(s) exceed allowed maximum {max_p1_issues}")

    if len(high_risk_prs) > max_high_risk_prs:
        failures.append(f"{len(high_risk_prs)} high-risk PR(s) exceed allowed maximum {max_high_risk_prs}")

    if report.release.blockers:
        warnings.append(f"{len(report.release.blockers)} release blocker note(s) found")

    passed = not failures
    return GateResult(
        passed=passed,
        status="passed" if passed else "failed",
        failures=tuple(failures),
        warnings=tuple(warnings),
    )


def gate_to_markdown(result: GateResult, report: AnalysisReport) -> str:
    lines = [
        f"# Maintainer Radar Quality Gate: {report.repository.name}",
        "",
        f"Status: **{result.status}**",
        "",
        "## Failures",
        "",
    ]

    if result.failures:
        lines.extend(f"- {failure}" for failure in result.failures)
    else:
        lines.append("- None")

    lines.extend(["", "## Warnings", ""])
    if result.warnings:
        lines.extend(f"- {warning}" for warning in result.warnings)
    else:
        lines.append("- None")

    lines.extend(["", "## Release Summary", "", f"- Release status: {report.release.status}"])
    lines.extend(f"- {blocker}" for blocker in report.release.blockers[:10])

    return "\n".join(lines) + "\n"


def gate_to_json(result: GateResult) -> str:
    return json.dumps(asdict(result), indent=2, sort_keys=True) + "\n"

