from pathlib import Path
import tempfile
import unittest

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


if __name__ == "__main__":
    unittest.main()

