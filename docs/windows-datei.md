# Windows: lokale App einrichten

Die App ist eine einzelne Datei (`Tokio-2027-offline.html`, Schriften und Karten-Bibliothek stecken darin). Sie läuft ohne Server und ohne Internet, nur der Kartenhintergrund braucht Internet. Auf dem Windows-PC liegt sie in `C:\AI\Tokio2027\Tokio 2027.html`.

## Einrichten (einmal)

1. PowerShell öffnen (Startmenü, „PowerShell“ tippen, Enter). Administratorrechte sind nicht nötig.
2. Diesen Befehl einfügen und Enter drücken:

```
powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing 'https://raw.githubusercontent.com/trax777-cyber/tokio-2027/main/tools/windows-einrichten.ps1' -OutFile $env:TEMP\tokio-einrichten.ps1; & $env:TEMP\tokio-einrichten.ps1"
```

Das Skript legt `C:\AI\Tokio2027\` an, lädt die App als `Tokio 2027.html`, schreibt `Aktualisieren.bat` dazu und setzt eine Verknüpfung auf den Desktop.

Ohne Skript geht es auch von Hand: `Tokio-2027-offline.html` aus dem Repository herunterladen (GitHub, Datei öffnen, „Download raw file“), als `C:\AI\Tokio2027\Tokio 2027.html` speichern und mit Doppelklick im Browser öffnen.

## Aktualisieren

Doppelklick auf `C:\AI\Tokio2027\Aktualisieren.bat`. Die alte Fassung wird als `Tokio 2027 (alt).html` gesichert. Die App zeigt beim Öffnen auch selbst „Neue Version der App verfügbar“ (höchstens alle 6 Stunden, nur mit Internet).

## Merkliste mitnehmen

Merken, Besucht und Notizen liegen im Browser, gebunden an Dateipfad und Browser. Auf dem neuen PC ist die Merkliste deshalb zuerst leer.

- Am alten Gerät in der Merkliste „Merkliste teilen“ drücken. Der Text enthält einen Link mit `#m=…`.
- Diesen Link am neuen PC in den Browser einfügen, aber die lokale Datei muss dieselbe sein, in der ihr die App nutzt: Der Link der Live-Seite (`https://trax777-cyber.github.io/tokio-2027/#m=…`) öffnet die Live-Fassung. Zum Übernehmen in die lokale Datei die Adresse der lokalen Datei plus `#m=…` verwenden (Beispiel: `file:///C:/AI/Tokio2027/Tokio%202027.html#m=0.4.6`). Die App fragt, ob die Orte auf die Merkliste sollen.
- Besucht-Markierungen und Notizen gehen so nicht mit.

## Beachten

- Immer denselben Browser und dieselbe Datei im selben Ordner benutzen. Ordner oder Dateiname ändern bedeutet leere Merkliste.
- Die Datei nicht selbst bearbeiten, sie wird beim Aktualisieren überschrieben.
- Getestet ist das nur in der Linux-Prüfumgebung mit Chromium, nicht unter Windows (PowerShell-Skript, Verknüpfung und `file:///`-Adressen sind ungeprüft).
