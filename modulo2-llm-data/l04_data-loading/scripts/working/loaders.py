"""loaders.py — leggere file di formati diversi e normalizzarli in un Document.

Un solo file per tutta la serata. I primi cinque pezzi si scrivono **col
docente** (🎤), gli ultimi due li scrivete **voi** (⌨️).

    python working/loaders.py

Il main gira anche a metà strada: ogni pezzo finito stampa il suo risultato,
quelli non ancora scritti dicono «ancora da fare» e il programma prosegue.
"""
import sys

from dataclasses import dataclass, field
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPTS / "scaffolding"))

from ask import mostra, rispondi  # noqa: E402 — il banco di prova, già scritto

DATASET = SCRIPTS / "dataset"


# --------------------------------------------------------- il formato interno
@dataclass
class Document:
    """Quello che ogni loader deve restituire: il testo estratto e la sua provenienza.

    metadata tiene almeno `source` (da quale file arriva) e `type` (il formato);
    i loader che lavorano pagina per pagina aggiungono anche `page`.
    """
    text: str
    metadata: dict = field(default_factory=dict)


# ------------------------------------------------------- TODO 1 · col docente 🎤
def load_pdf(path):
    """Il PDF, una pagina per Document (pypdf).

    Restituisce una lista di Document: uno per pagina, con il numero di pagina
    nei metadata.
    """
    raise NotImplementedError


# ------------------------------------------------------- TODO 2 · col docente 🎤
def load_docx(path):
    """Il documento Word, dai paragrafi dell'XML (python-docx).

    Restituisce una lista con un solo Document: tutto il testo del file.
    """
    raise NotImplementedError


# ------------------------------------------------------- TODO 3 · col docente 🎤
def load_html(path):
    """La pagina web, senza il boilerplate (BeautifulSoup).

    Restituisce una lista con un solo Document, con il testo del contenuto —
    fuori i tag di contorno: script, style, header, nav, aside, footer.
    """
    raise NotImplementedError


# ------------------------------------------------------- TODO 4 · col docente 🎤
def load_markdown(path):
    """Il Markdown come testo, senza la sintassi (markdown-it-py).

    Restituisce una lista con un solo Document.
    """
    raise NotImplementedError


# ------------------------------------------------------- TODO 5 · col docente 🎤
def load(path):
    """La porta unica: apre qualunque formato conosciuto, guardando l'estensione.

    Restituisce dei Document, come i loader specifici. Su un'estensione che non
    conosce, solleva ValueError.
    """
    raise NotImplementedError


# --------------------------------------------------------------- TODO 6 · voi ⌨️
def load_txt(path):
    """Il file di testo semplice, in Document.

    Restituisce dei Document con i metadata giusti.
    """
    raise NotImplementedError


# --------------------------------------------------------------- TODO 7 · voi ⌨️
def load_csv(path):
    """Il CSV, in Document.

    Restituisce dei Document con i metadata giusti. Quanti? Uno per riga o uno
    per tutto il file: la scelta è vostra — pensate a che cosa ci farete dopo,
    quando questi Document andranno in un motore di ricerca.
    """
    raise NotImplementedError


if __name__ == "__main__":
    DOMANDA_PDF = "Di quanto è cresciuto il fatturato nel 2025?"
    DOMANDA_DOCX = "Quale città è stata scelta per il secondo showroom, e con che budget?"
    DOMANDA_HTML = "Quanto dura la garanzia sul telaio della scrivania?"
    DOMANDA_MD = "Che cosa devo fare quando il display mostra E07?"
    DOMANDA_TXT = "Quante segnalazioni di codice E07 sono arrivate questa settimana?"
    DOMANDA_CSV = "Quanti ordini risultano consegnati?"

    print("### TODO 1 · PDF")
    try:
        docs = load_pdf(DATASET / "relazione-annuale.pdf")
        mostra(docs, "relazione-annuale.pdf")
        rispondi(docs, DOMANDA_PDF)
    except NotImplementedError:
        print("  TODO 1 ancora da fare")

    print("\n### TODO 2 · DOCX")
    try:
        docs = load_docx(DATASET / "verbale-consiglio.docx")
        mostra(docs, "verbale-consiglio.docx")
        rispondi(docs, DOMANDA_DOCX)
    except NotImplementedError:
        print("  TODO 2 ancora da fare")

    print("\n### TODO 3 · HTML")
    try:
        docs = load_html(DATASET / "faq-garanzia.html")
        mostra(docs, "faq-garanzia.html")
        rispondi(docs, DOMANDA_HTML)
    except NotImplementedError:
        print("  TODO 3 ancora da fare")

    print("\n### TODO 4 · Markdown")
    try:
        docs = load_markdown(DATASET / "guida-lumadesk.md")
        mostra(docs, "guida-lumadesk.md")
        rispondi(docs, DOMANDA_MD)
    except NotImplementedError:
        print("  TODO 4 ancora da fare")

    print("\n### TODO 5 · load(): la porta unica")
    for nome in ("relazione-annuale.pdf", "verbale-consiglio.docx",
                 "faq-garanzia.html", "guida-lumadesk.md",
                 "note-supporto.txt", "ordini.csv"):
        try:
            docs = load(DATASET / nome)
            print(f"  {nome:26} → {len(docs)} Document · {docs[0].metadata.get('type')}")
        except NotImplementedError:
            print(f"  {nome:26} → il loader di questo formato è ancora da fare")
        except ValueError as e:
            print(f"  {nome:26} → ValueError: {e}")

    print("\n### TODO 6 · TXT")
    try:
        docs = load_txt(DATASET / "note-supporto.txt")
        mostra(docs, "note-supporto.txt")
        rispondi(docs, DOMANDA_TXT)
    except NotImplementedError:
        print("  TODO 6 ancora da fare")

    print("\n### TODO 7 · CSV")
    try:
        docs = load_csv(DATASET / "ordini.csv")
        mostra(docs, "ordini.csv")
        rispondi(docs, DOMANDA_CSV)
    except NotImplementedError:
        print("  TODO 7 ancora da fare")
