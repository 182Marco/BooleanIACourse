"""Lab 1 — Triage del dataset: caricare TUTTO, capire cosa si rompe e perché.

In testa c'è il "primo giro" — il ciclo che il docente costruisce a schermo:
carica → guarda → diagnostica → correggi. È già scritto e gira subito. Il Lab 1
è generalizzarlo: lo stesso giro su tutti i file del dataset, e gli esiti in
una **tabella di triage**. Qui non si ripara ancora niente (il cleaning è il
Lab 2, LlamaParse viene dopo): si diagnostica.

Esiti possibili:
  OK      → il testo esce ed è plausibile (ma guarda l'anteprima: "esce del
            testo" non vuol dire "esce il testo GIUSTO"…)
  VUOTO   → il loader non solleva errori ma il testo estratto è (quasi) niente
  ERRORE  → il loader solleva un'eccezione: file corrotto, encoding sbagliato…

    python working/triage.py     (dalla cartella scripts/)
                                 → il primo giro + lo stato dei tuoi TODO

Il main gira anche coi TODO non ancora fatti: stampa quello che c'è e dice
quali mancano. Completali dall'alto verso il basso.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load

DATASET = Path(__file__).parent.parent / "dataset"
SOGLIA_VUOTO = 50          # sotto questi caratteri l'estrazione è "vuota"


# ------------------------------------------ 🎤 il primo giro (già scritto)
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


# --------------------------------------------------- ⌨️ Lab 1: tocca a voi
def carica_testo(path: str) -> str:
    """Tutto il testo di un file, in una stringa.

    TODO 1: usa `load(path)` (aikit) e unisci il testo dei Document. I file
    di testo vengono letti in utf-8: se la decodifica fallisce, rileggi il
    file con l'encoding latin-1 (quello storico di Windows/Excel). Ogni
    altra eccezione deve passare oltre: la gestisce triaga_file.
    """
    raise NotImplementedError("TODO 1: carica_testo")


def triaga_file(path: str) -> tuple[str, str, str]:
    """Un file → (esito, dettaglio, anteprima).

    TODO 2: chiama `carica_testo(path)`. Se solleva un'eccezione l'esito è
    "ERRORE", col nome dell'errore nel dettaglio. Altrimenti: "VUOTO" se i
    caratteri utili sono meno di SOGLIA_VUOTO, "OK" se no — col conteggio nel
    dettaglio. L'anteprima è l'inizio del testo, compattato su una riga
    (un'ottantina di caratteri bastano): è lì che si VEDE la tabella rotta.
    """
    raise NotImplementedError("TODO 2: triaga_file")


def triage_dataset() -> dict[str, tuple[str, str, str]]:
    """Tutto il dataset → {nome_file: (esito, dettaglio, anteprima)}.

    TODO 3: applica `triaga_file` a ogni file di DATASET, in ordine
    alfabetico, usando il nome del file come chiave.
    """
    raise NotImplementedError("TODO 3: triage_dataset")


# ------------------------------------------------- fornito: report e stampa
def scrivi_report(risultati: dict, out: str = "triage.md") -> None:
    """Scrive la tabella di triage in markdown (la porti al debrief)."""
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

    print("\n=== Lab 1 · il triage (i TODO si vedono appena fatti) ===")

    # TODO 1 — il file latin-1: con utf-8 sarebbe UnicodeDecodeError
    try:
        testo = carica_testo(str(DATASET / "note_interne.txt"))
        print(f"TODO 1 · carica_testo     note_interne.txt → {len(testo)} caratteri "
              "(l'encoding è gestito)")
    except NotImplementedError:
        print("TODO 1 · carica_testo     ancora da fare")

    # TODO 2 — un file sano e uno corrotto: due esiti diversi, zero crash
    try:
        for nome in ("guida_smartworking.pdf", "report_trimestrale.pdf"):
            esito, dettaglio, _ = triaga_file(str(DATASET / nome))
            if "NotImplementedError" in dettaglio:
                print(f"TODO 2 · triaga_file      {nome} → ERRORE, ma è il TODO 1 "
                      "non finito (sparirà da solo)")
            else:
                print(f"TODO 2 · triaga_file      {nome:<24} → {esito} · {dettaglio}")
    except NotImplementedError:
        print("TODO 2 · triaga_file      ancora da fare")

    # TODO 3 — la tabella completa
    try:
        risultati = triage_dataset()
    except NotImplementedError:
        print("TODO 3 · triage_dataset   ancora da fare")
    else:
        if any("NotImplementedError" in dettaglio
               for _, dettaglio, _ in risultati.values()):
            print("TODO 3 · triage_dataset   gira, ma la tabella è piena degli "
                  "ERRORE di un TODO precedente: finisci quello e rilancia")
            raise SystemExit(0)
        print()
        larghezza = max(len(n) for n in risultati)
        for nome, (esito, dettaglio, anteprima) in risultati.items():
            print(f"{nome:<{larghezza}}  {esito:<7} {dettaglio}")
            print(f"{'':<{larghezza}}          » {anteprima}")
        scrivi_report(risultati)
        print("\nTabella scritta in working/triage.md — è quella del debrief")
