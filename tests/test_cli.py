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

    def test_apply_pack_writes_application_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "application-pack.md"
            result = main(
                [
                    "apply-pack",
                    str(ROOT / "examples" / "github-snapshot.json"),
                    "--repository-url",
                    "https://github.com/example/critical-oss-project",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(result, 0)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Codex For Open Source Application Pack", text)
            self.assertIn("Character count: 336 / 500", text)
            self.assertIn("P0/P1 issues detected: 2", text)

    def test_gate_returns_failure_for_blocked_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "gate.md"
            result = main(["gate", str(ROOT / "examples" / "github-snapshot.json"), "--output", str(output)])

            self.assertEqual(result, 1)
            self.assertIn("Status: **failed**", output.read_text(encoding="utf-8"))

    def test_gate_warn_only_returns_success(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "gate.md"
            result = main(
                [
                    "gate",
                    str(ROOT / "examples" / "github-snapshot.json"),
                    "--warn-only",
                    "--output",
                    str(output),
                ]
            )

            self.assertEqual(result, 0)
            self.assertIn("Status: **failed**", output.read_text(encoding="utf-8"))

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
