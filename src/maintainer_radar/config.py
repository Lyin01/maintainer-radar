from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class LabelConfig:
    security: tuple[str, ...] = ("security", "vulnerability", "cve", "auth", "permissions")
    release_blocker: tuple[str, ...] = ("release-blocker", "regression", "breaking-change")
    bug: tuple[str, ...] = ("bug", "defect", "crash")
    needs_reproduction: tuple[str, ...] = ("needs-repro", "needs-reproduction", "cannot-reproduce")
    documentation: tuple[str, ...] = ("docs", "documentation")
    dependency: tuple[str, ...] = ("dependencies", "deps")


@dataclass(frozen=True)
class ThresholdConfig:
    stale_issue_days: int = 60
    stale_pr_days: int = 21
    large_pr_files: int = 15
    large_pr_lines: int = 600


@dataclass(frozen=True)
class RadarConfig:
    labels: LabelConfig = field(default_factory=LabelConfig)
    thresholds: ThresholdConfig = field(default_factory=ThresholdConfig)


DEFAULT_CONFIG_TEXT = """[labels]
security = ["security", "vulnerability", "cve", "auth", "permissions"]
release_blocker = ["release-blocker", "regression", "breaking-change"]
bug = ["bug", "defect", "crash"]
needs_reproduction = ["needs-repro", "needs-reproduction", "cannot-reproduce"]
documentation = ["docs", "documentation"]
dependency = ["dependencies", "deps"]

[thresholds]
stale_issue_days = 60
stale_pr_days = 21
large_pr_files = 15
large_pr_lines = 600
"""


def _tuple_from_table(table: dict[str, object], key: str, fallback: tuple[str, ...]) -> tuple[str, ...]:
    value = table.get(key)
    if not isinstance(value, list):
        return fallback
    return tuple(str(item).strip().lower() for item in value if str(item).strip())


def _int_from_table(table: dict[str, object], key: str, fallback: int) -> int:
    value = table.get(key)
    if isinstance(value, int) and value >= 0:
        return value
    return fallback


def load_config(path: Path | None) -> RadarConfig:
    if path is None or not path.exists():
        return RadarConfig()

    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    label_table = raw.get("labels", {})
    threshold_table = raw.get("thresholds", {})
    if not isinstance(label_table, dict):
        label_table = {}
    if not isinstance(threshold_table, dict):
        threshold_table = {}

    default_labels = LabelConfig()
    default_thresholds = ThresholdConfig()
    return RadarConfig(
        labels=LabelConfig(
            security=_tuple_from_table(label_table, "security", default_labels.security),
            release_blocker=_tuple_from_table(
                label_table,
                "release_blocker",
                default_labels.release_blocker,
            ),
            bug=_tuple_from_table(label_table, "bug", default_labels.bug),
            needs_reproduction=_tuple_from_table(
                label_table,
                "needs_reproduction",
                default_labels.needs_reproduction,
            ),
            documentation=_tuple_from_table(label_table, "documentation", default_labels.documentation),
            dependency=_tuple_from_table(label_table, "dependency", default_labels.dependency),
        ),
        thresholds=ThresholdConfig(
            stale_issue_days=_int_from_table(
                threshold_table,
                "stale_issue_days",
                default_thresholds.stale_issue_days,
            ),
            stale_pr_days=_int_from_table(threshold_table, "stale_pr_days", default_thresholds.stale_pr_days),
            large_pr_files=_int_from_table(threshold_table, "large_pr_files", default_thresholds.large_pr_files),
            large_pr_lines=_int_from_table(threshold_table, "large_pr_lines", default_thresholds.large_pr_lines),
        ),
    )

