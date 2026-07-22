# L20 — Semantic Search · guida agli script

Infrasettimanale (🎤 + ⌨️ + 📊, 2h): il corpus vettorizzato di L19 si
**interroga**. Col docente si riapre il corpus (`carica_corpus`, live
coding); poi gli studenti scrivono DA SOLI le due funzioni di ricerca —
`search(query, k)` e `search_mmr(query, k, lambda_)` — e le provano sulle
tre query del main variando K e LAMBDA (esercizio 1). Chiude il "query
round": il docente dà una query ostica alla volta e ognuno cerca col
proprio software i valori migliori, poi si discute (esercizio 2 — nessun
file nuovo; le query stanno in un file del docente fuori da `scripts/`).
Niente notebook, solo script `.py`.

Il `check_lab20.py` è **strumento del docente**, fuori dal percorso studente
(il "fatto quando" degli esercizi è l'output osservabile): serve per la
preparazione/regressione dei materiali e per la diagnosi rapida di uno
studente bloccato. Verifica i risultati su vettori a tavolino (istantaneo,
zero costi, zero rete, `embed` rimpiazzata da una finta); il giro reale via
API sta dietro `--live`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `numpy`; `sentence-transformers` è **commentato** — si scommenta solo se il corpus di L19 è col backend `local`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L19**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/aikit/embeddings.py` | 🧰 | Il modulo costruito a L19, da stasera nel toolkit `aikit/`: `embed()` con backend selezionabile e `cosine_similarity()` (senza la cache su disco di L19: qui non serve). **Non si tocca**: si importa. |
| `dataset/corpus_lumen.jsonl` | 📄 | I 48 testi brevi di Lumen S.r.l. (FAQ, prodotti, ticket, recensioni): servono per mostrare COSA si è trovato, non solo gli id. |
| `dataset/corpus_embeddings.npz` + `corpus_meta.json` | 📄 | Il corpus vettorizzato: **copia di riserva** identica a quella di L19 — chi ha i propri file di martedì li copia qui sopra. |
| `working/search.py` | 🎤⌨️ | L'unico file della serata. **TODO 1 col docente** (`carica_corpus`: npz + meta + testi nello stesso ordine); **TODO 2-3 da soli** (`search(query, k)` e `search_mmr(query, k, lambda_)` — prescritti solo nomi, variabili del main e scopo: il come è degli studenti). Nel main: 3 query pronte + `K` + `LAMBDA` da variare. Riferimento in `solutions/`. |
| `scaffolding/check_lab20.py` | 🧰 | **Strumento del docente** (preparazione, regressione, diagnosi di uno studente bloccato): `[OK]/[FAIL]` sui risultati, istantaneo, zero costi, zero rete; `--live` fa 2 query vere (~$0.000001); `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `scaffolding/benchmark_scala.py` | 🧰 | Il brute-force misurato a scala su vettori sintetici (48 → 200k, proiezione a 10M): i numeri del "non scala" citati in slide. |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L19
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e cache (git non li versiona). Chi ha il proprio
> corpus di L19 lo copia in `dataset/` sopra la riserva; per tutti gli altri
> la riserva funziona identica. `sentence-transformers` serve solo ai corpus
> `local` (su Linux: prima torch CPU, vedi `requirements.txt`).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/search.py                      # le prove sulle 3 query del main
python scaffolding/check_lab20.py             # verifica working/: istantanea, zero costi
python scaffolding/check_lab20.py --live      # 2 query vere via OpenAI (~$0.000001)
python scaffolding/check_lab20.py --solutions # per il docente: verifica solutions/
python scaffolding/benchmark_scala.py         # il "non scala", misurato
```

## Le idee da trasmettere (coi numeri misurati, luglio 2026)

1. **La ricerca è L19 ripetuta n volte.** `search()` non ha magia: embed
   della query, poi un ciclo — `[cosine_similarity(q, v) for v in vectors]` —
   la STESSA funzione di L19, una volta per testo. Sui 48 testi: **0.75 ms**.
2. **La query si embedda con lo STESSO backend del corpus.** Il
   `corpus_meta.json` è il certificato di origine: 1536 dim (openai) contro
   384 (local) sono **spazi diversi** — confrontarli è nonsense. Per questo
   `search()` legge il backend dal corpus e embedda la query con QUELLO:
   coerenza garantita per costruzione. Costo di una query: ~10 token →
   **$0.0000002** (rilanciare ri-paga, ma parliamo di decimillesimi di
   centesimo).
3. **Gli score si leggono a fasce, non in assoluto.** Query facile
   (`spedizione`) **0.756** staccata; query semantica (parole diverse)
   **0.607**; query vaga: top-3 appiattito (0.595 / 0.573 / 0.573); fuori
   dominio (carbonara) **0.196**. La SOGLIA che separa (qui **0.30**) non
   viene da un tutorial: si legge dalle fasce, e con un altro modello va
   ritarata (gli score non sono calibrati, L19 docet).
4. **La trappola di L19, vista dal lato ricerca.** "una scrivania affidabile
   che **non si guasta mai**" ritorna **rec-04 — la recensione col motore
   rotto — a 0.538**: l'embedding vede il TEMA guasti, non la negazione.
   Chi costruisce un RAG deve saperlo *prima* di collegarci un LLM.
5. **Top-k monotono → MMR.** Su "problemi con il motore" il top-5 è tutto
   guasti/rumori quasi uguali; con `lambda_=0.5` i quasi-doppioni (tic-09,
   rec-04) perdono il posto ed entrano una FAQ e un prodotto. λ è una
   manopola: a 1.0 MMR **è** il top-k.
6. **Il brute-force non scala — misurato.** Il tempo di una query cresce
   dritto con n: 0.1 ms su 48 vettori, 8.9 ms su 5k, **195.8 ms su 50k**,
   **830.7 ms su 200k** (1536 dim, float32, in forma vettoriale — quella del
   benchmark) → proiezione **~41.5 s su 10 milioni**, e OGNI query rifà
   tutto il lavoro da capo. È il motivo per cui esiste l'indice ANN: sabato
   (L21). In slide si parla di **tempo impiegato**, mai di "costi" (sembra
   denaro), e il benchmark non si nomina: i numeri e la provenienza vivono
   qui.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 40')**: dalla similarità di coppie alla ricerca, top-k e i
   suoi difetti, MMR, threshold, debug del retrieval, il tempo a scala.
2. **Live coding (🎤, 15')**: `carica_corpus` col docente (TODO 1); fatto
   quando la prova a schermo del docente e quella replicata coincidono.
3. **Esercizio 1 (⌨️, 35')**: `search` e `search_mmr` da soli (TODO 2-3),
   poi le tre query del main variando `K` e `LAMBDA`; fatto quando (tutto
   osservabile) la FAQ giusta esce prima e staccata, MMR cambia faccia ai
   doppioni e con λ=1.0 le due liste coincidono.
4. **Esercizio 2 (⌨️+📊, 25')**: il query round — il docente dà una query
   alla volta (file del docente, fuori da `scripts/`), si prova col proprio
   `search.py`, si discute fascia e manopole.
5. **Wrap-up (📊, 5')**: le fasce della serata e la soglia; sabato la stessa
   ricerca la fa un vector DB, indicizzata. Non cancellate il corpus in
   `dataset/`.
