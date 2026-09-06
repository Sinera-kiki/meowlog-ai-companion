# Security

## Reporting

Do not open public issues containing API keys, passwords, personal chat records, or deployment credentials. Revoke exposed keys immediately and report the issue privately to the repository owner.

## Demo security model

The public demo uses a random browser guest ID for lightweight data isolation. It is suitable for portfolio demonstration, not for sensitive production data. A production release should use authenticated accounts, signed sessions, rate limiting, abuse prevention and encrypted backups.
