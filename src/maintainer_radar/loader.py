from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import (
    Issue,
    PullRequest,
    ReleaseSignal,
    RepositoryInfo,
    RepositorySnapshot,
    normalize_labels,
    parse_datetime,
)


def _assignee_names(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    names: list[str] = []
    for item in value:
        if isinstance(item, str):
            name = item
        elif isinstance(item, dict):
            name = str(item.get("login") or item.get("name") or "")
        else:
            name = str(item)
        if name.strip():
            names.append(name.strip())
    return tuple(names)


def _checks(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    states: list[str] = []
    for item in value:
        if isinstance(item, str):
            states.append(item.lower())
        elif isinstance(item, dict):
            conclusion = item.get("conclusion") or item.get("status") or item.get("state")
            if conclusion:
                states.append(str(conclusion).lower())
    return tuple(states)


def _repository(raw: dict[str, Any]) -> RepositoryInfo:
    data = raw.get("repository", {})
    if not isinstance(data, dict):
        data = {}
    return RepositoryInfo(
        name=str(data.get("name") or data.get("full_name") or "unknown/repository"),
        default_branch=str(data.get("default_branch") or data.get("defaultBranchRef", "main")),
        description=str(data.get("description") or ""),
        url=str(data.get("url") or data.get("html_url") or ""),
    )


def _issue(item: dict[str, Any]) -> Issue:
    return Issue(
        number=int(item.get("number", 0)),
        title=str(item.get("title", "")),
        labels=normalize_labels(item.get("labels")),
        state=str(item.get("state", "open")).lower(),
        created_at=parse_datetime(item.get("createdAt") or item.get("created_at")),
        updated_at=parse_datetime(item.get("updatedAt") or item.get("updated_at")),
        comments=int(item.get("comments", 0) or item.get("comments_count", 0) or 0),
        assignees=_assignee_names(item.get("assignees")),
        url=str(item.get("url") or item.get("html_url") or ""),
    )


def _pull_request(item: dict[str, Any]) -> PullRequest:
    return PullRequest(
        number=int(item.get("number", 0)),
        title=str(item.get("title", "")),
        labels=normalize_labels(item.get("labels")),
        state=str(item.get("state", "open")).lower(),
        draft=bool(item.get("isDraft") or item.get("draft", False)),
        additions=int(item.get("additions", 0) or 0),
        deletions=int(item.get("deletions", 0) or 0),
        changed_files=int(item.get("changedFiles") or item.get("changed_files") or 0),
        review_decision=str(item.get("reviewDecision") or item.get("review_decision") or "").upper(),
        merge_state=str(item.get("mergeStateStatus") or item.get("merge_state") or "").upper(),
        checks=_checks(item.get("statusCheckRollup") or item.get("checks")),
        created_at=parse_datetime(item.get("createdAt") or item.get("created_at")),
        updated_at=parse_datetime(item.get("updatedAt") or item.get("updated_at")),
        url=str(item.get("url") or item.get("html_url") or ""),
    )


def _release(raw: dict[str, Any]) -> ReleaseSignal:
    data = raw.get("release", {})
    if not isinstance(data, dict):
        data = {}
    blockers = data.get("blockers") if isinstance(data.get("blockers"), list) else []
    notes = data.get("notes") if isinstance(data.get("notes"), list) else []
    return ReleaseSignal(
        next_version=str(data.get("next_version") or data.get("nextVersion") or ""),
        target_date=str(data.get("target_date") or data.get("targetDate") or ""),
        blockers=tuple(str(item) for item in blockers),
        notes=tuple(str(item) for item in notes),
    )


def load_snapshot(path: Path) -> RepositorySnapshot:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Snapshot must be a JSON object.")

    issues = raw.get("issues", [])
    pull_requests = raw.get("pull_requests", raw.get("pullRequests", []))
    if not isinstance(issues, list):
        raise ValueError("Snapshot field 'issues' must be a list.")
    if not isinstance(pull_requests, list):
        raise ValueError("Snapshot field 'pull_requests' must be a list.")

    return RepositorySnapshot(
        repository=_repository(raw),
        issues=tuple(_issue(item) for item in issues if isinstance(item, dict)),
        pull_requests=tuple(_pull_request(item) for item in pull_requests if isinstance(item, dict)),
        release=_release(raw),
    )

