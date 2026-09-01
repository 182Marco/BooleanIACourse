# Modulo 3 · Lezione 1 — RAG Architecture · guida agli script

Lezione infrasettimanale (📊 teoria forte + 🎤 demo, 2h): il progetto del
Modulo 2 scopre di chiamarsi RAG e di avere quattro modi di fallire —
retrieval miss, context overflow, hallucination nonostante il contesto,
lost-in-the-middle. **Stasera nessuno scrive codice**, né docente né
studenti: la demo si esegue e si commenta. Per questo non ci sono `working/`
né `solutions/`: tutto vive in `scaffolding/`.

La pipeline della demo è quella del Progetto Modulo 2, tale e quale
(load → clean → chunk → embed → index, poi search → prompt con grounding →
risposta strutturata), sul corpus Lumen già noto. Le quattro query della
demo falliscono **davvero**: verificate con chiamate reali, 5 run su 5
ciascuna — se se ne cambia una, il failure può non scattare più.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 demo eseguita dal docente ·
📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (le stesse del Progetto Modulo 2). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la stessa chiave del Modulo 2. |
| `scaffolding/aikit/` | 🧰 | Il toolkit del Modulo 2, **invariato**: loaders, clean, llm_client, embeddings, search, vectorstore, chunk. |
| `scaffolding/demo_failure.py` | 🎤 | La demo dei quattro failure mode: il docente la **esegue e commenta**, con pausa `[invio]` tra le sezioni. Versione singola: non si scrive a schermo. |
| `scaffolding/check_lab01.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura + wiring, tutto mockato); `--live` riproduce i quattro failure con chiamate vere. Non compare nel percorso studente. |
| `dataset/lumen/` | 📄 | I tre documenti lunghi Lumen già noti dal Modulo 2 (manuale LumaDesk, policy resi e garanzia, guida smart working) → 45 chunk. |

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
python scaffolding/demo_failure.py               # la demo della serata (chiave vera, ~2 centesimi)

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab01.py                # struttura + wiring: istantaneo, zero costi
python scaffolding/check_lab01.py --live         # i quattro failure con chiamate vere
```

Prima dell'aula: `check_lab01.py --live` tutto `[OK]`. I failure sono
stabili (5/5 nelle prove di preparazione) ma passano dal modello: le
verifiche live hanno due tentativi ciascuna.

## Percorso in aula (le slide sono la regia: lo switch ha la sua slide)

1. **Ripasso attivo (📊, 20')**: sei domande sul Modulo 2 con reveal, poi la
   rimappatura di `app.py` sull'anatomia ingest / retrieve / generate.
2. **Il pattern Retriever-Generator (📊, 25')**: retriever, generator, cosa
   passa in mezzo; grounding e citazioni; offline vs online; k, chunk size,
   soglia.
3. **RAG vs fine-tuning vs long-context (📊, 15')**: i criteri di scelta.
4. **I quattro failure mode (📊, 20')**: la tassonomia, un sintomo per
   failure.
5. **Demo (🎤, 30')**: `scaffolding/demo_failure.py`, quattro sezioni, si
   compila insieme il catalogo dei failure case.
6. **La mappa del modulo (📊, 10')**: quale lezione cura quale failure.
