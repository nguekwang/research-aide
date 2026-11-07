# CLAUDE.md

Shared instructions for every repository of Matsuura Yoshihiro (the owner): the website, research tools and papers. Other repositories import them. Apart from shared GitHub Actions workflows (`.github/workflows/`) and the scripts they run (`tools/`), this repository holds no code.

## Principles

- **Security first.** When security and anything else pull apart, security wins; every protection the platform allows is on by default.
- **One rule, one place.** A rule that applies to more than one repository lives here, not in each repository. A repository keeps only its own rules.
- **The owner decides and reviews.** Every change, here too, goes through a pull request that the owner merges.
- **Nothing private.** These files are read in public repositories' sessions; write rules, never private facts.

## How other repositories use this

- Clone this repository next to the other one (same parent folder), and add one line to that repository's `CLAUDE.md`: `@../research-aide/.claude/common.md`.
- `templates/CLAUDE.md` is the starting `CLAUDE.md` for a new repository. Copy it as it is, including the fallback line that tells Claude to read the shared files itself if the import was skipped.
- In claude.ai cloud sessions, add `research-aide` to the project or environment so it is cloned next to the other repositories.

## Where the rules are

`.claude/common.md` imports every shared rule file in `.claude/rules/`:

- `instruction-files.md`: how CLAUDE.md and rule files are organized.
- `working-with-the-owner.md`: starting a task, asking questions, reporting.
- `security-first.md`: security comes first in every repository; secrets, Actions permissions, dependencies.
- `git-and-prs.md`: branches, conflicts, checks, pull requests.
- `english-first.md`: which language each part of a repository is written in.
- `publishing.md`: what may be published.
- `titles.md`: the ` by yoshi` suffix on page titles.
- `profile-links.md`: the `?ref=` parameter on links to the personal site.
- `pr-previews.md`: a preview of the site on every pull request in website repositories (shared workflow `.github/workflows/pages-with-previews.yml`).
- `languages.md`: every language shows the same thing; notation follows each language's official documents.
- `web-browsers.md`: websites work in Chromium, Firefox and WebKit (Safari) on phones and computers (shared workflow `.github/workflows/browser-check.yml`).
- `web-security.md`: escaping, no inline scripts or styles, the policies every page carries, the headers to send where the host allows, no forms that send visitor data.
