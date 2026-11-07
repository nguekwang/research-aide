# Readable code

The owner's rule (2026-11-07), for every repository and every language (Python, JavaScript, CSS, HTML, shell, Typst): code must read clearly, and one value must never be defined twice. Two copies drift apart, and then two parts of the program follow different values (the case that started this rule: a Lang Log animation length written once in CSS and again in JavaScript).

## One value, one place

- Every value that has a meaning (a length, a duration, a count, a colour, a URL, a file name, a list of layers or languages) is written once, as a named constant, a CSS custom property or a config entry. Everything else reads it from there.
- Across languages, the second language reads the first; it never keeps a copy:
  - CSS to JavaScript: a custom property on `:root`, read with `getComputedStyle(...).getPropertyValue('--name')`.
  - A generator to a page script: an attribute (`data-*`) or the markup it writes, read by the script.
  - Between scripts: import a shared module (one file for names, paths, links), or read the constant from the file that defines it.
  - Hand-written files that must hold the same text as generated ones: a `--write` mode that writes it from the source and a `--check` mode in CI.
- When a copy cannot be avoided (CSS `@media` widths, a file opened on its own where the stylesheet does not apply), say at the copy where the source is, and list it in the repository's check as a known exception with the reason.
- No fallback defaults that repeat a value from elsewhere (`attr || 30`). If the value is missing, fail or skip visibly.
- Values a rule can compute are built by CI (`generated-values.md`); this rule covers the hand-written ones.

## Names and layout

- Name a value by what it means, not by what it is: `--accent`, not `--c-386e6d`; `STATS_DURATION`, not `D`. Put the unit in the name when it is a number (`GLIDE_MS`, `TAP_PX`).
- No unexplained literals in logic. A number other than 0, 1 or an obvious index becomes a named constant with a comment saying the unit and why that value.
- Do not copy a block of code; when the same steps appear twice, make one function.
- One statement per line, laid out by the repository's formatter. Never hand-minify source files.
- Comments say why, and point to the source of any value read from elsewhere.

## Checks

- Every repository runs a formatter and a linter in CI (for example Prettier and ESLint for JavaScript and CSS, Ruff for Python), and fails on their errors.
- Website and tool repositories also run a check that fails on copies of shared values: a list of each value and its one source file, colour literals outside the colour tokens, and constants with the same name and value in two files. The repository's rule file names the check and where each shared value lives.
- When adding a shared value, add it to that check in the same pull request. Never silence the check for a new copy; read the value from its source instead.
