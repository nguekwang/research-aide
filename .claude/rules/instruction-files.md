# Instruction files

Rules for the files Claude reads as instructions: `CLAUDE.md` and everything in `.claude/` (rules, skills, settings), in every repository.

## What goes where

- `CLAUDE.md`: what the repository is, the principles behind its rules, and a map of its rule files. No commands, file-by-file details or one-off decisions. Keep it under about 40 lines.
- `.claude/rules/<topic>.md` without `paths`: rules for every task in that repository. Loaded at the start of every session.
- `.claude/rules/<topic>.md` with `paths`: rules about one directory or one kind of file. Loaded only when Claude reads or edits a matching file. Name the file after the directory (`data.md`), or after the topic when it spans several directories.
- `.claude/skills/<name>/SKILL.md`: a procedure of several steps that is only needed for some tasks.
  Keep `SKILL.md` short, because it is loaded whole every time the skill runs: when to use it, the steps that must always be followed, and which file under `references/` to read at which step. Move details, examples and rules for only some cases into `references/<topic>.md`, without changing their wording (the owner's rule, 2026-11-24).
- Values a program reads (settings, lists, numbers) go in data or config files, not in prose. A rule file may point to them.
- A rule that applies to more than one repository goes in the shared `research-aide` repository, not in each repository. Each repository's `CLAUDE.md` imports it with `@../research-aide/.claude/common.md` (start from `templates/CLAUDE.md`). Claude Code skips an import from outside the repository until it is approved, so the same `CLAUDE.md` also tells Claude to read the shared files itself when they are missing from its context.
- A procedure that more than one repository follows goes in `research-aide/.claude/skills/<name>/`, laid out like any skill. Claude Code loads skills only from the repository it runs in, so each repository that uses a shared skill names it in its `CLAUDE.md` map by path (`../research-aide/.claude/skills/<name>/SKILL.md`), and Claude reads that file before the task.

## Path-scoped rules

```markdown
---
paths:
  - "data/**"
---
```

- `paths` is the only frontmatter field Claude Code reads. Patterns are globs relative to the repository root.
- A path-scoped rule is not loaded until a matching file is opened. If Claude must know a rule before it touches any file (for example, before planning), put it in an always-loaded file instead.
- `paths` does not work in files reached through an `@` import, so shared rules are always-loaded rules.

## How to write them

- One topic per file. Each rule is stated in one place only; elsewhere, point to it instead of repeating it.
- English, short imperative bullets. Add the reason when it is not obvious.
- Name real files, keys and commands so the rule can be checked against the code. When the code changes, update the rule in the same pull request.
- No private information (see `publishing.md`).
- Split a rule file when it grows past about 60 lines.
- When adding, renaming or removing a rule file, update the map in that repository's `CLAUDE.md`.
- When a decision is made, record it in the right rule file in the same pull request.
