#!/usr/bin/env python3
"""WCAG-Kontrasttabelle für die Farb-Tokens (Ist = App heute, Soll = docs/soll.css).
Aufruf: python3 tools/kontrast.py   (gibt eine Markdown-Tabelle aus; ✗ = Ziel verfehlt)"""

def _lin(v): return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
def _lum(h): h = h.lstrip('#'); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4)); return 0.2126*_lin(r) + 0.7152*_lin(g) + 0.0722*_lin(b)
def ratio(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

IST_HELL = dict(paper='#f2f0eb', card='#ffffff', ink='#23262b', soft='#5d6166', line='#d8d4c9', indigo='#2f3e50', indigoS='#e2e7ec',
                verm='#b1462f', vermS='#f4e4df', gold='#97702a', goldS='#f1e8d4', sage='#4d6a52', sageS='#e3ebe3', focus='#2f6fed')
IST_DUNKEL = dict(paper='#191b1e', card='#24262a', ink='#ece9e2', soft='#a7aab0', line='#35383d', indigo='#9db4cc', indigoS='#263041',
                  verm='#df917c', vermS='#3a2521', gold='#d3b06a', goldS='#3a3120', sage='#9bc0a1', sageS='#22301f', focus='#2f6fed')
SOLL_HELL = dict(IST_HELL, verm='#ae452e', gold='#836124', lineS='#8b8165', focus='#145ce9')
SOLL_DUNKEL = dict(IST_DUNKEL, lineS='#6c727c', focus='#568af0')

# (Beschreibung, Vordergrund Ist, Hintergrund, Ziel, Vordergrund Soll)
PAARE = [
 ('Fließtext', 'ink', 'paper', 4.5, 'ink'), ('Gedämpfter Text', 'soft', 'paper', 4.5, 'soft'), ('Gedämpfter Text auf Karte', 'soft', 'card', 4.5, 'soft'),
 ('Notizzeile', 'verm', 'paper', 4.5, 'verm'), ('Aktiver Tab', 'verm', 'vermS', 4.5, 'verm'),
 ('Stempel Essen', 'verm', 'vermS', 3.0, 'verm'), ('Stempel Café', 'gold', 'goldS', 3.0, 'gold'), ('Stempel Shop', 'indigo', 'indigoS', 3.0, 'indigo'), ('Stempel Ruhe', 'sage', 'sageS', 3.0, 'sage'),
 ('Knopf Gemerkt', 'gold', 'goldS', 4.5, 'gold'), ('Knopf Besucht', 'sage', 'sageS', 4.5, 'sage'),
 ('Aktiver Chip', 'paper', 'indigo', 4.5, 'paper'), ('Zähler Merkliste', 'paper', 'gold', 4.5, 'paper'), ('Zähler Filter', 'paper', 'verm', 4.5, 'paper'),
 ('Stern gemerkt', 'gold', 'paper', 3.0, 'gold'), ('Stern ungemerkt', 'line', 'paper', 3.0, 'soft'),
 ('Rand Eingabefeld', 'line', 'card', 3.0, 'lineS'), ('Fokusring', 'focus', 'paper', 3.0, 'focus'),
]

def zelle(r, ziel): return f"{r:.2f}".replace('.', ',') + (' ✓' if r >= ziel else ' ✗')

if __name__ == '__main__':
    print('| Paar | Ziel | Ist hell | Soll hell | Ist dunkel | Soll dunkel |\n|---|---:|---:|---:|---:|---:|')
    for name, f, b, ziel, f2 in PAARE:
        print(f"| {name} | {str(ziel).replace('.', ',')}:1 | {zelle(ratio(IST_HELL[f], IST_HELL[b]), ziel)} | {zelle(ratio(SOLL_HELL[f2], SOLL_HELL[b]), ziel)} | "
              f"{zelle(ratio(IST_DUNKEL[f], IST_DUNKEL[b]), ziel)} | {zelle(ratio(SOLL_DUNKEL[f2], SOLL_DUNKEL[b]), ziel)} |")
