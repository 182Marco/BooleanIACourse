"""strumenti_cartella.py — i tool di cartella dell'assistente: elencare, cercare, leggere.

L'assistente lavora sulla cartella dell'ufficio (ufficio/): i documenti dell'ufficio del
personale e gli export del gestionale in CSV. I tre tool non sono fatti per Valtesa: sono
gli stessi che un coding agent usa su qualunque cartella. Il confine lo tiene il codice:
ogni percorso che arriva dal modello passa da dentro_la_radice(), che rifiuta quello che
sta fuori da ufficio/.

Da scrivere con il coding agent, da specifica-strumenti.md: qui ci sono solo le firme.
"""
from pathlib import Path

from agents import function_tool

RADICE = (Path(__file__).parent / "ufficio").resolve()
MAX_CARATTERI = 20_000                              # quanto rimanda leggi_file, al massimo
MAX_RISULTATI = 30                                  # quante righe rimanda cerca, al massimo


def dentro_la_radice(percorso: str) -> Path:
    """Il percorso assoluto di un file della cartella; ValueError se è fuori dalla cartella."""
    raise NotImplementedError("da scrivere: vedi specifica-strumenti.md")


@function_tool
def elenca_file() -> str:
    """Elenca i file della cartella dell'ufficio del personale di Valtesa (documenti ed export
    del gestionale), uno per riga, con il percorso da passare a leggi_file."""
    raise NotImplementedError("da scrivere: vedi specifica-strumenti.md")


@function_tool
def leggi_file(percorso: str) -> str:
    """Legge un file di testo della cartella dell'ufficio e ne rimanda il contenuto.

    Args:
        percorso: il percorso del file, come lo dà elenca_file.
    """
    raise NotImplementedError("da scrivere: vedi specifica-strumenti.md")


@function_tool
def cerca(testo: str) -> str:
    """Cerca un testo in tutti i file della cartella dell'ufficio (senza distinguere maiuscole
    e minuscole) e rimanda le righe che lo contengono, nella forma file:riga: testo.

    Args:
        testo: la parola o la frase da cercare.
    """
    raise NotImplementedError("da scrivere: vedi specifica-strumenti.md")
