# L19 — Embeddings · guida agli script

Infrasettimanale (🎤 + 📊, 2h): il testo diventa **numeri che catturano il
significato**. Col docente si scrive `embeddings.py` — `cosine_similarity` a
mano in numpy, due backend dietro la stessa firma (`openai` a pagamento /
`local` gratis e offline), **cache su disco** — poi da soli si vettorizza il
**corpus Lumen** (48 testi brevi) misurando le 6 coppie assegnate, trappole
comprese. Il corpus embeddato (`corpus_embeddings.npz`) è l'input diretto di
L20 (ricerca semantica) e L21 (vector DB). Niente notebook, solo script `.py`.

Il check base è **strutturale**: istantaneo, zero costi e zero rete (la
matematica si verifica su vettori noti, la pipeline gira su un backend finto
iniettato nel registro); il giro reale via API sta dietro `--live`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `numpy`, `sentence-transformers`; su Linux prima `torch` CPU per evitare ~2 GB di pacchetti CUDA). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L15**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/make_dataset.py` | 🧰 | (Ri)genera il corpus: 48 testi brevi di Lumen S.r.l. (12 FAQ, 12 descrizioni, 12 ticket, 12 recensioni), con le coppie-esercizio progettate e documentate nel docstring. |
| `dataset/corpus_lumen.jsonl` | 📄 | Il corpus: una riga = `{"id", "tipo", "testo"}`. Testi **corti apposta** (il chunking arriva a L22) e già puliti (il lavoro sporco l'avete fatto a L18). |
| `working/embeddings.py` | 🎤 | **Live coding** (TODO 1-3): `cosine_similarity` a mano, i backend `embed_openai`/`embed_local`, `embed()` con registro `EMBEDDERS` e cache su disco. Si scrive col docente; riferimento in `solutions/`. |
| `working/esplora_corpus.py` | ⌨️ | **Esercizio** (TODO 4-6): costruire il ponte id → riga, embeddare il corpus, stampare la similarità delle 6 coppie assegnate, salvare `corpus_embeddings.npz` + `corpus_meta.json`. |
| `scaffolding/check_lab19.py` | 🧰 | Verifica `[OK]/[FAIL]` per requisito — **istantanea, zero costi, zero rete**, da lanciare a ogni salvataggio; `--live` fa 3 embedding veri (~$0.000002); `--solutions` per il docente. |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import), più il corpus vettorizzato di riferimento. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # solo Linux
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L15
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `.cache_embeddings/` (git non li versiona). Il
> primo uso del backend locale scarica il modello (88 MB) nella cache di
> Hugging Face: in aula si lancia a inizio live coding, non serve prepararlo
> da casa.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/embeddings.py                  # demo: 3 frasi, similarità a confronto
python working/esplora_corpus.py              # esercizio: corpus + coppie + npz (openai)
python working/esplora_corpus.py local        # stesso giro col modello locale (gratis)
python scaffolding/check_lab19.py             # verifica working/: istantanea, zero costi
python scaffolding/check_lab19.py --live      # 3 embedding veri via OpenAI (~$0.000002)
python scaffolding/check_lab19.py --solutions # per il docente: verifica solutions/
```

## Le idee da trasmettere (coi numeri misurati, luglio 2026)

1. **L'embedding vede il significato, non le parole.** La coppia faq-03 ↔
   tic-05 ("regolare l'altezza" / "impostare la posizione": zero parole
   chiave in comune) fa **0.637**, contro lo 0.284 della coppia di controllo.
   È ciò che il keyword matching non farà mai.
2. **…ma vede il TEMA, non la verità.** La trappola rec-03 ↔ rec-04 (stessa
   recensione, verdetto ribaltato: "la consiglio" / "non la consiglio") è la
   coppia **più simile di tutte: 0.866**. Chi costruisce retrieval deve
   saperlo.
3. **Il modello si sceglie coi numeri, non per fede.** Sul cross-lingua
   (faq-03 IT ↔ faq-09 EN) `text-embedding-3-small` fa 0.650, il MiniLM
   locale **crolla a 0.193**; e sull'italiano il locale separa peggio
   (controllo a 0.417 vs 0.284). In cambio: gratis, offline, i testi **non
   escono di casa**. È il trade-off costo / latenza / privacy.
4. **I valori assoluti non si confrontano tra modelli.** 0.6 di OpenAI e 0.6
   di MiniLM non sono "la stessa similarità": conta l'**ordinamento dentro
   un modello**, non il numero in sé.
5. **Embeddare è economico, ri-embeddare è evitabile.** L'intero corpus fa
   2767 token → **$0.000055**; API 1.5s, locale 0.28s di encode (+ ~6s di
   load), rilancio tutto in cache 0.1s. La cache su disco è mentalità L14:
   lo stesso testo non si paga due volte — e a scala (milioni di chunk) il
   conto torna a esistere.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 45')**: spazio semantico, dimensionalità, cosine, modelli e
   costi.
2. **Live coding (🎤, 50')**: `working/embeddings.py` col docente, TODO 1-3;
   il download del modello locale si lancia subito; in coda la demo con le
   trappole (negazione, multilingua).
3. **Esercizio (⌨️, 20')**: `working/esplora_corpus.py` da soli, TODO 4-6;
   fatto quando la tabella è stampata, l'npz è su disco e il check è tutto
   `[OK]`.
4. **Wrap-up (📊, 5')**: cosa portate a casa; giovedì il corpus si interroga
   (L20). Non cancellate `corpus_embeddings.npz`.
