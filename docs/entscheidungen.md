# Entscheidungen

Eine Zeile bis ein Absatz pro Entscheidung. Vorlage: `docs/design-guidelines.md`, Anhang A. Neueste zuerst.

## 2026-10-13 · Bildschirmleser-Texte, Merkliste teilen, Update-Hinweis für die Mac-Datei
Kontext:      Sterne, Trefferzahl und Tabs waren für Bildschirmleser schlecht benannt, die Merkliste ließ sich nicht weitergeben (jede Person hatte ihre eigene), und die Mac-Datei musste von Hand ersetzt werden.
Entscheidung: Unsichtbare Texte (`.sr`), `lang="ja"` für japanische Textstücke, `aria-live` an der Trefferzahl, Tabs mit Pfeiltasten und `aria-controls`, `inert` für den Hintergrund bei modalen Blättern. Merkliste teilen per Teilen-Menü oder Zwischenablage, dazu ein Link mit `#m=<Ortsnummern>`, der nach Bestätigung die Orte übernimmt (Notizen nicht). Die Ein-Datei-Fassung prüft per `version.json` auf Updates und bietet den Download an; Ersetzen bleibt Handarbeit, weil eine Seite sich nicht selbst überschreiben darf.
Alternativen: Gemeinsame Merkliste auf einem Server (verworfen: bräuchte Konten und Hosting), Chrome-only „File System Access“ zum Überschreiben (verworfen: nur ein Browser, Berechtigung bei jeder Sitzung).
Folgen:       Ortsnummern (`id`-Präfix) dürfen sich nie ändern, sonst zeigen alte Links auf falsche Orte. Mit echten Bildschirmlesern und Geräten nicht getestet.

## 2026-10-13 · Karten-Punkte größer und Offline-Betrieb
Kontext:      Karten-Punkte hatten 13 px Durchmesser und genau diese Trefferfläche. Ohne Netz startete die App nicht (Schriften und Karten-Bibliothek kamen von fremden Servern, kein Service Worker).
Entscheidung: Punkte in Canvas mit 10 px Trefferfläche, Radius nach Zoom 8/10/12 px. Schriften und Leaflet im Repository unter `vendor/`, Service Worker `sw.js` (App-Hülle vorab ablegen, Start online zuerst aus dem Netz, sonst aus dem Speicher), Ein-Datei-Fassung `Tokio-2027-offline.html` für den Mac. `sw.js` und die Ein-Datei-Fassung entstehen in `quelle/build.py`, die Version ergibt sich aus den Dateiinhalten.
Alternativen: Kartenkacheln ebenfalls zwischenspeichern (verworfen: Esri-Server war in der Prüfumgebung nicht erreichbar, ob er CORS erlaubt, ist unbekannt, ein falscher Versuch würde die Karte zerstören), Radius immer 12 px (verworfen: im Überblick verschwimmt Tokio).
Folgen:       Kartenhintergrund ist offline nicht verfügbar (Hinweis erscheint). Die Wartezeit für neue Fassungen beträgt bei schlechter Verbindung bis zu 4 s. Jeder neue Build erzeugt neue `sw.js` und `Tokio-2027-offline.html`, beide gehören ins Repository. Nicht auf echten Geräten getestet.

## 2026-10-13 · Zurück-Taste schließt das Blatt
Kontext:      Die Android-Zurück-Taste und die iPhone-Wischgeste verließen die App, auch wenn ein Blatt offen war.
Entscheidung: Beim Öffnen von Detail oder Filter ein Eintrag im Browser-Verlauf (`pushState`), bei Zurück schließt nur das Blatt. Schließt die App das Blatt selbst (Knopf, Esc, Hintergrund), nimmt sie den Eintrag mit `history.back()` zurück und ignoriert dessen `popstate`. Wird das Blatt währenddessen neu geöffnet, legt sie den Eintrag danach an. Zusätzlich: das verzögerte Verstecken nach dem Schließen wird bei erneutem Öffnen abgebrochen (vorher konnte ein schnelles Wiederöffnen sofort wieder verschwinden).
Alternativen: Hash-URLs (`#ort-123`, verworfen: ändert die Adresse und bräuchte Aufräumen beim Start), kein Verlaufseintrag (so war es vorher).
Folgen:       Zurück am Anfang verlässt die App wie üblich. Auf echten Geräten nicht getestet.

## 2026-10-13 · Laptop-Layout in die App übernommen (ab 1024 px)
Kontext:      Am Laptop war nur eine schmale Spalte mit Tabs sichtbar, Karte und Liste nie zugleich.
Entscheidung: Zwei Spalten (Liste 380 bis 460 px, Karte), Detail als Seitenleiste ohne Abdunkeln, Karte-Tab entfällt, Tab-Leiste bleibt links unten. Zoom und Übersicht der Karte links. Merkliste zeigt gemerkte Orte auf der Karte. `docs/soll.css` entfernt, weil alles umgesetzt ist.
Alternativen: Detail weiter als Blatt von unten (verworfen: verdeckt Liste und Karte), Tabs oben (verworfen: ändert die Bedienung vom Handy).
Folgen:       Beim Wechsel des Orts während des Bearbeitens fragt die App vor dem Verwerfen (Seitenleiste bleibt sonst offen und überschriebe nichts stillschweigend). Das Filterblatt bleibt ein Blatt von unten mit Abdunkeln. Karten-Kacheln im Test nicht geladen, nur Punkte, Zoom und Verhalten geprüft.

## 2026-10-13 · Schrift und Zustände in die App übernommen
Kontext:      Fließtext 15 px und Kleinstes 10 bis 11,5 px, keine Hover- und Gedrückt-Zustände, japanische Namen in Zufallsschrift.
Entscheidung: Basis 16 px (Zeilenhöhe 1,5), Zweittext 14 px, Zähler und Etiketten 12 px, Leaflet-Hinweis 11 px (Pflichtangabe, bleibt knapp unter 12). Ersatzschriften Hiragino Sans, Yu Gothic, Noto Sans JP. Hover nur bei Mausgeräten und nicht auf aktiven Elementen, Gedrückt 97 %, Gesperrt 45 %, alles ohne Bewegung bei „Bewegung reduzieren“.
Alternativen: Hover auch auf aktive Elemente (verworfen: die Auswahlfarbe verschwände unter dem Mauszeiger, so war es in `soll.css` zunächst angelegt).
Folgen:       Zeilen werden höher, weniger Orte pro Bildschirm. Laptop-Layout, Karten-Punkte und Code-Punkte bleiben offen. `.status` (12,5 px) bewusst nicht auf 12 gesenkt.

## 2026-10-13 · Farben und Tippflächen in die App übernommen
Kontext:      Fünf Farbpaare lagen unter dem WCAG-Ziel, mehrere Bedienelemente unter 40 px.
Entscheidung: `--vermillion`, `--gold`, `--focus` angepasst, `--line-strong` neu (hell/dunkel). Ränder der Bedienelemente und der ungemerkte Stern nutzen die neuen Werte. Mindesthöhen: Chip 40, Tab 56, Schließen/Pille/Knöpfe 44, kleiner Knopf 40, Karten-Zoom 44.
Alternativen: `soll.css` als Zusatz anhängen (verworfen: zwei Quellen für dieselben Werte).
Folgen:       Schrift, Zustände, Laptop-Layout und Code-Punkte bleiben offen. Karten-Punkte (JavaScript) nicht angepasst. Echte Geräte noch nicht getestet.

## 2026-10-13 · Design-Leitfaden beschreibt Ist und zeigt Soll, ändert die App nicht
Kontext:      Die App wird von Familie genutzt, ein Design-Leitfaden fehlte.
Entscheidung: Schlanker Leitfaden (ca. 10 Seiten) im Repository, Ziel-Design als `docs/soll.css`, Beispiele als `docs/design-beispiele.html`. Die App bleibt unverändert, bis das Soll bewusst übernommen wird (Farben und Tippflächen: siehe oben).
Alternativen: Notion-Seite (verworfen: nicht neben dem Code versioniert), volle 12-Kapitel-Fassung (verworfen: zu groß für eine Ein-Datei-App).
Folgen:       Soll-Werte (Farben, Größen) sind noch nicht in der App. Übernahme nach Abschnitt 12 des Leitfadens.
