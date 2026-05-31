# Security Policy

## Supported Versions

Maintainer Radar is pre-1.0. Security fixes are applied to the `main` branch until a stable release line exists.

## Reporting A Vulnerability

Please do not open public issues for vulnerabilities that could expose tokens, private repository data, or unsafe prompt construction. Email the maintainer address listed on the repository profile, or open a minimal private advisory if GitHub security advisories are enabled.

Expected response:

- Acknowledgement within 7 days.
- Initial triage within 14 days.
- Public advisory or release note once a fix is available.

## Data Handling

The default CLI only reads local JSON and TOML files. It does not call external services.

Future integrations must follow these rules:

- Do not send secrets, tokens, private advisory details, or private repository content to AI APIs.
- Require explicit opt-in for network calls.
- Print or save the exact prompt payload before submission when possible.
- Keep AI output as maintainer-reviewed suggestions.

