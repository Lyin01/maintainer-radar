from datetime import datetime, timezone
from pathlib import Path
import unittest

from maintainer_radar.config import RadarConfig
from maintainer_radar.loader import load_snapshot
from maintainer_radar.rules import analyze_snapshot

ROOT = Path(__file__).resolve().parents[1]


class RulesTests(unittest.TestCase):
    def test_security_issue_is_p0_and_blocks_release(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")
        report = analyze_snapshot(snapshot, RadarConfig(), now=datetime(2026, 6, 1, tzinfo=timezone.utc))

        self.assertEqual(report.issues[0].number, 41)
        self.assertEqual(report.issues[0].priority, "P0")
        self.assertEqual(report.release.status, "blocked")

    def test_large_security_pr_is_critical(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")
        report = analyze_snapshot(snapshot, RadarConfig(), now=datetime(2026, 6, 1, tzinfo=timezone.utc))

        risky_pr = report.pull_requests[0]
        self.assertEqual(risky_pr.number, 88)
        self.assertEqual(risky_pr.risk, "critical")
        self.assertGreaterEqual(risky_pr.score, 75)


if __name__ == "__main__":
    unittest.main()
