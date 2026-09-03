"""Lab 1 — Triage del dataset (SOLUZIONE di riferimento).

Stesso nome e stessa struttura di `working/triage.py`: il primo giro in testa
(la demo del docente), i tre TODO del Lab 1 risolti, il main a stadi. È UNA
soluzione possibile, non l'unica.

    python solutions/triage.py     (dalla cartella scripts/)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load

DATASET = Path(__file__).parent.parent / "dataset"
SOGLIA_VUOTO = 50          # sotto questi caratteri l'estrazione è "vuota"


# ------------------------------------------ 🎤 il primo giro (la demo)
def primo_giro():
    """Il metodo del giorno, su UN file: carica → guarda → diagnostica → correggi."""
    path = DATASET / "faq_prodotto.html"

    # 1 · CARICA
    docs = load(str(path))

    # 2 · GUARDA — mai fidarsi del "nessun errore": quanti caratteri? che aspetto ha?
    testo = "\n".join(d.text for d in docs)
    print(f"{path.name}: {len(docs)} document(i), {len(testo)} caratteri")
    print("--- inizio dell'output ---")
    print(testo[:300])
    print("…")

    # 3 · DIAGNOSTICA — il contenuto c'è, ma è annegato nel boilerplate web:
    #     cookie banner, menu, newsletter, footer. Al chatbot arriverebbe TUTTO.

    # 4 · CORREGGI — un primo fix, mirato: via le righe del cookie banner.
    #     (Il fix sistematico, con una ricetta per ogni file, è il Lab 2.)
    senza_cookie = "\n".join(l for l in testo.split("\n") if "cookie" not in l.lower())
    print(f"dopo il primo fix: {len(senza_cookie)} caratteri "
          f"({len(testo) - len(senza_cookie)} di cookie banner in meno)")


# --------------------------------------------------- ⌨️ Lab 1, risolto
def carica_testo(path: str) -> str:
    """Tutto il testo di un file, gestendo l'edge case dell'encoding.

    I file di testo vengono letti in utf-8; quelli "storici" di Windows/Excel
    sono spesso in latin-1. Se la decodifica fallisce, rileggiamo a mano: il triage
    deve DIAGNOSTICARE, non arrendersi al primo accento. Ogni altra eccezione
    passa oltre: la gestisce triaga_file.
    """
    try:
        return "\n".join(d.text for d in load(path))
    except UnicodeDecodeError:
        return Path(path).read_text(encoding="latin-1")


def triaga_file(path: str) -> tuple[str, str, str]:
    """Un file → (esito, dettaglio, anteprima)."""
    try:
        testo = carica_testo(path)
    except Exception as e:                      # corrotti, formati ignoti…
        return "ERRORE", f"{type(e).__name__}: {e}", "—"

    anteprima = " ".join(testo.split())[:90] or "—"
    if len(testo.strip()) < SOGLIA_VUOTO:
        return "VUOTO", f"{len(testo.strip())} char estratti", anteprima
    return "OK", f"{len(testo)} char", anteprima


def triage_dataset() -> dict[str, tuple[str, str, str]]:
    """Tutto il dataset → {nome_file: (esito, dettaglio, anteprima)}."""
    return {p.name: triaga_file(str(p)) for p in sorted(DATASET.iterdir())}


# ------------------------------------------------- fornito: report e stampa
def scrivi_report(risultati: dict, out: str = "triage.md") -> None:
    """Scrive la tabella di triage in markdown (si porta al debrief)."""
    righe = [
        "# Triage del dataset — Lab Modulo 2 · Lezione 6",
        "",
        "| File | Esito | Dettaglio | Anteprima |",
        "|---|---|---|---|",
    ]
    for nome, (esito, dettaglio, anteprima) in risultati.items():
        righe.append(f"| `{nome}` | {esito} | {dettaglio} | {anteprima} |")
    Path(__file__).parent.joinpath(out).write_text("\n".join(righe) + "\n", encoding="utf-8")


if __name__ == "__main__":
    primo_giro()

    print("\n=== Lab 1 · il triage ===")
    testo = carica_testo(str(DATASET / "note_interne.txt"))
    print(f"TODO 1 · carica_testo     note_interne.txt → {len(testo)} caratteri "
          "(l'encoding è gestito)")
    for nome in ("guida_smartworking.pdf", "report_trimestrale.pdf"):
        esito, dettaglio, _ = triaga_file(str(DATASET / nome))
        print(f"TODO 2 · triaga_file      {nome:<24} → {esito} · {dettaglio}")

    risultati = triage_dataset()
    print()
    larghezza = max(len(n) for n in risultati)
    for nome, (esito, dettaglio, anteprima) in risultati.items():
        print(f"{nome:<{larghezza}}  {esito:<7} {dettaglio}")
        print(f"{'':<{larghezza}}          » {anteprima}")
    scrivi_report(risultati)
    print("\nTabella scritta in solutions/triage.md")
