"""Lab 1 — Triage del dataset (SOLUZIONE di riferimento).

Il metodo è quello della demo: carica → guarda l'output → diagnostica. Qui non
si ripara ancora niente: si compila la **tabella di triage**, un esito per file.

    python triage.py        → stampa la tabella e scrive triage.md
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import Document, load

DATASET = Path(__file__).parent.parent / "dataset"
SOGLIA_VUOTO = 50          # sotto questi caratteri l'estrazione è "vuota"


def carica_robusto(path: str) -> list[Document]:
    """Come `aikit.load`, ma gestisce l'edge case dell'encoding.

    I loader di aikit leggono in utf-8; i file "storici" di Windows/Excel sono
    spesso in latin-1. Se la decodifica fallisce, rileggiamo a mano: il triage
    deve DIAGNOSTICARE, non arrendersi al primo accento.
    """
    try:
        return load(path)
    except UnicodeDecodeError:
        testo = Path(path).read_bytes().decode("latin-1")
        return [Document(testo, {"source": path, "type": "txt", "encoding": "latin-1"})]


def triaga_file(path: str) -> tuple[str, str, str]:
    """Un file → (esito, dettaglio, anteprima)."""
    try:
        docs = carica_robusto(path)
    except Exception as e:                      # corrotti, formati ignoti…
        return "ERRORE", f"{type(e).__name__}: {e}", "—"

    testo = "\n".join(d.text for d in docs)
    anteprima = " ".join(testo.split())[:90] or "—"
    if len(testo.strip()) < SOGLIA_VUOTO:
        return "VUOTO", f"{len(testo.strip())} char estratti", anteprima
    return "OK", f"{len(testo)} char · {len(docs)} document(i)", anteprima


def triage_dataset() -> dict[str, tuple[str, str, str]]:
    """Tutto il dataset → {nome_file: (esito, dettaglio, anteprima)}."""
    return {p.name: triaga_file(str(p)) for p in sorted(DATASET.iterdir())}


# ------------------------------------------------- report e stampa
def scrivi_report(risultati: dict, out: str = "triage.md") -> None:
    """Scrive la tabella di triage in markdown (si porta allo show & tell)."""
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
    risultati = triage_dataset()
    larghezza = max(len(n) for n in risultati)
    for nome, (esito, dettaglio, anteprima) in risultati.items():
        print(f"{nome:<{larghezza}}  {esito:<7} {dettaglio}")
        print(f"{'':<{larghezza}}          » {anteprima}")
    scrivi_report(risultati)
    print("\nTabella scritta in triage.md")
