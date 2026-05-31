from pathlib import Path
import tempfile
import unittest

from maintainer_radar.config import DEFAULT_CONFIG_TEXT, load_config


class ConfigTests(unittest.TestCase):
    def test_loads_custom_threshold(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".maintainer-radar.toml"
            path.write_text(DEFAULT_CONFIG_TEXT.replace("stale_pr_days = 21", "stale_pr_days = 10"), encoding="utf-8")

            config = load_config(path)

            self.assertEqual(config.thresholds.stale_pr_days, 10)


if __name__ == "__main__":
    unittest.main()

