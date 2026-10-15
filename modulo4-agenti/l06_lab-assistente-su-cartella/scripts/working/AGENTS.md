# AGENTS.md

Istruzioni per il coding agent che lavora in questa cartella.

## Regole del corso (non cambiarle)

- Python è quello del venv del modulo, tre cartelle sopra: `../../../.venv/bin/python`
  (su Windows `..\..\..\.venv\Scripts\python.exe`). Non creare altri venv e non
  installare pacchetti che non sono in `requirements.txt`.
- Le versioni fissate in `requirements.txt` (`openai-agents==0.22.3`,
  `chromadb==1.5.9`, `mcp` 2.x) non si cambiano.
- Il modello è `gpt-6-luna` e non si cambia.
- Il codice che usa l'Agents SDK è solo async: `await Runner.run(...)`
  dentro `asyncio.run(main())`, mai `Runner.run_sync` (nemmeno accanto ad
  `asyncio.run`: in un programma async `run_sync` si ferma con un errore).
- `mcp` è alla versione 2.x: l'import è `from mcp.server import MCPServer`.
  `from mcp.server.fastmcp import FastMCP` nella 2.x non esiste più.
- Prima di usare un'API che in questo progetto non c'è ancora, leggi il
  sorgente del pacchetto installato nel venv.
- La chiave sta in `.env`: non stamparne il contenuto e non copiarla altrove.
- Non creare `CLAUDE.md`, neanche con `/init`: se c'è, Claude Code non legge
  più questo file.

## Il progetto

Il software dell'ufficio del personale di Valtesa S.r.l.:

- `assistente.py` è l'assistente per i dipendenti (Agents SDK, `gpt-6-luna`),
  con i tool di cartella di `strumenti_cartella.py` (`elenca_file`, `cerca`,
  `leggi_file`) sulla cartella `ufficio-completo/`. `rispondi()` è un giro
  dell'assistente su una domanda: la usano `main()` e `valuta.py`. Con
  `ESEGUI_PYTHON = True` ha anche `esegui_python` di `esecuzione.py`, che
  esegue codice scritto dal modello ed è sempre sotto approvazione.
- `valuta.py` fa all'assistente le domande di `domande.json` (o di
  `domande-extra.json`) e dice quante risposte sono giuste, con chiamate e
  token; scrive una riga in `output/valutazioni.csv`.
- `esecuzione.py`: `esegui_python` (un processo a parte, nella cartella
  dell'ufficio, con un timeout, senza sandbox) e il ciclo di approvazione.
- `rimborsi.py` e `report.py` controllano e riassumono le note spese di
  `dati/`.
- `ufficio-completo/` è la cartella dell'ufficio: i documenti, anche in PDF
  e DOCX, e una copia degli export di `dati/` in CSV.
- `guasti.md` è il quaderno dello studente: dove l'assistente sbaglia e
  perché.

Come si testa: `pytest` dalla cartella del progetto, prima e dopo ogni
modifica. I test non chiamano le API: i tool si chiamano con `chiama()` di
`tests/test_assistente.py`, il modello si sostituisce con `ScriptedModel`
(`modello_finto()` di `tests/test_esecuzione.py`).

## Le regole del lab

L'obiettivo è che l'assistente risponda giusto alle domande di
`domande.json` con meno token possibile. Si cambiano i tool e il giro
dell'assistente, non il metro né i limiti:

- `MAX_CARATTERI`, `MAX_RISULTATI` (`strumenti_cartella.py`), `MAX_TURNI` e
  `MODELLO` (`assistente.py`) restano quelli che sono. Un file più lungo del
  limite si legge a pagine, non alzando il limite.
- `leggi_file` rimanda al massimo `MAX_CARATTERI` caratteri per chiamata e
  `cerca` al massimo `MAX_RISULTATI` righe, più una riga di nota per il
  modello.
- I tool restano tre e generici (`elenca_file`, `cerca`, `leggi_file`):
  niente tool fatti per questi CSV o per queste domande, e niente `query_db`
  su `dati/valtesa.db`. `leggi_file` può
  ricevere da che riga leggere (`da_riga`), `cerca` riceve solo `testo`.
- `rispondi()` fa al massimo `MAX_TURNI` chiamate al modello con i tool,
  più una senza tool per la risposta finale. Il result che ritorna conta le
  chiamate e i token di tutto il giro.
- Nella parte 1 `ESEGUI_PYTHON` resta `False`: i conti con il codice sono la
  parte 2.
- La nota per il modello dice cosa manca e come continuare, non riassume i
  dati: niente conteggi o somme calcolate dal tool.
- `tests/test_regole.py` controlla queste regole e non si modifica.
- `valuta.py`, `domande.json` e `domande-extra.json` non si modificano.
- Nelle istruzioni dell'assistente non vanno le risposte né il contenuto
  dei documenti.
- Le dipendenze sono quelle di `requirements.txt`: per PDF e DOCX ci sono i
  loader di `aikit/loaders`.
- Ogni rimedio ha i suoi test, senza API. Un test esistente si cambia solo
  se il rimedio cambia di proposito quel comportamento, e si dice perché.
- Non lanciare `assistente.py` né `valuta.py`: chiamano le API e le lancia
  lo studente.

Cosa non toccare:

- `ufficio-completo/` e `dati/`: sono i documenti e gli export
  dell'ufficio, non si modificano;
- `esegui_python` ha `needs_approval=True` e lo tiene: nessuna esecuzione
  del codice del modello parte senza il sì di una persona;
- non leggere `../ripartenza/` né `../solutions/`: sono le soluzioni del
  docente, per chi si ferma.
