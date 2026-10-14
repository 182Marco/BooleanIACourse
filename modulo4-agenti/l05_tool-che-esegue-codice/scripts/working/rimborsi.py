"""Controllo delle note spese di Valtesa S.r.l. contro i massimali della policy trasferte.

Uso:
  python rimborsi.py                            -> tutte le note spese di dati/note_spese.csv
  python rimborsi.py dati/export-ottobre.csv    -> le note di un altro export del gestionale
  python rimborsi.py --dipendente "Luca Ferri"  -> solo le note di una persona
In fondo all'output il riepilogo per città e il totale.
"""
import argparse
import csv
from collections import Counter
from pathlib import Path

CARTELLA = Path(__file__).parent
MASSIMALI = CARTELLA / "dati" / "massimali.csv"
NOTE_SPESE = CARTELLA / "dati" / "note_spese.csv"


def carica_massimali():
    with open(MASSIMALI, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def massimale(voce, citta, giorno):
    """Il massimale in euro per una voce di spesa in una città, valido nel giorno dato (AAAA-MM-GG)."""
    # Vale la riga più recente già in vigore nel giorno della spesa.
    # Le date sono in formato ISO, quindi si confrontano come stringhe.
    validi = [
        riga for riga in carica_massimali()
        if riga["voce"] == voce and riga["citta"] == citta and riga["valido_dal"] <= giorno
    ]
    if not validi:
        raise KeyError(f"nessun massimale per {voce} a {citta} il {giorno}")
    return float(max(validi, key=lambda riga: riga["valido_dal"])["massimale"])


def notti(nota):
    """Le notti della nota: per l'hotel la riga è il soggiorno (policy trasferte, art. 2 e 6).
    Negli export senza la colonna notti, e per le voci che non sono hotel (cella vuota), è una."""
    return int(nota.get("notti") or 1)


def limite_nota(nota):
    """Il massimale della nota in euro: per l'hotel, il massimale per notte per le notti del soggiorno."""
    return massimale(nota["voce"], nota["citta"], nota["giorno"]) * notti(nota)


def controlla(nota):
    """True se l'importo della nota rientra nel massimale."""
    return float(nota["importo"]) <= limite_nota(nota)


def main():
    parser = argparse.ArgumentParser(description="Controlla le note spese contro i massimali.")
    # in più: il file da controllare come argomento
    parser.add_argument("file", nargs="?", default=NOTE_SPESE,
                        help="l'export da controllare (senza: dati/note_spese.csv)")
    # modifica 1: solo le note di una persona
    parser.add_argument("--dipendente", help="solo le note di questa persona")
    args = parser.parse_args()

    with open(args.file, newline="", encoding="utf-8") as f:
        note = list(csv.DictReader(f))
    if args.dipendente:
        note = [nota for nota in note if nota["dipendente"] == args.dipendente]

    fuori = 0
    mancanti = 0                          # note di città senza massimali (i massimali li fissa l'autorizzazione)
    note_per_citta = Counter()
    fuori_per_citta = Counter()
    mancanti_per_citta = Counter()
    for nota in note:
        note_per_citta[nota["citta"]] += 1
        try:
            limite = limite_nota(nota)
        except KeyError:
            mancanti += 1
            mancanti_per_citta[nota["citta"]] += 1
            esito = "MASSIMALE MANCANTE"
        else:
            ok = float(nota["importo"]) <= limite
            if not ok:
                fuori += 1
                fuori_per_citta[nota["citta"]] += 1
            esito = "ok" if ok else f"FUORI MASSIMALE ({limite:.2f})"
        print(f"{nota['id']:>5}  {nota['dipendente']:<18} {nota['voce']:<8} {nota['citta']:<8} {nota['giorno']}  {float(nota['importo']):>7.2f}  {esito}")

    # modifica 2: il riepilogo per città, prima della riga dei totali
    print("\nPer città:")
    for citta in sorted(note_per_citta):
        riga = f"  {citta:<8} {note_per_citta[citta]:>5} note, {fuori_per_citta[citta]:>4} fuori massimale"
        if mancanti_per_citta[citta]:
            riga += f", {mancanti_per_citta[citta]} con massimale mancante"
        print(riga)
    # l'ultima riga resta identica quando non ci sono note senza massimale
    totale = f"\n{len(note)} note spese, {fuori} fuori massimale"
    if mancanti:
        totale += f", {mancanti} con massimale mancante"
    print(totale)


if __name__ == "__main__":
    main()
