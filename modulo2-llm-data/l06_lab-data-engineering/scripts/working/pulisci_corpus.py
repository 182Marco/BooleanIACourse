"""Lab 2 — Ogni file al suo parser (e al suo TIER).

È il deliverable del lab: `python pulisci_corpus.py` deve (ri)costruire da zero
`corpus_pulito/` + `report.md`. La decisione che conta è la mappa **ROUTING**:
per ogni file, il loader nativo (gratis) o LlamaParse — e a quale tier. La
compili coi risultati della *caccia al tier* fatta nel playground (scheda_tier.md).

Il cleaning qui è FORNITO (è il mestiere di L17, oggi si riusa): pipeline per
file già pronte, comprese quelle per il boilerplate web.

Senza LLAMA_CLOUD_API_KEY gira comunque (tutto nativo): i file ostici escono
degradati, e la differenza si LEGGE nel report.

Occhio ai rilanci: ogni run CON la chiave richiama LlamaParse sui file non
nativi (niente cache) e consuma crediti. Sistema prima il ROUTING e verifica
offline col check; il giro vero con la chiave fallo quando sei convinto.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import clean
from aikit.clean import (
    dehyphenate,
    normalize_unicode,
    normalize_whitespace,
    remove_page_numbers,
    remove_repeated_lines,
)
from llamaparse import TIERS, load_llamaparse
from triage import carica_robusto

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


# ------------------------------------------------- cleaning FORNITO (da L17)
def drop_lines_containing(marcatori: list):
    """Step factory: toglie le righe che contengono uno dei marcatori.

    Case-sensitive di proposito: "Assistenza" (voce di menu) non deve portarsi
    via "richiedo assistenza" (contenuto)."""
    def step(text: str) -> str:
        return "\n".join(
            l for l in text.split("\n")
            if not any(m in l for m in marcatori)
        )
    return step


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

PIPELINE_PER_FILE = {
    "guida_smartworking.pdf": [dehyphenate, remove_repeated_lines(min_repeats=3),
                               remove_page_numbers, normalize_whitespace],
    "faq_prodotto.html": [drop_lines_containing(BOILERPLATE_WEB), normalize_whitespace],
    "note_interne.txt": [normalize_unicode, normalize_whitespace],
    "contratto_fornitura.docx": [normalize_unicode, normalize_whitespace],
    # l'output LlamaParse è markdown: si normalizza e basta, la struttura non si tocca
    "listino_prezzi.pdf": [normalize_whitespace],
    "verbale_scansionato.pdf": [normalize_whitespace],
    "fattura_scansionata.pdf": [normalize_whitespace],
    "rassegna_stampa.pdf": [normalize_whitespace],
}


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
    use_llamaparse = bool(os.getenv("LLAMA_CLOUD_API_KEY", "").strip())
    righe = []

    for path in sorted(DATASET.iterdir()):
        if path.name in ESCLUSI:
            righe.append({"file": path.name, "loader": "—", "prima": 0, "dopo": 0,
                          "crediti": "—", "nota": ESCLUSI[path.name]})
            continue

        rotta = ROUTING.get(path.name, "nativo")
        if rotta != "nativo" and use_llamaparse:
            docs, loader = load_llamaparse(str(path), tier=rotta), rotta
            pagine = _pagine(path)
            crediti = f"~{pagine * TIERS[rotta]}" if pagine else "n/d"
        else:
            docs, loader = carica_robusto(str(path)), "nativo"
            crediti = "0"

        grezzo = "\n".join(d.text for d in docs)
        steps = PIPELINE_PER_FILE.get(path.name, [normalize_unicode, normalize_whitespace])
        pulito = clean(grezzo, steps)

        (OUT / f"{path.stem}.txt").write_text(pulito, encoding="utf-8")
        nota = "" if loader != "nativo" or rotta == "nativo" \
            else f"chiave assente: previsto tier {rotta}, uscito testo degradato"
        righe.append({"file": path.name, "loader": loader,
                      "prima": len(grezzo), "dopo": len(pulito),
                      "crediti": crediti, "nota": nota})
    return righe


def scrivi_report(righe: list[dict], out: str = "report.md") -> None:
    md = [
        "# Corpus pulito — report del Lab L18", "",
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
