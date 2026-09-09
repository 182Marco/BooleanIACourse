# Modulo 2 · Lezione 7 — Embeddings · consegna

Stasera il testo diventa **numeri**: costruiamo `embeddings.py` (col docente,
dal vivo) e poi vettorizzate il corpus Lumen da soli. Tutto si lancia dalla
cartella `scripts/`.

## Setup (una volta sola, durante la teoria)

Aprite il terminale **nella cartella della lezione** (quella scaricata, che
contiene `scripts/`), poi:

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # solo Linux (su Windows/macOS saltatela)
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di Modulo 2 · Lezioni 1-3
python scaffolding/scarica_modello.py   # il modello locale (~88 MB), parte ora così è pronto dopo
```

> La chiave è quella che avete già usato (di solito nel `.env` della cartella
> di una lezione scorsa). Se non la ritrovate, chiedetela al docente.

> Il corpus (`dataset/corpus_lumen.jsonl`) è **già pronto**: non serve
> lanciare `scaffolding/make_dataset.py` (serve solo a rigenerarlo).

## Live coding col docente (🎤 si replica) — `working/embeddings.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `cosine_similarity(a, b)` a mano in numpy | lanciando il file, la prima riga stampa `cosine su vettori noti: 1 / 0 / -1` |
| 2 | i due backend: `embed_openai` (API, a pagamento) e `embed_local` (gratis, offline) | — |
| 3 | `embed(texts, backend=...)`: un if sui backend | la demo in fondo al file gira e stampa le similarità: A~B alta, A~C bassa, per entrambi i backend |

Per provare, a ogni passo:

```bash
python working/embeddings.py
```

## Esercizio (⌨️ da soli) — `working/esplora_corpus.py`

`carica_corpus()` e `salva()` sono **già scritte**: a voi le due funzioni in
mezzo.

| TODO | Cosa | Fatto quando |
|---|---|---|
| 4 | `indice_per_id`: il ponte id → riga (le coppie parlano per id, i vettori per posizione) | il dizionario ha 48 voci e `"faq-01"` punta a `0` |
| 5 | `misura_coppie`: la similarità delle 6 coppie assegnate (facili + trappole) | la tabella è stampata e sai dire PERCHÉ ogni numero è alto o basso |

```bash
python working/esplora_corpus.py    # un giro completo costa ~$0.000055
```

Fatto quando: la tabella delle coppie è stampata e in `working/` sono
comparsi `corpus_embeddings.npz` + `corpus_meta.json`.

**Stretch per chi finisce prima (facoltativo):** cambiate `BACKEND` in
`"local"` nel main e rilanciate (gratis): confrontate le due trappole coi
due backend. Attenzione: **ogni giro sovrascrive i due file** in `working/` —
dopo lo stretch richiudete con un ultimo giro con `BACKEND = "openai"`, è la
versione che serve alla prossima lezione. Restano **fuori dalla serata**:
Cohere, il parametro `dimensions`, `text-embedding-3-large` — se ne riparla
più avanti.

## A fine serata: `embeddings.py` entra nel toolkit

Prima di chiudere, **lanciate voi** questo comando (lo facciamo tutti insieme
nel wrap-up): promuove il file che avete scritto in `aikit/` — dalla prossima
lezione si importa, non si riscrive.

```bash
cp working/embeddings.py scaffolding/aikit/embeddings.py
```

## Cosa portate a casa

`aikit/embeddings.py` e il corpus vettorizzato: nella prossima lezione
(Modulo 2 · Lezione 8) si interroga — query → i 5 testi più vicini. **Non
cancellate** `corpus_embeddings.npz` e `corpus_meta.json` da `working/`.
