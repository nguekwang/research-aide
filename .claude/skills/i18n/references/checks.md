# Checks

1. Run the site's language check (`references/sites.md`); it fails when a language lacks a key or uses a placeholder its English text lacks. Then the site's other checks before pushing (its `git-and-prs.md` or `code-quality.md`).
2. Look at the page in English, Japanese and one right-to-left language (Arabic), at phone width (390 px) and desktop, light and dark (`web-browsers.md`):
   - Japanese text uses Japanese glyphs and has no letter-spacing.
   - Arabic and Persian read right to left, with the layout mirrored (logical CSS properties only).
   - Long words (German, Russian, Vietnamese) wrap instead of widening the page.
3. Look at the screenshots of the browser check (Chromium, Firefox and WebKit; `browser-check.md`) and, on the personal site, of the `screenshots` workflow.
