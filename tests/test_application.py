from datetime import datetime, timezone
from pathlib import Path
import unittest

from maintainer_radar.application import (
    API_CREDIT_DRAFT,
    OPTIONAL_NOTE_DRAFT,
    QUALIFICATION_DRAFT,
    build_application_pack,
    character_count,
)
from maintainer_radar.config import RadarConfig
from maintainer_radar.loader import load_snapshot
from maintainer_radar.rules import analyze_snapshot


ROOT = Path(__file__).resolve().parents[1]


class ApplicationPackTests(unittest.TestCase):
    def test_draft_answers_fit_form_limits(self) -> None:
        self.assertLessEqual(character_count(QUALIFICATION_DRAFT), 500)
        self.assertLessEqual(character_count(API_CREDIT_DRAFT), 500)
        self.assertLessEqual(character_count(OPTIONAL_NOTE_DRAFT), 500)

    def test_application_pack_includes_readiness_and_missing_evidence(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")
        report = analyze_snapshot(snapshot, RadarConfig(), now=datetime(2026, 6, 1, tzinfo=timezone.utc))

        text = build_application_pack(
            snapshot,
            report,
            repository_url="https://github.com/example/critical-oss-project",
        )

        self.assertIn("Readiness Checklist", text)
        self.assertIn("[x] Public GitHub repository URL", text)
        self.assertIn("[ ] External adoption evidence", text)
        self.assertIn("High-risk pull requests detected: 1", text)


if __name__ == "__main__":
    unittest.main()

