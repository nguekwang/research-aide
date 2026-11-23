# Browser check (website repositories)

How every website repository checks the rules in `web-browsers.md`.

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
- The check's server answers a missing path with the site's `404.html` (status 404), as GitHub Pages does. A page the site serves through `404.html` on purpose (such as a search page at `/q=<terms>`) is listed as `404:/q=<terms>`: it must answer 404, and that answer is not counted as a problem. List the page itself, not a link that redirects to it.
