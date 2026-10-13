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
VERSION = h.hexdigest()[:10]
# Hinweis auf neue Version (nur in der Datei, die am Mac von der Festplatte geöffnet wird; eine Seite kann sich nicht selbst überschreiben,
# deshalb: prüfen, melden, Datei herunterladen, der Nutzer ersetzt die alte)
UPDATE = """<script>
(function () {
  if (location.protocol !== "file:") return;
  var V = "%s", RAW = "https://raw.githubusercontent.com/trax777-cyber/tokio-2027/main/", KEY = "tokio-update-geprueft", bar;
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) {} }
  function show(text, buttons) {
    if (!bar) {
      bar = document.createElement("div"); bar.id = "tokio-update"; bar.setAttribute("role", "status");
      bar.style.cssText = "position:fixed;left:50%%;transform:translateX(-50%%);bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:40;max-width:calc(100%% - 24px);background:var(--ink);color:var(--paper);padding:10px 14px;border-radius:12px;font-size:14px;box-shadow:var(--shadow);display:flex;gap:10px;align-items:center;flex-wrap:wrap";
      document.body.appendChild(bar);
    }
    bar.textContent = ""; var t = document.createElement("span"); t.textContent = text; bar.appendChild(t);
    buttons.forEach(function (b) {
      var el = document.createElement("button"); el.type = "button"; el.textContent = b[0]; el.onclick = b[1];
      el.style.cssText = "min-height:44px;padding:6px 14px;border-radius:10px;border:1px solid var(--paper);background:transparent;color:var(--paper);font:inherit;font-weight:600;cursor:pointer";
      bar.appendChild(el);
    });
  }
  function laden() {
    show("Lade neue Version …", []);
    fetch(RAW + "Tokio-2027-offline.html", { cache: "no-store" }).then(function (r) { if (!r.ok) throw 0; return r.blob(); }).then(function (blob) {
      var a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "Tokio 2027.html"; document.body.appendChild(a); a.click(); a.remove();
      show("Heruntergeladen. Ersetze damit die alte Datei im Ordner TokioOrte (beim Speichern „Ersetzen“ wählen) und öffne sie neu.", [["Schließen", function () { bar.remove(); bar = null; }]]);
    }).catch(function () { show("Download nicht möglich. Bitte später noch einmal versuchen.", [["Schließen", function () { bar.remove(); bar = null; }]]); });
  }
  var last = Number(store(KEY) || 0);
  if (Date.now() - last < 6 * 3600 * 1000) return;       // höchstens alle 6 Stunden nachsehen
  fetch(RAW + "version.json", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (j) {
    store(KEY, String(Date.now()));
    if (j && j.version && j.version !== V) show("Neue Version der App verfügbar.", [["Herunterladen", laden], ["Später", function () { bar.remove(); bar = null; }]]);
  }).catch(function () {});
})();
</script>""" % VERSION
page = page.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n<meta name="app-version" content="' + VERSION + '">', 1)
assert "</body>" in page
page = page.replace("</body>", UPDATE + "\n</body>", 1)
(root / "version.json").write_text(json.dumps({"version": VERSION, "datei": "Tokio-2027-offline.html"}, ensure_ascii=False) + "\n", encoding="utf-8")
(root / "Tokio-2027-offline.html").write_text(page, encoding="utf-8")
print("Tokio-2027-offline.html gebaut,", round(len(page) / 1024), "KB")
