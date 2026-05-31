from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_ROOT = "https://api.github.com"
USER_AGENT = "maintainer-radar/0.1"


class GitHubApiError(RuntimeError):
    """Raised when GitHub snapshot collection fails."""


def _request_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GitHubApiError(f"GitHub API request failed with HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise GitHubApiError(f"GitHub API request failed: {exc.reason}") from exc
    except json.JSONDecodeError as exc:
        raise GitHubApiError(f"GitHub API returned invalid JSON from {url}") from exc


def _validate_repository(repository: str) -> str:
    cleaned = repository.strip().strip("/")
    parts = cleaned.split("/")
    if len(parts) != 2 or not all(parts):
        raise GitHubApiError("Repository must be in owner/name form.")
    return cleaned


def _paginate(path: str, token: str | None, limit: int) -> list[dict[str, Any]]:
    if limit <= 0:
        return []

    collected: list[dict[str, Any]] = []
    page = 1
    per_page = min(max(limit, 1), 100)
    while len(collected) < limit:
        query = urlencode({"state": "open", "per_page": per_page, "page": page})
        data = _request_json(f"{API_ROOT}{path}?{query}", token)
        if not isinstance(data, list):
            raise GitHubApiError(f"GitHub API returned unexpected payload for {path}.")
        collected.extend(item for item in data if isinstance(item, dict))
        if len(data) < per_page:
            break
        page += 1
    return collected[:limit]


def _label_names(labels: Any) -> list[str]:
    if not isinstance(labels, list):
        return []
    names: list[str] = []
    for label in labels:
        if isinstance(label, dict) and label.get("name"):
            names.append(str(label["name"]))
        elif isinstance(label, str):
            names.append(label)
    return names


def _assignees(assignees: Any) -> list[dict[str, str]]:
    if not isinstance(assignees, list):
        return []
    result: list[dict[str, str]] = []
    for assignee in assignees:
        if isinstance(assignee, dict) and assignee.get("login"):
            result.append({"login": str(assignee["login"])})
    return result


def _issue_to_snapshot(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "number": issue.get("number", 0),
        "title": issue.get("title", ""),
        "labels": _label_names(issue.get("labels")),
        "state": issue.get("state", "open"),
        "createdAt": issue.get("created_at"),
        "updatedAt": issue.get("updated_at"),
        "comments": issue.get("comments", 0),
        "assignees": _assignees(issue.get("assignees")),
        "url": issue.get("html_url", ""),
    }


def _pr_to_snapshot(pr: dict[str, Any], issue: dict[str, Any] | None = None) -> dict[str, Any]:
    issue = issue or {}
    return {
        "number": pr.get("number", 0),
        "title": pr.get("title", ""),
        "labels": _label_names(issue.get("labels") or pr.get("labels")),
        "state": pr.get("state", "open"),
        "isDraft": bool(pr.get("draft", False)),
        "additions": int(pr.get("additions") or 0),
        "deletions": int(pr.get("deletions") or 0),
        "changedFiles": int(pr.get("changed_files") or 0),
        "reviewDecision": "",
        "mergeStateStatus": str(pr.get("mergeable_state") or "").upper(),
        "statusCheckRollup": [],
        "createdAt": pr.get("created_at"),
        "updatedAt": pr.get("updated_at"),
        "url": pr.get("html_url", ""),
    }


def _latest_release(repository: str, token: str | None) -> dict[str, Any]:
    try:
        release = _request_json(f"{API_ROOT}/repos/{repository}/releases/latest", token)
    except GitHubApiError as exc:
        if "HTTP 404" in str(exc):
            return {"next_version": "", "target_date": "", "blockers": [], "notes": ["No latest release found."]}
        raise
    if not isinstance(release, dict):
        return {"next_version": "", "target_date": "", "blockers": [], "notes": []}
    tag = str(release.get("tag_name") or "")
    published = str(release.get("published_at") or "")
    note = f"Latest release is {tag} published at {published}." if tag else "Latest release metadata is incomplete."
    return {"next_version": "", "target_date": "", "blockers": [], "notes": [note]}


def fetch_repository_snapshot(
    repository: str,
    *,
    issue_limit: int = 100,
    pr_limit: int = 50,
    token: str | None = None,
) -> dict[str, Any]:
    repository = _validate_repository(repository)
    token = token or os.getenv("GITHUB_TOKEN")

    repo = _request_json(f"{API_ROOT}/repos/{repository}", token)
    if not isinstance(repo, dict):
        raise GitHubApiError("GitHub API returned unexpected repository payload.")

    issue_items = _paginate(f"/repos/{repository}/issues", token, issue_limit + pr_limit)
    issues = [item for item in issue_items if "pull_request" not in item][:issue_limit]
    pr_issue_map = {int(item.get("number", 0)): item for item in issue_items if "pull_request" in item}

    pull_items = _paginate(f"/repos/{repository}/pulls", token, pr_limit)
    pull_requests: list[dict[str, Any]] = []
    for pr in pull_items:
        number = int(pr.get("number", 0))
        detail_url = pr.get("url")
        detail = _request_json(str(detail_url), token) if detail_url else pr
        if not isinstance(detail, dict):
            detail = pr

        issue = pr_issue_map.get(number)
        if issue is None:
            issue_payload = _request_json(f"{API_ROOT}/repos/{repository}/issues/{number}", token)
            issue = issue_payload if isinstance(issue_payload, dict) else {}

        pull_requests.append(_pr_to_snapshot(detail, issue))

    return {
        "repository": {
            "name": repo.get("full_name") or repository,
            "default_branch": repo.get("default_branch") or "main",
            "description": repo.get("description") or "",
            "url": repo.get("html_url") or f"https://github.com/{repository}",
        },
        "issues": [_issue_to_snapshot(issue) for issue in issues],
        "pull_requests": pull_requests,
        "release": _latest_release(repository, token),
    }

