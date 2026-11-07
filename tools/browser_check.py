#!/usr/bin/env python3
"""Open a built website in Chromium, Firefox and WebKit (Safari) and fail on layout or script errors.

Run by the shared workflow .github/workflows/browser-check.yml; rule: .claude/rules/web-browsers.md.

Serves the built site from a local web server and opens each listed page in each engine at
desktop width (1280 px) and phone width (390 px, touch), in light and in dark colour scheme,
and once for each browser language in --locales (for sites that pick the interface language
from the browser).
A page fails if it:
  - scrolls sideways (is wider than the window),
  - raises a JavaScript error or logs a console error (Content-Security-Policy violations
    included),
  - requests a file from the site that does not exist (HTTP 400 or more).

Requests that leave the local server (measurement and other third parties) get an empty answer,
so the check never counts as a visit.

Writes to --out:
  <engine>-<page>-<view>.png    the top of each page in one engine
  compare-<page>-<view>.png     the three engines side by side
  summary.md                    the problems found, as a Markdown table

Usage:
  python3 browser_check.py --site dist --out browser-check --pages "" about/ ja/ [--locales en-US ja-JP]
  (an empty string is the top page). BROWSER_CHECK_CHROMIUM may name a local Chromium binary.
"""
import argparse, functools, http.server, os, re, sys, threading

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ENGINES = ["chromium", "firefox", "webkit"]
SIZES = {
    "desktop": {"viewport": {"width": 1280, "height": 800}},
    # A phone: narrow, touch, no hover. Firefox has no mobile emulation in Playwright, so
    # is_mobile is passed only to the engines that support it (see context_options()).
    "mobile": {"viewport": {"width": 390, "height": 844}, "has_touch": True, "is_mobile": True},
}
SCHEMES = ["light", "dark"]

# Measured in the page. `width` is the window width asked for: a phone browser may widen its
# layout to fit content that is too wide and zoom out, so window.innerWidth cannot be trusted.
MEASURE = """(width) => {
  const doc = document.documentElement;
  const wide = Math.max(doc.scrollWidth, document.body ? document.body.scrollWidth : 0, window.innerWidth);
  return wide > width + 1
    ? [`page is ${wide}px wide in a ${width}px window (scrolls sideways or zooms out)`]
    : [];
}"""


def serve(directory):
    """Serve `directory` on a free local port in a background thread; return its base URL."""
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", 0), functools.partial(Quiet, directory=directory))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_port}/"


def context_options(engine, size, scheme, locale):
    opts = dict(SIZES[size], device_scale_factor=1, color_scheme=scheme, locale=locale)
    if engine == "firefox":
        opts.pop("is_mobile", None)
    return opts


def check_page(context, base, path, shot):
    problems = []
    page = context.new_page()
    page.route("**/*", lambda route: route.continue_()
               if route.request.url.startswith(base) else route.fulfill(status=200, body=""))
    page.on("pageerror", lambda e: problems.append(f"JavaScript error: {e}"))
    def on_console(m):
        if m.type == "error":
            problems.append(f"console error: {m.text}")
    page.on("console", on_console)
    def on_response(r):
        if r.url.startswith(base) and r.status >= 400:
            problems.append(f"HTTP {r.status}: /{r.url[len(base):]}")
    page.on("response", on_response)
    response = page.goto(base + path, wait_until="load")
    if response is None or response.status >= 400:
        problems.append("page did not load")
    page.wait_for_timeout(500)
    problems += page.evaluate(MEASURE, page.viewport_size["width"])
    # Taken after the checks, with the console no longer watched: to hide the text caret,
    # Playwright injects its own <style>, which WebKit blocks under a strict
    # Content-Security-Policy and reports as a console error. That is the tool, not the site.
    page.remove_listener("console", on_console)
    page.screenshot(path=shot, caret="initial")
    page.close()
    return problems


def compare(paths, labels, out):
    ims = [Image.open(p).convert("RGB") for p in paths]
    gap, head = 12, 22
    canvas = Image.new("RGB", (sum(i.width for i in ims) + gap * (len(ims) - 1),
                               max(i.height for i in ims) + head), "white")
    draw, x = ImageDraw.Draw(canvas), 0
    for im, label in zip(ims, labels):
        draw.text((x + 4, 4), label, fill="black")
        canvas.paste(im, (x, head))
        x += im.width + gap
    canvas.save(out)


def view_name(path, size, scheme, locale):
    page = re.sub(r"[^A-Za-z0-9]+", "-", path).strip("-") or "top"
    return f"{page}-{size}-{scheme}-{locale}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--site", required=True, help="the built site")
    ap.add_argument("--out", default="browser-check")
    ap.add_argument("--pages", nargs="+", required=True,
                    help='paths under the site root; "" is the top page')
    ap.add_argument("--engines", nargs="+", default=ENGINES, choices=ENGINES)
    ap.add_argument("--locales", nargs="+", default=["en-US"],
                    help="browser languages, such as en-US ja-JP")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    base = serve(args.site)
    pages = [p.strip().lstrip("/") for p in args.pages]
    views = [(size, scheme, locale) for locale in args.locales for size in SIZES for scheme in SCHEMES]
    failures = []

    with sync_playwright() as pw:
        for engine in args.engines:
            launch = {}
            if engine == "chromium" and os.environ.get("BROWSER_CHECK_CHROMIUM"):
                launch["executable_path"] = os.environ["BROWSER_CHECK_CHROMIUM"]
            browser = getattr(pw, engine).launch(**launch)
            for size, scheme, locale in views:
                context = browser.new_context(**context_options(engine, size, scheme, locale))
                for path in pages:
                    shot = os.path.join(args.out, f"{engine}-{view_name(path, size, scheme, locale)}.png")
                    for problem in check_page(context, base, path, shot):
                        failures.append((engine, f"{size} {scheme} {locale}", "/" + path, problem))
                context.close()
            browser.close()

    for path in pages:
        for size, scheme, locale in views:
            name = view_name(path, size, scheme, locale)
            files = [os.path.join(args.out, f"{e}-{name}.png") for e in args.engines]
            compare(files, args.engines, os.path.join(args.out, f"compare-{name}.png"))

    lines = [f"Checked {len(pages)} pages x {len(views)} views in {', '.join(args.engines)}.", ""]
    if failures:
        lines += ["| Engine | View | Page | Problem |", "| --- | --- | --- | --- |"]
        lines += [f"| {e} | {v} | `{p}` | {msg.replace('|', '/')} |" for e, v, p, msg in failures]
    else:
        lines.append("No problems found.")
    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
