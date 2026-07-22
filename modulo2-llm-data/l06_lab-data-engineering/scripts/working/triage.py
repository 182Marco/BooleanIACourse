"""Lab 1 — Triage del dataset: caricare TUTTO, capire cosa si rompe e perché.

Il metodo è quello della demo: carica → guarda l'output → diagnostica. Qui non
si ripara ancora niente (il cleaning è il Lab 2, LlamaParse viene dopo): si
compila la **tabella di triage**, un esito per ogni file del dataset.

Esiti possibili:
  OK      → il testo esce ed è plausibile (ma guarda l'anteprima: "esce del
            testo" non vuol dire "esce il testo GIUSTO"…)
  VUOTO   → il loader non solleva errori ma il testo estratto è (quasi) niente
  ERRORE  → il loader solleva un'eccezione: file corrotto, encoding sbagliato…

    python triage.py        → stampa la tabella e scrive triage.md

Completa i tre TODO dall'alto verso il basso; `python check_lab18.py` ti dice
a che punto sei.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import Document, load

DATASET = Path(__file__).parent.parent / "dataset"
SOGLIA_VUOTO = 50          # sotto questi caratteri l'estrazione è "vuota"


def carica_robusto(path: str) -> list[Document]:
    """Come `aikit.load`, ma gestisce l'edge case dell'encoding.

    TODO 1: i loader di aikit leggono in utf-8. Se `load(path)` solleva
    `UnicodeDecodeError`, rileggi il file a mano con encoding="latin-1"
    (l'encoding storico di Windows/Excel) e restituisci comunque una
    `[Document(...)]` con metadata `{"source": path, "type": "txt",
    "encoding": "latin-1"}`. Ogni altra eccezione deve PASSARE oltre
    (la gestisce triaga_file).
    """
    raise NotImplementedError("TODO 1: carica_robusto")


def triaga_file(path: str) -> tuple[str, str, str]:
    """Un file → (esito, dettaglio, anteprima).

    TODO 2:
    - chiama `carica_robusto(path)` dentro un try/except: se solleva,
      l'esito è "ERRORE" e il dettaglio è `f"{type(e).__name__}: {e}"`.
    - altrimenti unisci il testo dei Document; se i caratteri (strip) sono
      meno di SOGLIA_VUOTO l'esito è "VUOTO", altrimenti "OK".
    - dettaglio per i casi non-errore: f"{n_char} char · {n_doc} document(i)"
    - anteprima: i primi ~90 caratteri del testo, su una riga
      (" ".join(testo.split())[:90]) — è lì che si VEDE la tabella rotta.
    """
    raise NotImplementedError("TODO 2: triaga_file")


def triage_dataset() -> dict[str, tuple[str, str, str]]:
    """Tutto il dataset → {nome_file: (esito, dettaglio, anteprima)}.

    TODO 3: applica `triaga_file` a ogni file di DATASET (in ordine
    alfabetico: `sorted(DATASET.iterdir())`), usando come chiave `p.name`.
    """
    raise NotImplementedError("TODO 3: triage_dataset")


# ------------------------------------------------- fornito: report e stampa
def scrivi_report(risultati: dict, out: str = "triage.md") -> None:
    """Scrive la tabella di triage in markdown (la porti allo show & tell)."""
    righe = [
        "# Triage del dataset — Lab L18",
        "",
        "| File | Esito | Dettaglio | Anteprima |",
        "|---|---|---|---|",
    ]
    for nome, (esito, dettaglio, anteprima) in risultati.items():
        righe.append(f"| `{nome}` | {esito} | {dettaglio} | {anteprima} |")
    Path(__file__).parent.joinpath(out).write_text("\n".join(righe) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        risultati = triage_dataset()
    except NotImplementedError as e:
        raise SystemExit(f"Manca un pezzo: {e} — completa i TODO in triage.py")

    larghezza = max(len(n) for n in risultati)
    for nome, (esito, dettaglio, anteprima) in risultati.items():
        print(f"{nome:<{larghezza}}  {esito:<7} {dettaglio}")
        print(f"{'':<{larghezza}}          » {anteprima}")
    scrivi_report(risultati)
    print("\nTabella scritta in triage.md")
