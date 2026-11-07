# Values computed by CI

The owner's rule (2026-11-07), for every repository: anything that a rule can compute from data the repository already has is computed by a script in CI, never written by hand and never written out by an AI.

## What counts

- Counts, totals and statistics (for example "344 records", "8,304 languages", "21 languages").
- Lists, indexes, tables of contents, sitemaps and summaries built from other files.
- Values derived from another value (a host taken from a URL, a writing direction taken from a language code, a date taken from git).
- Generated files (built HTML, JSON, XML, OPML, archives of data built from source files).

## How

- Write the source value once, in a data or config file, and let a build script derive the rest. Text that shows a computed value holds a placeholder (such as `{count}`) that the build fills in; translations keep the placeholder.
- Run the script in the repository's CI build, so the value is recomputed on every pull request and every deployment. Do not commit what CI builds; list it in `.gitignore`.
- When a value cannot be derived yet (for example the source is in another repository or behind a login), keep it in one data file with a comment that says where it comes from, and add a CI check that fails when it no longer matches, where one is possible.
- A check that compares a computed value with a fixed expected number (such as a snapshot size) is fine, as long as the number shown to visitors comes from the data.
- Claude never types a count or a derived value into a page, a translation or a data file. When one is needed, add or extend the script instead.
- Human decisions stay hand-written: wording, choices of the owner, the date a person checked something, and data quoted from a source.

## Checking

- When a repository is set up or its build changes, look for numbers and derived values written by hand (in page text, translations, templates and committed generated files) and move them into the build. Each repository's rule file names its build script.
