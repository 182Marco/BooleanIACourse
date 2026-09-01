# Modulo 3 · Lezione 2 — RAG End-to-End · consegna

Si lavora in **un solo file**: `working/rag.py`. Dentro ci sono la `CONFIG`
in cima, tre funzioni e un main già pronto che le prova in sequenza — ogni
funzione completata fa comparire il suo pezzo di output.

## TODO 1 — `indicizza()` (🎤 la scriviamo insieme)

L'ingest del corpus: load → clean → chunk → embed → upsert nella collection
`lumen_m3`, con id `<documento>-<numero>` e metadata `source`. Si scrive
durante il live coding, replicando dal docente.

## TODO 2 — `recupera(query, k)` (⌨️ da soli)

I `k` chunk più pertinenti per la query (il `k` di default sta in `CONFIG`).
Ogni chunk è un dict con `id`, `testo`, `score`, `source`. La collection si
riapre dentro la funzione con
`vectorstore.apri_collection(CONFIG["collection"])`.

## TODO 3 — `rispondi(query)` (⌨️ da soli)

Il giro completo: recupera i chunk, costruisce il prompt RAG a sezioni
marcate (quello di Modulo 2 · Lezione 11: risposta SOLO dai documenti,
citazione della fonte tra parentesi quadre, rifiuto pulito se la risposta
non c'è) e ritorna **la risposta insieme ai chunk usati**.

Promemoria per la chiamata al modello (la stessa del Modulo 2, il client
`client` è già pronto in cima al file):

```python
r = client.responses.create(model=CONFIG["modello"],
                            input=[{"role": "user", "content": prompt}])
testo = r.output_text
```

## Quando è fatto

Lancia `python working/rag.py` dalla cartella `scripts/` e guarda l'output:

- sulla domanda **nel corpus**, la risposta cita una fonte tra parentesi
  quadre, e quella fonte compare tra i chunk stampati sopra — aprendo il
  chunk, l'informazione c'è davvero;
- sulla domanda **fuori corpus**, la risposta è il rifiuto pulito, non
  un'invenzione.

Il formato esatto della citazione è una scelta tua: conta che punti a un
chunk vero.

Il testo completo del prompt è sulla slide «Il prompt RAG si riusa, non si
riscrive» — ed è lo stesso del tuo `rag.py` di Modulo 2 · Lezione 11.

## Se finisci prima

Gira il `k` in `CONFIG` (2, poi 8), rilancia e guarda come cambiano i chunk
stampati e la risposta. Poi prova domande tue sui documenti nuovi (ticket,
listino, changelog): il criterio resta lo stesso — la citazione punta a un
chunk vero. Rilanciare non è un problema di costi: un giro completo del
main (tre domande) resta sotto il millesimo di dollaro.
