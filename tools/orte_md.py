#!/usr/bin/env python3
"""Erzeugt orte.md (Übersicht aller Orte) aus den in index.html eingebetteten Daten.

Mit --kompakt PFAD: zusätzlich eine kurze Tabellen-Fassung (für Google Drive)."""
import json, collections, datetime, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
s = (root / "index.html").read_text(encoding="utf-8")
i = s.find('[{"name"')
data, _ = json.JSONDecoder().raw_decode(s[i:])

REST = "Außerhalb der 23 Bezirke"
def gruppe(d):
    if d["region"] != "Tokio": return (2, "Außerhalb Tokios")
    if d["bezirk"] == REST: return (1, "Tokio – außerhalb der 23 Bezirke")
    return (0, d["bezirk"])

def maps(u):
    m = re.search(r"0x[0-9a-f]+:(0x[0-9a-f]+)", u or "")
    return f"https://maps.google.com/?cid={int(m.group(1), 16)}" if m else u

def md(t): return str(t).replace("|", "\\|").replace("\n", " ").strip()

gruppen = collections.defaultdict(list)
for d in data: gruppen[gruppe(d)].append(d)

heute = datetime.date.today().strftime("%d.%m.%Y")
out = [f"# Tokio 2027 – Orte", "",
       f"Stand: {heute} · {len(data)} Orte · App: https://trax777-cyber.github.io/tokio-2027/", "",
       "> Automatisch aus der App erzeugt – Änderungen hier werden beim nächsten Update überschrieben.", "",
       "## Übersicht nach Kategorie", "", "| Kategorie | Anzahl |", "|---|---:|"]
for k, n in collections.Counter(d["kategorie"] for d in data).most_common():
    out.append(f"| {k} | {n} |")
out += ["", "## Inhalt", ""]
keys = sorted(gruppen, key=lambda g: (g[0], -len(gruppen[g]), g[1]))
for g in keys:
    out.append(f"- {g[1]} ({len(gruppen[g])})")
for g in keys:
    out += ["", f"## {g[1]} ({len(gruppen[g])})", ""]
    for d in sorted(gruppen[g], key=lambda d: (d["kategorie"], d["name"].lower())):
        kopf = f"**{md(d['name'])}** · {d['kategorie']}"
        if d.get("rating"): kopf += f" · ★ {d['rating']:.1f}".replace(".", ",")
        if d.get("stadtteil"): kopf += f" · {md(d['stadtteil'])}"
        out.append(f"- {kopf}")
        if d.get("beschreibung"): out.append(f"  {md(d['beschreibung'])}")
        links = []
        if d.get("googleUrl"): links.append(f"[Maps]({maps(d['googleUrl'])})")
        if d.get("website"): links.append(f"[Website]({d['website']})")
        if d.get("adresse"): links.append(md(d["adresse"]))
        if links: out.append("  " + " · ".join(links))
(root / "orte.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"orte.md: {len(data)} Orte")

if "--kompakt" in sys.argv:
    ziel = pathlib.Path(sys.argv[sys.argv.index("--kompakt") + 1])
    k = [f"# Tokio 2027 – Orte (kompakt)", "",
         f"Stand: {heute} · {len(data)} Orte · App: https://trax777-cyber.github.io/tokio-2027/", "",
         "Vollständige Fassung mit Beschreibungen und Adressen: https://github.com/trax777-cyber/tokio-2027/blob/main/orte.md", "",
         "> Automatisch erzeugt – wird bei jedem Update ersetzt."]
    for g in keys:
        k += ["", f"## {g[1]} ({len(gruppen[g])})", "", "| Ort | Kategorie | ★ | Maps |", "|---|---|---|---|"]
        for d in sorted(gruppen[g], key=lambda d: (d["kategorie"], d["name"].lower())):
            r = f"{d['rating']:.1f}".replace(".", ",") if d.get("rating") else ""
            k.append(f"| {md(d['name'])} | {d['kategorie']} | {r} | [↗]({maps(d['googleUrl'])}) |")
    ziel.write_text("\n".join(k) + "\n", encoding="utf-8")
    print(f"{ziel.name}: kompakt")
