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

- `assistente.py` è l'assistente dell'ufficio, versione 0.9 (Agents SDK,
  `gpt-6-luna`): i tool di cartella di `strumenti_cartella.py` (`elenca_file`,
  `cerca`, `leggi_file`) sulla cartella `ufficio-completo/`; le skill di
  `skill-assistente/`, con l'indice nelle istruzioni e `apri_skill` di
  `skill.py`; il function tool `note_fuori_massimale` (chiama `rimborsi.py`);
  con `--app`, il server MCP remoto
  di un'app (Trello, Notion o Airtable) di `app.py`, collegato con
  `MCPServerStreamableHttp`. `rispondi()` è un giro dell'assistente su una
  domanda: la usano `main()` e `valuta.py`. Con `ESEGUI_PYTHON = True` ha
  anche `esegui_python` di `esecuzione.py`, che esegue codice scritto dal
  modello ed è sempre sotto approvazione. Le versioni sono in `CHANGELOG.md`.
- `valuta.py` fa all'assistente le domande di `domande.json` (o di
  `domande-extra.json`) e dice quante risposte sono giuste, con chiamate e
  token; scrive una riga in `output/valutazioni.csv`.
- `esecuzione.py`: `esegui_python` (un processo a parte, nella cartella
  dell'ufficio, con un timeout, senza sandbox) e il ciclo di approvazione.
- `rimborsi.py` e `report.py` controllano e riassumono le note spese di
  `dati/`.
- `login_mcp.py` fa il login OAuth all'app e salva il token in
  `.mcp-token/`. Non leggere, stampare né copiare i file di `.mcp-token/`:
  sono le chiavi degli account.
- `ufficio-completo/` è la cartella dell'ufficio: i documenti, anche in PDF
  e DOCX, e una copia degli export di `dati/` in CSV.
- `dati/assunzioni.csv` sono i nuovi assunti, con la data di ingresso; la
  procedura di ingresso è `ufficio-completo/procedura-ingresso-dotazioni.pdf`.

Come si testa: `pytest` dalla cartella del progetto, prima e dopo ogni
modifica. I test non chiamano le API: i tool si chiamano con `chiama()` di
`tests/test_assistente.py`, il modello si sostituisce con `ScriptedModel`
(`modello_finto()` di `tests/test_esecuzione.py`). Non lanciare
`assistente.py` né `valuta.py`: chiamano le API (e `assistente.py --app` apre
il browser per il login) e li lancia lo studente.

Cosa non toccare:

- `ufficio-completo/` e `dati/`: sono i documenti e gli export
  dell'ufficio, non si modificano;
- `esegui_python` ha `needs_approval=True` e lo tiene: nessuna esecuzione
  del codice del modello parte senza il sì di una persona;
- non leggere `../solutions/` né `../ripartenza/`: sono le soluzioni del docente.
