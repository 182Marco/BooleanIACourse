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
