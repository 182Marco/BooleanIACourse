# L20 — Semantic Search · consegna

Stasera il corpus vettorizzato di martedì si **interroga**: col docente si
riapre il corpus (`carica_corpus`), poi scrivete VOI le due funzioni di
ricerca e le mettete alla prova sulle query — prima le tre del main, poi
quelle "a sorpresa" che il docente dà una alla volta. Tutto si lancia dalla
cartella `scripts/`.

## Setup (una volta sola, nei primi minuti della teoria)

Ogni lezione ha la sua cartella `scripts/` col suo venv: quello di stasera
è **nuovo** (non si riusa quello di L19). Se `scripts/.venv` esiste già,
il setup l'avete già fatto: saltate al blocco successivo.

Aprite il terminale **nella cartella della lezione** (quella scaricata da
Drive, che contiene `scripts/` — un `ls` deve mostrarvela), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L19
```

> Chiave persa (laptop cambiato, `.env` cancellato)? **Alzate la mano**: il
> docente ha una chiave di riserva.

> `sentence-transformers` è **commentato** in `requirements.txt`: il
> `pip install` qui sopra NON lo installa. Scommentatelo **solo** se a L19
> avete embeddato il corpus col backend `local`: apritelo con l'editor
> (es. VS Code) e controllate `corpus_meta.json` → `"backend"`. In quel
> caso, su Linux, installate prima torch CPU (istruzioni nel
> `requirements.txt`).

## Il corpus: il VOSTRO, di martedì

La ricerca gira sul corpus embeddato di L19. Se avete i vostri file,
**copiateli in `dataset/`** al posto della copia di riserva:

```bash
cp ../../lezione-19-embeddings/scripts/working/corpus_embeddings.npz dataset/
cp ../../lezione-19-embeddings/scripts/working/corpus_meta.json dataset/
```

(adattate il percorso a dove avete la cartella di L19). Se il comando dà
`No such file or directory` — struttura cartelle diversa, o esercizio di
L19 non finito — **lasciate perdere e usate la riserva già in `dataset/`**:
è identica, non serve altro.

## Live coding col docente (🎤 si replica) — `working/search.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `carica_corpus()`: npz + meta + testi, nello stesso ordine | il docente la prova a schermo — 48 testi, 48 vettori, il backend — e la vostra fa lo stesso |

## Esercizio 1 (⌨️ da soli) — sempre `working/search.py`

Scrivete le due funzioni di ricerca. **Prescritti solo i nomi, le variabili
del main e lo scopo**: il come è vostro — soluzioni diverse sono benvenute.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 2 | `search(query, k)`: i k testi più simili, dal più simile in giù, ognuno con il suo score | su `QUERY_FACILE` la FAQ sulla spedizione esce **prima**, con score staccato dagli altri |
| 3 | `search_mmr(query, k, lambda_)`: come search, ma i k li sceglie MMR | su `QUERY_DOPPIONI` la lista cambia faccia — e con `lambda_=1.0` le due liste **coincidono** (provatelo: è il vostro test) |

Poi **provate**: nel main ci sono `QUERY_FACILE`, `QUERY_GENERICA`,
`QUERY_DOPPIONI`, più `K` e `LAMBDA`. Per ciascuna query confrontate le due
funzioni **variando K e LAMBDA**: cosa cambia tra le due liste? Quando MMR
aiuta e quando no?

```bash
python working/search.py                  # le vostre prove (~$0.000002 a lancio)
```

## Esercizio 2 (⌨️ + discussione) — i round del docente

**Nessun file nuovo**: si lavora ancora nel vostro `working/search.py`. Il
docente dà **una query alla volta** (non le vedete in anticipo): avete
qualche minuto per provarla con `search` e `search_mmr`, cercando i valori
di `K` e `LAMBDA` che danno i risultati migliori — poi si discute insieme
cosa è uscito (che fascia di score? meglio top-k o MMR? perché?).

## Cosa portate a casa

`search.py` (top-k + MMR, scritti da voi) entrerà nel toolkit `aikit/`
dalla prossima lezione, dove la stessa ricerca verrà **riscritta sopra un
vector DB** (sabato, L21) — più le **fasce di score** osservate nei round e
il vostro criterio per la soglia. **Non cancellate** il corpus in
`dataset/`: serve anche sabato.
