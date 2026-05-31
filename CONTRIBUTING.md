# Contributing

Thanks for helping maintainers spend less time sorting queues and more time making good decisions.

## Development Setup

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest
```

On macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest
```

## Contribution Guidelines

- Keep the default path local-first and deterministic.
- Do not add network calls without an explicit flag and tests.
- Treat AI-generated output as a draft for maintainers, not as an authority.
- Add or update tests for rules, report formatting, and CLI behavior.
- Keep issue and PR labels configurable because every project has its own maintenance language.

## Good First Contributions

- Add snapshot examples from different project types.
- Improve default label mappings.
- Add a new report format.
- Expand release readiness checks.
- Improve docs for maintainers who are new to automation.

