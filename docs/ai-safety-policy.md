# AI Safety Policy

Maintainer Radar is useful without AI. AI integrations must remain optional and auditable.

## Default Behavior

- No network calls.
- No external AI API calls.
- No secret scanning bypass.
- No automatic issue closure, PR approval, or merge.

## Allowed AI Use

With explicit maintainer opt-in, AI may help:

- Cluster duplicate public issues.
- Draft maintainer replies.
- Produce focused PR review checklists.
- Summarize public release notes.
- Suggest test gaps from public metadata and diffs.

## Disallowed AI Use

- Sending secrets, tokens, private advisory text, or private repository content.
- Treating generated text as authoritative.
- Auto-approving or auto-merging PRs.
- Posting generated comments without maintainer review.

## Prompt Review

Future AI features should expose the prompt payload before submission and support a dry-run mode.

