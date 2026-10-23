"""Le date e l'indirizzo di posta per l'ingresso di un nuovo assunto, dalla procedura PR-PER-04.

Uso:
  python scadenze.py 205                  -> i dati e le date dell'ingresso 205 di dati/assunzioni.csv
  python scadenze.py --tutti              -> tutti gli ingressi
  python scadenze.py --entro 2026-11-09   -> la data 5 giorni lavorativi dopo, per i solleciti
I giorni lavorativi sono dal lunedì al venerdì, senza le festività nazionali.
"""
import argparse
import csv
import unicodedata
from datetime import date, timedelta
from pathlib import Path

CARTELLA = Path(__file__).parent
ASSUNZIONI = CARTELLA / "dati" / "assunzioni.csv"
DIPENDENTI = CARTELLA / "dati" / "dipendenti.csv"

# le festività nazionali: giorno e mese, più il lunedì dopo Pasqua, che cambia ogni anno
# (qui gli anni degli ingressi: per un anno che non c'è, va aggiunto)
FESTIVITA = ["01-01", "01-06", "04-25", "05-01", "06-02", "08-15", "11-01", "12-08", "12-25", "12-26"]
PASQUETTA = {2026: date(2026, 4, 6), 2027: date(2027, 3, 29), 2028: date(2028, 4, 17)}
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]


def lavorativo(giorno):
    """True se il giorno è lavorativo: dal lunedì al venerdì e non festivo."""
    if giorno.weekday() >= 5:
        return False
    return giorno.strftime("%m-%d") not in FESTIVITA and giorno != PASQUETTA.get(giorno.year)


def lavorativi_prima(giorno, n):
    """Il giorno che sta n giorni lavorativi prima di giorno."""
    while n > 0:
        giorno -= timedelta(days=1)
        if lavorativo(giorno):
            n -= 1
    return giorno


def lavorativi_dopo(giorno, n):
    """Il giorno che sta n giorni lavorativi dopo giorno."""
    while n > 0:
        giorno += timedelta(days=1)
        if lavorativo(giorno):
            n -= 1
    return giorno


def mesi_dopo(giorno, mesi):
    """Lo stesso giorno, qualche mese dopo (il 31 diventa l'ultimo giorno del mese, se serve)."""
    anno, mese = divmod(giorno.month - 1 + mesi, 12)
    anno, mese = giorno.year + anno, mese + 1
    for numero in (giorno.day, 30, 29, 28):
        try:
            return date(anno, mese, numero)
        except ValueError:
            continue


def scrivi(giorno):
    return f"{GIORNI[giorno.weekday()]} {giorno.strftime('%d/%m/%Y')}"


def semplice(testo):
    """Minuscolo, senza accenti, spazi e apostrofi: «D'Angelo» diventa «dangelo»."""
    testo = unicodedata.normalize("NFKD", testo).encode("ascii", "ignore").decode()
    return "".join(c for c in testo.lower() if c.isalpha())


def indirizzo(nome, cognome):
    """nome.cognome@valtesa.it; con un omonimo tra i dipendenti, un numero dopo il cognome (art. 6):
    il primo che arriva dopo un dipendente con lo stesso nome è il 2, poi il 3, e così via."""
    with open(DIPENDENTI, newline="", encoding="utf-8") as f:
        omonimi = sum(1 for d in csv.DictReader(f)
                      if semplice(d["nome"]) == semplice(nome) and semplice(d["cognome"]) == semplice(cognome))
    numero = str(omonimi + 1) if omonimi else ""
    return f"{semplice(nome)}.{semplice(cognome)}{numero}@valtesa.it"


def carica():
    with open(ASSUNZIONI, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def scadenze(ingresso):
    """Le date della procedura per un ingresso nel giorno dato."""
    quarta = ingresso + timedelta(days=27)              # l'ultimo giorno della quarta settimana
    while not lavorativo(quarta):
        quarta -= timedelta(days=1)
    return {
        "10 giorni lavorativi prima (lettera di benvenuto, richiesta delle dotazioni)": lavorativi_prima(ingresso, 10),
        "ultimo giorno lavorativo prima (visita medica, per Produzione e Logistica)": lavorativi_prima(ingresso, 1),
        "primo giorno": ingresso,
        "fine della quarta settimana (colloquio di verifica)": quarta,
        "30 giorni dall'ingresso": ingresso + timedelta(days=30),
        "60 giorni dall'ingresso": ingresso + timedelta(days=60),
        "90 giorni dall'ingresso": ingresso + timedelta(days=90),
        "6 mesi dall'ingresso (scelta sul TFR)": mesi_dopo(ingresso, 6),
    }


def testo(assunto):
    """Una scheda di testo per un ingresso: chi è, l'indirizzo di posta, le date."""
    ingresso = date.fromisoformat(assunto["data_ingresso"])
    righe = [f"{assunto['nome']} {assunto['cognome']} (id {assunto['id']}): {assunto['ruolo']}, "
             f"{assunto['reparto']} a {assunto['sede']}, contratto {assunto['contratto']}",
             f"note: {assunto['note'] or '-'}",
             f"indirizzo di posta: {indirizzo(assunto['nome'], assunto['cognome'])}"]
    for cosa, giorno in scadenze(ingresso).items():
        righe.append(f"{cosa}: {scrivi(giorno)}")
    return "\n".join(righe)


def main():
    parser = argparse.ArgumentParser(description="Le date e l'indirizzo di posta per un nuovo assunto.")
    parser.add_argument("id", nargs="?", help="l'id dell'ingresso in dati/assunzioni.csv")
    parser.add_argument("--tutti", action="store_true", help="tutti gli ingressi")
    parser.add_argument("--entro", help="AAAA-MM-GG: la data 5 giorni lavorativi dopo")
    args = parser.parse_args()
    if args.entro:
        print(f"5 giorni lavorativi dopo {scrivi(date.fromisoformat(args.entro))}: "
              f"{scrivi(lavorativi_dopo(date.fromisoformat(args.entro), 5))}")
        return
    assunti = carica()
    scelti = assunti if args.tutti else [a for a in assunti if a["id"] == args.id]
    if not scelti:
        parser.error(f"nessun ingresso con id {args.id}: gli id sono {', '.join(a['id'] for a in assunti)}")
    print("\n\n".join(testo(a) for a in scelti))


if __name__ == "__main__":
    main()
