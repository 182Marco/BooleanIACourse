# Leggere una trace — scheda

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

- Risposta:
- Pezzo della harness:
- Voi:

## 2. Tra una chiamata e l'altra la harness aggiunge dei messaggi che nessuno ha scritto (le righe «Aggiunto dalla harness»), e a volte una riga dentro un risultato. Di che tipo sono, e cosa dicono? (Non serve far tornare i numeri del budget di token.)

- Risposta:
- Pezzo della harness:
- Voi:

## 3. In una chiamata il modello chiede due `Edit` insieme. Quale chiamata, su quali file, con quali parametri? Cosa gli risponde la harness? E cosa sarebbe successo se il testo da sostituire fosse comparso due volte nel file? (La definizione di `Edit` è in testa alla trace.)

- Risposta:
- Pezzo della harness:
- Voi:

## 4. Dopo la correzione il modello deve dire quante note cambiano esito, senza leggere i due output interi (più di 100.000 caratteri l'uno). Come fa?

- Risposta:
- Pezzo della harness:
- Voi:

## 5. Nella seconda richiesta qualcosa va storto. Cosa, e cosa fa il modello dopo?

- Risposta:
- Pezzo della harness:
- Voi:

## 6. All'ultima chiamata della seconda richiesta, quanti token vengono dalla cache e quanti no? Perché?

- Risposta:
- Pezzo della harness:
- Voi:

## Per chi finisce prima

Nella chiamata 3 della prima richiesta il modello salva i risultati in
`/tmp/claude/scratchpad`. In quale punto della trace la harness gli ha detto
che quella cartella esiste?

Il risultato di `Write` nella chiamata 3 della seconda richiesta finisce con
«(file state is current in your context — no need to Read it back)». Chi
l'ha scritto, e a cosa serve?

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
