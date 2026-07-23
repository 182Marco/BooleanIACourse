# Modulo 2 · Lezione 15 — Progetto Modulo 2 · guida agli script

Lab del sabato (⌨️ progetto studenti, 4h): tutto il modulo confluisce in
un'unica app RAG, `load → clean → chunk → embed → search → generate`, con
output strutturato in due punti — la risposta finale (Modulo 2 · Lezione 13)
e l'estrazione fatture (Modulo 2 · Lezione 14). Un solo file di lavoro:
`working/app.py`. Niente notebook, solo script `.py`.

`aikit/` ha sette moduli in tutto. Oggi `working/app.py` ne richiama
attivamente **cinque**: `loaders` e `clean`, dormienti da un mese, tornano
necessari ora che il corpus non è più pre-pulito da uno script, insieme a
`chunk`, `embeddings`, `vectorstore` che non hanno mai smesso di servire.
`llm_client` e `aikit.search` restano nel toolkit ma non si usano in questa
lezione (structured outputs passa dal client OpenAI diretto, la ricerca reale
dal vector DB).

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · ⌨️ da completare dagli studenti ·
📄 documenti/dati di esempio · — riferimento docente (non live-codato oggi).

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `pydantic`, `chromadb`, `numpy`, parser di Modulo 2 · Lezione 4). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la stessa di Modulo 2 · Lezioni 1-14. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della giornata per gli studenti. |
| `scaffolding/aikit/loaders/` | 🧰 | Load nativo per formato (Modulo 2 · Lezione 4), promosso da un mese di pausa. |
| `scaffolding/aikit/clean.py` | 🧰 | Pipeline di pulizia componibile (Modulo 2 · Lezione 5), idem. |
| `scaffolding/aikit/llm_client.py` | 🧰 | Client LLM con conteggio costi (Modulo 2 · Lezione 3). |
| `scaffolding/aikit/embeddings.py` | 🧰 | `embed()` con backend selezionabile (Modulo 2 · Lezione 7). |
| `scaffolding/aikit/search.py` | 🧰 | Ricerca brute-force di riferimento (Modulo 2 · Lezione 8). |
| `scaffolding/aikit/vectorstore.py` | 🧰 | Collection ChromaDB (Modulo 2 · Lezione 9-10). |
| `scaffolding/aikit/chunk.py` | 🧰 | Le tre strategie di chunking (Modulo 2 · Lezione 10). |
| `scaffolding/check_lab27.py` | 🧰 | **Strumento del docente**: `[OK]/[FAIL]` su schema e wiring (base: istantaneo, zero rete — mocka client/embeddings/vectorstore); `--live` indicizza davvero la riserva Lumen, cerca, genera, estrae; `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `working/app.py` | ⌨️ | L'unico file della giornata. Quattro TODO: `indicizza_corpus`, `cerca_chunk`, `genera_risposta`, `estrai_fattura`. Riferimento in `solutions/`. |
| `solutions/app.py` | — | La versione **completa** del file di `working/` (stesso nome, stessi import). Riferimento per il docente durante Build/Demo — nessun live coding oggi. |
| `dataset/mio_corpus/` | 📄 | Vuota di proposito: ci mette i propri file lo studente (o la riserva Lumen). |
| `dataset/riserva_lumen/` | 📄 | I tre documenti lunghi Lumen di Modulo 2 · Lezione 10-12, per chi non ha un corpus pronto. |
| `dataset/fatture_lumen/` | 📄 | Le tre fatture Lumen di Modulo 2 · Lezione 14, fisse e uguali per tutti (blocco estrazione). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di Modulo 2 · Lezioni 1-14
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). `dataset/mio_corpus/`
> arriva vuota (solo un `.gitkeep` con le istruzioni).
>
> **Nota diagnostica:** `aikit/loaders/pdf.py` restituisce testo vuoto (non un
> errore) se un PDF è scansionato/immagine e `pypdf` non estrae nulla. Un
> conteggio di chunk basso ma non zero al checkpoint può nascondere questo
> caso, non un bug nel codice dello studente.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/app.py                            # la propria pipeline, con chiave vera

# da qui in giù: solo docente, non fanno parte del percorso studente
python scaffolding/check_lab27.py                 # verifica working/: istantaneo, zero costi
python scaffolding/check_lab27.py --live          # chiamate vere su riserva Lumen + fatture
python scaffolding/check_lab27.py --solutions     # verifica solutions/
```

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Brief progetto (📊, 25')**: lo schema della pipeline completa, perché
   `aikit` si riunisce oggi, il corpus libero (+ riserva), requisiti e rubrica.
2. **Build (⌨️, 170')**: `working/app.py`, i quattro TODO. Nessun live coding:
   il docente gira tra i banchi. Checkpoint informale a metà.
3. **Demo & valutazione (⌨️, 45')**: ogni studente mostra la propria pipeline
   su query del proprio corpus più l'estrazione fatture.
