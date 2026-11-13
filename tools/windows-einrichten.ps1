# Tokio 2027: Windows-Einrichtung (nur ASCII, damit PowerShell 5 keine Zeichen verwechselt)
# Laedt die Offline-App von GitHub nach C:\AI\Tokio2027, legt Aktualisieren.bat und eine Desktop-Verknuepfung an.
# Kann beliebig oft ausgefuehrt werden: ersetzt die App, sichert die vorherige Fassung als "Tokio 2027 (alt).html".
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$ordner = 'C:\AI\Tokio2027'
$ziel   = Join-Path $ordner 'Tokio 2027.html'
$neu    = Join-Path $ordner '.neu.html'
$raw    = 'https://raw.githubusercontent.com/trax777-cyber/tokio-2027/main/'

New-Item -ItemType Directory -Force -Path $ordner | Out-Null

Invoke-WebRequest -Uri ($raw + 'Tokio-2027-offline.html') -OutFile $neu -UseBasicParsing
if ((Get-Item $neu).Length -lt 200000) { Remove-Item $neu -Force; throw 'Download zu klein, Datei nicht ersetzt.' }

if (Test-Path $ziel) { Copy-Item $ziel (Join-Path $ordner 'Tokio 2027 (alt).html') -Force }
Move-Item $neu $ziel -Force

# Aktualisieren.bat: laedt das Skript erneut und fuehrt es aus
$bat = '@echo off' + "`r`n" +
  'powershell -NoProfile -ExecutionPolicy Bypass -Command "iwr -UseBasicParsing ''' + $raw + 'tools/windows-einrichten.ps1'' -OutFile $env:TEMP\tokio-einrichten.ps1; & $env:TEMP\tokio-einrichten.ps1"' + "`r`n" +
  'pause' + "`r`n"
[IO.File]::WriteAllText((Join-Path $ordner 'Aktualisieren.bat'), $bat, [Text.Encoding]::ASCII)

# Desktop-Verknuepfung
try {
  $ws = New-Object -ComObject WScript.Shell
  $lnk = $ws.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Tokio 2027.lnk'))
  $lnk.TargetPath = $ziel
  $lnk.Save()
} catch { Write-Host 'Verknuepfung nicht angelegt (egal, Datei liegt im Ordner).' }

$v = ''
try { $v = (Invoke-WebRequest -Uri ($raw + 'version.json') -UseBasicParsing).Content.Trim() } catch {}
Write-Host ''
Write-Host "Fertig. App: $ziel"
if ($v) { Write-Host "Version: $v" }
Write-Host 'Immer dieselbe Datei im selben Browser oeffnen, sonst ist die Merkliste leer.'
