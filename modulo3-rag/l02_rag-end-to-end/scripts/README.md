# Modulo 3 · Lezione 2 — RAG End-to-End (from scratch) · guida agli script

Lezione infrasettimanale (📊 teoria + 🎤 live coding + ⌨️ esercizio, 2h): lo
script sparso del Progetto Modulo 2 diventa `rag.py`, la pipeline unica del
modulo — tre funzioni piatte (`indicizza()` · `recupera()` · `rispondi()`) e
un dizionario `CONFIG` in cima al file. Stasera nasce anche il **corpus del
modulo**: il Lumen esteso a sei documenti, generato da `make_dataset.py` e
indicizzato una volta per tutte nella collection `lumen_m3` (82 chunk). Da
qui a Modulo 3 · Lezione 14 non cambia più.

Il docente live-coda `indicizza()` (plumbing già noto dal Modulo 2); gli
studenti scrivono da soli `recupera()` e `rispondi()` — la consegna completa
è in `CONSEGNA.md`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 live coding del docente ·
⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (le stesse del Progetto Modulo 2). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la stessa chiave del Modulo 2. |
| `CONSEGNA.md` | ⌨️ | La consegna dell'esercizio (TODO 2 e TODO 3) e il criterio di "fatto". |
| `scaffolding/aikit/` | 🧰 | Il toolkit del Modulo 2, **invariato**: loaders, clean, llm_client, embeddings, search, vectorstore, chunk. Stasera `rag.py` ne usa cinque; `llm_client` e `search` restano per continuità e non servono. |
| `scaffolding/make_dataset.py` | 🧰 | Genera il corpus Lumen esteso in `dataset/lumen_m3/` (deterministico, trappole documentate nel docstring). Il corpus è già generato: si rilancia solo per ricostruirlo da zero. |
| `scaffolding/check_lab02.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura + wiring, tutto mockato); `--solutions` per la versione completa; `--live` fa chiamate vere (ingest + grounding + rifiuto + trappole). Non compare nel percorso studente. |
| `scaffolding/demo_reveal.py` | 🧰 | **Strumento del docente**: la demo del follow-up nel reveal — lancia sulle soluzioni la domanda sui ticket e poi "E per il secondo caso?", con pausa `[invio]` tra le due. Non compare nel percorso studente. |
| `working/rag.py` | 🎤⌨️ | **L'unico file della serata**: `CONFIG`, TODO 1 (live coding), TODO 2-3 (esercizio), main con feedback per ogni TODO completato. |
| `solutions/rag.py` | 🧰 | La versione completa di `working/rag.py`, stesso nome file (import identici). |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen: i tre già noti dal Modulo 2 (identici byte per byte) + listino/catalogo, knowledge base ticket, changelog dei rilasci → 82 chunk. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI del Modulo 2
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/rag.py            # il file della serata (al primo avvio indicizza: ~2 min di attenzione, costo irrisorio)

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab02.py                       # struttura + wiring: istantaneo, zero costi
python scaffolding/check_lab02.py --solutions           # regressione sulla versione completa
python scaffolding/check_lab02.py --solutions --live    # chiamate vere: ingest, grounding, rifiuto, trappole
python scaffolding/demo_reveal.py                       # la demo del follow-up per il reveal (blocco 4)
```

Numeri di riferimento (misurati con chiamate reali): 82 chunk da 6 documenti;
l'embedding dell'intero corpus costa 8.547 token ≈ $0,0002. Il main
re-indicizza solo se la collection è vuota.

> **Prima dell'aula (docente):** se durante le prove hai indicizzato versioni
> intermedie del corpus, cancella `scripts/chroma/` e rilancia
> `python solutions/rag.py`: i numeri a schermo devono combaciare con quelli
> in slide (82 chunk, conteggio per documento). Poi prova una volta
> `python scaffolding/demo_reveal.py`. Infine, **subito prima dell'aula,
> cancella di nuovo `scripts/chroma/`**: il live coding deve trovare la
> collection vuota, così l'indicizzazione parte davvero a schermo.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 30')**: le tre interfacce della pipeline, il punto unico di
   configurazione, citazioni e grounding, i chunk usati come strumento di
   debug; il corpus esteso a sei documenti.
2. **Live coding (🎤, 30')**: `indicizza()` in `working/rag.py`, replicando
   dal docente; si lancia e si vede il conteggio per documento, poi si
   rilancia e i chunk non raddoppiano.
3. **Esercizio (⌨️, 45')**: `recupera()` e `rispondi()` da soli, consegna in
   `CONSEGNA.md`; fatto quando la citazione punta a un chunk vero e la
   domanda fuori corpus produce il rifiuto pulito.
4. **Reveal e ponte (📊, 15')**: due `rispondi()` a confronto, poi la demo
   del follow-up che fallisce (`python scaffolding/demo_reveal.py`, esegue
   il docente) — il problema di Modulo 3 · Lezione 3.

## Diagnosi rapida in aula (docente)

- Studente bloccato → `python scaffolding/check_lab02.py` dice quale TODO
  non è cablato e perché.
- `NotFoundError` sulla collection → succede quando `indicizza()` ricrea la
  collection da zero mentre un riferimento aperto prima punta ancora a
  quella vecchia: rilanciare `python working/rag.py`.
- Risposte senza citazione ma chunk giusti → il prompt non chiede le
  parentesi quadre: guardare il prompt, non il retrieval.
