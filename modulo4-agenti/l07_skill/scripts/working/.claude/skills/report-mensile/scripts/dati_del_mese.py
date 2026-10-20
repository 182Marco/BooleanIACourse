"""In quali file di dati/ ci sono le note spese di un mese, e cosa manca per farne il report.

Uso (dalla cartella del progetto):
  python .claude/skills/report-mensile/scripts/dati_del_mese.py 2026-07

Per dati/note_spese.csv e per ogni export (dati/export-*.csv): le note del mese e il totale,
le colonne che mancano rispetto a note_spese.csv, le città senza massimali in dati/massimali.csv.
Se il mese non ha note in nessun file esce con codice 1. Legge e basta: non scrive niente.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

CARTELLA = Path(__file__).resolve().parents[4]     # scripts -> report-mensile -> skills -> .claude -> progetto
DATI = CARTELLA / "dati"
NOTE_SPESE = DATI / "note_spese.csv"
MASSIMALI = DATI / "massimali.csv"


def carica(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        lettore = csv.DictReader(f)
        return lettore.fieldnames or [], list(lettore)


def euro(valore):
    """1234.5 -> «1.234,50 €», come report.py."""
    return f"{valore:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    parser = argparse.ArgumentParser(description="Le note spese di un mese, file per file.")
    parser.add_argument("mese", help="il mese, AAAA-MM (per esempio 2026-07)")
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}", args.mese):
        sys.exit(f"mese non valido: {args.mese!r} (serve AAAA-MM, per esempio 2026-07)")

    colonne_attese, _ = carica(NOTE_SPESE)
    citta_con_massimali = {riga["citta"] for riga in carica(MASSIMALI)[1]}

    note_tot = 0
    importo_tot = 0.0
    for percorso in [NOTE_SPESE, *sorted(DATI.glob("export-*.csv"))]:
        colonne, righe = carica(percorso)
        note = [nota for nota in righe if nota["giorno"].startswith(args.mese + "-")]
        importo = sum(float(nota["importo"]) for nota in note)
        note_tot += len(note)
        importo_tot += importo

        print(f"{percorso.relative_to(CARTELLA)}: {len(note)} note di {args.mese}, {euro(importo)}")
        mancanti = [c for c in colonne_attese if c not in colonne]
        if mancanti:
            print(f"  colonne mancanti: {', '.join(mancanti)}")
        # solo le città delle note del mese: le altre non entrano nel report
        senza = sorted({nota["citta"] for nota in note} - citta_con_massimali)
        if senza:
            print(f"  città senza massimale: {', '.join(senza)}")

    if not note_tot:
        print(f"\nnessuna nota per {args.mese}")
        sys.exit(1)
    print(f"\nIn tutto: {note_tot} note di {args.mese}, {euro(importo_tot)}")


if __name__ == "__main__":
    main()
