# Modulo 2 · Lezione 7 — Embeddings · guida agli script

Infrasettimanale (🎤 + 📊, 2h): il testo diventa **numeri che catturano il
significato**. Col docente si scrive `embeddings.py` — `cosine_similarity` a
mano in numpy, due backend dietro la stessa firma (`openai` a pagamento /
`local` gratis e offline) — poi da soli si vettorizza il **corpus Lumen**
(48 testi brevi) misurando le 6 coppie assegnate, trappole comprese. A fine
serata `embeddings.py` si promuove nel toolkit `aikit/`, e il corpus
embeddato (`working/corpus_embeddings.npz`) è l'input diretto di Modulo 2 ·
Lezione 8 (ricerca semantica) e Modulo 2 · Lezione 9 (vector DB). Niente
notebook, solo script `.py`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `numpy`, `sentence-transformers`; su Linux prima `torch` CPU per evitare ~2 GB di pacchetti CUDA). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di Modulo 2 · Lezioni 1-3**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/scarica_modello.py` | 🧰 | Scarica il modello locale (~88 MB, una tantum): si lancia nel setup, poi il backend `local` è offline. |
| `scaffolding/aikit/` | 🧰 | Il toolkit del corso. Stasera parte vuoto (solo la mappa in `__init__.py`): a fine serata ci si promuove `embeddings.py`. |
| `scaffolding/make_dataset.py` | 🧰 | (Ri)genera il corpus: 48 testi brevi di Lumen S.r.l. (12 FAQ, 12 descrizioni, 12 ticket, 12 recensioni), con le coppie-esercizio progettate e documentate nel docstring. |
| `scaffolding/check_lab07.py` | 🧰 | Strumento del **docente**: verifica `[OK]/[FAIL]` sugli esiti (regressione in preparazione, diagnosi in aula); `--live` fa 3 embedding veri, `--solutions` verifica il riferimento. |
| `dataset/corpus_lumen.jsonl` | 📄 | Il corpus: una riga = `{"id", "tipo", "testo"}`. Testi **corti apposta** (il chunking arriva a Modulo 2 · Lezione 10) e già puliti (il lavoro sporco l'avete fatto a Modulo 2 · Lezione 6). |
| `working/embeddings.py` | 🎤 | **Live coding** (TODO 1-3): `cosine_similarity` a mano, i backend `embed_openai`/`embed_local`, `embed()` col dispatch sui backend. Si scrive col docente; riferimento in `solutions/`. |
| `working/esplora_corpus.py` | ⌨️ | **Esercizio** (TODO 4-5): il ponte id → riga e la similarità delle 6 coppie assegnate. `carica_corpus()` e `salva()` sono già scritte: il giro completo lascia in `working/` il corpus vettorizzato (`corpus_embeddings.npz` + `corpus_meta.json`). |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu   # solo Linux
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di Modulo 2 · Lezioni 1-3
python scaffolding/scarica_modello.py   # modello locale (~88 MB), una tantum
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e senza gli output in `working/`
> (`corpus_embeddings.npz`, `corpus_meta.json`): git non li versiona, quindi
> non possono finire nel materiale distribuito — se li vedete sul vostro
> disco sono i residui delle vostre prove. Il download del modello locale si
> fa in aula durante il setup, non serve prepararlo da casa.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/embeddings.py                  # demo: 3 frasi, similarità a confronto
python working/esplora_corpus.py              # esercizio: corpus + coppie + npz in working/
python scaffolding/check_lab07.py             # docente: verifica working/ (istantanea, zero costi)
python scaffolding/check_lab07.py --solutions # docente: regressione sul riferimento
python scaffolding/check_lab07.py --live      # docente: 3 embedding veri (~$0.000002)
```

Il backend dell'esercizio si cambia con la variabile `BACKEND` in cima al
main di `esplora_corpus.py` (`"openai"` / `"local"`).

## Le idee da trasmettere

Vivono, coi numeri misurati e la tabella-reveal delle 6 coppie, nel materiale
di conduzione del docente (`conduzione-docente.md` nella cartella della
lezione, fuori da `scripts/`): qui non stanno perché questa guida arriva agli
studenti — e il reveal si fa in aula.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 40')**: spazio semantico, dimensionalità, cosine, modelli e
   costi. Nel frattempo, il setup (venv + modello locale).
2. **Live coding (🎤, 40')**: `working/embeddings.py` col docente, TODO 1-3;
   in coda la demo con le due frasi gemelle e il tema diverso.
3. **Esercizio (⌨️, 30')**: `working/esplora_corpus.py` da soli, TODO 4-5;
   fatto quando la tabella è stampata e i due file sono in `working/`.
4. **Wrap-up (📊, 10')**: reveal delle coppie sui due backend, promozione di
   `embeddings.py` in `aikit/`, ponte a Modulo 2 · Lezione 8. Non cancellate
   `corpus_embeddings.npz`.
