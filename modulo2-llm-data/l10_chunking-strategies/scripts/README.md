# Modulo 2 · Lezione 10 — Chunking Strategies · guida agli script

Serata infrasettimanale (🎤 + ⌨️ + 📊, 2h): arrivano i **documenti lunghi** di
Lumen e si impara a spezzarli. Col docente si scrivono `chunk_fixed` e
`chunk_recursive` in `working/chunk.py` (si guarda e si replica);
`chunk_semantic` è **già nel file** e il docente la mostra in demo (si usa,
non si scrive). Poi gli esperimenti: si girano le quattro manopole in testa
al file (`STRATEGIA`, `CHUNK_SIZE`, `OVERLAP`, `SOGLIA`), a ogni giro lo
script ri-chunka, ri-embedda, **ricrea la collection** `lumen_chunks` e
rilancia le tre query note — e l'esito si annota nella tabella commentata in
fondo al file. Niente notebook, solo script `.py`.

Il `check_lab10.py` è **strumento del docente**, fuori dal percorso studente
(il "fatto quando" degli esperimenti è l'output osservabile): serve per la
preparazione/regressione dei materiali e per la diagnosi rapida di uno
studente bloccato. La verifica base è **istantanea e a zero costi** (le
funzioni dei due TODO sono Python puro, le trappole si controllano sulle
stringhe); il giro reale via API sta dietro `--live`. Le righe `[--]` sono
requisiti **sospesi** — TODO non ancora scritti, non errori.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`chromadb`, `openai`, `numpy`, `python-dotenv`). Stasera il backend è `openai` per tutti: `sentence-transformers` NON serve. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di Modulo 2 · Lezione 1-9**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/aikit/embeddings.py` | 🧰 | Il modulo di Modulo 2 · Lezione 7: `embed()` e `cosine_similarity()` — stasera riusato anche DENTRO `chunk_semantic`. **Non si tocca**: si importa. |
| `scaffolding/aikit/search.py` | 🧰 | Il brute-force di Modulo 2 · Lezione 8, nel toolkit da Modulo 2 · Lezione 9. Stasera non si usa: resta nel toolkit. |
| `scaffolding/aikit/vectorstore.py` | 🧰 | Il modulo **scritto dagli studenti a Modulo 2 · Lezione 9**, promosso nel toolkit: `crea_collection()` (riparte da zero — la novità di stasera), `apri_collection()`, `indicizza()`, `search()`. **Non si tocca**: si importa. |
| `scaffolding/make_dataset.py` | 🧰 | (Ri)genera i 3 documenti lunghi in `dataset/` e **verifica le trappole** (posizioni dei tagli tarate al carattere, documentate nel docstring). Deterministico. |
| `dataset/guida-smart-working.txt` | 📄 | La policy HR di Lumen (5.100 caratteri) — dentro: il contributo postazione **a cavallo di due paragrafi** (trappola B). |
| `dataset/policy-resi-garanzia.txt` | 📄 | Resi, rimborsi, garanzia (5.396 caratteri) — dentro: la frase dei saldi a cavallo di un taglio fixed(500,0) (trappola A). |
| `dataset/manuale-lumadesk.txt` | 📄 | Il manuale LD-200/LD-210 (5.681 caratteri) — dentro: la procedura E07 in un paragrafo lungo dai molti argomenti (trappola C). |
| `working/chunk.py` | 🎤⌨️ | L'unico file della serata. **TODO 1-2 col docente** (`chunk_fixed`, `chunk_recursive` — si replica); `chunk_semantic` **già scritta** (demo docente); il main fa tutto il giro (chunk → embed → indicizza → tre query) guidato dalle **4 manopole** in testa, stampa i tagli sui due documenti delle trappole A e B e, per ogni query, la **risposta attesa** accanto al 1° risultato; in fondo la **tabella esperimenti** da compilare. Riferimento in `solutions/`. |
| `scaffolding/check_lab10.py` | 🧰 | **Strumento del docente**: `[OK]/[FAIL]` sull'integrità di toolkit e dataset e sugli esiti dei due TODO — taglie, overlap, trappole (base: istantaneo, zero rete); `--live` fa semantic vero + quattro giri di indicizzazione su un DB usa-e-getta (~$0.003); `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `scaffolding/misura_costi.py` | 🧰 | **Strumento del docente**: la tabella token/costo per configurazione citata in slide, da chiamate vere (~$0.001 a lancio). |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import). |

La cartella `chroma/` (il DB su disco, con la collection `lumen_chunks`)
nasce al primo lancio e NON si versiona (`.gitignore`); si **ricrea a ogni
giro** ed è la base del RAG di Modulo 2 · Lezione 11 — a fine serata non va
cancellata. Resta quella dell'**ultimo lancio**: per questo la consegna
chiede di rilanciare con la config scelta prima di chiudere (in dubbio:
`recursive` 500, il punto di ripartenza comune).

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di Modulo 2 · Lezione 1-9
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). Niente corpus
> embeddato stasera: i documenti sono in chiaro in `dataset/` e gli embedding
> si calcolano a ogni giro.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/chunk.py                       # un esperimento = un lancio (~$0.0001-0.0002 a giro)
python scaffolding/check_lab10.py             # verifica working/: istantanea, zero costi
python scaffolding/check_lab10.py --live      # semantic vero + 4 giri su DB usa-e-getta (~$0.003)
python scaffolding/check_lab10.py --solutions # per il docente: verifica solutions/
python scaffolding/make_dataset.py            # rigenera i documenti + verifica delle trappole
python scaffolding/misura_costi.py            # la tabella dei costi per configurazione (~$0.001)
```

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 32')**: l'ordine di esecuzione della pipeline (dove cade il
   chunking), la prova sui documenti interi, le tre strategie, il disegno
   della stessa pagina spezzata nei tre modi, i costi in tre numeri.
2. **Live coding (🎤, 45')**: setup + `chunk_fixed` (TODO 1, si replica) →
   `chunk_recursive` (TODO 2, si replica) → demo `chunk_semantic` (si
   guarda); dopo ogni funzione, lancio su un documento vero e lettura dei
   tagli stampati.
3. **Esperimenti (⌨️, 38')**: le 4 manopole, un giro = una riga della tabella
   in fondo a `working/chunk.py`; fatto quando almeno una configurazione
   porta in testa la risposta integra per ognuna delle tre query — e si sa
   dire quale manopola ha fatto la differenza. Prima di chiudere si rilancia
   con la config scelta: quella resta su disco.
4. **Wrap-up (📊, 5')**: il reveal della tabella, "si sceglie sperimentando",
   ponte a Modulo 2 · Lezione 11 (i chunk di `lumen_chunks` dentro un prompt:
   il primo RAG completo del corso).
