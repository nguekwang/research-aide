# Browsers (website repositories)

The owner's rule (2026-11-07): every website of the owner (the personal site, Lang Log and any later one) looks and works the same in every current browser, on phones and on computers. Internet Explorer is not supported.

## Which browsers

- Three engines: Chromium (Chrome, Edge, Opera, most Android browsers), Firefox (Gecko) and WebKit (Safari on Mac, and every browser on iPhone and iPad).
- Each at phone width (390 px, touch, no hover) and desktop width, in light and dark mode, and in every interface language, including right-to-left ones where the site has them.

## Writing CSS

- Use only features that all three engines support in their current release (check MDN's compatibility table or caniuse.com). Never rely on Chromium-only behaviour.
- A feature one engine lacks goes inside `@supports (...)`, after a plain rule that already looks right without it.
- For a new unit or value, write the widely supported value first and the new one second (`max-height: 70vh; max-height: 70dvh;`).
- Write the standard property next to any prefixed one, never a prefixed property alone.
- Long words and URLs wrap instead of widening the page (`overflow-wrap: anywhere` or `break-word` on `body`).
- Keep `color-scheme: light dark` on `:root` (or the site's theme root), so each engine draws scroll bars and controls in the right colours.
- Fix a difference once, in the site's shared stylesheet or template, not with a rule for one browser, page or language.

## Behaviour that differs between engines

Check each of these in Firefox and Safari whenever a change uses it:

- Prefixed properties: `-webkit-user-select` with `user-select`, `-webkit-backdrop-filter` with `backdrop-filter`, `-webkit-text-size-adjust` with `text-size-adjust`, `-webkit-mask` with `mask`, `-webkit-line-clamp` (needs `display: -webkit-box` and `-webkit-box-orient`), `-webkit-tap-highlight-color`.
- Touch: `touch-action` for panning and zooming (maps, trees), `overscroll-behavior`, pointer events rather than mouse events alone, `@media (hover: hover)` around hover-only effects (a tap must not leave a hover state stuck), and controls at least 44 px high. iOS Safari zooms into a text field whose font is under 16 px.
- Viewport height: `100vh` on iOS Safari includes the hidden toolbar; use `dvh`/`svh` after a `vh` fallback.
- Flex and grid: `min-width: 0` on flex and grid children that hold long text, `gap` with `flex-wrap`, `position: sticky` inside an element with `overflow`, and subgrid.
- Form controls and buttons: `appearance: none` before restyling, `<select>` and `<input type="search">` look different in each engine; set `font: inherit` and colours explicitly.
- Scroll bars: `scrollbar-width` and `scrollbar-color` (Firefox, Chromium) and `::-webkit-scrollbar` (Safari) are separate; a page must look right with either.
- Text: `text-box`, `text-wrap: balance`, `hyphens` (needs `lang` on the element), `font-variant-*` and vertical writing; fonts the visitor may not have need a fallback in `font-family`.
- SVG: `<use href>` to another file, sizing an `<svg>` without `width`/`height` attributes, and `transform-origin` on SVG elements.
- Scripts: `structuredClone`, `Array.prototype.at` and other recent APIs; check the engine support first. Clipboard and `history` APIs behave differently in Safari.
- Smooth scrolling, `scroll-snap`, `:has()`, container queries and `@layer` are fine in all three today, but keep a fallback when a missing feature would hide content.

## Checking

- Every website repository has a check in CI that opens its pages in Chromium, Firefox and WebKit at desktop and phone width on every pull request that can change what visitors see, and fails on sideways scrolling and on JavaScript or console errors. Use the shared workflow `nguekwang/research-aide/.github/workflows/browser-check.yml` (setup below), or a repository's own check that covers at least the same; the repository's rule file names it.
- Look at the screenshots the check uploads (the three engines side by side) for every visible change, and mention any difference between engines in the pull request description.
- Fix the CSS, template or script when the check fails; never loosen the check or skip an engine.

## Setting up the shared check

`.github/workflows/browsers.yml` in the website repository:

```yaml
name: browsers
on:
  pull_request:
  workflow_dispatch:
permissions:
  contents: read
jobs:
  browsers:
    uses: nguekwang/research-aide/.github/workflows/browser-check.yml@main
    with:
      build: <commands that build the site>
      site-dir: <build output directory>
      pages: |
        <one path per line, such as "/" for the top page or "/about/">
```

- Sites that pick the interface language from the browser also set `locales` (such as `en-US ja-JP`); each page is then opened once per browser language.
- List one page of every kind (top page, each kind of sub-page, every interface language, a right-to-left page if the site has them); the check opens each in every engine, at both widths and in both colour schemes.
