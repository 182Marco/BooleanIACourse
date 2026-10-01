# Leggere una trace — scheda (soluzione)

Modulo 4 · Lezione 1 · da soli · 20 minuti

La trace è in `dataset/trace-claude-code.md`: una sessione vera di Claude
Code sul controllo delle note spese di Valtesa, con due richieste (correggere
un bug, poi esportare un file Excel).

Per ogni domanda scrivete tre cose:

- **Risposta**: quello che trovate nella trace, con il punto (richiesta e
  numero di chiamata).
- **Pezzo della harness**: uno degli otto della lezione (il giro, i limiti,
  gli errori, il contesto, gli output, i tool, i permessi, la traccia): il
  pezzo che riguarda quella situazione, anche quando a gestirla è il
  modello. Se ne vanno bene due, scriveteli tutti e due.
- **Voi**: dove ne avete scritto la versione di base, se c'è: la lezione e
  il nome nel codice (la tabella è in fondo a questa scheda).

Due parole della trace: una **chiamata** è un invio della harness al
modello (il turno di Modulo 3 · Lezione 10); una **richiesta** è un
messaggio dell'utente con tutte le chiamate che ne seguono (lo scambio di
Modulo 3 · Lezione 11). Non serve
capire ogni comando bash: la descrizione tra parentesi dice cosa fa.

Fatto quando: le sei domande hanno risposta, pezzo e «Voi». Niente codice
da scrivere.

## 1. Da cosa si capisce, nella trace, che il giro di una richiesta è finito? Quante chiamate servono alla seconda richiesta?

- Risposta: il giro finisce quando il modello scrive la risposta senza
  chiedere tool: nella prima richiesta alla chiamata 7, nella seconda alla
  chiamata 5. La seconda richiesta usa 5 chiamate (la prima 7).
- Pezzo della harness: il giro.
- Voi: `if not chiamate: return r.output_text, usati` in `chiedi()`, Modulo 3
  · Lezioni 7-9.

## 2. Tra una chiamata e l'altra la harness aggiunge dei messaggi che nessuno ha scritto (le righe «Aggiunto dalla harness»), e a volte una riga dentro un risultato. Di che tipo sono, e cosa dicono? (Non serve far tornare i numeri del budget di token.)

- Risposta: tra una chiamata e l'altra, due tipi. `total_tokens_reminder`,
  dopo ogni richiesta dell'utente e dopo ogni risultato: i token di budget che restano secondo la harness
  (per esempio «14971834 tokens left»); non è la finestra del modello. Nella
  prima richiesta il numero è 15.000.000 meno i token in ingresso e in
  uscita dell'ultima chiamata (27.979 + 187 = 28.166): è la grandezza della
  conversazione rispetto a un budget. Nella seconda richiesta il conteggio
  riparte. `task_reminder`, nella seconda richiesta: la lista dei compiti in
  corso, qui vuota. Dentro un risultato: «Shell cwd was reset to …» alla fine
  della chiamata 6 della prima richiesta (vale anche la riga in fondo al
  risultato di `Write`, domanda per chi finisce prima). Stanno tutti in coda
  alla conversazione, non in cima: l'inizio resta uguale e la cache regge.
- Pezzo della harness: il contesto; per il budget vanno bene anche i limiti.
- Voi: Modulo 3 · Lezione 3, `riassumi()` in `chat.py`: mette nella storia
  «Riassunto della conversazione finora: …» e «D'accordo, ne tengo conto.»,
  due messaggi che nessuno ha scritto. Vale anche Modulo 3 · Lezione 8,
  `query_db`: aggiunge «(mostrate solo le prime 50 righe)» dentro il
  risultato.

## 3. In una chiamata il modello chiede due `Edit` insieme. Quale chiamata, su quali file, con quali parametri? Cosa gli risponde la harness? E cosa sarebbe successo se il testo da sostituire fosse comparso due volte nel file? (La definizione di `Edit` è in testa alla trace.)

- Risposta: prima richiesta, chiamata 4. Il primo `Edit` è su `rimborsi.py`
  (la correzione di `massimale()`), il secondo su `tests/test_rimborsi.py`
  (i test nuovi). Per ognuno il modello passa `file_path`, `old_string` (il
  testo da sostituire, copiato dal file), `new_string` (il testo nuovo) e
  `replace_all: false`. La harness li esegue tutti e due e risponde a
  ognuno «The file … has been updated successfully.». Se `old_string`
  fosse comparso due volte, la modifica non sarebbe stata fatta: la
  definizione dice «be unique — the edit fails otherwise», e il modello
  avrebbe ricevuto un errore (come `str_replace` di Anthropic in slide:
  «Multiple occurrences … Please ensure it is unique»). Avrebbe dovuto
  copiare più righe attorno, o usare `replace_all: true`.
- Pezzo della harness: i tool (va bene anche il giro, per i due tool
  insieme, e gli errori, per il caso delle due occorrenze).
- Voi: Modulo 3 · Lezione 7, nome, descrizione e parametri scritti da voi
  (la classe Pydantic); il `for` su tutte le `function_call` di `chiedi()`,
  Modulo 3 · Lezione 9.

## 4. Dopo la correzione il modello deve dire quante note cambiano esito, senza leggere i due output interi (più di 100.000 caratteri l'uno). Come fa?

- Risposta: prima richiesta. Chiamata 3: manda l'output del controllo su un
  file (`$PY rimborsi.py > $S/prima.txt`) e ne legge solo l'ultima riga.
  Chiamata 5: dopo la correzione fa lo stesso su `dopo.txt`, poi confronta i
  due file con `diff` e conta le righe cambiate (19). Chiamata 6: le conta
  per voce (7 cene e 12 hotel a Milano).
- Pezzo della harness: gli output. Qui a proteggersi è il modello, nella
  cartella temporanea che la harness gli ha dato; se non lo facesse, sarebbe
  la harness a tagliare o salvare su file l'output troppo lungo.
- Voi: `LIMITE = 50` righe in `query_db`, Modulo 3 · Lezione 8.

## 5. Nella seconda richiesta qualcosa va storto. Cosa, e cosa fa il modello dopo?

- Risposta: seconda richiesta, chiamata 1: `ModuleNotFoundError: No module
  named 'openpyxl'`. L'errore torna al modello come risultato del tool. Nella
  chiamata 2 il modello dice che non vuole toccare le dipendenze del
  progetto e installa `openpyxl` in una cartella temporanea, poi scrive lo
  script di export lì (chiamata 3) e lo lancia (chiamata 4).
- Pezzo della harness: gli errori.
- Voi: l'errore SQL che `query_db` rimanda al modello come testo, Modulo 3 ·
  Lezione 8.

## 6. All'ultima chiamata della seconda richiesta, quanti token vengono dalla cache e quanti no? Perché?

- Risposta: chiamata 5: 37.694 letti dalla cache, 2.105 scritti in cache, 2
  nuovi. Dalla chiamata prima la harness ha solo aggiunto in coda (l'ultimo scambio: la richiesta di tool del modello e il suo risultato): l'inizio è identico e il fornitore del modello
  lo ha già in cache.
- Pezzo della harness: il contesto (la cache).
- Voi: la cache la fa il fornitore del modello; alla harness tocca non
  rompere l'inizio della conversazione. Anche il vostro giro aggiunge solo in
  coda: va bene «`storia += r.output` in `chiedi()`, Modulo 3 · Lezione 9»,
  o le lezioni della riga «il contesto» della tabella (Modulo 3 · Lezioni 3,
  7, 9 e 11).

## Per chi finisce prima

Nella chiamata 3 della prima richiesta il modello salva i risultati in
`/tmp/claude/scratchpad`. In quale punto della trace la harness gli ha detto
che quella cartella esiste?

Il risultato di `Write` nella chiamata 3 della seconda richiesta finisce con
«(file state is current in your context — no need to Read it back)». Chi
l'ha scritto, e a cosa serve?

- Risposta: in testa alla trace, «Il messaggio dell'utente, prima della
  richiesta»: tra i promemoria c'è l'ambiente, con una cartella temporanea
  per i file di lavoro (`/tmp/claude/scratchpad`). L'utente non l'ha mai
  nominata.

- Seconda domanda: l'ha scritta la harness, in fondo al risultato del tool:
  non viene dal modello né dal file. Dice al modello che non serve rileggere
  il file appena scritto per controllarlo: a quanto si vede, la harness
  tiene lo stato dei file che il modello ha letto e scritto (il codice di
  Claude Code non è pubblico). È lo stesso elenco per cui `Edit`
  fallisce su un file mai letto (la definizione in testa alla trace, «You
  must Read the file … or the call will fail»). Risparmia una chiamata e dei
  token.

## La tabella delle lezioni (per la colonna «Voi»)

| Pezzo | Dove | La vostra versione |
|---|---|---|
| Il giro | Modulo 3 · Lezioni 7-9 | `chiedi()` |
| I limiti | Modulo 3 · Lezioni 8-10 | `MAX_CHIAMATE = 6`, poi `max_turns` |
| Gli errori | Modulo 2 · Lezione 3, Modulo 3 · Lezione 8 | il client che riprova da solo; l'errore SQL torna al modello come testo |
| Il contesto | Modulo 3 · Lezioni 3, 7, 9 e 11 | `ISTRUZIONI` e `TOOLS` a ogni chiamata; `riassumi()`, che mette nella storia due messaggi che nessuno ha scritto; la storia che cresce solo in coda (`storia += r.output`); la sessione col tetto |
| Gli output | Modulo 3 · Lezione 8 | `LIMITE = 50` righe, e la riga «(mostrate solo le prime 50 righe)» aggiunta al risultato |
| I tool | Modulo 3 · Lezione 7 | nome, descrizione e parametri da una classe Pydantic |
| I permessi | Modulo 3 · Lezione 8 | il database aperto in sola lettura, `mode=ro` |
| La traccia | Modulo 2 · Lezione 3, Modulo 3 · Lezioni 9-10 | il costo, la strada presa, il tracing |
