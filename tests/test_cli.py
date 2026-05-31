from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from maintainer_radar.cli import main


ROOT = Path(__file__).resolve().parents[1]


class CliTests(unittest.TestCase):
    def test_analyze_writes_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.md"
            result = main(["analyze", str(ROOT / "examples" / "github-snapshot.json"), "--output", str(output)])

            self.assertEqual(result, 0)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Maintainer Radar Report", text)
            self.assertIn("Possible token leak", text)

    def test_brief_writes_codex_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "brief.md"
            result = main(["brief", str(ROOT / "examples" / "github-snapshot.json"), "--output", str(output)])

            self.assertEqual(result, 0)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Codex Maintenance Brief", text)
            self.assertIn("Requested Codex Work", text)

    def test_snapshot_github_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "snapshot.json"
            snapshot = {
                "repository": {"name": "example/project"},
                "issues": [],
                "pull_requests": [],
                "release": {"blockers": [], "notes": []},
            }
            with patch("maintainer_radar.cli.fetch_repository_snapshot", return_value=snapshot):
                result = main(["snapshot-github", "example/project", "--output", str(output)])

            self.assertEqual(result, 0)
            self.assertIn('"example/project"', output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
