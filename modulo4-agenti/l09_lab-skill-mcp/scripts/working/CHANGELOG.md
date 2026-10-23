# Assistente dell'ufficio del personale di Valtesa

## 0.9

Un assistente solo, da `assistente.py`, al posto dei tre programmi di prima
(`assistente.py`, `skill_agente.py`, `app_agente.py`).

- Tool di cartella su `ufficio-completo/`: `elenca_file`, `cerca`, `leggi_file`.
- Skill in `skill-assistente/`: `rimborso-trasferta`; nelle istruzioni l'indice,
  il corpo con `apri_skill` (`skill.py`).
- Function tool: `note_fuori_massimale` (`rimborsi.py`).
- L'app dell'ufficio si sceglie al lancio, con `--app trello`, `--app notion` o
  `--app airtable` (`app.py`, login con `login_mcp.py`); per Trello anche i tool
  delle checklist.
- `MAX_TURNI` da 10 a 40: con l'app servono più chiamate al modello.
- `ISTRUZIONI_APP` dice che conti e date li fanno i function tool, senza
  nominarli.
- `esegui_python`, sotto approvazione, resta spento (`ESEGUI_PYTHON = False`).
