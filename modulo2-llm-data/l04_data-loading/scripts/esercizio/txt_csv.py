"""Esercizio L16 — aggiungi un loader per .txt e .csv.

Avete visto il pattern quattro volte (pdf, docx, html, markdown). Ora tocca a voi:
due formati nuovi, stessa interfaccia `Document`.

Cosa fare:
  1. completate `load_txt` e `load_csv` qui sotto (devono tornare list[Document]
     coi giusti metadata: almeno source e type);
  2. agganciateli al dispatcher `load()` nel modulo loaders/ (oppure provateli a mano);
  3. verificate con `ask()` su un vostro file reale: "riassumi questo documento".

Per il CSV decidete voi la granularità: una riga = un Document, oppure tutto
insieme? (Suggerimento: dipende da cosa ci farete dopo nel retrieval.)
"""
from loaders.base import Document


def load_txt(path: str) -> list[Document]:
    # TODO: leggi il file di testo e torna [Document(text, {"source": ..., "type": "txt"})]
    raise NotImplementedError


def load_csv(path: str) -> list[Document]:
    # TODO: usa il modulo `csv` della stdlib; decidi la granularità (riga vs tutto)
    raise NotImplementedError
