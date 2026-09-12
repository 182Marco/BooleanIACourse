# La griglia dei failure

La scheda della giornata: si compila a mano mentre gira `debug.py`, una
riga per failure. Nel **Lab 2** si riempie la prima tabella (cosa dice la
diagnostica, e il caso); nel **Lab 3** la seconda (la leva e cosa è
successo). Le due tabelle si legano per **numero**.

Sei failure sono il minimo, e due cure. Se ne servono altre righe, si
aggiungono.

**I casi**

| Caso | Cosa dice la diagnostica |
|---|---|
| A | esiste, non è nel top-k, **vicino**: entro i `candidati` guardati (10) |
| B | esiste, non è nel top-k, **lontano**: oltre i 10 (per vedere dove sta, `candidati = 30`) |
| C | non esiste (frase attesa `None`) e il modello lo dice: non è un failure, si annota e non conta tra i sei |
| D | non esiste e il modello risponde lo stesso |
| E | è nel top-k, e la risposta non lo usa |
| F | tutto giusto, ma con un `k` alto che costa su ogni domanda: non si incontra nel Lab 2, si produce nel Lab 3 alzando `k` |

**Quale leva per quale caso** (il dettaglio è in `CONSEGNA.md`; dove sta
ogni file, in `MAPPA.md`)

| Caso | Leve |
|---|---|
| A | `k` più alto · `retrieval` → `"rerank"` · `"hybrid"` (le parole esatte, i codici) |
| B | `"hybrid"` se nella domanda c'è un codice; altrimenti nessuna leva di oggi |
| D | `soglia` (solo col semantico o con rerank Cohere) · `istruzioni` |
| E | `"rerank"` per metterlo primo + `k` basso · `istruzioni` |
| F | `k` più basso, verificando che resti giusta |

## Lab 2 — i failure trovati

«Giusta» = la risposta cita il chunk atteso, o dice «Non lo trovo nei
documenti.» se la risposta non è nel corpus.

| # | domanda | frase attesa | esiste? | posizione | giusta? | caso |
|---|---------|--------------|---------|-----------|---------|------|
| 1 |         |              |         |           |         |      |
| 2 |         |              |         |           |         |      |
| 3 |         |              |         |           |         |      |
| 4 |         |              |         |           |         |      |
| 5 |         |              |         |           |         |      |
| 6 |         |              |         |           |         |      |

## Lab 3 — le cure

Una leva alla volta, e `CONFIG` riportata alla baseline tra una prova e
l'altra. «Dopo» = posizione e giusta con la leva attiva. «Regressioni» =
le domande che erano giuste e ora non lo sono più, con il perché.

| # | caso | leva | dopo | regressioni |
|---|------|------|------|-------------|
|   |      |      |      |             |
|   |      |      |      |             |
|   |      |      |      |             |

## La CONFIG con cui chiudo

```python
"retrieval":     # "semantico" · "hybrid" · "rerank"
"backend":       # solo con "rerank": "cohere" · "llm"
"chunk_size":
"soglia":
"k":
"candidati":
"istruzioni":
```

Perché questa:
