# Tokio 2027 – Arbeitsablauf

- Datenquelle: `quelle/orte.json`. App-Code: `quelle/app.src.html`.
- `index.html` nie direkt bearbeiten, sondern mit `python3 quelle/build.py` erzeugen.
- Neuen Ort hinzufügen:
  1. Eintrag an `quelle/orte.json` anhängen (gleiche Felder, `id` = fortlaufende Nummer + Slug).
  2. `python3 quelle/build.py` und `python3 tools/orte_md.py` ausführen.
  3. Commit und Push auf `main`. GitHub Pages veröffentlicht automatisch. Die GitHub Action `orte-md.yml` hält `orte.md` aktuell.
- Google Drive (Ordner „Tokyo“, ID `1EQibKV8NZg-K7Gs_1C3iePJjIRc6Kr9e`): die Datei „Tokio 2027 – Orte.md“ ist die kompakte Fassung.
  Sie wird mit `python3 tools/orte_md.py --kompakt <pfad>` erzeugt. Die Drive-Anbindung kann Dateien nicht überschreiben:
  alte Datei in den Papierkorb, neue mit gleichem Titel anlegen (`disableConversionToGoogleType: true`).
- Ortsdaten wie Sterne, Typ und Adresse: Google Maps per Playwright laden (Chromium mit `proxy: {server: $HTTPS_PROXY}`, Seite `https://www.google.com/maps/place/<Name>/data=!4m2!3m1!1s<hex>:<hex>?hl=en`, etwa 20 s warten, `innerText` lesen). Das klappt nicht immer (ERR_TOO_MANY_RETRIES), dann einzeln wiederholen.
  Koordinaten: aus `!3d…!4d…` im aufgelösten Link, sonst aus dem Plus Code der Seite.
