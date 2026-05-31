from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def normalize_labels(labels: list[Any] | tuple[Any, ...] | None) -> tuple[str, ...]:
    if not labels:
        return ()
    normalized: list[str] = []
    for label in labels:
        if isinstance(label, str):
            name = label
        elif isinstance(label, dict):
            name = str(label.get("name", ""))
        else:
            name = str(label)
        name = name.strip().lower()
        if name:
            normalized.append(name)
    return tuple(dict.fromkeys(normalized))


@dataclass(frozen=True)
class RepositoryInfo:
    name: str = "unknown/repository"
    default_branch: str = "main"
    description: str = ""
    url: str = ""


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    labels: tuple[str, ...] = ()
    state: str = "open"
    created_at: datetime | None = None
    updated_at: datetime | None = None
    comments: int = 0
    assignees: tuple[str, ...] = ()
    url: str = ""


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    labels: tuple[str, ...] = ()
    state: str = "open"
    draft: bool = False
    additions: int = 0
    deletions: int = 0
    changed_files: int = 0
    review_decision: str = ""
    merge_state: str = ""
    checks: tuple[str, ...] = ()
    created_at: datetime | None = None
    updated_at: datetime | None = None
    url: str = ""


@dataclass(frozen=True)
class ReleaseSignal:
    next_version: str = ""
    target_date: str = ""
    blockers: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class RepositorySnapshot:
    repository: RepositoryInfo = field(default_factory=RepositoryInfo)
    issues: tuple[Issue, ...] = ()
    pull_requests: tuple[PullRequest, ...] = ()
    release: ReleaseSignal = field(default_factory=ReleaseSignal)


@dataclass(frozen=True)
class IssueFinding:
    number: int
    title: str
    priority: str
    reason: str
    recommended_action: str
    labels: tuple[str, ...]
    url: str = ""


@dataclass(frozen=True)
class PullRequestFinding:
    number: int
    title: str
    risk: str
    score: int
    reason: str
    recommended_action: str
    labels: tuple[str, ...]
    url: str = ""


@dataclass(frozen=True)
class ReleaseFinding:
    status: str
    summary: str
    blockers: tuple[str, ...]


@dataclass(frozen=True)
class AnalysisReport:
    repository: RepositoryInfo
    issues: tuple[IssueFinding, ...]
    pull_requests: tuple[PullRequestFinding, ...]
    release: ReleaseFinding

