# La griglia delle domande (Lab 2)

La scheda del Lab 2: si compila a mano mentre gira `assistente.py`, una
riga per domanda. Prima le colonne di sinistra (la strada attesa, quella
presa, l'esito); poi, per le domande sbagliate, la leva che si prova e
cosa succede dopo.

**Le strade** (le stampa il main, riga `strada:` sotto ogni risposta)

| Strada | Quando |
|---|---|
| documenti | ha usato `cerca_documenti` |
| dati | ha usato `query_db` |
| documenti+dati | tutti e due |
| nessuna | nessun tool: ha risposto da sé, o ha rifiutato senza cercare |

**Gli esiti**

| Esito | Cosa vuol dire |
|---|---|
| giusta | strada attesa e risposta vera; oppure la risposta non c'era e lo dice, senza citare niente |
| strada sbagliata | ha preso un'altra strada: per esempio ha risposto dai documenti senza guardare il database |
| risposta sbagliata | strada giusta, ma la risposta non torna con i documenti o con i dati; oppure dice di non aver trovato, e nei documenti c'era |
| inventata | la risposta non c'era, e ha risposto lo stesso; oppure ha detto di non trovarla ma ha citato chunk che non c'entrano |

Per sapere qual è la risposta vera: i documenti sono in
`dataset/lumen_m3/`, i dati si guardano con `python scaffolding/sql.py
"<query>"`.

**Le due leve** (tutte e due in `working/assistente.py`)

| Leva | Dove | Cosa muove |
|---|---|---|
| le istruzioni | `ISTRUZIONI` | quando usare quale tool, come citare, quando rifiutare |
| la descrizione del tool | la docstring di `CercaDocumenti` | se e quando il modello sceglie i documenti, e cosa sa che c'è dentro (i ticket, i rilasci) |

## Le domande

| # | domanda | strada attesa | strada presa | ricerche (quante, con che parole) | esito | leva | dopo |
|---|---------|---------------|--------------|------|-------|------|------|
| 1 |         |               |              |      |       |      |      |
| 2 |         |               |              |      |       |      |      |
| 3 |         |               |              |      |       |      |      |
| 4 |         |               |              |      |       |      |      |
| 5 |         |               |              |      |       |      |      |
| 6 |         |               |              |      |       |      |      |
| 7 |         |               |              |      |       |      |      |
| 8 |         |               |              |      |       |      |      |
| 9 |         |               |              |      |       |      |      |
| 10 |        |               |              |      |       |      |      |

Se servono altre righe, si aggiungono.

«Dopo» = strada presa ed esito con la leva attiva, rilanciando **tutte** le
domande: se una che era giusta ora non lo è più, si scrive qui. Il modello
non è deterministico: prima di dire che una leva ha rotto qualcosa, quella
domanda va in `SOLO` e si rilancia due volte.

## Con cosa chiudo

```
ISTRUZIONI: cosa ho cambiato →
descrizione di cerca_documenti: cosa ho cambiato →
```
