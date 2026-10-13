# Mitgelieferte Bibliotheken

Damit die App ohne Internet startet, liegen Schriften und Karten-Bibliothek im Repository statt bei fremden Servern.

| Was | Version | Lizenz | Quelle |
|---|---|---|---|
| Leaflet (`leaflet/`) | 1.9.4 | BSD-2-Clause | npm-Paket `leaflet@1.9.4`, Ordner `dist/` |
| Source Sans 3 (`fonts/`) | Fontsource-Stand vom 13.10.2026, Gewichte 400/500/600, Latein und Latein erweitert | SIL Open Font License 1.1 | npm-Paket `@fontsource/source-sans-3` |
| Shippori Mincho (`fonts/`) | Fontsource-Stand vom 13.10.2026, nur Gewicht 700, nur Latein und die Kanji der App-Oberfläche (食 茶 酒 店 市 館 社 寺 園 景 宿 他 東 京 一 覧 地 図) | SIL Open Font License 1.1 | npm-Paket `@fontsource/shippori-mincho` |

Japanische Ortsnamen in Mincho-Überschriften, die nicht in diesen Ausschnitten stehen, zeigt der Browser in einer Systemschrift (Hiragino Mincho ProN, Yu Mincho).

**Neu erzeugen:** Pakete per `npm install leaflet@1.9.4 @fontsource/source-sans-3 @fontsource/shippori-mincho` holen, Dateien wie oben auswählen und in `vendor/` kopieren. `vendor/fonts/fonts.css` enthält pro Datei einen `@font-face`-Block mit dem ursprünglichen `unicode-range`.

Kartenhintergrund (Esri-Kacheln) kommt weiter aus dem Netz und ist offline nicht verfügbar.
