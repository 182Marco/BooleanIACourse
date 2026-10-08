# AGENTS.md

Istruzioni per il coding agent che lavora in questa cartella.

## Regole del corso (non cambiarle)

- Python è quello del venv del modulo, due cartelle sopra: `../../.venv/bin/python`
  (su Windows `..\..\.venv\Scripts\python.exe`). Non creare altri venv e non
  installare pacchetti che non sono in `requirements.txt`.
- Le versioni fissate in `requirements.txt` (`openai-agents==0.22.3`,
  `chromadb==1.5.9`, `mcp` 2.x) non si cambiano.
- Il modello è `gpt-5.6-luna` e non si cambia.
- Il codice nuovo che usa l'Agents SDK è solo async: `await Runner.run(...)`
  dentro `asyncio.run(main())`, mai `Runner.run_sync`. `assistente.py` usa
  ancora `run_sync`: resta così finché non viene chiesto di cambiarlo.
- `mcp` è alla versione 2.x: l'import è `from mcp.server import MCPServer`.
  `from mcp.server.fastmcp import FastMCP` nella 2.x non esiste più.
- Prima di usare un'API che in questo progetto non c'è ancora, leggi il
  sorgente del pacchetto installato nel venv.
- La chiave sta in `.env`: non stamparne il contenuto e non copiarla altrove.
- Non creare `CLAUDE.md`, neanche con `/init`: se c'è, Claude Code non legge
  più questo file.

## Il progetto

Il software dell'ufficio del personale di Valtesa S.r.l. Due programmi:

- `rimborsi.py` controlla le note spese di `dati/note_spese.csv` contro
  `dati/massimali.csv`: vale il massimale in vigore nel giorno della spesa
  (colonna `valido_dal`). Si lancia con `python rimborsi.py`; l'ultima riga
  oggi è «1500 note spese, 267 fuori massimale». Accetta anche un altro
  export come argomento (`python rimborsi.py dati/export-ottobre.csv`) e
  `--dipendente "Nome Cognome"`.
- `assistente.py` è l'assistente per i dipendenti (Agents SDK), con
  `cerca_documenti` sull'indice dei documenti di `ufficio/` e `query_db` su
  `dati/valtesa.db`, in sola lettura. Si lancia con `python assistente.py`
  e chiama le API: per provare `rimborsi.py` non serve.

Come si testa: `pytest` dalla cartella del progetto, prima e dopo ogni
modifica. I test non chiamano le API.

Cosa non toccare:

- i file in `dati/` sono export del gestionale e non si modificano a mano,
  neanche `massimali.csv`: un massimale nuovo arriva con una circolare e un
  export nuovo;
- `ufficio/` contiene i documenti dell'ufficio: non si modificano;
- i test esistenti non si cambiano per farli passare: se un test fallisce,
  prima si capisce perché;
- `OBIETTIVI.md` e `ticket-report.md` sono il materiale della lezione: non
  si modificano.
