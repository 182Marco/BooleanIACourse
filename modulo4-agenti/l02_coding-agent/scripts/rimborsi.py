"""Controllo delle note spese di Valtesa S.r.l. contro i massimali della policy trasferte.

Uso: python rimborsi.py   -> stampa l'esito di tutte le note spese in dati/note_spese.csv
"""
import csv
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


def controlla(nota):
    """True se l'importo della nota rientra nel massimale."""
    limite = massimale(nota["voce"], nota["citta"], nota["giorno"])
    return float(nota["importo"]) <= limite


def main():
    with open(NOTE_SPESE, newline="", encoding="utf-8") as f:
        note = list(csv.DictReader(f))
    fuori = 0
    for nota in note:
        limite = massimale(nota["voce"], nota["citta"], nota["giorno"])
        ok = float(nota["importo"]) <= limite
        if not ok:
            fuori += 1
        esito = "ok" if ok else f"FUORI MASSIMALE ({limite:.2f})"
        print(f"{nota['id']:>5}  {nota['dipendente']:<18} {nota['voce']:<8} {nota['citta']:<8} {nota['giorno']}  {float(nota['importo']):>7.2f}  {esito}")
    print(f"\n{len(note)} note spese, {fuori} fuori massimale")


if __name__ == "__main__":
    main()
