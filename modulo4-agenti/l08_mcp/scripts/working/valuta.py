"""valuta.py — il test dell'assistente: le domande di domande.json, una alla volta.

Ogni domanda va all'assistente in una sessione nuova, con rispondi() di assistente.py: quello
che cambiate in assistente.py e in strumenti_cartella.py vale anche qui. Per ogni domanda:
giusta o sbagliata, chiamate al modello e token. Una risposta è giusta se contiene tutte le
parti di "controllo" della domanda (espressioni regolari, senza distinguere maiuscole). In
fondo il totale e il costo, e una riga in output/valutazioni.csv, per confrontare prima e dopo.

Questo file, domande.json e domande-extra.json non si cambiano: sono il metro con cui misurate.

Uso:  python valuta.py                     tutte le domande
      python valuta.py --solo 1,5          solo alcune
      python valuta.py --file domande-extra.json   le domande più difficili, per l'estensione
      python valuta.py --traccia           con la traccia di ogni risposta
      python valuta.py --nota "PDF letti"  una nota sulla riga di valutazioni.csv
"""
import argparse
import asyncio
import csv
import json
import re
from datetime import datetime
from pathlib import Path

from agents import MaxTurnsExceeded, SQLiteSession

import assistente
from aikit.llm_client import cost_usd

CARTELLA = Path(__file__).parent
DOMANDE = CARTELLA / "domande.json"
VALUTAZIONI = CARTELLA / "output" / "valutazioni.csv"


def giusta(risposta, controllo):
    """True se la risposta contiene tutte le parti del controllo."""
    return all(re.search(parte, risposta, re.IGNORECASE) for parte in controllo)


def usage_di(result_o_errore):
    """Chiamate e token di un run, anche di uno finito con MaxTurnsExceeded."""
    contesto = getattr(result_o_errore, "context_wrapper", None)
    if contesto is None:                            # l'eccezione porta i dati del run in run_data
        dati = getattr(result_o_errore, "run_data", None)
        contesto = getattr(dati, "context_wrapper", None)
    if contesto is None:
        return 0, 0, 0
    u = contesto.usage
    return u.requests, u.input_tokens, u.output_tokens


async def valuta(domande, traccia):
    righe = []
    for d in domande:
        sessione = SQLiteSession(f"valuta-{d['id']}")   # una sessione nuova, in memoria
        try:
            result = await assistente.rispondi(d["domanda"], sessione)
        except MaxTurnsExceeded as errore:
            risposta = f"(nessuna risposta dopo {assistente.MAX_TURNI} chiamate)"
            chiamate, token_in, token_out = usage_di(errore)
            if traccia and errore.run_data is not None:   # la traccia fino al limite
                assistente.stampa_traccia(errore.run_data)
        else:
            if result is None:                      # uscita a metà di un'approvazione
                risposta, chiamate, token_in, token_out = "(uscita a metà)", 0, 0, 0
            else:
                risposta = str(result.final_output)
                chiamate, token_in, token_out = usage_di(result)
                if traccia:
                    assistente.stampa_traccia(result)
        ok = giusta(risposta, d["controllo"])
        print(f"{d['id']:>3}  {'giusta   ' if ok else 'SBAGLIATA'}  {chiamate:>3} chiamat{'a' if chiamate == 1 else 'e'}  {token_in:>7} token  "
              f"{risposta.replace(chr(10), ' ')[:90]}")
        righe.append((ok, chiamate, token_in, token_out))
    return righe


def main():
    parser = argparse.ArgumentParser(description="Il test dell'assistente sulle domande di domande.json.")
    parser.add_argument("--file", default="domande.json", help="il file delle domande")
    parser.add_argument("--solo", help="le domande da fare, per esempio 1,5,7")
    parser.add_argument("--traccia", action="store_true", help="stampa la traccia di ogni risposta")
    parser.add_argument("--nota", default="", help="una nota per la riga di valutazioni.csv")
    args = parser.parse_args()

    domande = json.loads((CARTELLA / args.file).read_text(encoding="utf-8"))
    if args.solo:
        scelte = {int(x) for x in args.solo.split(",")}
        domande = [d for d in domande if d["id"] in scelte]
    print(f"  #  esito      chiamate     token  risposta")
    righe = asyncio.run(valuta(domande, args.traccia))

    giuste = sum(1 for r in righe if r[0])
    token_in = sum(r[2] for r in righe)
    token_out = sum(r[3] for r in righe)
    costo = cost_usd(assistente.MODELLO, token_in, token_out)
    print(f"\n{giuste} su {len(righe)} giuste · {sum(r[1] for r in righe)} chiamate · "
          f"{token_in} token in, {token_out} out · ${costo:.4f}")

    VALUTAZIONI.parent.mkdir(exist_ok=True)
    nuovo = not VALUTAZIONI.exists()
    with VALUTAZIONI.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if nuovo:
            w.writerow(["quando", "nota", "domande", "giuste", "token_in", "token_out", "costo_usd"])
        w.writerow([datetime.now().isoformat(timespec="seconds"), args.nota,
                    " ".join(str(d["id"]) for d in domande), giuste, token_in, token_out, f"{costo:.4f}"])


if __name__ == "__main__":
    main()
