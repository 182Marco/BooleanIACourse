"""strumenti_cartella.py — i tool di cartella dell'assistente: elencare, cercare, leggere.

L'assistente lavora sulla cartella completa dell'ufficio (ufficio-completo/): i documenti
dell'ufficio del personale, anche in PDF e DOCX, e gli export del gestionale in CSV. Il
confine lo tiene il codice: ogni percorso che arriva dal modello passa da dentro_la_radice(),
che rifiuta quello che sta fuori dalla cartella.

La versione del docente di Modulo 4 · Lezione 6, con i rimedi del lab:
- i formati: PDF e DOCX si leggono con i loader di aikit (Modulo 2 · Lezione 4), in
  leggi_file e in cerca;
- gli output lunghi: leggi_file legge a pagine e dice da che riga ripartire; cerca dice
  che ci sono altre righe, senza contarle (la nota non fa conti);
- gli errori per il modello: un file che non esiste torna con i nomi simili.
I limiti (MAX_CARATTERI, MAX_RISULTATI) sono quelli di prima: cambia cosa sa il modello.
"""
from difflib import get_close_matches
from pathlib import Path

from agents import function_tool

from aikit.loaders import load

RADICE = (Path(__file__).parent / "ufficio-completo").resolve()
MAX_CARATTERI = 20_000                              # quanto rimanda leggi_file, al massimo, per pagina
MAX_RISULTATI = 30                                  # quante righe rimanda cerca, al massimo
FORMATI = {".pdf", ".docx"}                         # letti con i loader, non come testo


def dentro_la_radice(percorso: str) -> Path:
    """Il percorso assoluto di un file della cartella; ValueError se è fuori dalla cartella."""
    completo = (RADICE / percorso).resolve()        # risolve .. e i link simbolici; un percorso assoluto resta com'è
    if not completo.is_relative_to(RADICE):
        raise ValueError(f"{percorso} è fuori dalla cartella dell'ufficio")
    return completo


def file_della_cartella() -> list[Path]:
    """I file della cartella, senza i link che portano fuori."""
    return [f for f in sorted(RADICE.rglob("*")) if f.is_file() and f.resolve().is_relative_to(RADICE)]


def testo_di(file: Path) -> str:
    """Il testo di un file: PDF e DOCX con i loader di aikit, il resto letto come testo."""
    if file.suffix.lower() in FORMATI:
        return "\n".join(doc.text for doc in load(str(file)))
    return file.read_text(encoding="utf-8", errors="replace")


@function_tool
def elenca_file() -> str:
    """Elenca i file della cartella dell'ufficio del personale di Valtesa (documenti, anche in
    PDF e DOCX, ed export del gestionale in CSV), uno per riga, con il percorso da passare a
    leggi_file."""
    return "\n".join(str(f.relative_to(RADICE)) for f in file_della_cartella())


@function_tool
def leggi_file(percorso: str, da_riga: int = 1) -> str:
    """Legge un file della cartella dell'ufficio (testo, CSV, HTML, PDF, DOCX) e ne rimanda il
    contenuto a pagine, di al massimo 20.000 caratteri. Se il file continua, in fondo c'è una
    nota con la riga da cui chiedere la pagina successiva.

    Args:
        percorso: il percorso del file, come lo dà elenca_file.
        da_riga: la riga da cui partire, contando da 1; per la pagina successiva, quella
            indicata nella nota in fondo.
    """
    file = dentro_la_radice(percorso)
    if not file.is_file():
        nomi = [str(f.relative_to(RADICE)) for f in file_della_cartella()]
        simili = get_close_matches(percorso, nomi, n=3, cutoff=0.5)
        if simili:
            return f"Il file {percorso} non esiste. File con un nome simile: {', '.join(simili)}."
        return f"Il file {percorso} non esiste. I file della cartella li dà elenca_file."
    righe = testo_di(file).splitlines()
    inizio = max(da_riga, 1) - 1
    pagina = []
    if inizio > 0 and file.suffix.lower() == ".csv":
        pagina.append(righe[0])                     # l'intestazione, su ogni pagina di un CSV
    lunghezza = sum(len(r) + 1 for r in pagina)
    fine = inizio
    while fine < len(righe) and lunghezza + len(righe[fine]) + 1 <= MAX_CARATTERI:
        pagina.append(righe[fine])
        lunghezza += len(righe[fine]) + 1
        fine += 1
    if fine == inizio and fine < len(righe):        # una riga sola più lunga di una pagina
        pagina.append(righe[fine][:MAX_CARATTERI])
        fine += 1
    testo = "\n".join(pagina)
    if fine < len(righe):
        testo += (f"\n[Righe {inizio + 1}-{fine} di {len(righe)}: il file continua. Per la pagina "
                  f"successiva: leggi_file(percorso=\"{percorso}\", da_riga={fine + 1}).]")
    return testo


@function_tool
def cerca(testo: str) -> str:
    """Cerca un testo in tutti i file della cartella dell'ufficio, anche nei PDF e nei DOCX
    (senza distinguere maiuscole e minuscole), e rimanda le righe che lo contengono, nella forma
    file:riga: testo, al massimo 30. Se le righe sono di più, in fondo c'è una nota.

    Args:
        testo: la parola o la frase da cercare.
    """
    risultati = []
    for file in file_della_cartella():
        for numero, riga in enumerate(testo_di(file).splitlines(), start=1):
            if testo.lower() in riga.lower():
                risultati.append(f"{file.relative_to(RADICE)}:{numero}: {riga.strip()}")
    if not risultati:
        return f"Nessuna riga contiene «{testo}»."
    testo_risultati = "\n".join(risultati[:MAX_RISULTATI])
    if len(risultati) > MAX_RISULTATI:
        testo_risultati += (f"\n[Mostrate le prime {MAX_RISULTATI} righe: ce ne sono altre. Restringi la "
                            f"ricerca, o leggi il file a pagine con leggi_file.]")
    return testo_risultati
