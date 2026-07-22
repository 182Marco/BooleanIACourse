# L19 — Embeddings · consegna

Stasera il testo diventa **numeri**: costruiamo `embeddings.py` (col docente,
dal vivo) e poi vettorizzate il corpus Lumen da soli. Tutto si lancia dalla
cartella `scripts/`.

## Setup (una volta sola)

Aprite il terminale **nella cartella della lezione** (quella scaricata, che
contiene `scripts/`), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # solo Linux
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L15
```

> Il corpus (`dataset/corpus_lumen.jsonl`) è **già pronto**: non serve
> lanciare `scaffolding/make_dataset.py` (serve solo a rigenerarlo).

## Prima mossa del live coding: il download del modello locale

Il modello del backend `local` si scarica al primo uso (~88 MB). Lanciate il
download **subito**, in un secondo terminale, e lasciatelo lavorare — nel
secondo terminale il venv va **riattivato** (`source .venv/bin/activate`,
sempre da `scripts/`):

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## Live coding col docente (🎤 si replica) — `working/embeddings.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `cosine_similarity(a, b)` a mano in numpy | il check dà `[OK]` sui 5 casi noti |
| 2 | i due backend: `embed_openai` (API, a pagamento) e `embed_local` (gratis, offline) | la demo in fondo al file stampa `[openai] … token → $…` e le similarità |
| 3 | `embed(texts, backend=...)` con **cache su disco** | il check conferma: lo stesso testo non si ricalcola |

Verifica a ogni salvataggio (istantanea, **zero costi**, niente rete):

```bash
python scaffolding/check_lab19.py
```

> A fine live coding è **normale** vedere ancora dei `[FAIL]` sulle sezioni
> TODO 4-6 e sul deliverable: arrivano con l'esercizio. Contano gli `[OK]`
> su cosine, errori e cache.

## Esercizio (⌨️ da soli) — `working/esplora_corpus.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 4 | `indice_per_id`: il ponte id → riga (le coppie parlano per id, i vettori per posizione) | il check dà `[OK]` sul dizionario |
| 5 | `misura_coppie`: la similarità delle 6 coppie assegnate (facili + trappole), via TODO 4 | la tabella è stampata e sai dire PERCHÉ ogni numero è alto o basso |
| 6 | `salva`: il corpus vettorizzato su disco | esistono `corpus_embeddings.npz` + `corpus_meta.json` |

```bash
python working/esplora_corpus.py          # backend openai (costa ~$0.000055, la cache evita i rilanci)
python scaffolding/check_lab19.py         # tutto [OK]?
python scaffolding/check_lab19.py --live  # il giro vero via API (~$0.000002)
```

**Stretch per chi finisce prima (facoltativo):** rilanciate con
`python working/esplora_corpus.py local` (gratis) e confrontate le due
trappole coi due backend. Restano **fuori dalla serata**: Cohere, il
parametro `dimensions`, `text-embedding-3-large` — se ne riparla più avanti.

## Cosa portate a casa

`embeddings.py` entrerà nel toolkit `aikit/` dalla prossima lezione: giovedì (L20) il corpus
vettorizzato di stasera si interroga — query → i 5 testi più vicini. **Non
cancellate** `corpus_embeddings.npz` e `corpus_meta.json`.
