# Instagram Automation

Multi-account Instagram content automation orchestrated by GitHub Actions.

## Status

Phase 0 foundation is being initialized. Meta authentication, media generation, publishing, scheduling, and production integrations are not implemented yet.

## Principles

- Isolate configuration and publishing state per Instagram account.
- Use the official Meta Instagram API, not browser automation.
- Never commit access tokens, app secrets, or encryption keys.
- Make workflows idempotent and safe to rerun.
- Treat GitHub Actions schedules as approximate; always check whether work is due.
- Never silently use paid APIs or GPU providers.
- A failure for one account must not block other accounts.

## Development

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

## Planned phases

1. Foundation: schemas, config validation, CI, logging, storage contracts.
2. Meta account connection and encrypted token lifecycle.
3. Single-image publishing with processing checks and duplicate protection.
4. Carousel publishing and media composition.
5. Image provider abstraction and deterministic fallback.
6. Content research, generation, approval, and scheduling.
7. Monitoring, recovery, backups, and runbooks.

Do not enable real publishing until integration tests and account-level safety checks pass.
