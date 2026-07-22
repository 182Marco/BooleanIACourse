# Scheda esperimenti — Lab Prompt & Search

Una riga per giro. **Annotate PRIMA di cambiare la manopola successiva**,
così la storia dei tentativi resta leggibile. Le quattro query sono quelle
nel main di `rag.py` (facile · trappola · fuori-corpus · facile-2).

Esito per query: ✔ corretta e fondata · ✂ incompleta/parziale · ✗ sbagliata
o inventata · ∅ rifiuto (corretto solo per la query fuori-corpus)

## Lab 1 — A/B di prompt

Config di partenza: `GROUNDING=morbido · CON_COT=False · CITAZIONE=breve`.
Cambiate UNA manopola alla volta rispetto alla riga precedente.

| # | GROUNDING | CON_COT | CITAZIONE | facile | trappola | fuori-corpus | facile-2 | token out (tot.) | costo (tot.) | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | morbido | no | breve | | | | | | | baseline |
| 2 | severo | no | breve | | | | | | | |
| 3 | morbido | sì | breve | | | | | | | |
| 4 | morbido | no | estesa | | | | | | | |
| 5 | | | | | | | | | | combinazione a scelta vostra |

**Quale variante vince, e su quali query si stacca dalle altre?**

—

## Lab 2 — tuning del retrieval

Config di partenza: `K=4 · SOGLIA=0.0` sulla collection `recursive/500`
(la riserva di L22-L23). Una manopola alla volta.

| # | K | SOGLIA | strategia/size collection | facile | trappola | fuori-corpus | facile-2 | note |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 0.0 | recursive/500 | | | | | baseline |
| 2 | 8 | 0.0 | recursive/500 | | | | | |
| 3 | 4 | 0.0 | recursive/800 (reindicizza_chunks) | | | | | |
| 4 | | | | | | | | manopola a scelta vostra |

**Quale modifica ha cambiato visibilmente la risposta finale? Sapete
spiegare perché** (guardate i chunk recuperati con `cerca_chunk`, non solo
la risposta finale)?

—

## Conclusione della giornata

Prompt vincente: —

Configurazione di retrieval vincente: —

Perché (in due righe):
