"""Il riepilogo mensile delle note spese: punto di ripartenza a metà dell'obiettivo 3.

Uso:  python report.py 2026-07   -> per ora stampa i numeri nel terminale

C'è la parte che calcola: le note del mese, i totali per sede e per voce, le note fuori
massimale con il massimale applicato e l'eccedenza, con controlla() di rimborsi.py. Manca la
pagina HTML del ticket, con il grafico, in output/report-AAAA-MM.html.
Si copia nella cartella del progetto, da scripts/: cp ../ripartenza/report.py report.py
"""
import argparse
import csv
from collections import Counter

from rimborsi import CARTELLA, NOTE_SPESE, controlla, limite_nota

DIPENDENTI = CARTELLA / "dati" / "dipendenti.csv"
VOCI = ["pranzo", "cena", "hotel", "taxi"]


def carica(percorso):
    with open(percorso, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def riepilogo(note, sede_di):
    """I numeri del report: totali, per sede, per voce, e le note fuori massimale."""
    per_sede = Counter()
    note_per_sede = Counter()
    per_voce = Counter()
    fuori = []
    for nota in note:
        importo = float(nota["importo"])
        sede = sede_di[nota["dipendente_id"]]
        per_sede[sede] += importo
        note_per_sede[sede] += 1
        per_voce[nota["voce"]] += importo
        if not controlla(nota):
            riga = dict(nota)                       # la nota, più massimale ed eccedenza
            riga["limite"] = limite_nota(nota)
            riga["eccedenza"] = importo - riga["limite"]
            fuori.append(riga)
    return {
        "note": len(note),
        "totale": sum(float(nota["importo"]) for nota in note),
        "per_sede": per_sede,
        "note_per_sede": note_per_sede,
        "per_voce": per_voce,
        "fuori": fuori,
    }


def main():
    parser = argparse.ArgumentParser(description="Il riepilogo mensile delle note spese.")
    parser.add_argument("mese", help="il mese, AAAA-MM (per esempio 2026-07)")
    args = parser.parse_args()

    sede_di = {d["id"]: d["sede"] for d in carica(DIPENDENTI)}
    note = [nota for nota in carica(NOTE_SPESE) if nota["giorno"].startswith(args.mese + "-")]
    r = riepilogo(note, sede_di)
    print(f"{r['note']} note spese, {r['totale']:.2f} €")
    for sede in sorted(r["per_sede"]):
        print(f"  {sede:<8} {r['note_per_sede'][sede]:>4} note  {r['per_sede'][sede]:>9.2f} €")
    for voce in VOCI:
        print(f"  {voce:<8} {r['per_voce'][voce]:>9.2f} €")
    print(f"{len(r['fuori'])} fuori massimale:")
    for n in r["fuori"]:
        print(f"  {n['id']:>5}  {n['dipendente']:<18} {n['voce']:<8} {n['citta']:<8} {n['giorno']}  "
              f"{float(n['importo']):>7.2f}  massimale {n['limite']:.2f}, eccedenza {n['eccedenza']:.2f}")


if __name__ == "__main__":
    main()
