# Consegna — Modulo 4 · Lezione 2

## Esercizio: una modifica verificata (33')

Lavorate in questa cartella. Dalla vostra copia della repo del corso:
`git pull`, poi `cd modulo4-agenti/l02_coding-agent/scripts` (`pwd` dice
dove siete). Il coding agent aperto qui:
nell'app di Claude una sessione Local su questa cartella, **senza**
l'opzione worktree (con il worktree l'agente lavora in un'altra cartella
e qui non vedete le sue modifiche); da terminale, `claude` in questa
cartella. In un terminale nella stessa cartella `pytest` e git, con il
venv del modulo attivo:

- macOS, Linux, WSL: `source ../../.venv/bin/activate`
- PowerShell: `..\..\.venv\Scripts\Activate.ps1` (se Windows lo blocca:
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, una volta sola)

Quando il venv è attivo, il prompt del terminale comincia con `(.venv)`.

Il codice lo scrive il coding agent: voi dite cosa volete, leggete il
piano, leggete il diff, verificate.

File che cambiano: `rimborsi.py` (e `tests/test_rimborsi.py`, se l'agente
aggiunge un test).

### I passi

1. **Un branch per il lavoro della lezione**, dopo il `git pull`:
   `git switch -c l02-lavoro` (se il branch c'è già: `git switch
   l02-lavoro`). Poi `git status --short .` deve essere vuoto; il punto
   vuol dire «solo questa cartella». Se non è vuoto, chiamate il docente
   prima di cominciare.
2. **Una modifica di `rimborsi.py` dal menu**, con la richiesta in
   modalità piano. Nella richiesta scrivete anche come la verificherete,
   come i criteri di accettazione della demo di `valida.py`
   (Slide 14; per esempio: «senza argomenti l'ultima riga resta
   identica»). Oggi `AGENTS.md` ha solo le regole del corso (la parte sul
   progetto è un'estensione, per stare nel tempo): quello che
   l'agente deve sapere sul progetto per questa modifica (per esempio
   che `dati/` non si tocca) scrivetelo nella richiesta.
3. **Il piano.** Leggetelo: se va bene, «Yes, manually approve edits»
   (ogni modifica la approvate voi); se no, «No, keep planning» e scrivete
   la correzione. Nell'app di Claude le risposte sono le stesse.
4. **Il diff.** Guardatelo con `git status --short .` (anche i file
   nuovi), `git diff --stat .` e `git diff .` (si esce con `q`). I sei
   controlli: file toccati; righe tolte o cambiate non richieste; test
   cambiati, e perché; dipendenze nuove; valori scritti a mano; cosa non è
   stato lanciato. Poi un commit, che salva il lavoro anche se non
   arrivate al passo 5: `git add .` e `git commit -m "modifica dal
   menu"`.
5. **La verifica fatta da voi**, dal terminale: `pytest`, il
   controllo del menu, e l'ultima riga di `python rimborsi.py` senza
   argomenti (`python rimborsi.py | tail -1`). Se durante il lavoro
   l'agente chiede di lanciare i test, ditegli pure sì: poi li rilanciate
   voi. La verifica vera della modifica è il controllo del menu: `pytest`
   dice che `controlla()` non si è rotto, ma `main()`, dove sta la vostra
   modifica, i test non lo coprono. Se qualcosa non torna, chiedete la
   correzione all'agente, rifate i controlli e un altro commit; per
   ripartire da capo, `git restore --source=main rimborsi.py` e un commit.
   **Se non ci arrivate, va bene.**

Anche se non avete finito, prima di chiudere fate un commit sul branch:
il lavoro resta lì.

### Il menu (una a scelta)

Per tutte e due: senza argomenti l'ultima riga di `python rimborsi.py`
resta `1500 note spese, 293 fuori massimale`.

1. `python rimborsi.py --dipendente "Luca Ferri"`: solo le note di quella
   persona, e quante sono fuori massimale.
   *Il controllo:* `grep -c "Luca Ferri" dati/note_spese.csv` per le note;
   `python rimborsi.py | grep "Luca Ferri" | grep -c FUORI` per i fuori
   massimale. I due numeri si confrontano con quelli che stampa la vostra
   versione.
2. Un riepilogo per città, quante note e quante fuori massimale, prima
   della riga dei totali, che resta l'ultima.
   *Il controllo:* una città contata sul CSV, per esempio
   `grep -c ",Milano," dati/note_spese.csv`; e le somme per città tornano
   ai totali.

Con PowerShell, al posto di `grep` e `tail`:

| Controllo | PowerShell |
|---|---|
| le note di Luca Ferri | `(Select-String -Path dati\note_spese.csv -Pattern "Luca Ferri").Count` |
| i suoi fuori massimale | `(python rimborsi.py \| Select-String "Luca Ferri.*FUORI").Count` |
| una città (modifica 2) | `(Select-String -Path dati\note_spese.csv -Pattern ",Milano,").Count` |
| l'ultima riga | `python rimborsi.py \| Select-Object -Last 1` |

### Fatto quando

- dopo il commit, `git diff main --stat .` (tutto il lavoro del branch)
  mostra solo i file che vi aspettate: `rimborsi.py`, e i test se l'agente
  ne ha aggiunti;
- del diff sapete dire cosa fa ogni parte;
- se ci arrivate: `pytest` verde, lanciato da voi (se fallisce solo il
  test sull'indice dei documenti, basta `pytest tests/test_rimborsi.py`), il numero della modifica che torna con il
  vostro controllo, e senza argomenti l'ultima riga ancora `1500 note
  spese, 293 fuori massimale`.

### Se finite prima

Prima un commit di quello che avete fatto, così `git restore` non lo tocca.
Le estensioni con l'agente consumano l'abbonamento, che serve anche al lab
della lezione dopo: `/usage` (nell'app l'anello accanto al menu del
modello) dice quanto ne avete usato. L'ultima, senza coding agent, non
consuma niente.

- **La parte sul progetto di `AGENTS.md`**, come nella demo:
  - la richiesta d'esempio: `Aggiungi in AGENTS.md, sotto le regole del
    corso, una sezione "## Il progetto": come si lancia, come si testa,
    cosa non toccare. Non cambiare le regole del corso.`;
  - può partire anche senza modalità piano, con le modifiche approvate a
    mano (Manual nel selettore dell'app; da terminale Shift+Tab fino a
    `manual mode on`): l'agente tocca solo `AGENTS.md`;
  - nel diff provate i comandi che scrive (`assistente.py` e
    `indicizza.py` chiamano le API: oggi non servono) e tenete una regola
    solo se sapete dire perché c'è;
  - poi `git status --short .` (solo `AGENTS.md`), un commit e `/clear`
    (nell'app una sessione nuova; Codex `/new`): la richiesta dopo parte
    con il nuovo `AGENTS.md`.
- L'altra modifica del menu, dopo un commit e un `/clear` (nell'app una
  sessione nuova).
- Un diff che non vi convince (un file toccato senza motivo, un test
  cambiato, l'ultima riga diversa): `git restore <file>` per i file
  cambiati, i file nuovi si cancellano (`rm`, o dal Finder / Esplora
  risorse), poi una richiesta migliore.
- Senza coding agent: in `controlla()` di `rimborsi.py` cambiate `<=` in
  `<`, poi `pytest` e l'ultima riga di `python rimborsi.py`. Quanti test
  se ne accorgono, e perché gli altri no? Poi `git restore rimborsi.py`.

### Alla lezione dopo

`git switch main`, poi `git pull`. Il vostro lavoro resta sul branch
`l02-lavoro`; la cartella della lezione nuova ha già un `AGENTS.md`
completo.

## I comandi

| | Claude Code | Codex |
|---|---|---|
| Avviare, nella cartella | `claude` | `codex` |
| Modalità piano | Shift+Tab, oppure `/plan` davanti alla richiesta · nell'app: Plan nel selettore accanto al tasto di invio | Shift+Tab, oppure `/plan` |
| Cambiare i permessi | Shift+Tab · nell'app: il selettore (Cmd+Shift+M, su Windows Ctrl+Shift+M); Shift+Tab nell'app non vale | `/permissions` |
| Vedere le modifiche | `/diff` · nell'app: l'indicatore `+N -M` | `/diff` |
| Il contesto | `/context` | `/status` |
| Ricominciare con il contesto vuoto | `/clear` · nell'app: una sessione nuova | `/new` |
| Riprendere l'ultima sessione | `claude --continue` | `codex resume --last` |
| Quanto avete usato dell'abbonamento | `/usage` · nell'app: l'anello accanto al menu del modello | `/status` |

Il coding agent legge `AGENTS.md`. Claude Code lo legge solo se nella
cartella o sopra non c'è un `CLAUDE.md`: non lanciate `/init`, e se ne
trovate uno, spostatelo o cancellatelo.
