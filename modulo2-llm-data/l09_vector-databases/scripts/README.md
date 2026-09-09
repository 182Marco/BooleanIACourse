# Modulo 2 · Lezione 9 — Vector Databases · guida agli script

> Cerchi le istruzioni della giornata? Parti da **`CONSEGNA.md`**: questa
> guida descrive ogni file della cartella, comprese le parti che servono
> solo a chi prepara la lezione.

Lab del sabato (⌨️ + 🎤 + 📊, 4h): la ricerca della lezione scorsa **trasloca
in un vector DB**. Col docente si apre la collection ChromaDB su disco e si fa
il quick start (`apri_collection`, i primi 3 doc, una query); poi gli
studenti caricano DA SOLI il corpus completo (`carica_corpus_nel_db`),
riscrivono la ricerca sopra il DB (`search`) e la confrontano fianco a fianco
col proprio brute-force della lezione scorsa; nel Lab 2 arrivano
`search_filtrata` (metadata) e le
prove CRUD (delete + update fatto bene). Chiude la demo pgvector del docente
(materiale fuori da `scripts/`) e l'ultimo blocco flessibile: criteri di
scelta, poi Q&A o l'esercizio extra "il 49° documento" (a scelta del
docente).
Niente notebook, solo script `.py`.

Il `check_lab09.py` è **strumento del docente**, fuori dal percorso studente
(il "fatto quando" degli esercizi è l'output osservabile): serve per la
preparazione/regressione dei materiali e per la diagnosi rapida di uno
studente bloccato. Verifica i risultati su un DB usa-e-getta con query prese
dai vettori GIÀ calcolati del corpus (istantaneo, zero costi, zero rete);
le righe `[--]` sono TODO non ancora fatti, non errori; il giro reale via
API sta dietro `--live`. Lanciarlo non fa danni, ma il criterio di
completamento resta l'output dei vostri script, non il check.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`chromadb`, `openai`, `numpy`; `sentence-transformers` è **commentato** — si scommenta solo se il corpus di Modulo 2 · Lezione 7 è col backend `local`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave usata da Modulo 2 · Lezione 1**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della giornata per gli studenti. |
| `scaffolding/aikit/embeddings.py` | 🧰 | Il modulo di Modulo 2 · Lezione 7: `embed()` con backend selezionabile e `cosine_similarity()`. **Non si tocca**: si importa. |
| `scaffolding/aikit/search.py` | 🧰 | Il brute-force **scritto dagli studenti a Modulo 2 · Lezione 8**, promosso nel toolkit: stamattina è il termine di confronto per la ricerca sul DB. **Non si tocca**: si importa. |
| `dataset/corpus_lumen.jsonl` | 📄 | I 48 testi brevi di Lumen S.r.l. (12 FAQ, 12 prodotti, 12 ticket, 12 recensioni): il campo `tipo` diventa il metadata su cui si filtra. |
| `dataset/corpus_embeddings.npz` + `corpus_meta.json` | 📄 | Il corpus vettorizzato: **copia di riserva** identica a quella di Modulo 2 · Lezione 7 e Lezione 8 — chi ha i propri file li copia qui sopra. |
| `working/vectorstore.py` | 🎤⌨️ | L'unico file della giornata. **TODO 1 col docente** (`apri_collection` + quick start nel main); **TODO 2-4 da soli** (`carica_corpus_nel_db`, `search`, `search_filtrata` — prescritti solo nomi, variabili del main e scopo); **TODO 5 nel main** (prove CRUD: delete + update); **TODO 6 extra** (il 49° documento, solo se il docente lo lancia). Il main è **già scritto a stadi** (stampe comprese, con `stampa()` fornita): ogni TODO fatto accende il suo pezzo di output, `[--]` = TODO che manca. Riferimento in `solutions/`. |
| `scaffolding/check_lab09.py` | 🧰 | **Strumento del docente** (preparazione, regressione, diagnosi): `[OK]/[FAIL]` sui risultati, su un DB usa-e-getta — istantaneo, zero costi, zero rete; `--live` fa 2 query vere (~$0.000001); `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `scaffolding/benchmark_ann.py` | 🧰 | Brute-force vs indice ChromaDB sugli stessi vettori sintetici della lezione scorsa: i numeri del "reveal" citati in slide. |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import). |

La cartella `chroma/` (il DB su disco) nasce al primo lancio e NON si
versiona (`.gitignore`); la demo pgvector del docente vive **fuori da
`scripts/`**: `demo-pgvector-docente.md` + `demo-pgvector-carica.py` nella
cartella della lezione.

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI usata da Modulo 2 · Lezione 1
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona); `solutions/`
> arriva solo a fine lezione, sul branch delle soluzioni della repo
> studenti. Chi ha il proprio corpus di Modulo 2 · Lezione 7 lo copia in
> `dataset/` sopra la riserva; per tutti gli altri la riserva funziona
> identica.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/vectorstore.py                 # le prove della giornata (query via API, ~$0.000005 a giro completo)
python scaffolding/check_lab09.py             # verifica working/: istantanea, zero costi
python scaffolding/check_lab09.py --live      # 2 query vere via OpenAI (~$0.000001)
python scaffolding/check_lab09.py --solutions # per il docente: verifica solutions/
python scaffolding/benchmark_ann.py           # brute-force vs indice, misurato (~40 s)
```

## Le idee da trasmettere

Vivono, coi numeri misurati e le tracce di diagnosi, nel materiale di
conduzione del docente (`conduzione-docente.md` nella cartella della
lezione, fuori da `scripts/`, accanto a `demo-pgvector-docente.md`): questa
guida arriva agli studenti.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Brief/teoria (📊, 35')**: da brute-force a indice (i numeri del punto 2),
   modello dati del vector DB, le tre famiglie, la regola degli embedding
   espliciti.
2. **Quick start (🎤, 15')**: `apri_collection` + primi 3 doc + query di
   prova col docente (TODO 1); fatto quando rilanciando lo script i doc sono
   ancora lì.
3. **Lab 1 (⌨️, 75')**: `carica_corpus_nel_db` e `search` da soli (TODO 2-3);
   fatto quando `count()` dice 48 (e resta 48 al rilancio) e le tre query del
   main danno gli stessi documenti in testa del brute-force, fianco a fianco.
4. **☕ Pausa (15')**.
5. **Lab 2 (⌨️, 60')**: `search_filtrata` (TODO 4) e le prove CRUD nel main
   (TODO 5); fatto quando la stessa query cambia faccia col filtro, il doc
   cancellato sparisce e quello aggiornato cambia query di appartenenza.
6. **Demo pgvector (🎤, 15')**: solo docente, materiale fuori da `scripts/`;
   al rientro il parallelo ChromaDB/pgvector e Pinecone, in slide.
7. **Criteri di scelta + ultimo blocco (📊⌨️, 25')**: la tabella di scelta a
   slide, poi due strade a scelta del docente — Q&A aperto (anche sulle
   lezioni passate) oppure l'esercizio extra "il 49° documento" (TODO 6:
   una voce nuova del corpus scritta dallo studente, embed + upsert con id
   nuovo; riferimento in `solutions/`). Chiude il wrap-up col ponte a
   Modulo 2 · Lezione 10 (documenti lunghi → chunking).
