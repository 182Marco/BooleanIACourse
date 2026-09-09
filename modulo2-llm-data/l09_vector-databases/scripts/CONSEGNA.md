# Modulo 2 · Lezione 9 — Vector Databases · consegna

Stamattina la ricerca della lezione scorsa trasloca: il corpus Lumen entra in
un **vector DB** (ChromaDB) che vive su disco, e la vostra `search()` viene
riscritta sopra il database — stessi risultati, ma indicizzati, persistenti
e filtrabili. Tutto si lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti del brief)

Ogni lezione ha la sua cartella `scripts/` col suo venv: quello di stamattina
è **nuovo** (non si riusa quello della lezione scorsa). Aprite il terminale
**nella cartella della lezione** (quella scaricata da Drive, che contiene
`scripts/`), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI usata da Modulo 2 · Lezione 1
```

> Il `pip install` stamattina è **lungo**: `chromadb` si porta dietro parecchi
> pacchetti. Lanciatelo e lasciatelo andare mentre il brief continua — non
> siete bloccati voi, è il download.

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

> `sentence-transformers` è **commentato** in `requirements.txt`: si
> scommenta solo se il vostro corpus di Modulo 2 · Lezione 7 è col backend
> `local` — aprite `dataset/corpus_meta.json` con l'editor (es. VS Code) e
> guardate la riga `"backend"`. La **riserva** già in `dataset/` è `openai`:
> il dubbio esiste solo se portate il VOSTRO corpus. (Su Linux prima torch
> CPU, istruzioni nel `requirements.txt`.)

**Setup finito quando:** il `pip install` chiude senza errori e
`python working/vectorstore.py` stampa la riga del corpus
(`corpus: 48 testi, …`) — la riga `[--]` sotto è normale: è un TODO della
giornata, ancora da scrivere.

## Il corpus: il VOSTRO, di Modulo 2 · Lezione 7 e Lezione 8

Come nella lezione scorsa: se avete i vostri `corpus_embeddings.npz` +
`corpus_meta.json`, copiateli in `dataset/` sopra la riserva:

```bash
cp ../../lezione-08-semantic-search/scripts/dataset/corpus_* dataset/
```

(adattate il percorso a dove avete la cartella della lezione scorsa). Se il
comando dà `No such file or directory`, **lasciate perdere e usate la
riserva già in `dataset/`**: è identica, non serve altro. (Quel messaggio è
atteso solo qui, sul `cp`: se ve lo dà `python working/vectorstore.py`,
siete nella cartella sbagliata — `cd scripts` e riprovate.)

## Quick start col docente (🎤 si replica) — `working/vectorstore.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `apri_collection()`: client persistente + collection `lumen` (metrica cosine), poi nel main l'upsert dei primi 3 doc (embedding dall'npz, espliciti) e una query di prova | rilanciate lo script e i documenti **sono ancora lì** — nessun npz da ricaricare: il DB vive in `scripts/chroma/` |

## Lab 1 (⌨️ da soli) — il corpus nel DB

Scrivete le due funzioni. **Prescritti solo i nomi, le variabili del main e
lo scopo**: il come è vostro — soluzioni diverse sono benvenute.

Il main è **già scritto a stadi**: stampa il corpus, il count della
collection e le prove (query fianco a fianco col brute-force, poi i filtri)
man mano che i TODO prendono vita — una riga `[--]` è un TODO che manca,
non un errore. Solo le prove CRUD (TODO 5) le scrivete voi, in coda al main.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 2 | `carica_corpus_nel_db(collection)`: upsert dei 48 doc — id, testo, embedding dall'npz, metadata `tipo` | `collection.count()` dice 48, e rilanciando lo script RESTA 48 (upsert, non insert) |
| 3 | `search(query, k)`: i k doc più simili chiesti al DB, risultati come nella lezione scorsa (score, non distanze). Collection e backend non sono parametri: riapriteli/rileggeteli dentro la funzione, come fa il vostro `search.py` della lezione scorsa col corpus | sulle tre query del main, il DB e il vostro brute-force della lezione scorsa (`bruteforce.search`, già importato) mettono in testa **gli stessi documenti**, fianco a fianco |

**Stretch per chi finisce prima (facoltativo):** variate `K` sulle tre
query; poi inventate una query vostra per famiglia — una sensata, una vaga,
una fuori dominio — e guardate se le fasce di score della lezione scorsa
reggono anche dal DB. Il TODO 6 invece resta per l'ultimo blocco, **solo se
il docente lo lancia**.

## Lab 2 (⌨️ da soli) — filtri e CRUD

> Rientrate dalla pausa o avete aperto un terminale nuovo? Prima di tutto:
> `cd scripts` e `source .venv/bin/activate` di nuovo. Un
> `ModuleNotFoundError: No module named 'chromadb'` vuol dire venv non
> attivo — non avete rotto niente.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 4 | `search_filtrata(query, k, tipo)`: la stessa ricerca ma solo tra i doc di un tipo — il parametro di `collection.query` è `where={"tipo": ...}` | la stessa query cambia faccia: senza filtro escono ticket e recensioni, con `tipo="faq"` escono solo FAQ |
| 5 | nel main, le prove CRUD: `delete` di un doc che sta in top-3 (di una delle query del main, a vostra scelta — la firma è `collection.delete(ids=[...])`), poi l'**update fatto bene** — nuovo testo, ri-embed con `embed()`, upsert con lo **stesso id** | il doc cancellato sparisce dai risultati; il doc aggiornato non esce più sulla query di prima e compare su quella nuova |

Il punto del TODO 5: il DB **non si accorge** dei testi cambiati — testo ed
embedding li tenete sincronizzati VOI (è la regola backend/modello della
lezione scorsa, vista dal lato scrittura).

## Esercizio extra (SOLO se il docente lo lancia) — il 49° documento

| TODO | Cosa | Fatto quando |
|---|---|---|
| 6 | il corpus ha 48 voci: scrivetene **una nuova voi** (una FAQ che manca, un ticket realistico) — embed con `embed()`, upsert con **id nuovo** e il **tipo giusto** | `count()` dice **49**; la vostra query la trova **in top-1** (provate con parole diverse dal testo); col filtro del tipo giusto esce, con quello sbagliato no |

```bash
python working/vectorstore.py      # le vostre prove (qualche query via API, ~$0.000005 a giro completo)
```

**Se il DB finisce in uno stato strano** (il `count()` non torna più 48,
doc di prova rimasti in giro — un upsert con un id inventato resta lì anche
ai rilanci): cancellate la cartella `scripts/chroma/` e rilanciate lo
script. Si ricrea da zero — il corpus vero sta sempre nei file di
`dataset/`, non si perde niente.

## Cosa portate a casa

`vectorstore.py` — il corpus in una collection **persistente** con la
ricerca sopra il DB, scritto da voi. Nella prossima lezione (Modulo 2 ·
Lezione 10) arrivano i documenti **lunghi**, e questo modulo lo ritroverete
in `aikit/`, riscritto in forma generica.
