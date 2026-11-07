# Security (website repositories)

The owner's rules for every website, under `security-first.md`: no injection, every security policy the host allows, and nothing collected from visitors beyond the page views and click events the owner chose to measure.

## Pages and scripts

- Escape all data written into HTML. Never turn off a template engine's autoescape and never mark data as safe to skip escaping; in scripts, set text with `textContent`, not `innerHTML`, unless the HTML is built from escaped parts.
- No inline scripts and no inline event handlers (`onclick=` and the like); the only inline `<script>` allowed is a JSON-LD data block (`application/ld+json`). No inline `style="..."` attributes or `<style>` elements in pages either; use classes in the site's stylesheet (setting `element.style` from a script is fine). Scripts and styles live in the repository and load from the site itself, never from a CDN.
- No forms that send visitor input to a server, and no third-party relay services. A search box that only reads the site's own files is fine. Visitors contact the owner by `mailto:` only.
- No cookies and no `localStorage` for anything but the visitor's own settings (theme, language).
- Links that open in a new tab carry `rel="noopener noreferrer"`.

## Policies every page carries

Written once in the site's template or build tool, right after `<meta charset="utf-8">` (a `<meta>` policy covers only what comes after it), and checked on every page in CI. The repository's rule file names where.

- `<meta http-equiv="Content-Security-Policy">` with at least: `default-src 'none'`; `script-src`, `style-src`, `img-src` and `connect-src` listing only `'self'` and the services the site really uses (the measurement service the owner chose, an API a page calls); no `'unsafe-inline'`, `'unsafe-eval'`, `data:` or wildcard unless the rule file says why; `form-action 'none'` (or `'self'` with a search form); `base-uri 'none'`; `object-src 'none'`. Leave out `upgrade-insecure-requests`: with no `http:` source allowed it adds nothing, and WebKit applies it to `http://127.0.0.1`, which breaks the shared browser check. A new source changes the policy in the same pull request.
- `<meta name="referrer" content="no-referrer">`, or `strict-origin-when-cross-origin` where the measurement the owner chose needs it.
- Do not put `frame-ancestors`, `report-uri`, `report-to` or `sandbox` in the `<meta>` policy: browsers ignore them there.

## Headers, where the host can send them

GitHub Pages cannot set response headers. On a host that can (such as Cloudflare), send all of these, and until then list them in the repository's rule file as waiting:

- The same Content-Security-Policy as a header, plus `frame-ancestors 'none'`.
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`.
- `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.
- `Referrer-Policy` as above, and `Permissions-Policy` turning off every feature the site does not use (camera, microphone, geolocation, payment, USB and the rest).
- `Cross-Origin-Opener-Policy: same-origin` and `Cross-Origin-Resource-Policy: same-origin`.
- Trusted Types (`require-trusted-types-for 'script'`) once no script writes `innerHTML` with strings.

On GitHub Pages, keep Settings > Pages > "Enforce HTTPS" on.
