# Visueller Auffrischungs-Vorschlag für die Tokyo-App

Stand: 09.11.2026. **Umsetzung:** Phase 1, 2 und 3 sind in der App (siehe `docs/entscheidungen.md`); nicht umgesetzt: weitere Dichte-Optionen. *Ursprünglich nur ein Vorschlag, an der App war nichts geändert.* Grundlage: der laufende Code (`quelle/app.src.html`), `docs/design-guidelines.md`, die Gestaltungskritik vom 05.11. und Screenshots im headless Chromium (390, 320, 1280 px, hell und dunkel). Nicht getestet: echte Geräte, Bildschirmleser, Kartenkacheln.

## 0. Einordnung und Gegenargumente

Der Skill „design-taste-frontend“ ist für Firmen-Landingpages gebaut (Stockfotos, Effekte, „ein Abschnitt pro Bildschirm“, erfundene Öffnungszeiten, keine Koordinaten). Das passt nicht auf eine Offline-Reise-App. **Übernommen sind nur Prinzipien:** ein System statt Einzelwerte, gleiche Ränder, ruhige Rückmeldung auf Berührung, jede Fläche zeichnet immer. Nicht übernommen: Workflow, Skripte, Fotos, Effekte. Ich habe den Skill-Ablauf nicht ausgeführt.

**Drei stärkste Gründe, warum eine große Auffrischung falsch sein könnte**
1. **Der Nutzen ist klein.** Die App erfüllt ihren eigenen Leitfaden: kein Text unter 12 px, alle gemessenen Kontraste über 4,5:1, Tippflächen 44 px. Eine Auffrischung ohne Messwert-Ziel ist Geschmack, und niemand außer dir und deiner Familie nutzt die App.
2. **Das Risiko ist größer als der Gewinn.** Jede Änderung geht durch Service Worker, Mac-Datei und Offline-Cache. Auf echten Geräten (iPhone, Android, VoiceOver) ist nichts getestet, ein Regressionsfehler fiele erst unterwegs in Japan auf.
3. **Die Bausteine der Liste passen nicht.** Es gibt keine Komponenten-Bibliothek, kein Figma und keine Tabellen. Figma-/Storybook-Exporte und „hochauflösende Mockups“ wären Aufwand ohne Gegenstück im Projekt (eine HTML-Datei, Vanilla-JS). Das Figma-Plugin war in dieser Sitzung zudem nicht verbunden.

**Empfehlung:** Statt „Redesign“ ein **gezieltes Token-Aufräumen** (Phase 1, 2). Das bringt den Hauptgewinn bei kleinem Risiko.

## 1. Ziele und Erfolgskriterien

Ziele: ruhiger und einheitlicher wirken, mit dem Daumen unterwegs schneller zu bedienen, Marke (Zinnober, Mincho-Zeichen) klarer. **Messbar, ohne Analytics** (die App hat bewusst keines):
- Kontrast: Text ≥ 4,5:1, Bedienelementränder und Zeichen ≥ 3:1 (`tools/kontrast.py` plus Browser-Messung).
- Tippflächen ≥ 44 px (Mindestwert 40 px bei Chips), nichts unter 12 px.
- Kein Überlauf bei 320 px, kein Konsolenfehler, 199 Orte.
- Vorher/nachher-Screenshots in acht Ansichten (Liste, Detail, Filter, Karte, Merkliste; hell/dunkel).
- Kurzer Familien-Test mit zwei Aufgaben: „Finde ein Café in Shibuya und merke es“ (Taps und Sekunden), „Öffne die Route zu einem Ort“.

## 2. Einschränkungen

Ablauf, Zustände und Logik bleiben: Tabs, Zurück-Taste schließt das Blatt, Merken/Besucht/Notiz im Browser, Teilen-Link `#m=…`, Ortsnummern der `id`, Offline-Start, nichts von fremden Servern. Nur Oberfläche: CSS, Markup-Details, Symbole.

## 3. Visuelles System

**Ist (gemessen):** 0 Abstands-Tokens (alle Werte hartkodiert), 8 verschiedene Eckradien (3, 4, 6, 8, 9, 10, 18, 999 px), 12 Schriftgrößen in px (u. a. 13, 15, 17, 19), verstreute z-index-Werte (0, 1, 20, 21, 30, 500).

**Farbe** (Palette bleibt, sie ist WCAG-AA-geprüft): Washi-Papier `--paper`, Indigo für Aktion, Zinnober für Marke, Gold für Merken, Salbei für Besucht. Vorschlag: nur Form ändern, nicht Farben:
- **Nicht-Primär-Bedienelemente mit Fläche statt starkem Rand:** `--paper-2`-Füllung plus dünner Rand in `--line`, aber nur dort, wo das Element auch ohne Rand erkennbar bleibt (Chips, Pillen). **Eingabefelder und Schalter behalten `--line-strong`** (WCAG 1.4.11 verlangt 3:1 für Grenzen von Bedienelementen). Das macht die Seite ruhiger, ohne Kontrast zu opfern.
- Neue Ebenen-Tokens statt Einzelschatten: `--elev-0` (Fläche), `--elev-1` (Karte, 0 1px 2px), `--elev-2` (Blatt, 0 10px 40px, ist `--shadow`).

**Typografie** (Schriften bleiben: Shippori Mincho für Titel und Stempel, Source Sans 3 für Text): Skala als Tokens in `rem` (16 px = 1 rem):
| Stufe | Wert | Verwendung |
|---|---|---|
| `--fs-title` | 1,375rem (ab 720 px: 1,625rem) | App-Titel |
| `--fs-h2` | 1,5rem | Ortsname |
| `--fs-h3` | 1,125rem | Blatt- und Leerzustand-Titel |
| `--fs-text` | 1rem | Fließtext, Eingaben |
| `--fs-small` | 0,875rem | Untertitel, Adresse |
| `--fs-label` | 0,75rem, Versalien, 0,08em | Etiketten |
Die streunenden 13, 15, 17, 19 und 20 px fallen weg. Zeilenhöhe 1,5 bleibt.

**Abstand und Radius:** Tokens `--s-1`…`--s-6` = 4, 8, 12, 16, 24, 32 px (wie im Leitfaden). Radien auf **vier** Stufen: `--r-s` 6, `--r-m` 10 (Standard), `--r-l` 18 (Blatt), `--r-pill` 999.

**Ebenen:** `--z-map` 0, `--z-legend` 10, `--z-sheet` 30, `--z-scrim` 20, `--z-top` 40 statt Einzelwerten.

**Symbole:** Kanji-Stempel bleiben (Wiedererkennung). ☆ ○ ✓ ↗ sind Textzeichen, die je Gerät unterschiedlich aussehen. Vorschlag: ein kleines Inline-SVG-Set (Stern, Haken, Kreis, Pfeil) mit gleicher Strichstärke, immer mit Wort daneben. Karten-Punkte behalten ihre Formen (Kreis, Raute, Quadrat, Dreieck).

## 4. Bausteine mit Zuständen (Redlines)

| Baustein | Ruhe | Hover (nur Maus) | Gedrückt | Fokus | Gewählt | Gesperrt |
|---|---|---|---|---|---|---|
| Hauptknopf (`.btn.primary`) | Indigo-Fläche, 44 px, `--r-m` | 92 % Helligkeit | scale .97 | 2 px `--focus`, Abstand 2 px | – | 45 % |
| Zweitknopf (`.btn`) | `--card`, Rand `--line-strong` | `--paper-2` | scale .97 | wie oben | – | 45 % |
| Schalter (`.toggle`) | wie Zweitknopf, 44 px | `--paper-2` (nicht wenn gewählt) | scale .97 | wie oben | Gruppenfarbe als Fläche (Gold/Salbei) plus ✓ | 45 % |
| Pille/Link (`.pill-link`) | `--indigo-soft`, 44 px | leicht dunkler | scale .97 | wie oben | – | – |
| Chip | `--card` + Rand `--line-strong`, 40 px | `--paper-2` | scale .97 | wie oben | Indigo-Fläche, Zähler sichtbar | – |
| Eingabefeld, Auswahl | `--card`, Rand `--line-strong`, 16 px Text | – | – | Ring 2 px | – | 45 % |
| Listenzeile | transparent, Trennlinie `--line` | `--paper-2` | `--paper-2` | Ring innen | – | – |
| Tab | Wort + Zeichen, 56 px | `--paper-2` | scale .97 | wie oben | Zinnober, Fläche `--vermillion-soft` | – |
| Blatt (Detail/Filter) | `--paper`, `--r-l`, `--elev-2`, Rückseite abgedunkelt | – | – | Fokus bleibt im Blatt | – | – |

Keine Tabellen in der App (nur in `orte.md`), deshalb dort keine Gestaltung.

## 5. Barrierefreiheit

- Schrift in `rem` statt `px`: folgt einer geänderten Standardschrift des Browsers und dem Seitenzoom sauberer. Auf iOS bitte testen, ob das wirklich greift (ich weiß es nicht sicher).
- Fokusring: bleibt 2 px mit Abstand (zwei Seiten kontrastreich). Zusatz: `scroll-padding-bottom` für die feste Tab-Leiste, damit ein fokussiertes Element nicht darunter liegt (WCAG 2.2, 2.4.11).
- Zusatzmodi: `@media (forced-colors: active)` für Rahmen, `prefers-contrast: more` (kräftigere Ränder). Beides fehlt bisher.
- Weiter: Zeichen immer mit Wort, Karten-Punkte mit Formen, Liste bleibt die vollständige Alternative zur Karte.

## 6. Responsiv

Breakpoints bleiben (720, 1024). **Neu: ab 1440 px drei Spalten** (Liste, Karte, Detail), damit das Detail die Karte nicht mehr überdeckt (Kritikpunkt 5, strukturell gelöst). Dichte der Listenzeilen: eine Zeile weniger Beschreibung ab 1024 px möglich. Tippflächen 44 px (Chips 40), sichere Ränder für iPhone mit `env(safe-area-inset-*)` sind schon vorhanden.

## 7. Bewegung

Zweck: Rückmeldung, nicht Schmuck. **Dauer:** Hover/Druck 120 ms, Blatt 220 ms (ist so), Ein-/Ausblenden 180 ms. **Easing:** `cubic-bezier(.2,.8,.2,1)` (ist so). **Reduzierte Bewegung:** Blatt blendet nur ein (80 ms Überblenden statt Schieben), Druck-Skalierung entfällt (ist so). Keine Scroll-Effekte, keine Parallax, keine Dauerbewegung.

## 8. Liefergegenstände (realistisch)

| Gewünscht | Machbar | Hinweis |
|---|---|---|
| Styleguide | Ja, `docs/design-guidelines.md` ergänzen | Abschnitte 3, 4 oben |
| Tokens | Ja, `:root`-Block im Code (CSS-Variablen) | keine Bibliothek nötig |
| Hochauflösende Mockups | Teilweise: PNG-Screenshots der Beispielseite `docs/design-beispiele.html` | echte Bilder, kein Figma |
| Interaktiver Prototyp | Ja, die Beispielseite selbst (HTML) | keine zweite Technik |
| Redlines | Ja, Tabelle in Abschnitt 4 | Pixelmaße im Leitfaden |
| Figma-/Storybook-Exporte | **Nein** | kein Figma-Zugang, keine Komponenten-Bibliothek |

## 9. Phasenplan

**Phase 1 (schnelle Erfolge, Risiko klein):** Tokens für Abstand, Radius, Ebene, z-index, `rem`-Skala einführen und die hartkodierten Werte ersetzen (ohne sichtbare Änderung). Prüfung: Screenshot-Vergleich.
**Phase 2 (sichtbar, mittleres Risiko):** ruhigere Zweitknöpfe (Fläche statt Rand außer bei Feldern und Schaltern), SVG-Symbole, `forced-colors`/`prefers-contrast`, `scroll-padding`, Drei-Spalten ab 1440.
**Phase 3 (nur wenn gewollt):** weitere Dichte-Optionen, Punkt-Zusammenfassen in Tokio (Gruppenpunkt mit Zahl), Dunkel-Feinheiten.
Jede Phase ein Commit, bei Problem zurücksetzen; Mac-Datei erst danach ersetzen.

## 10. Begründung und Erfolgskontrolle

Der größte erwartbare Nutzen liegt bei Phase 1: Änderungen werden billiger und sicherer, weil ein Wert an einer Stelle steht. Phase 2 liefert die sichtbare Ruhe und schließt echte Lücken (kein `forced-colors`, Schrift in `px`). Erfolg: die Kriterien aus Abschnitt 1 plus der Familien-Test. Ohne Geräte-Test auf iPhone, Android und mit Bildschirmleser ist keine Aussage über die reale Wirkung möglich.
