# Tokio 2027 – Arbeitsablauf

- Datenquelle: `quelle/orte.json`. App-Code: `quelle/app.src.html`.
- `index.html`, `sw.js` und `Tokio-2027-offline.html` nie direkt bearbeiten: `python3 quelle/build.py` erzeugt alle drei (Service-Worker-Vorlage: `quelle/sw.src.js`). Alle drei mit committen.
- Schriften und Leaflet liegen in `vendor/` (siehe `vendor/LIESMICH.md`), nichts von fremden Servern einbinden, sonst bricht der Offline-Start.
- Neuen Ort hinzufügen:
  1. Eintrag an `quelle/orte.json` anhängen (gleiche Felder, `id` = fortlaufende Nummer + Slug).
  2. `python3 quelle/build.py` und `python3 tools/orte_md.py` ausführen.
  3. Commit und Push auf `main`. GitHub Pages veröffentlicht automatisch. Die GitHub Action `orte-md.yml` hält `orte.md` aktuell.
- Google Drive (Ordner „Tokyo“, ID `1EQibKV8NZg-K7Gs_1C3iePJjIRc6Kr9e`): die Datei „Tokio 2027 – Orte.md“ ist die kompakte Fassung.
  Sie wird mit `python3 tools/orte_md.py --kompakt <pfad>` erzeugt. Die Drive-Anbindung kann Dateien nicht überschreiben:
  alte Datei in den Papierkorb, neue mit gleichem Titel anlegen (`disableConversionToGoogleType: true`).
- Ortsdaten wie Sterne, Typ und Adresse: Google Maps per Playwright laden (Chromium mit `proxy: {server: $HTTPS_PROXY}`, Seite `https://www.google.com/maps/place/<Name>/data=!4m2!3m1!1s<hex>:<hex>?hl=en`, etwa 20 s warten, `innerText` lesen). Das klappt nicht immer (ERR_TOO_MANY_RETRIES), dann einzeln wiederholen.
  Koordinaten: aus `!3d…!4d…` im aufgelösten Link, sonst aus dem Plus Code der Seite.
- Design: `docs/design-guidelines.md` (Ist und Soll), `docs/design-beispiele.html` (Beispielseite), `docs/entscheidungen.md` (Entscheidungsprotokoll).
  Neue Oberflächenelemente richten sich nach dem Leitfaden: Token-Farben, Tippflächen mind. 40/44 px, nichts unter 12 px, Zeichen immer mit Wort. Kontrast prüfen mit `python3 tools/kontrast.py`.
