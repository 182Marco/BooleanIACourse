"""dati_del_mese.py — in quali file di dati/ ci sono le note spese di un mese, e cosa manca.

Guarda note_spese.csv e gli export (export-*.csv): per ognuno le note del mese, il totale,
le colonne che mancano rispetto a note_spese.csv e le città che non hanno massimali.

Uso, dalla cartella del progetto:
    python .claude/skills/report-mensile/scripts/dati_del_mese.py 2026-07
"""
import csv
import sys
from collections import Counter
from pathlib import Path

DATI = Path(__file__).resolve().parents[4] / "dati"   # scripts/ → report-mensile/ → skills/ → .claude/ → progetto


def leggi(file):
    with open(file, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


mese = sys.argv[1]
colonne = list(leggi(DATI / "note_spese.csv")[0])
citta_con_massimale = {riga["citta"] for riga in leggi(DATI / "massimali.csv")}
trovato = False
for file in [DATI / "note_spese.csv"] + sorted(DATI.glob("export-*.csv")):
    note = [n for n in leggi(file) if n["giorno"].startswith(mese + "-")]
    if not note:
        print(f"{file.name}: nessuna nota di {mese}")
        continue
    trovato = True
    totale = sum(float(n["importo"]) for n in note)
    print(f"{file.name}: {len(note)} note di {mese}, totale {totale:.2f} €")
    mancanti = [c for c in colonne if c not in note[0]]
    if mancanti:
        print(f"  colonne che mancano rispetto a note_spese.csv: {', '.join(mancanti)}")
    if "notti" in mancanti:
        print(f"  righe di hotel senza il numero di notti: {sum(n['voce'] == 'hotel' for n in note)}")
    senza = Counter(n["citta"] for n in note if n["citta"] not in citta_con_massimale)
    for citta, quante in senza.items():
        print(f"  città senza massimale in massimali.csv: {citta} ({quante} note)")
if not trovato:
    print(f"Nessun file di dati/ ha note di {mese}.")
