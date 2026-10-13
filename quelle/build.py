# Baut ../index.html (die App für GitHub Pages) aus app.src.html + orte.json.
# Aufruf: python3 quelle/build.py
import json, pathlib

here = pathlib.Path(__file__).parent
root = here.parent
data = json.dumps(json.loads((here / "orte.json").read_text()), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (here / "app.src.html").read_text().replace("__DATA__", data, 1)
i = src.index('<div class="app">')
head = ('<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">\n'
        '<style>:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }</style>\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
        '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
        '<meta name="mobile-web-app-capable" content="yes">\n'
        '<meta name="apple-mobile-web-app-title" content="Tokio 2027">\n'
        '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
        '<meta name="theme-color" content="#f2f0eb" media="(prefers-color-scheme: light)">\n'
        '<meta name="theme-color" content="#191b1e" media="(prefers-color-scheme: dark)">\n')
(root / "index.html").write_text(head + src[:i] + "</head>\n<body>\n" + src[i:] + "\n</body>\n</html>\n")
print("index.html gebaut")

# ---------- Offline: Service Worker und Ein-Datei-Fassung ----------
import hashlib, base64, re
vendor = sorted(str(f.relative_to(root)) for f in (root / "vendor").rglob("*") if f.is_file() and f.suffix != ".md")
shell_files = ["index.html", "manifest.webmanifest", "icon-192.png", "icon-512.png", "apple-touch-icon.png"] + vendor
h = hashlib.sha1()
for f in shell_files:
    h.update(f.encode()); h.update((root / f).read_bytes())
sw = (here / "sw.src.js").read_text(encoding="utf-8").replace("__VERSION__", h.hexdigest()[:10]).replace("__SHELL__", json.dumps(["./"] + shell_files))
(root / "sw.js").write_text(sw, encoding="utf-8")
print("sw.js gebaut, Version", h.hexdigest()[:10])

# Ein-Datei-Fassung: Schriften und Leaflet stecken im HTML, läuft ohne Ordner und ohne Internet (außer Kartenhintergrund)
def inline_css(path):
    css = (root / path).read_text(encoding="utf-8")
    def font(m):
        data = (root / "vendor/fonts" / m.group(1)).read_bytes()
        return "url(data:font/woff2;base64," + base64.b64encode(data).decode() + ")"
    css = re.sub(r"url\(([\w.\-\[\]]+\.woff2)\)", font, css)
    return re.sub(r"url\(images/[^)]+\)", "none", css)
page = (root / "index.html").read_text(encoding="utf-8")
js = (root / "vendor/leaflet/leaflet.js").read_text(encoding="utf-8").replace("//# sourceMappingURL=leaflet.js.map", "").replace("</script", "<\\/script")
for old, new in [
    ('<link rel="stylesheet" href="vendor/leaflet/leaflet.css">', "<style>" + inline_css("vendor/leaflet/leaflet.css") + "</style>"),
    ('<script src="vendor/leaflet/leaflet.js"></script>', "<script>" + js + "</script>"),
    ('<link rel="stylesheet" href="vendor/fonts/fonts.css">', "<style>" + inline_css("vendor/fonts/fonts.css") + "</style>"),
    ('<link rel="manifest" href="manifest.webmanifest">\n', ""),
]:
    assert old in page, old
    page = page.replace(old, new)
(root / "Tokio-2027-offline.html").write_text(page, encoding="utf-8")
print("Tokio-2027-offline.html gebaut,", round(len(page) / 1024), "KB")
