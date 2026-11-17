# Security Policy

## Reporting

Do not open public issues containing access tokens, app secrets, encryption keys, personal data, or unpublished account information. Report security vulnerabilities privately to the repository owner.

## Secret handling

- Never commit Meta access tokens, app secrets, encryption keys, or OAuth client secrets.
- Never print credentials or authorization headers in logs.
- Store credentials in GitHub Actions secrets or an encrypted private state store.
- Do not expose secrets to workflows triggered by untrusted pull requests.
- Use least-privilege GitHub workflow permissions.
- Rotate credentials immediately if exposure is suspected.

## Publishing safety

Real publishing must remain disabled until account authorization, approval, idempotency, quota checks, and uncertain-result reconciliation are implemented and tested.
