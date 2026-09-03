"""Il banco di prova: chiedere al modello qualcosa sul documento caricato.

Come si sa se un loader funziona *davvero*? Non basta vedere del testo: deve
essere testo che il modello capisce. Quindi, dopo ogni loader, gli si fa una
domanda sul documento.

`ask()` è volutamente NAIVE: infila TUTTO il testo nel prompt, niente ricerca.
È la baseline della lezione — funziona su un documento, non regge su cinquecento.

Qui dentro c'è anche `mostra()`, l'helper di stampa usato dal main di
`working/loaders.py`: la formattazione dell'output è già scritta, così il
tempo va sui loader.

Non si tocca: si importa.
"""
import os

from pathlib import Path

from aikit.llm_client import LLMClient

ISTRUZIONI = (
    "Rispondi alla domanda usando SOLO il documento fornito. "
    "Se l'informazione non è nel documento, dillo invece di inventare."
)

_client = None


def ask(testo, domanda):
    """La risposta del modello alla domanda, leggendo solo `testo`.

    Il client si crea alla prima chiamata: così tutta la parte di loading
    gira anche senza chiave nel .env.
    """
    global _client
    if _client is None:
        _client = LLMClient(temperature=0)   # banco di prova: stessa risposta a ogni giro
    prompt = f'Documento:\n"""\n{testo}\n"""\n\nDomanda: {domanda}'
    return _client.chat([{"role": "user", "content": prompt}], instructions=ISTRUZIONI)


def mostra(docs, titolo):
    """Stampa che cosa è uscito da un loader: quanti Document, metadata, anteprima."""
    print(f"\n=== {titolo}: {len(docs)} Document")
    for d in docs[:3]:
        meta = dict(d.metadata)
        if "source" in meta:          # a schermo basta il nome del file
            meta["source"] = Path(meta["source"]).name
        anteprima = " ".join(d.text.split())[:88]
        print(f"  {meta}")
        print(f"    {len(d.text):5d} car · {anteprima}…")
    if len(docs) > 3:
        print(f"  … e altri {len(docs) - 3}")


def rispondi(docs, domanda):
    """Fa la domanda al modello su tutti i Document passati, e stampa la risposta."""
    print(f"  🤖 {domanda}")
    if not os.getenv("OPENAI_API_KEY", "").strip():
        print("     (nessuna chiave nel .env: il caricamento gira lo stesso, "
              "la domanda no)")
        return
    testo = "\n\n".join(d.text for d in docs)
    for riga in ask(testo, domanda).strip().splitlines():
        print(f"     {riga}")
