# Security (website repositories)

The owner's rules for every website: no injection, and nothing collected from visitors beyond the page views and click events the owner chose to measure.

- Escape all data written into HTML. Never turn off a template engine's autoescape and never mark data as safe to skip escaping; in scripts, set text with `textContent`, not `innerHTML`, unless the HTML is built from escaped parts.
- No inline scripts and no inline event handlers (`onclick=` and the like); the only inline `<script>` allowed is a JSON-LD data block (`application/ld+json`). Scripts live in the repository and load from the site itself, never from a CDN.
- A Content-Security-Policy (`<meta http-equiv="Content-Security-Policy">`) allows only the site itself and the measurement service the owner chose, and keeps `default-src 'none'`, `form-action 'none'` (or `'self'` when the site has a search form), `base-uri 'none'` and `object-src 'none'`. A repository's rule file names where the policy is written; a new script source changes the policy in the same pull request.
- No forms that send visitor input to a server, and no third-party relay services. A search box that only reads the site's own files is fine. Visitors contact the owner by `mailto:` only.
- No cookies and no `localStorage` for anything but the visitor's own settings (theme, language).
- Links that open in a new tab carry `rel="noopener noreferrer"`.
