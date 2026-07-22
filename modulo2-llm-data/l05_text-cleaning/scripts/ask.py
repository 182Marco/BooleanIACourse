"""L'unico runner della lezione: before/after del cleaning e prova col chatbot.

Le ricette di cleaning vivono in `aikit/clean.py` (`PIPELINES` + `pipeline_for`):
per lavorare su un documento nuovo si tocca SOLO quel file. Qui si guarda l'effetto.

    python ask.py
        → before/after (offline) su tutti i documenti in sample_docs/

    python ask.py sample_docs/frankenstein.txt
        → before/after di un documento, con estratto prima/dopo (offline)

    python ask.py sample_docs/wikipedia_nlp.html "che cos'è l'NLP?"
        → confronto della RISPOSTA del chatbot su testo SPORCO vs PULITO
          (serve OPENAI_API_KEY nel .env)

Perché conta: quel testo lo diamo al chatbot (ask(), come a L16). Su testo sporco
la risposta peggiora e costa di più; pulito, migliora.
"""
import sys
from pathlib import Path

from aikit import Document, clean, load
from aikit.clean import pipeline_for

ISTRUZIONI = (
    "Rispondi alla domanda usando SOLO il documento fornito. "
    "Se l'informazione non è nel documento, dillo invece di inventare."
)

CAMPIONI = [
    "sample_docs/frankenstein.txt",
    "sample_docs/arxiv_1905.00075.pdf",
    "sample_docs/wikipedia_nlp.html",
]

_client = None


def _get_client():
    # creato solo quando serve: così il before/after gira anche senza chiave
    global _client
    if _client is None:
        from llm_client import LLMClient
        _client = LLMClient()
    return _client


def ask(testo, domanda: str) -> str:
    if isinstance(testo, Document):
        testo = testo.text
    messaggi = [{
        "role": "user",
        "content": f'Documento:\n"""\n{testo}\n"""\n\nDomanda: {domanda}',
    }]
    return _get_client().chat(messaggi, instructions=ISTRUZIONI)


def _grezzo_e_pulito(path: str):
    grezzo = "\n".join(d.text for d in load(path))
    return grezzo, clean(grezzo, pipeline_for(path))


def _report(path: str, anteprima: bool = False) -> None:
    grezzo, pulito = _grezzo_e_pulito(path)
    tolti = len(grezzo) - len(pulito)
    pct = (tolti / len(grezzo) * 100) if grezzo else 0
    print(f"\n### {path}")
    print(f"  prima: {len(grezzo):>7} char · dopo: {len(pulito):>7} char · "
          f"noise rimosso: {tolti} ({pct:.1f}%)")
    if anteprima:
        print("\n  --- prima (estratto) ---\n  " + grezzo[:400].replace("\n", "\n  "))
        print("\n  --- dopo (estratto) ---\n  " + pulito[:400].replace("\n", "\n  "))


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:                                   # before/after su tutti i campioni
        for s in CAMPIONI:
            _report(s)
    elif len(args) == 1:                           # before/after di un documento
        _report(args[0], anteprima=True)
    else:                                          # confronto col chatbot
        path, domanda = args[0], args[1]
        grezzo, pulito = _grezzo_e_pulito(path)
        client = _get_client()
        print(f"{path}\n\n🤖 {domanda}\n")
        print("  --- sul testo SPORCO ---")
        print("   ", ask(grezzo, domanda))
        print(f"     ({client.ultimo_uso[0]} token nel prompt)")
        print("\n  --- sul testo PULITO ---")
        print("   ", ask(pulito, domanda))
        print(f"     ({client.ultimo_uso[0]} token nel prompt)")
