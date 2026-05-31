from datetime import datetime, timezone
from pathlib import Path
import unittest

from maintainer_radar.config import RadarConfig
from maintainer_radar.gate import evaluate_gate, gate_to_json, gate_to_markdown
from maintainer_radar.loader import load_snapshot
from maintainer_radar.rules import analyze_snapshot


ROOT = Path(__file__).resolve().parents[1]


class GateTests(unittest.TestCase):
    def test_gate_fails_blocked_security_snapshot(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")
        report = analyze_snapshot(snapshot, RadarConfig(), now=datetime(2026, 6, 1, tzinfo=timezone.utc))

        result = evaluate_gate(report)

        self.assertFalse(result.passed)
        self.assertIn("release status is blocked", result.failures)
        self.assertTrue(any("P0 issue" in failure for failure in result.failures))

    def test_gate_report_formats(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")
        report = analyze_snapshot(snapshot, RadarConfig(), now=datetime(2026, 6, 1, tzinfo=timezone.utc))
        result = evaluate_gate(report)

        self.assertIn("Quality Gate", gate_to_markdown(result, report))
        self.assertIn('"status": "failed"', gate_to_json(result))


if __name__ == "__main__":
    unittest.main()

