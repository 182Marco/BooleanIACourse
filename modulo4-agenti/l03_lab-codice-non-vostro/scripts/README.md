# Valtesa: rimborsi e assistente dell'ufficio del personale

Valtesa S.r.l. è un'azienda di 120 dipendenti con due sedi, Brescia e Padova.
Questo progetto è il software interno del suo ufficio del personale e
contiene due programmi:

- **`rimborsi.py`** controlla le note spese dei dipendenti in trasferta
  contro i massimali della policy aziendale. È il programma della trace di
  Modulo 4 · Lezione 1, con la correzione fatta lì: il massimale è quello in vigore nel
  giorno della spesa.
- **`assistente.py`** è l'assistente per i dipendenti costruito con l'OpenAI
  Agents SDK: risponde sui documenti dell'ufficio (con `cerca_documenti`)
  e sui dati di dipendenti, assenze e note spese (con `query_db`, in sola
  lettura). È l'assistente del docente di Modulo 3 · Lezione 12.

È il progetto di tutto il Modulo 4: ogni lezione ne ha una copia nella sua
cartella, che parte da quella della lezione prima.

## Primo avvio

Si fa una volta sola, prima di Modulo 4 · Lezione 2, e lo fa il coding agent
(la checklist del modulo dice come).

1. Il venv del modulo sta nella cartella del modulo, due cartelle sopra
   questa (`../../.venv`), ed è uno solo per tutte le lezioni. Si crea con
   Python 3.10 o più recente e si installa `requirements.txt`.
2. `.env.example` si copia in `.env` e si scrive la chiave OpenAI del corso.
3. `python indicizza.py` costruisce l'indice dei documenti in `indice/`
   (124 chunk, meno di un centesimo di dollaro).
4. `pytest` dalla cartella del progetto: tutti i test verdi.

Nelle lezioni dopo servono solo i punti 2 e 3 nella cartella nuova: in
Modulo 4 · Lezione 3 sono nell'avvio di `OBIETTIVI.md`.

## Se il setup non parte

| Cosa vedete | Cosa fare |
|---|---|
| `claude` non viene trovato dopo l'installazione | Aprite un terminale nuovo. Su Windows, se non basta, aggiungete `%USERPROFILE%\.local\bin` al PATH dell'utente |
| «'irm' is not recognized» | Siete nel Prompt dei comandi: il comando va lanciato in PowerShell |
| «The token '&&' is not a valid statement separator» | Siete in PowerShell con il comando per il Prompt dei comandi: usate quello per PowerShell |
| «A parameter cannot be found that matches parameter name 'fsSL'» | In PowerShell avete lanciato il comando per macOS e Linux: usate quello per PowerShell |
| «Failed to download binary: The process cannot access the file …» | Di solito è l'antivirus: in PowerShell cancellate la cartella `.claude\downloads` della vostra utenza (`Remove-Item -Recurse -Force ~\.claude\downloads`) e rilanciate l'installazione |
| `claude` apre una vecchia Claude Desktop | Una versione vecchia dell'app prende il comando: aggiornatela o disinstallatela |
| In WSL il login chiede di incollare un codice | Copiate il codice dal browser e incollatelo nel terminale |
| `/status` dice che state usando una chiave API e non l'abbonamento | Nel sistema c'è `ANTHROPIC_API_KEY`: toglietela (`unset ANTHROPIC_API_KEY`) e riaprite |
| L'installazione di `mcp` o `openai-agents` fallisce, con un errore su «Requires-Python» | Serve Python 3.10 o più recente: installatelo e fate ricreare il venv al coding agent |
| `pytest`: fallisce il test sull'indice dei documenti | Manca l'indice di questa cartella: `python indicizza.py` (con la chiave nel `.env` di questa cartella). Se la chiave ancora non c'è, per gli obiettivi 2 e 3 basta `pytest tests/test_rimborsi.py` (9 passed) |
| `source ../../.venv/bin/activate`: «No such file or directory» | Non siete in `modulo4-agenti/l03_lab-codice-non-vostro/scripts/` (`pwd` lo dice), oppure il venv è altrove: chiedete al coding agent dove l'ha creato. Deve stare in `modulo4-agenti/.venv` |
| `pytest` non trovato, o errori di `import` | Il venv del modulo non è attivo in quel terminale: vedi «I comandi» |
| `indicizza.py` o l'assistente: errore sulla chiave | Manca `.env`, o la chiave è quella vecchia: copiate `.env.example` in `.env` e scrivete la chiave nuova |
| Il coding agent ignora le regole di `AGENTS.md` | C'è un `CLAUDE.md` nella cartella o in una cartella sopra (per esempio creato da `/init`): cancellatelo. Se non c'è: Claude Code legge `AGENTS.md` dalla 2.1.277, controllate con `claude --version` e aggiornate con `claude update` |
| Sonnet 5.5 non c'è nell'elenco dei modelli | Serve Claude Code 2.1.284 o successivo: `claude --version`, e `claude update` per aggiornare |
| `git switch main` si ferma con «Your local changes … would be overwritten» | Ci sono modifiche non salvate sul branch della lezione scorsa: un commit su `l02-lavoro` (`git add .`, `git commit -m "fine della lezione scorsa"`), poi di nuovo `git switch main` |
| `git commit` risponde «Author identity unknown» | Una volta sola: `git config --global user.name "Nome Cognome"` e `git config --global user.email "la vostra email"` |
| `git pull` si ferma con «Need to specify how to reconcile divergent branches» | Avete fatto commit su `main`: il lavoro delle lezioni va su un branch. `git branch l03-salvato` (tiene i vostri commit su un branch), `git reset --keep origin/main` (`main` torna come quello del corso; le modifiche non salvate restano), `git pull`. Se `reset` si ferma, chiamate il docente |

## I comandi

Dalla cartella del progetto, con il venv del modulo attivo. Per attivarlo:
`source ../../.venv/bin/activate` (macOS, Linux, WSL) oppure
`..\..\.venv\Scripts\Activate.ps1` (PowerShell; se Windows lo blocca,
una volta sola `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`).

```
python rimborsi.py        # l'esito di tutte le note spese; in fondo il totale
python assistente.py      # chiede il nome della sessione, poi le domande
python indicizza.py       # ricostruisce l'indice dei documenti
pytest                    # i test, senza chiamate alle API
```

## I file

| File | Cosa fa | Ruolo |
|---|---|---|
| `rimborsi.py` | Legge `dati/note_spese.csv` (o l'export passato come argomento) e `dati/massimali.csv` e stampa l'esito di ogni nota, il riepilogo per città e il totale | ⌨️ obiettivo 2 |
| `assistente.py` | L'agente con `cerca_documenti` e `query_db`; ricorda la conversazione in `sessioni.db` | 🧰 l'assistente del modulo; obiettivo 1 |
| `indicizza.py` | Carica, pulisce e divide in chunk i documenti di `ufficio/`, calcola gli embedding e li salva in `indice/` | 🧰 |
| `aikit/` | Il toolkit del corso: loader, pulizia, chunking, embedding, collection Chroma, client LLM | 🧰 |
| `tests/test_rimborsi.py` | I nove test di `rimborsi.py`: sei su `controlla()`, tre con il programma lanciato da terminale | 🧰 |
| `tests/test_assistente.py` | I test dell'assistente che non chiamano il modello: database, `query_db`, indice | 🧰 |
| `tests/__init__.py` | Rende `tests/` un pacchetto, vuoto | 🧰 |
| `AGENTS.md` | Le istruzioni per il coding agent: le regole del corso e la parte sul progetto (scritta nella lezione scorsa) | ⌨️ si aggiorna nell'obiettivo 2 |
| `OBIETTIVI.md` | I tre obiettivi di Modulo 4 · Lezione 3, con l'avvio e i punti di ripartenza | ⌨️ |
| `SPIEGAZIONE.md` | Le vostre risposte, una sezione per obiettivo | ⌨️ lo scrivete voi |
| `ticket-report.md` | Il ticket del report mensile, con i criteri di accettazione (obiettivo 3) | 📄 |
| `ticket-confronto.md` | Il ticket 215, il confronto con il mese prima: l'estensione dell'obiettivo 3, per chi ha finito | 📄 |
| `requirements.txt` | Le dipendenze del modulo, con le versioni fissate | 🧰 |
| `.env.example` | Il modello del file con la chiave | 🧰 |
| `pytest.ini` | Dice a pytest dove stanno i test e da dove si importa | 🧰 |
| `.gitignore` | Tiene fuori da git la chiave, l'indice, le sessioni, i file generati | 🧰 |
| `dati/` | Gli export del gestionale: `note_spese.csv` (1.500 note, gennaio-agosto 2026; l'export nuovo ha in fondo la colonna `notti`), `massimali.csv`, `dipendenti.csv`, `assenze.csv`, `export-ottobre.csv` (le note di settembre, esportate il 1° ottobre), e `valtesa.db` con le tabelle `note_spese`, `massimali`, `dipendenti` e `assenze` | 📄 |
| `output/` | Fuori da git: le pagine che scrive `report.py` (obiettivo 3) | 📄 generato |
| `ufficio/` | I sei documenti dell'ufficio del personale: policy trasferte, circolari 2026, regolamento ferie, regolamento welfare, procedura di ingresso, FAQ del portale | 📄 |
| `indice/` | L'indice dei documenti, fuori da git: lo costruisce `indicizza.py` | 📄 generato |
| `../ripartenza/` | Fuori da questa cartella, perché il coding agent non la legga: `rimborsi.py` e `AGENTS.md` con la correzione dell'obiettivo 2, e `report.py` a metà (calcola i numeri, manca la pagina), per l'obiettivo 3 | ⌨️ solo se servono |
| `solutions/` | Solo sul branch `soluzioni` della repo studenti: la soluzione del docente (`AGENTS.md`, `MAPPA.html`, `SPIEGAZIONE.md`, `specifica.md`, `prova_tool.py`, `rimborsi.py`, `report.py`, `tests/test_rimborsi.py`, `tests/test_report.py`, con gli stessi percorsi); in `solutions/estensione/` `report.py` e `tests/test_report.py` con il ticket 215, da copiare sopra quelli dell'obiettivo 3 | ⌨️ da guardare dopo |
| `scaffolding/` | Solo nel materiale del docente, non nella repo studenti: `make_valtesa.py` genera `dati/` e `ufficio/` da `valtesa_contenuti.py` e da `sorgenti/note_spese_m4l1.csv` (le note della trace di Modulo 4 · Lezione 1); `check_lab03.py` controlla le soluzioni | 🧰 docente |

Ruoli: 🧰 ambiente e codice del progetto · ⌨️ su cui lavorate voi, con il
coding agent · 📄 documenti e dati.

## Le regole dei rimborsi, in breve

- I massimali sono per voce (pranzo, cena, hotel a notte, taxi a corsa) e per
  città: Milano, Torino e Roma. Sono nell'art. 6 della policy trasferte
  (`ufficio/policy-trasferte-note-spese.docx`) e in `dati/massimali.csv`.
- Dal 1° luglio 2026 a Milano la cena passa da 45 a 55 € e l'hotel da 130 a
  150 € a notte (circolare 7/2026, in `ufficio/circolari-personale-2026.html`).
  Vale il massimale in vigore nel giorno della spesa.
