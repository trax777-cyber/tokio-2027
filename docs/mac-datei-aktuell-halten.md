# Mac-Datei aktuell halten

Die Datei `Tokio-2027-offline.html` im Repository ist die komplette App in einer Datei (Schriften und Karten-Bibliothek stecken darin). Sie läuft am Mac ohne Internet, nur der Kartenhintergrund fehlt. Dieses Dokument beschreibt, wie sie aktuell bleibt, **ohne am Repository etwas zu ändern**: Es wird nur heruntergeladen.

## Weg 1: Hinweis in der Datei selbst (nach dem ersten Einrichten)

Die Datei prüft beim Öffnen (höchstens alle 6 Stunden, nur mit Internet), ob es eine neuere Fassung gibt, und zeigt dann unten „Neue Version der App verfügbar“ mit „Herunterladen“.

1. Auf „Herunterladen“ klicken. Der Browser speichert `Tokio 2027.html` in den Ordner „Downloads“.
2. Die heruntergeladene Datei in den Ordner `~/Claude/TokioOrte/` ziehen und **„Ersetzen“** wählen. Gleicher Name und gleicher Ordner, damit die Merkliste im Browser erhalten bleibt.
3. Die App neu laden.

Eine Webseite darf sich nicht selbst überschreiben. Deshalb muss der letzte Schritt (Ersetzen) von Hand erfolgen. Das automatische Ersetzen ginge nur mit Skripten außerhalb des Browsers (Weg 2).

## Weg 2: Doppelklick-Skript (ersetzt automatisch)

Einmal im Terminal anlegen:

```
cat > "$HOME/Claude/TokioOrte/Aktualisieren.command" <<'EOF'
#!/bin/bash
cd "$HOME/Claude/TokioOrte" || exit 1
curl -fL -o .neu.html "https://raw.githubusercontent.com/trax777-cyber/tokio-2027/main/Tokio-2027-offline.html" && mv .neu.html "Tokio 2027.html" && echo "Aktualisiert am $(date)" || echo "Fehler: nicht aktualisiert"
EOF
chmod +x "$HOME/Claude/TokioOrte/Aktualisieren.command"
```

Danach genügt ein Doppelklick auf `Aktualisieren.command`. Beim ersten Mal fragt macOS eventuell nach (Rechtsklick, Öffnen).

## Was man beachten sollte

- Vor dem ersten Ersetzen einen Screenshot der Merkliste machen und die alte Datei sichern (`cp "Tokio 2027.html" "Tokio 2027 (alt).html"`). Ob die alte Mac-Fassung dieselben Speicherschlüssel hat, ist unbekannt.
- Die Datei am Mac nicht selbst bearbeiten, sie wird beim Aktualisieren überschrieben. Neue Orte kommen über das Repository.
- Die Merkliste liegt im Browser für genau diesen Dateipfad. Anderer Ordner oder anderer Browser bedeutet andere Merkliste. Zum Mitnehmen gibt es in der App „Merkliste teilen“.
- `version.json` im Repository enthält die aktuelle Versionsnummer. `quelle/build.py` erzeugt sie zusammen mit der Datei.
