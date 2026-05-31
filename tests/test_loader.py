from pathlib import Path
import unittest

from maintainer_radar.loader import load_snapshot


ROOT = Path(__file__).resolve().parents[1]


class LoaderTests(unittest.TestCase):
    def test_loads_example_snapshot(self) -> None:
        snapshot = load_snapshot(ROOT / "examples" / "github-snapshot.json")

        self.assertEqual(snapshot.repository.name, "example/critical-oss-project")
        self.assertEqual(len(snapshot.issues), 3)
        self.assertEqual(len(snapshot.pull_requests), 2)
        self.assertEqual(snapshot.issues[0].labels, ("security", "bug"))
        self.assertEqual(snapshot.pull_requests[0].checks, ("failure",))


if __name__ == "__main__":
    unittest.main()

