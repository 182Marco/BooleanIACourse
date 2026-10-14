"""strumenti_cartella.py — i tool di cartella dell'assistente: elencare, cercare, leggere.

L'assistente lavora sulla cartella dell'ufficio (ufficio/): i documenti dell'ufficio del
personale e gli export del gestionale in CSV. I tre tool non sono fatti per Valtesa: sono
gli stessi che un coding agent usa su qualunque cartella. Il confine lo tiene il codice:
ogni percorso che arriva dal modello passa da dentro_la_radice(), che rifiuta quello che
sta fuori da ufficio/.

La versione del docente, scritta in Modulo 4 · Lezione 4.
"""
from pathlib import Path

from agents import function_tool

RADICE = (Path(__file__).parent / "ufficio").resolve()
MAX_CARATTERI = 20_000                              # quanto rimanda leggi_file, al massimo
MAX_RISULTATI = 30                                  # quante righe rimanda cerca, al massimo


def dentro_la_radice(percorso: str) -> Path:
    """Il percorso assoluto di un file della cartella; ValueError se è fuori dalla cartella."""
    completo = (RADICE / percorso).resolve()        # risolve .. e i link simbolici; un percorso assoluto resta com'è
    if not completo.is_relative_to(RADICE):
        raise ValueError(f"{percorso} è fuori dalla cartella dell'ufficio")
    return completo


@function_tool
def elenca_file() -> str:
    """Elenca i file della cartella dell'ufficio del personale di Valtesa (documenti ed export
    del gestionale), uno per riga, con il percorso da passare a leggi_file."""
    righe = []
    for file in sorted(RADICE.rglob("*")):
        if file.is_file() and file.resolve().is_relative_to(RADICE):   # un link che porta fuori non si elenca
            righe.append(str(file.relative_to(RADICE)))
    return "\n".join(righe)


@function_tool
def leggi_file(percorso: str) -> str:
    """Legge un file di testo della cartella dell'ufficio e ne rimanda il contenuto.

    Args:
        percorso: il percorso del file, come lo dà elenca_file.
    """
    file = dentro_la_radice(percorso)
    testo = file.read_text(encoding="utf-8", errors="replace")
    return testo[:MAX_CARATTERI]


@function_tool
def cerca(testo: str) -> str:
    """Cerca un testo in tutti i file della cartella dell'ufficio (senza distinguere maiuscole
    e minuscole) e rimanda le righe che lo contengono, nella forma file:riga: testo.

    Args:
        testo: la parola o la frase da cercare.
    """
    risultati = []
    for file in sorted(RADICE.rglob("*")):
        if not file.is_file() or not file.resolve().is_relative_to(RADICE):
            continue                                # un link che porta fuori non si legge
        righe = file.read_text(encoding="utf-8", errors="replace").splitlines()
        for numero, riga in enumerate(righe, start=1):
            if testo.lower() in riga.lower():
                risultati.append(f"{file.relative_to(RADICE)}:{numero}: {riga.strip()}")
    if not risultati:
        return f"Nessuna riga contiene «{testo}»."
    return "\n".join(risultati[:MAX_RISULTATI])
