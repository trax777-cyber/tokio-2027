# Entscheidungen

Eine Zeile bis ein Absatz pro Entscheidung. Vorlage: `docs/design-guidelines.md`, Anhang A. Neueste zuerst.

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
