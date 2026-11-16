#!/usr/bin/env python3
"""Build the Stitch Pattern Maker.

  python3 build.py

Writes two things from src/:
  dist/stitch-pattern-maker.html  one file with everything inside; open it by double-click, works offline
  docs/                           the same page as an installable web app (served by GitHub Pages)
"""
import base64, hashlib, json, pathlib

ROOT = pathlib.Path(__file__).parent
FONTS = [("Barlow", 400), ("Barlow", 500), ("Barlow", 600), ("IBM Plex Mono", 400), ("IBM Plex Mono", 500), ("Pirata One", 400)]

def font_css():
    out = []
    for fam, wt in FONTS:
        data = (ROOT / "vendor" / "fonts" / f"{fam.replace(' ', '')}-{wt}.woff2").read_bytes()
        b64 = base64.b64encode(data).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{wt};font-display:swap;"
                   f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n".join(out)

def page(pwa_head=""):
    html = (ROOT / "src" / "index.html").read_text(encoding="utf8")
    jspdf = (ROOT / "vendor" / "jspdf.umd.min.js").read_text(encoding="utf8")
    assert "</script" not in jspdf.lower()
    parts = {
        "/*FONTS*/": font_css(),
        "/*STRINGS*/": (ROOT / "src" / "strings.js").read_text(encoding="utf8"),
        "<!--JSPDF-->": "<script>" + jspdf + "</script>",
        "<!--PWA-->": pwa_head,
    }
    for key, value in parts.items():
        assert html.count(key) == 1, key
        html = html.replace(key, value)
    return html

PWA_HEAD = """<link rel="manifest" href="manifest.webmanifest">
<meta name="theme-color" content="#E8EBEF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101216" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Stitch">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">"""

MANIFEST = {
    "name": "Stitch Pattern Maker", "short_name": "Stitch", "description": "Turn a logo into an embroidery pattern at exact size.",
    "start_url": "./", "scope": "./", "display": "standalone", "background_color": "#E8EBEF", "theme_color": "#AE1430",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
}

SW = """// Keeps the app working without internet. The cache name changes with every build.
const CACHE = 'stitch-pattern-maker-%s';
const FILES = ['./', 'manifest.webmanifest', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES.map((f) => new Request(f, { cache: 'reload' })))).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(caches.open(CACHE).then(async (c) => {
    const hit = await c.match(e.request, { ignoreSearch: true }) || (e.request.mode === 'navigate' ? await c.match('./') : null);
    return hit || fetch(e.request);
  }));
});
"""

def main():
    (ROOT / "dist").mkdir(exist_ok=True); (ROOT / "docs").mkdir(exist_ok=True)
    single = page()
    (ROOT / "dist" / "stitch-pattern-maker.html").write_text(single, encoding="utf8")
    app = page(PWA_HEAD)
    (ROOT / "docs" / "index.html").write_text(app, encoding="utf8")
    (ROOT / "docs" / "manifest.webmanifest").write_text(json.dumps(MANIFEST, indent=2), encoding="utf8")
    (ROOT / "docs" / ".nojekyll").write_text("")
    h = hashlib.sha256(app.encode("utf8"))
    for icon in ("icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        (ROOT / "docs" / icon).write_bytes((ROOT / "src" / "icons" / icon).read_bytes())
        h.update((ROOT / "src" / "icons" / icon).read_bytes())
    (ROOT / "docs" / "sw.js").write_text(SW % h.hexdigest()[:12], encoding="utf8")
    print("built: dist/stitch-pattern-maker.html (%d KB), docs/ (cache %s)" % (len(single.encode()) // 1024, h.hexdigest()[:12]))

if __name__ == "__main__":
    main()
