from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import DEFAULT_CONFIG_TEXT, load_config
from .github_api import fetch_repository_snapshot
from .loader import load_snapshot
from .report import to_codex_brief, to_json, to_markdown
from .rules import analyze_snapshot


def _write_or_print(text: str, output: Path | None) -> None:
    if output is None:
        print(text, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")


def _build_report(args: argparse.Namespace) -> object:
    config = load_config(args.config)
    snapshot = load_snapshot(args.snapshot)
    return analyze_snapshot(snapshot, config)


def analyze_command(args: argparse.Namespace) -> int:
    report = _build_report(args)
    if args.format == "json":
        text = to_json(report)
    else:
        text = to_markdown(report)
    _write_or_print(text, args.output)
    return 0


def brief_command(args: argparse.Namespace) -> int:
    report = _build_report(args)
    _write_or_print(to_codex_brief(report), args.output)
    return 0


def init_config_command(args: argparse.Namespace) -> int:
    if args.output.exists() and not args.force:
        raise SystemExit(f"{args.output} already exists. Pass --force to overwrite.")
    _write_or_print(DEFAULT_CONFIG_TEXT, args.output)
    return 0


def snapshot_github_command(args: argparse.Namespace) -> int:
    snapshot = fetch_repository_snapshot(
        args.repository,
        issue_limit=args.issues,
        pr_limit=args.prs,
        token=args.token,
    )
    text = json.dumps(snapshot, indent=2, sort_keys=True) + "\n"
    _write_or_print(text, args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="maintainer-radar",
        description="Analyze open-source maintenance queues and create Codex-ready review briefs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Generate a maintainer triage report.")
    analyze.add_argument("snapshot", type=Path, help="Path to a GitHub metadata snapshot JSON file.")
    analyze.add_argument("--config", type=Path, default=None, help="Path to .maintainer-radar.toml.")
    analyze.add_argument("--format", choices=("markdown", "json"), default="markdown")
    analyze.add_argument("--output", type=Path, default=None, help="Write report to this file.")
    analyze.set_defaults(func=analyze_command)

    brief = subparsers.add_parser("brief", help="Generate a Codex-ready maintenance brief.")
    brief.add_argument("snapshot", type=Path, help="Path to a GitHub metadata snapshot JSON file.")
    brief.add_argument("--config", type=Path, default=None, help="Path to .maintainer-radar.toml.")
    brief.add_argument("--output", type=Path, default=None, help="Write brief to this file.")
    brief.set_defaults(func=brief_command)

    init_config = subparsers.add_parser("init-config", help="Write a starter configuration file.")
    init_config.add_argument("--output", type=Path, default=Path(".maintainer-radar.toml"))
    init_config.add_argument("--force", action="store_true", help="Overwrite an existing config.")
    init_config.set_defaults(func=init_config_command)

    snapshot = subparsers.add_parser("snapshot-github", help="Fetch a public GitHub repository snapshot.")
    snapshot.add_argument("repository", help="Repository in owner/name form.")
    snapshot.add_argument("--issues", type=int, default=100, help="Maximum open issues to include.")
    snapshot.add_argument("--prs", type=int, default=50, help="Maximum open pull requests to include.")
    snapshot.add_argument("--token", default=None, help="GitHub token. Defaults to GITHUB_TOKEN.")
    snapshot.add_argument("--output", type=Path, default=None, help="Write snapshot JSON to this file.")
    snapshot.set_defaults(func=snapshot_github_command)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
