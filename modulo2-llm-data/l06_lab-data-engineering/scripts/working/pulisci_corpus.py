"""Lab 2 — Ogni file al suo parser (e al suo TIER).

È il deliverable del lab: `python working/pulisci_corpus.py` deve (ri)costruire
da zero `corpus_pulito/` + `report.md`. La decisione che conta è la mappa
**ROUTING**: per ogni file, il loader nativo (gratis) o LlamaParse — e a quale
tier. La compili coi risultati della *caccia al tier* fatta nel playground
(scheda_tier.md).

Il cleaning qui è FORNITO (è il mestiere di Modulo 2 · Lezione 5, oggi si
riusa): la ricetta giusta per ogni file è già scritta in fondo.

Questo script NON dipende dal Lab 1: gira anche se il triage non è finito.
Senza LLAMA_CLOUD_API_KEY gira comunque (tutto nativo): i file ostici escono
degradati, e la differenza si LEGGE nel report.

Occhio ai rilanci: ogni run CON la chiave richiama LlamaParse sui file non
nativi (niente cache) e consuma crediti — un giro completo con un routing
tipico costa ~15-20 crediti. Sistema prima il ROUTING lanciando lo script
SENZA chiave (giro offline, zero crediti); il giro vero fallo quando sei
convinto.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import load
from aikit.clean import normalize_whitespace, pulisci_pdf

# Import tollerante: se llamaparse.py è rotto o il TODO 4 non è finito, il
# Lab 2 gira lo stesso — tutto nativo, e il report lo dice.
try:
    from llamaparse import TIERS, load_llamaparse
except Exception:
    TIERS, load_llamaparse = {}, None

DATASET = Path(__file__).parent.parent / "dataset"
OUT = Path(__file__).parent / "corpus_pulito"

# ------------------------------------------------------------------ ROUTING
# TODO 5 — LA decisione del Lab 2: per ogni file, "nativo" oppure un tier
# LlamaParse ("fast" / "cost_effective" / "agentic" / "agentic_plus").
# Compilala DOPO la caccia al tier (scheda_tier.md). Regola: il tier giusto è
# il più BASSO che risolve il difetto di QUEL file — non il più potente.
# I tre "nativo" sono già decisi (il loro difetto non è il parsing); mancano
# i 5 file su cui hai indagato.
ROUTING = {
    "guida_smartworking.pdf": "nativo",     # testo lineare: pypdf basta
    "faq_prodotto.html": "nativo",          # il difetto è il noise → cleaning
    "note_interne.txt": "nativo",           # bastava l'encoding giusto
    # "verbale_scansionato.pdf":  ...,      # ← scansione di solo testo: serve davvero un tier alto?
    # "listino_prezzi.pdf":       ...,      # ← la tabella da ricostruire
    # "contratto_fornitura.docx": ...,      # ← le 2 tabelle perse dai paragrafi
    # "fattura_scansionata.pdf":  ...,      # ← OCR + tabella insieme
    # "rassegna_stampa.pdf":      ...,      # ← 2 colonne: quale tier le tiene in ordine?
}

# Irrecuperabili: nessun parser (e nessun tier) resuscita un download troncato.
ESCLUSI = {"report_trimestrale.pdf": "PDF troncato: irrecuperabile, va riscaricato"}


# --------------------------------------------- fornito: caricamento robusto
def carica_nativo(path: Path) -> str:
    """Tutto il testo con i loader di aikit, più il recupero dell'encoding.

    È la stessa mossa del Lab 1, fornita qui: il pomeriggio non deve
    dipendere dal mattino.
    """
    try:
        return "\n".join(d.text for d in load(str(path)))
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


# ------------------------------------- fornito: cleaning (Modulo 2 · Lezione 5)
BOILERPLATE_WEB = [
    # cookie banner
    "cookie", "profilazione", "pubblicità", "Accetta tutti", "Solo necessari",
    "Preferenze",
    # menu di navigazione e breadcrumb (voci esatte, maiuscole)
    "Home", "Prodotti", "Listino", "Assistenza", "Azienda", "Contatti",
    "Il mio account", "Carrello",
    # strip promozionale
    "SUMMER SALE", "ESTATE15", "Spedizione gratuita",
    # sidebar "correlati" + recensioni
    "Ti potrebbero interessare", "aggiungi al carrello", "recensioni",
    "nostri clienti",
    # newsletter + footer
    "newsletter", "offerte esclusive", "anteprime sui nuovi prodotti",
    "privacy policy per iniziare", "Chi siamo", "Lavora con noi",
    "Sostenibilità", "Rivenditori", "Spedizioni e resi", "Privacy policy",
    "Termini e condizioni", "Cookie policy", "© 2026", "P.IVA", "Cap. soc.",
    "Seguici", "Facebook",
    # i separatori "|" del menu diventano righe a sé dopo l'estrazione
    "|",
]


def rimuovi_boilerplate_web(text):
    """Toglie le righe che contengono un marcatore del contorno web.

    Case-sensitive di proposito: "Assistenza" (voce di menu) non deve portarsi
    via "richiedo assistenza" (contenuto). L'elenco è tarato su questo sito —
    su un sito nuovo si ritara guardando cosa esce.
    """
    return "\n".join(
        riga for riga in text.split("\n")
        if not any(m in riga for m in BOILERPLATE_WEB)
    )


def pulisci_locale(nome: str, text: str, via_llamaparse: bool) -> str:
    """La ricetta giusta per ogni file. Un if, non un registry (Modulo 2 · Lezione 5)."""
    if via_llamaparse:
        # l'output è markdown: si normalizza e basta, la struttura non si tocca
        return normalize_whitespace(text)
    if nome.endswith(".html"):
        return normalize_whitespace(rimuovi_boilerplate_web(text))
    if nome.endswith(".pdf"):
        return pulisci_pdf(text)
    return normalize_whitespace(text)


# ----------------------------------------------- fornito: il giro completo
def _pagine(path: Path) -> int | None:
    """Pagine di un PDF (per stimare i crediti); None se non conteggiabile."""
    if path.suffix.lower() != ".pdf":
        return None
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        return None


def pulisci() -> list[dict]:
    """Tutto il dataset → corpus_pulito/ + righe di metrica per il report."""
    OUT.mkdir(exist_ok=True)
    con_chiave = bool(os.getenv("LLAMA_CLOUD_API_KEY", "").strip())
    righe = []

    for path in sorted(DATASET.iterdir()):
        if path.name in ESCLUSI:
            righe.append({"file": path.name, "loader": "—", "prima": 0, "dopo": 0,
                          "crediti": "—", "nota": ESCLUSI[path.name]})
            continue

        rotta = ROUTING.get(path.name, "nativo")
        loader, crediti, nota = "nativo", "0", ""
        docs = None
        if rotta != "nativo":
            if load_llamaparse is None:
                nota = f"previsto tier {rotta}, ma llamaparse.py non è pronto: testo nativo degradato"
            elif not con_chiave:
                nota = f"chiave assente: previsto tier {rotta}, uscito testo nativo degradato"
            else:
                try:
                    docs = load_llamaparse(str(path), tier=rotta)
                    loader = rotta
                    pagine = _pagine(path)
                    crediti = f"~{pagine * TIERS[rotta]}" if pagine else "n/d"
                except NotImplementedError:
                    nota = f"previsto tier {rotta}, ma il TODO 4 non è finito: testo nativo degradato"
                except ValueError as e:
                    # un typo nel ROUTING non deve far crashare il giro
                    # (magari dopo aver già speso crediti sui file precedenti)
                    nota = f"{e}: uscito testo nativo degradato"

        if docs is not None:
            grezzo = "\n".join(d.text for d in docs)
        else:
            grezzo = carica_nativo(path)

        pulito = pulisci_locale(path.name, grezzo, via_llamaparse=loader != "nativo")

        (OUT / f"{path.stem}.txt").write_text(pulito, encoding="utf-8")
        righe.append({"file": path.name, "loader": loader,
                      "prima": len(grezzo), "dopo": len(pulito),
                      "crediti": crediti, "nota": nota})
    return righe


def scrivi_report(righe: list[dict], out: str = "report.md") -> None:
    md = [
        "# Corpus pulito — report del Lab Modulo 2 · Lezione 6", "",
        "| File | Loader / tier | Char grezzi | Char puliti | Crediti | Nota |",
        "|---|---|---|---|---|---|",
    ]
    for r in righe:
        md.append(f"| `{r['file']}` | {r['loader']} | {r['prima']} | {r['dopo']} "
                  f"| {r['crediti']} | {r['nota']} |")
    Path(__file__).parent.joinpath(out).write_text("\n".join(md) + "\n", encoding="utf-8")


if __name__ == "__main__":
    righe = pulisci()
    scrivi_report(righe)
    for r in righe:
        print(f"{r['file']:<28} {r['loader']:<15} {r['prima']:>7} → {r['dopo']:>7} "
              f"  crediti: {r['crediti']:<5} {r['nota']}")
    print(f"\nCorpus in {OUT.name}/ · metriche in report.md")
    if not ROUTING.keys() >= {"verbale_scansionato.pdf", "listino_prezzi.pdf",
                              "contratto_fornitura.docx", "fattura_scansionata.pdf",
                              "rassegna_stampa.pdf"}:
        print("TODO 5 · ROUTING: mancano ancora file da instradare (guarda i commenti)")
