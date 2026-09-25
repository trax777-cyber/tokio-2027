# Baut die App aus app.src.html + den Ortsdaten in orte.json:
#   "Tokio 2027.html"        – zum direkten Öffnen am Laptop
#   github-pages/index.html  – für GitHub Pages (mit App-Symbol für den Home-Bildschirm)
import json, pathlib

here = pathlib.Path(__file__).parent
data = json.dumps(json.loads((here / "orte.json").read_text()), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (here / "app.src.html").read_text().replace("__DATA__", data, 1)
i = src.index('<div class="app">')

head = ('<!DOCTYPE html>\n<html lang="de">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        # Abstand zu Notch und Home-Leiste, wenn die App vom Home-Bildschirm startet
        '<style>:root { padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }</style>\n')
web_head = ('<link rel="manifest" href="manifest.webmanifest">\n'
            '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
            '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n'
            '<meta name="apple-mobile-web-app-capable" content="yes">\n'
            '<meta name="mobile-web-app-capable" content="yes">\n'
            '<meta name="apple-mobile-web-app-title" content="Tokio 2027">\n'
            '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
            '<meta name="theme-color" content="#f2f0eb" media="(prefers-color-scheme: light)">\n'
            '<meta name="theme-color" content="#191b1e" media="(prefers-color-scheme: dark)">\n')

def page(extra):
    return head + extra + src[:i] + "</head>\n<body>\n" + src[i:] + "\n</body>\n</html>\n"

(here / "Tokio 2027.html").write_text(page(""))
(here / "github-pages").mkdir(exist_ok=True)
(here / "github-pages" / "index.html").write_text(page(web_head))
print("Gebaut: Tokio 2027.html und github-pages/index.html")
