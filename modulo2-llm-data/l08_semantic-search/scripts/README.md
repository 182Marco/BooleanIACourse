# Modulo 2 · Lezione 8 — Semantic Search · guida agli script

> Cerchi le istruzioni della serata? Parti da **`CONSEGNA.md`**: questa
> guida descrive ogni file della cartella, comprese le parti che servono
> solo a chi prepara la lezione.

Infrasettimanale (🎤 + ⌨️ + 📊, 2h): il corpus vettorizzato di Modulo 2 · Lezione 7 si
**interroga**. Col docente si legge `carica_corpus()` (fornita, lettura
guidata); poi gli studenti scrivono DA SOLI le due funzioni di ricerca —
`search(query, k)` e `search_mmr(query, k, lambda_)` — e le provano sulle
tre query del main variando K e LAMBDA (esercizio 1; il main con la stampa
degli score è fornito). Chiude il "query round": il docente dà una query ostica alla volta e ognuno cerca col
proprio software i valori migliori, poi si discute (esercizio 2 — nessun
file nuovo; le query stanno in un file del docente fuori da `scripts/`).
Niente notebook, solo script `.py`.

Il `check_lab08.py` è **strumento del docente**, fuori dal percorso studente
(il "fatto quando" degli esercizi è l'output osservabile): serve per la
preparazione/regressione dei materiali e per la diagnosi rapida di uno
studente bloccato. Verifica i risultati su vettori a tavolino (istantaneo,
zero costi, zero rete, `embed` rimpiazzata da una finta); il giro reale via
API sta dietro `--live`. Lanciarlo non fa danni, ma il criterio di
completamento resta l'output dei vostri script, non il check.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `numpy`; `sentence-transformers` è **commentato** — si scommenta solo se il corpus di Modulo 2 · Lezione 7 è col backend `local`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 7**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/aikit/` | 🧰 | Il toolkit del corso: `embeddings.py` (identico al file promosso a fine Modulo 2 · Lezione 7: `embed()` con backend selezionabile, `cosine_similarity()`) — **non si tocca, si importa**. A fine serata ci si promuove `search.py`. |
| `dataset/corpus_lumen.jsonl` | 📄 | I 48 testi brevi di Lumen S.r.l. (FAQ, prodotti, ticket, recensioni): servono per mostrare COSA si è trovato, non solo gli id. |
| `dataset/corpus_embeddings.npz` + `corpus_meta.json` | 📄 | Il corpus vettorizzato: **copia di riserva** identica a quella di Modulo 2 · Lezione 7 — chi ha i propri file della lezione scorsa li copia qui sopra. |
| `working/search.py` | 🎤⌨️ | L'unico file della serata. `carica_corpus()` **fornita** (si legge col docente); **TODO 1-2 da soli** (`search(query, k)` e poi `search_mmr(query, k, lambda_)` — prescritti solo nomi, variabili del main e scopo: il come è degli studenti). Il main è già scritto: prova le 3 query e stampa i risultati con gli score; `K` e `LAMBDA` da variare. Riferimento in `solutions/`. |
| `scaffolding/check_lab08.py` | 🧰 | **Strumento del docente** (preparazione, regressione, diagnosi di uno studente bloccato): `[OK]/[FAIL]` sui risultati, istantaneo, zero costi, zero rete; `--live` fa 2 query vere (~$0.000001); `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `scaffolding/benchmark_scala.py` | 🧰 | Il brute-force misurato a scala su vettori sintetici (48 → 200k, proiezione a 10M): i numeri del "non scala" citati in slide. |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 7
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e cache (git non li versiona); `solutions/`
> arriva solo a fine lezione, sul branch delle soluzioni della repo
> studenti. Chi ha il proprio
> corpus di Modulo 2 · Lezione 7 lo copia in `dataset/` sopra la riserva; per tutti gli altri
> la riserva funziona identica. `sentence-transformers` serve solo ai corpus
> `local` (su Linux: prima torch CPU, vedi `requirements.txt`).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/search.py                      # le prove sulle 3 query del main
python scaffolding/check_lab08.py             # verifica working/: istantanea, zero costi
python scaffolding/check_lab08.py --live      # 2 query vere via OpenAI (~$0.000001)
python scaffolding/check_lab08.py --solutions # per il docente: verifica solutions/
python scaffolding/benchmark_scala.py         # il "non scala", misurato
```

## Le idee da trasmettere

Vivono, coi numeri misurati, le fasce del reveal e le query del round, nel
materiale di conduzione del docente (`conduzione-docente.md` nella cartella
della lezione, fuori da `scripts/`): qui non stanno perché questa guida
arriva agli studenti — e le query del round non si vedono in anticipo.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 40')**: dalla similarità di coppie alla ricerca, top-k e i
   suoi difetti, MMR, threshold, debug del retrieval, il tempo a scala.
2. **Lettura guidata (🎤, 10')**: `carica_corpus` (fornita) si legge col
   docente; fatto quando la prima riga stampata dice 48 testi, 48 vettori e
   il backend.
3. **Esercizio 1 (⌨️, 40')**: `search` e poi `search_mmr` da soli (TODO 1-2;
   priorità a `search` se il tempo stringe), poi le tre query del main
   variando `K` e `LAMBDA`; fatto quando (tutto osservabile) la FAQ giusta
   esce prima e staccata, MMR cambia faccia ai doppioni e con λ=1.0 le due
   liste coincidono.
4. **Esercizio 2 (⌨️+📊, 25')**: il query round — il docente dà una query
   alla volta (file del docente, fuori da `scripts/`), si prova col proprio
   `search.py`, si discute fascia e manopole.
5. **Wrap-up (📊, 5')**: le fasce della serata e la soglia; promozione di
   `search.py` in `aikit/` (`cp working/search.py
   scaffolding/aikit/search.py`); nella prossima lezione la stessa ricerca
   la fa un vector DB, indicizzata. Non cancellate il corpus in `dataset/`.
