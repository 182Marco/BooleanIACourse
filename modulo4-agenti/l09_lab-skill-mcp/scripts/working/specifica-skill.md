# Specifica: la skill `ingresso-nuovo-assunto`

## La richiesta dell'ufficio

Per ogni nuovo assunto di `dati/assunzioni.csv`, un task in Trello con le
attività del suo ruolo, chi le fa e la scadenza, secondo la procedura
PR-PER-04 (`ufficio-completo/procedura-ingresso-dotazioni.pdf`). Rilanciata,
la skill non rifà chi c'è già.

## I fatti

- I giorni lavorativi vanno dal lunedì al venerdì, senza le festività
  nazionali: 1 e 6 gennaio, lunedì di Pasqua, 25 aprile, 1 maggio, 2 giugno,
  15 agosto, 1 novembre, 8 dicembre, 25 e 26 dicembre.
- L'indirizzo di posta è `nome.cognome@valtesa.it`, minuscolo, senza accenti,
  spazi e apostrofi; se in `dati/dipendenti.csv` c'è già qualcuno con lo
  stesso nome e cognome, un numero dopo il cognome: 2 se c'è un omonimo, 3
  se ce ne sono due.
- La skill sta in `.claude/skills/ingresso-nuovo-assunto/`. Le date e
  l'indirizzo li calcola uno script, `scadenze.py`, nella cartella del
  progetto, con i suoi test in `tests/test_scadenze.py`; si lancia con
  `python scadenze.py ID` per un ingresso e `python scadenze.py --tutti` per
  tutti.
- I file di `dati/` e di `ufficio-completo/` non si modificano. In Trello si
  crea, non si modifica né si cancella niente che c'era già.

## La procedura

<!-- Da scrivere voi: i passi che la skill fa seguire al coding agent, in
ordine, dal file dei nuovi assunti al riepilogo finale. Dove si prendono le
date, come si scelgono le attività di una persona, cosa si legge in Trello
prima di scrivere. -->

## Lo script

<!-- Da scrivere voi: cosa stampa scadenze.py per un nuovo assunto, e con
--tutti. Quali date della procedura servono (prima dell'ingresso, il primo
giorno, dopo), quali sono in giorni lavorativi e quali di calendario, che
data dare a quelle che la procedura lascia aperte (la visita medica, il
colloquio, i corsi «prima della mansione»), e cosa provano i suoi test. -->

## La descrizione

<!-- Da scrivere voi: una o due frasi, su una riga, nel campo description di
SKILL.md. Cosa fa la skill e quando usarla, con le parole con cui chiederete
di preparare un ingresso. Su una riga, senza «parola: testo»: l'intestazione è
YAML (Modulo 4 · Lezione 7). -->

## Il formato in Trello

<!-- Da scrivere voi: dove stanno gli ingressi (lo spazio si chiama
«Valtesa · nuovi ingressi»), com'è fatto il task di una persona (il titolo,
cosa c'è dentro), com'è scritta un'attività (chi la fa, la scadenza), e come
si riconosce un ingresso già preparato. Un esempio di titolo: «Elena Fabbri ·
ingresso 16/11/2026». -->

## Criteri di accettazione

<!-- Da scrivere voi: da tre a cinque, ognuno verificabile guardando la
sessione, Trello, o lanciando un comando. Pensate ai casi diversi: la
stagista, chi ha già un attestato, chi usa il carrello, l'omonima, l'ingresso
a ridosso di una festività, la stessa richiesta fatta due volte. -->

## Cosa ha deciso le attività

<!-- Da scrivere voi, alla fine: due righe. Per una persona a scelta, cosa
nella skill (la tabella, una riga della procedura, le note) ha deciso quali
attività ha avuto. -->

## Seconda parte: a che punto sono gli ingressi

### La richiesta dell'ufficio

A una data (per esempio il 9 novembre 2026), un file con chi deve fare cosa
entro i 5 giorni lavorativi dopo, diviso per responsabile, letto da Trello
senza scriverci.

### I fatti

- Le spunte stanno nelle checklist delle card, e si leggono con
  `trelloReadChecklist`: la lettura delle card le dà vuote.
- Il file è `output/solleciti-AAAA-MM-GG.md`. La data 5 giorni lavorativi
  dopo la stampa `python scadenze.py --entro AAAA-MM-GG`, un'opzione nuova
  dello script, con il suo test.

### Cosa fa la seconda parte

<!-- Da scrivere voi: cosa entra nel file e cosa no (le attività spuntate,
quelle già scadute, quelle senza una data), come si divide, e come cambia la
descrizione della skill perché si apra anche con «a che punto sono gli
ingressi?». -->

### Criteri di accettazione della seconda parte

<!-- Da scrivere voi: due o tre, verificabili confrontando il file con Trello. -->
