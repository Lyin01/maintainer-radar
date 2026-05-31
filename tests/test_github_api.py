import unittest
from unittest.mock import patch

from maintainer_radar.github_api import GitHubApiError, fetch_repository_snapshot


class GitHubApiTests(unittest.TestCase):
    def test_rejects_invalid_repository_name(self) -> None:
        with self.assertRaises(GitHubApiError):
            fetch_repository_snapshot("not-a-repo")

    def test_fetches_repository_snapshot_from_api_payloads(self) -> None:
        payloads = {
            "https://api.github.com/repos/example/project": {
                "full_name": "example/project",
                "default_branch": "main",
                "description": "Example",
                "html_url": "https://github.com/example/project",
            },
            "https://api.github.com/repos/example/project/issues?state=open&per_page=3&page=1": [
                {
                    "number": 1,
                    "title": "Bug",
                    "state": "open",
                    "labels": [{"name": "bug"}],
                    "created_at": "2026-05-01T00:00:00Z",
                    "updated_at": "2026-05-02T00:00:00Z",
                    "comments": 2,
                    "assignees": [{"login": "maintainer"}],
                    "html_url": "https://github.com/example/project/issues/1",
                },
                {
                    "number": 2,
                    "title": "Security PR",
                    "state": "open",
                    "labels": [{"name": "security"}],
                    "pull_request": {},
                    "created_at": "2026-05-03T00:00:00Z",
                    "updated_at": "2026-05-04T00:00:00Z",
                    "comments": 1,
                    "assignees": [],
                    "html_url": "https://github.com/example/project/pull/2",
                },
            ],
            "https://api.github.com/repos/example/project/pulls?state=open&per_page=1&page=1": [
                {
                    "number": 2,
                    "url": "https://api.github.com/repos/example/project/pulls/2",
                }
            ],
            "https://api.github.com/repos/example/project/pulls/2": {
                "number": 2,
                "title": "Security PR",
                "state": "open",
                "draft": False,
                "additions": 20,
                "deletions": 5,
                "changed_files": 3,
                "mergeable_state": "blocked",
                "created_at": "2026-05-03T00:00:00Z",
                "updated_at": "2026-05-04T00:00:00Z",
                "html_url": "https://github.com/example/project/pull/2",
            },
            "https://api.github.com/repos/example/project/releases/latest": {
                "tag_name": "v1.0.0",
                "published_at": "2026-05-05T00:00:00Z",
            },
        }

        with patch("maintainer_radar.github_api._request_json", side_effect=lambda url, token=None: payloads[url]):
            snapshot = fetch_repository_snapshot("example/project", issue_limit=2, pr_limit=1)

        self.assertEqual(snapshot["repository"]["name"], "example/project")
        self.assertEqual(snapshot["issues"][0]["labels"], ["bug"])
        self.assertEqual(snapshot["pull_requests"][0]["labels"], ["security"])
        self.assertEqual(snapshot["pull_requests"][0]["changedFiles"], 3)
        self.assertIn("v1.0.0", snapshot["release"]["notes"][0])


if __name__ == "__main__":
    unittest.main()

