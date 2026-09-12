# Modulo 3 · Lezione 6 — dove sta cosa

I file che servono oggi, in ordine di quando si aprono. Tutto si lancia
dalla cartella `scripts/`: ci si entra una volta e si resta lì.

```bash
cd scripts          # se sei già dentro, `ls` mostra CONSEGNA.md e working/
python working/debug.py
```

```
le slide della lezione (PDF)                      accanto a scripts/
scripts/
├── CONSEGNA.md          cosa fare, blocco per blocco
├── MAPPA.md             questo file
├── README.md            setup e guida agli script
├── requirements.txt     le dipendenze del venv
├── .env.example         da copiare in .env con le chiavi
├── working/
│   ├── debug.py         ⌨️ IL FILE DI LAVORO: CONFIG, il query set, i tre TODO
│   └── griglia.md       ⌨️ LA SCHEDA: i failure, le cure, la CONFIG finale
├── dataset/lumen_m3/    i sei documenti Lumen: qui si cercano le frasi attese
├── chroma/              il vector database, creato al primo avvio
└── scaffolding/aikit/   il toolkit: si importa, non si tocca
```

## I tre file su cui si lavora

| Quando | File | Cosa ci si fa |
|---|---|---|
| Lab 1 | `working/debug.py` | i tre TODO: `trova_nel_corpus()`, `diagnostica()`, `giro()` |
| Lab 2 | `working/debug.py` → `LE_MIE_QUERY` | le domande avversarie vostre, con la frase attesa |
| Lab 2 e 3 | `working/griglia.md` | una riga per failure, poi la cura e le regressioni |
| Lab 3 | `working/debug.py` → `CONFIG` | una leva alla volta, e si rilancia il giro |

`dataset/lumen_m3/` sono i sei documenti su cui il sistema risponde: si
aprono per leggere i testi e copiare la frase attesa di una domanda
propria.

## Il toolkit: `scaffolding/aikit/`

Sono i moduli scritti nelle lezioni scorse. `debug.py` li importa e oggi
**non si toccano**: tutte le leve si girano da `CONFIG`.

| Modulo | Da dove viene | Cosa usa `debug.py` |
|---|---|---|
| `rag.py` | Modulo 3 · Lezione 2-3 | `recupera(query, k)` (il retrieval semantico), `genera(chunks, domanda)` (la risposta con le citazioni), `CONFIG` (collection e chunk size), `ISTRUZIONI` (le regole del prompt), `indicizza()` |
| `hybrid.py` | Modulo 3 · Lezione 4 | `cerca_hybrid(query, k)` (BM25 + semantico fusi con RRF), `costruisci_indice_bm25()`, `INDICE["chunks"]` (tutti i chunk, dove `trova_nel_corpus()` cerca) |
| `rerank.py` | Modulo 3 · Lezione 5, da oggi in `aikit/` | `cerca_due_stadi(query, k_largo, k_finale, backend)` (recupera tanti candidati e li riordina con Cohere o con l'LLM) |
| `vectorstore.py` | Modulo 2 · Lezione 9 | `apri_collection()`, per sapere se il corpus è già indicizzato |

Sotto ci sono anche gli altri moduli del Modulo 2 (`chunk.py`,
`clean.py`, `embeddings.py`, `llm_client.py`, `search.py`, `loaders/`):
li usano `rag.py` e `hybrid.py`, non `debug.py`.

## `chroma/`: il vector database

Non c'è finché non si lancia il file la prima volta. Al primo avvio
`debug.py` indicizza i sei documenti e crea qui la collection
`lumen_m3`: 82 chunk, un paio di minuti, meno di un centesimo. Dalla
seconda volta parte subito.

Con `CONFIG["chunk_size"]` diverso da 500 ne crea un'altra accanto
(`lumen_m3_300`, e così via), e la prima volta ci mette di nuovo un paio
di minuti. La cartella non viaggia con il materiale: si ricostruisce
sempre da sola.

## Cosa non serve aprire

Se nella vostra copia ci sono `scaffolding/check_lab06.py` e
`scaffolding/make_dataset.py`, sono strumenti del docente: il primo
verifica la lezione, il secondo ha generato i documenti. Se c'è una
cartella `solutions/`, dentro c'è `debug.py` con i tre TODO risolti:
guardarla prima di aver provato toglie l'esercizio.
