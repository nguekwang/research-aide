# Security first

The owner's rule for every repository and every task (2026-11-07): security comes first.

- When security and something else pull apart (convenience, speed, looks, less work), choose security. When unsure whether something is safe enough, take the safer option and tell the owner what it costs.
- Turn on every protection the platform allows, by default, in new work and whenever existing work is touched. Leaving one off needs a reason written in the repository's rule file (for example "GitHub Pages cannot send headers").
- A repository's own rules may be stricter than the shared ones, never looser. A conflict between security and another recorded rule goes to the owner as a question.
- Never weaken, skip or turn off a security check, policy or setting to make something work or pass CI; fix the cause instead.
- Each repository's rule file lists what it has and what it cannot have yet (and why), so the gap is closed when the platform allows it.

## Everywhere

- No secrets in repositories, logs, pull requests or chat. Secrets live in GitHub Actions secrets or the host's secret store.
- GitHub Actions: `permissions` set per workflow and job, read-only unless a job must write; no `pull_request_target` that checks out pull request code; pin third-party actions to a release tag or commit.
- Dependencies: as few as possible, from the official registry, with Dependabot alerts on.
- Collect the minimum data. No visitor data beyond what the owner chose to measure (`web-security.md`).
- Any later login or payment: no passwords (single sign-on or passkeys only), two-factor authentication required, and card data handled only by the payment provider.

Websites add the rules in `web-security.md`.
