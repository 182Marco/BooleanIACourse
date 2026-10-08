# Modulo 4 · Lezione 3 — Obiettivi

Tre lavori sul progetto Valtesa, su codice che non avete scritto voi.
Lavorate in questa cartella, come nella lezione scorsa: il coding agent
(nell'app o in un terminale) e un terminale per `pytest` e git, con il venv
attivo. Il
codice lo scrive il coding agent; le risposte in `SPIEGAZIONE.md` le
scrivete voi. Alla fine di ogni obiettivo, un commit: `git add .` e `git
commit -m "obiettivo 1"` (con il numero dell'obiettivo).

Gli obiettivi 1 e 2 partono tutti e due dal progetto com'è: se non finite
l'1, passate al 2. Il 3 usa la correzione del 2.

Ogni obiettivo ha un «Se finite prima». Nel coding agent lavorate con
Sonnet 5.5 a effort medio; alto se l'agente salta un file, non lancia i
test o non ricontrolla (come si sceglie: «Avvio»). Il lab usa una parte
della finestra del vostro abbonamento: `/usage` (Codex `/status`) dice
quanta; se finisce, chiamate il docente. Tra un obiettivo e l'altro,
`/clear` (nell'app, una sessione nuova; Codex `/new`): una sessione sola
per tutto il lab si porta dietro tutto il contesto, e consuma molto di
più. A ogni sessione nuova nell'app ricontrollate: Local, senza worktree,
e i due menu del modello e dell'effort.

I sei controlli su un diff, dalla lezione scorsa: file toccati; righe
tolte o cambiate non richieste; test cambiati, e perché; dipendenze
nuove; valori scritti a mano; cosa non è stato lanciato.

## Avvio (5')

Dalla radice della vostra copia della repo del corso (la cartella che
contiene `modulo4-agenti/`):

```
git switch main
git pull
cd modulo4-agenti/l03_lab-codice-non-vostro/scripts
source ../../.venv/bin/activate
cp ../../l02_coding-agent/scripts/.env .env
python indicizza.py
pytest
git switch -c l03-lavoro
```

(Se il branch `l03-lavoro` c'è già: `git switch l03-lavoro`.)

Su PowerShell il venv si attiva con `..\..\.venv\Scripts\Activate.ps1`.
Poi il coding agent in questa stessa cartella: nell'app di Claude una
sessione Local nuova su questa cartella, senza l'opzione worktree (con il
worktree l'agente lavora in un'altra cartella); da terminale `claude` (o
`codex`), nell'altro terminale. Se è ancora aperto quello della lezione
scorsa, chiudetelo: lavora sull'altra cartella e legge l'altro `AGENTS.md`.

Nel coding agent scegliete Sonnet 5.5 con effort medio:

- nell'app, i due menu accanto al tasto di invio: il modello
  (Cmd/Ctrl+Shift+I) e l'effort (Cmd/Ctrl+Shift+E);
- da terminale, `/model sonnet` e poi `/effort medium`: restano anche per
  le sessioni dopo;
- con Codex, `/model`, che sceglie modello ed effort nello stesso menu.

Se Sonnet 5.5 non c'è nell'elenco, aggiornate Claude Code con `claude
update` (serve la versione 2.1.284 o successiva), o aggiornate l'app.

Se qualcosa non parte: la sezione «Se il setup non parte» del `README.md`
di questa cartella.

**Fatto quando** `pytest` dice `14 passed`, `git status --short .` è vuoto
e il coding agent è su Sonnet 5.5, effort medio.

## 1. Orientarsi nel progetto (25')

1. **La mappa.** Fate scrivere all'agente una pagina HTML, `MAPPA.html`:
   i file, cosa fa ognuno, chi chiama chi. Apritela nel browser.
2. **Il controllo.** Almeno cinque voci della mappa, ognuna aprendo il file
   che cita. Dove sbaglia, correggete.
3. **Tre domande**, nella sezione 1 di `SPIEGAZIONE.md`, ognuna con il file
   e la riga in cui avete letto la risposta.

- **Fatto quando:** almeno cinque voci di `MAPPA.html` controllate aprendo
  il file che citano, e corrette dove sbagliavano (quali, in `SPIEGAZIONE.md`); le
  tre risposte con file e riga.
- **Se finite prima:** cominciate l'obiettivo 2, che non dipende da
  questo.
- **Da riguardare:** Modulo 4 · Lezione 2; Modulo 3 · Lezioni 10-12.

## 2. Un bug, riprodotto e corretto (45')

La segnalazione dell'ufficio del personale: «La nota 1441 di Matteo
Barbieri, hotel a Roma dall'11 luglio, tre notti, 390 €, risulta fuori
massimale. Per noi è in regola: potete controllare?»

1. **Riproducete.** `python rimborsi.py | grep 1441`: cosa esce, e cosa vi
   aspettate. Prima di cambiare qualcosa, segnatevi i numeri di controllo:
   - l'ultima riga: `python rimborsi.py | tail -1`;
   - le note fuori massimale che non sono hotel:
     `python rimborsi.py | grep -v hotel | grep -c FUORI`;
   - l'ultima riga con l'export di ottobre (le note di settembre, nel
     formato vecchio, senza la colonna `notti`):
     `python rimborsi.py dati/export-ottobre.csv | tail -1`.
2. **La causa.** In modalità piano, date all'agente la segnalazione e
   chiedete un test che riproduce il caso, senza correggere niente. Il test
   lo lanciate voi: deve fallire (se passa già, non prova il bug).
3. **La correzione.** La fa l'agente; voi leggete il diff, con i sei
   controlli.
4. **La verifica.** Il test nuovo passa, i test di prima pure. Dei numeri
   di controllo cambia solo l'ultima riga.

- **Fatto quando:**
  - la 1441 ora è «ok»; in `SPIEGAZIONE.md` atteso e ottenuto, e la causa
    in due righe;
  - il test nuovo prima falliva e ora passa, e i test che c'erano non
    sono cambiati (in `git diff main tests/` solo righe aggiunte);
    `pytest` verde;
  - l'ultima riga ha il numero nuovo; le note fuori massimale che non sono
    hotel e l'ultima riga con l'export di ottobre sono quelle di prima;
  - in `AGENTS.md`, nella frase «l'ultima riga oggi è …», il numero
    nuovo, scritto da voi (l'agente di solito lo segnala e non lo cambia):
    con quello vecchio l'agente sbaglia i piani dopo.
- **Se finite prima:** leggete il ticket dell'obiettivo 3 e cominciate
  `specifica.md`.
- **Da riguardare:** Modulo 4 · Lezione 2 (il diff); Modulo 4 · Lezione 1.

## ☕ Pausa (15')

## 3. Il report mensile, da un ticket (80')

Il ticket è in `ticket-report.md`. `specifica.md` la scrivete voi;
`report.py` e `tests/test_report.py` li scrive l'agente: sono tutti e tre
file nuovi.

1. **La specifica.** `specifica.md`: cosa fa lo strumento, da dove prende
   i dati, cosa non fa, i criteri di accettazione (quelli del ticket e i
   vostri).
2. **Il piano.** La richiesta in modalità piano, con la specifica. Il piano
   lo correggete prima di dire sì: guardate quali file tocca, se il fuori
   massimale lo chiede a `controlla()` di `rimborsi.py`, quali numeri mette
   nei test.
3. **Il codice.** `report.py` e i test li scrive l'agente; voi leggete il
   diff, con i sei controlli.
4. **La verifica.** I criteri uno per uno, da voi, con la tabella qui
   sotto; `pytest`; la pagina aperta nel browser.

| Criterio | Controllo | Atteso |
|---|---|---|
| 1 · il file | `ls output` | `report-2026-07.html` |
| 2-3 · i numeri di luglio | la pagina contro il ticket | gli stessi numeri |
| 4 · fuori massimale | le righe della tabella nella pagina | 20, e la 1441 non c'è |
| 5 · un mese senza note | `python report.py 2026-12` | una pagina con zero note, senza errori |
| 6 · senza connessione | `grep -cE "https?://" output/report-2026-07.html` | 0; se è 1 per l'`xmlns` di un SVG, fatelo togliere: il criterio è alla lettera, e dentro l'HTML non serve |
| 7 · `dati/` intatta, i test | `git status --short dati/`, `ls tests` | niente in `dati/`; `tests/test_report.py` |

Per aprire la pagina: macOS `open output/report-2026-07.html`; WSL
`explorer.exe "$(wslpath -w output/report-2026-07.html)"`; PowerShell
`start output\report-2026-07.html`; Linux `xdg-open
output/report-2026-07.html`.

- **Fatto quando:**
  - i criteri del ticket verificati da voi, uno per uno;
  - chi è fuori massimale lo decide `controlla()` di `rimborsi.py`;
  - il massimale applicato lo dà una funzione di `rimborsi.py` (nella
    ripartenza si chiama `limite_nota()`; se nel vostro manca, fatela
    aggiungere lì): il report non rifà il calcolo, e si vede nel diff;
  - in `SPIEGAZIONE.md` come avete verificato i criteri, una funzione del
    diff spiegata riga per riga e cosa non avete verificato.
- **Punti di ripartenza**, da questa cartella:
  - se non avete chiuso l'obiettivo 2: `cp ../ripartenza/rimborsi.py
    rimborsi.py` e `cp ../ripartenza/AGENTS.md AGENTS.md`, poi un commit;
  - se dopo un'ora non avete ancora i numeri del ticket: anche
    `cp ../ripartenza/report.py report.py`, che calcola i numeri e non
    scrive la pagina: la pagina la fate aggiungere all'agente. `report.py`
    usa `limite_nota()` del `rimborsi.py` della ripartenza: se non l'avete
    copiato, copiatelo insieme;
  - dopo una copia, `pytest`: se fallisce un vostro test che chiama una
    funzione che nel file copiato non c'è, o che si aspetta una regola
    diversa, toglietelo e scrivetelo in `SPIEGAZIONE.md`.
- **Se finite prima:** il ticket 215, in `ticket-confronto.md`: nella
  pagina del report, il mese prima e la differenza. Stesso giro: la
  specifica, il piano, il codice, i criteri verificati uno per uno.
- **Da riguardare:** Modulo 4 · Lezione 2 (i criteri di accettazione di
  `valida.py`).

## Alla fine: quanto abbonamento avete usato (3')

Nel coding agent `/usage` (Codex `/status`); nell'app, l'anello accanto al
menu del modello. Scrivete nella chat della lezione due numeri: quanta
sessione di 5 ore e quanta settimana avete usato. Per confronto: l'agente
da solo, con Sonnet 5.5 a effort medio, fa il lab con circa l'8% della
finestra di 5 ore di un piano Pro; voi avete fatto più
richieste. Le prossime lezioni di laboratorio e il progetto personale
usano lo stesso abbonamento.

## I comandi

| | Claude Code | Codex |
|---|---|---|
| Scegliere il modello | `/model` (app: il menu accanto al tasto di invio) | `/model` |
| Scegliere l'effort | `/effort` (app: il menu dell'effort, accanto al tasto di invio) | `/model` |
| Modalità piano | Shift+Tab, oppure `/plan` davanti alla richiesta (app: Plan nel selettore delle modalità, Cmd/Ctrl+Shift+M) | Shift+Tab, oppure `/plan` |
| Vedere le modifiche | `/diff` | `/diff` |
| Ricominciare con il contesto vuoto | `/clear` (app: una sessione nuova) | `/new` |
| Quanto avete usato dell'abbonamento | `/usage` (app: l'anello accanto al menu del modello) | `/status` |

Con PowerShell, al posto di `grep` e `tail`:

| | PowerShell |
|---|---|
| la nota 1441 | `python rimborsi.py \| Select-String "1441"` |
| fuori massimale che non sono hotel | `(python rimborsi.py \| Select-String -NotMatch "hotel" \| Select-String -CaseSensitive "FUORI").Count` |
| l'ultima riga | `python rimborsi.py \| Select-Object -Last 1` |
| indirizzi nella pagina | `(Select-String -Path output\report-2026-07.html -Pattern "https?://").Count` |
