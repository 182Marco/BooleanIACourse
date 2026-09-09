# Modulo 2 · Lezione 8 — Semantic Search · consegna

Stasera il corpus vettorizzato della lezione scorsa si **interroga**: col
docente si legge `carica_corpus()` (già scritta), poi scrivete VOI le due
funzioni di ricerca e le mettete alla prova sulle query — prima le tre del
main, poi quelle "a sorpresa" che il docente dà una alla volta. Tutto si
lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti della teoria)

Ogni lezione ha la sua cartella `scripts/` col suo venv: quello di stasera
è **nuovo** (non si riusa quello di Modulo 2 · Lezione 7). Se `scripts/.venv` esiste già,
il setup l'avete già fatto: saltate al blocco successivo.

Aprite il terminale **nella cartella della lezione** (quella scaricata da
Drive, che contiene `scripts/` — un `ls` deve mostrarvela), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 7
```

> Chiave persa (laptop cambiato, `.env` cancellato)? **Alzate la mano**: il
> docente ha una chiave di riserva.

> `sentence-transformers` è **commentato** in `requirements.txt`: il
> `pip install` qui sopra NON lo installa. Scommentatelo **solo** se a Modulo 2 · Lezione 7
> avete embeddato il corpus col backend `local`: apritelo con l'editor
> (es. VS Code) e controllate `corpus_meta.json` → `"backend"`. In quel
> caso, su Linux, installate prima torch CPU (istruzioni nel
> `requirements.txt`).

## Il corpus: il VOSTRO, della lezione scorsa

La ricerca gira sul corpus embeddato di Modulo 2 · Lezione 7. Se avete i vostri file,
**copiateli in `dataset/`** al posto della copia di riserva (sempre dalla
cartella `scripts/`, come tutto il resto — se avete chiuso il terminale,
rifate `cd scripts`):

```bash
cp ../../lezione-07-embeddings/scripts/working/corpus_* dataset/
```

(adattate il percorso a dove avete la cartella di Modulo 2 · Lezione 7). Se il comando dà
`No such file or directory` — struttura cartelle diversa, o esercizio di
Modulo 2 · Lezione 7 non finito — **lasciate perdere e usate la riserva già in `dataset/`**:
è identica, non serve altro.

## Lettura guidata col docente (🎤) — `working/search.py`

`carica_corpus()` è **già scritta**: si legge insieme, riga per riga — npz +
meta + testi, nello stesso ordine, e il backend dal meta. Fatto quando:
lanciando il file, la prima riga stampa `corpus: 48 testi, vettori
(48, 1536), backend=openai` (o `local`, se il vostro corpus è locale).

## Esercizio 1 (⌨️ da soli) — sempre `working/search.py`

Scrivete le due funzioni di ricerca, **in quest'ordine**. Prescritti solo i
nomi, le variabili del main e lo scopo: il come è vostro — soluzioni diverse
sono benvenute. Il main è già scritto: prova le tre query con entrambe le
funzioni e stampa i risultati **con gli score accanto**.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `search(query, k)`: i k testi più simili, dal più simile in giù, ognuno con il suo score | su `QUERY_FACILE` la FAQ sulla spedizione esce **prima**, con score staccato dagli altri |
| 2 | `search_mmr(query, k, lambda_)`: come search, ma i k li sceglie MMR | su `QUERY_DOPPIONI` la lista cambia faccia — e con `LAMBDA = 1.0` nel main le due liste **coincidono** (cambiatela, rilanciate, confrontate: è il vostro test) |

> Se il tempo stringe: **prima `search`** — è quello che serve alla prossima
> lezione. MMR si completa insieme al debrief.

Poi **provate**: nel main ci sono `QUERY_FACILE`, `QUERY_GENERICA`,
`QUERY_DOPPIONI`, più `K` e `LAMBDA`. Per ciascuna query confrontate le due
funzioni **variando K e LAMBDA**: cosa cambia tra le due liste? Quando MMR
aiuta e quando no?

```bash
python working/search.py                  # le vostre prove (~$0.000002 a lancio)
```

**Stretch per chi finisce prima (facoltativo):** inventate una query vostra
per famiglia — una sensata, una vaga, una fuori dominio — e guardate in che
fascia cade il top-1 di ciascuna: vi tornerà utile alla discussione finale
sulle fasce. Il backend `local` e altri modelli restano **fuori dalla
serata**.

## Esercizio 2 (⌨️ + discussione) — i round del docente

**Nessun file nuovo**: si lavora ancora nel vostro `working/search.py`. Il
docente dà **una query alla volta** (non le vedete in anticipo): sostituite
una delle query nel main con quella del round, rilanciate il file e
provatela con `search` e `search_mmr`, cercando i valori di `K` e `LAMBDA`
che danno i risultati migliori — poi si discute insieme cosa è uscito (che
fascia di score? meglio top-k o MMR? perché?).

## A fine serata: `search.py` entra nel toolkit

Prima di chiudere, **lanciate voi** questo comando (lo facciamo tutti insieme
nel wrap-up): promuove il file che avete scritto in `aikit/`, accanto a
`embeddings.py` della lezione scorsa.

```bash
cp working/search.py scaffolding/aikit/search.py
```

## Cosa portate a casa

`aikit/search.py` (top-k + MMR, scritto da voi) — nella prossima lezione
(Modulo 2 · Lezione 9) la stessa ricerca verrà **riscritta sopra un vector
DB** — più le **fasce di score** osservate nei round e il vostro criterio
per la soglia. **Non cancellate** il corpus in `dataset/`: serve anche
nella prossima lezione.
