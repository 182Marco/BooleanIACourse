# Modulo 3 · Lezione 4 — Advanced Retrieval I: Hybrid Search · guida agli script

Lezione infrasettimanale (📊 teoria + 🎤 codice spiegato + ⌨️ esercizio, 2h): il
`rag.py` del modulo cerca solo per **significato** (embedding + coseno);
stasera si aggiunge la ricerca per **parole** (BM25, libreria `rank-bm25`)
sugli stessi 82 chunk della collection `lumen_m3`, e si fondono i due
ranking con **RRF** (Reciprocal Rank Fusion). Tutto in **un solo file**,
`working/hybrid.py`: le due funzioni dell'indice BM25 (1-2) arrivano
**già scritte** nel file degli studenti e il docente le spiega (leggendole
o live-codandole: la scelta è di chi eroga, il materiale è lo stesso), gli
studenti seguono senza ricopiare; la fusione (TODO 3-4) la scrivono da soli.

Stasera nasce anche il **query set fisso** del modulo: tredici domande
(`QUERY_SET` in cima al file) che il main passa nelle tre modalità
(semantico / bm25 / hybrid). Da qui a Modulo 3 · Lezione 6 si giudica sempre
su queste. La chiave di lettura (chunk atteso, esiti) **non è in questa
cartella**: sta in `query-set.md`, nella cartella della lezione (docente).

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 live coding del docente ·
⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le dipendenze di Modulo 3 · Lezione 2 più `rank-bm25`. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la stessa chiave del Modulo 2. |
| `CONSEGNA.md` | ⌨️ | La spiegazione delle due funzioni già scritte, la consegna dei TODO 3-4 e il criterio di "fatto". |
| `scaffolding/aikit/` | 🧰 | Il toolkit: i sette moduli del Modulo 2 + `rag.py` (identico a quello finito a Modulo 3 · Lezione 3: `indicizza()` · `recupera()` · `genera()` · `rispondi()`). Stasera `hybrid.py` usa `rag.recupera()` (il semantico) e `vectorstore.apri_collection()` (per leggere i chunk su cui costruire l'indice). `chat.py` resta fuori: si lavora single-turn. |
| `scaffolding/make_dataset.py` | 🧰 | Il generatore del corpus (Modulo 3 · Lezione 2). Il corpus è già generato e non cambia: serve al check per verificare che lo scaffolding sia intatto. |
| `scaffolding/check_lab04.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura + le quattro funzioni su un mini-corpus finto e liste costruite a mano); `--solutions` per la versione completa; `--live` embedda le query del set con la chiave vera e verifica le due tesi della serata. Nel percorso studente entra in un solo punto (CONSEGNA, «Quando è fatto»): i due errori invisibili a occhio in `rrf()` e `cerca_hybrid()`. |
| `working/hybrid.py` | 🎤⌨️ | **L'unico file della serata**: `CONFIG`, `DOMANDA_DEMO`, `QUERY_SET`, `tokenizza()` dato, le funzioni 1-2 dell'indice BM25 **già scritte** (codice spiegato), TODO 3-4 (esercizio), gli helper di stampa, il main e la tabella da compilare in fondo. |
| `solutions/hybrid.py` | 🧰 | La versione completa di `working/hybrid.py`, stesso nome file: differisce solo nei TODO 3-4. Se il docente live-coda le funzioni 1-2 invece di leggerle, è il riferimento da replicare. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen, identici a Modulo 3 · Lezione 2 (82 chunk). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI del Modulo 2
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). La collection
> `lumen_m3` NON viaggia con la cartella: al primo avvio `hybrid.py` la
> ricostruisce da solo (82 chunk, ~2 minuti, meno di un centesimo).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/hybrid.py         # il file della serata: demo del codice spiegato, poi il query set nelle tre modalità

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab04.py                       # struttura + le quattro funzioni: istantaneo, zero costi (lo lanciano anche gli studenti per i due errori invisibili)
python scaffolding/check_lab04.py --solutions           # regressione sulla versione completa
python scaffolding/check_lab04.py --solutions --live    # chiamate vere: le tesi della serata sul query set
```

Numeri di riferimento: l'indice BM25 copre 82 chunk e 1.394 termini
distinti e si costruisce in una frazione di secondo, senza chiamate; un
giro completo del main (demo + 13 query nelle tre modalità) embedda 14
domande, frazioni di centesimo. Il token `1152` sta in un solo chunk (idf
4.00), `piano` in 29 (idf 0.60).

> **Prima dell'aula (docente):** le posizioni in `query-set.md` e nelle
> slide sono definitive (misurate l'08/09/2026 col backend OpenAI). Se il
> corpus o il modello di embedding cambiano, si rimisura: `python
> scaffolding/check_lab04.py --solutions --live` (deve dare tutto `[OK]`)
> e, dalla cartella della lezione, `scripts/.venv/bin/python
> misura_query_set.py` (la nota in `query-set.md` dice quali slide
> dipendono da quali numeri). Lancia una volta `python
> solutions/hybrid.py` per vedere l'output completo che gli studenti
> avranno a schermo.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 45')**: dove il semantico sbaglia (esempi misurati dal
   corpus), la mappa dei pezzi (due ranking, una fusione), TF-IDF con la
   formula e BM25 come TF-IDF con saturazione e lunghezza, sui numeri del
   nostro indice, il problema della fusione di score non confrontabili, RRF con il disegno
   e i numeri, quando l'hybrid vince e quando è peso morto, il query set.
2. **Codice spiegato (🎤, 12')**: le funzioni 1-2 sono già in
   `working/hybrid.py`; il docente le spiega riga per riga (leggendole dal
   file o, se preferisce, riscrivendole a schermo) e gli studenti seguono
   sul proprio file senza ricopiare. Si lancia e si vede la demo
   (`DOMANDA_DEMO`) fianco a fianco: BM25 mette primo il ticket citato per
   codice, il semantico lo tiene decimo.
3. **Esercizio (⌨️, 45')**: TODO 3-4 da soli, consegna in `CONSEGNA.md`; il main passa il query set nelle tre modalità
   e si compila la tabella in fondo al file. Fatto quando sulle query con
   codice l'hybrid non è mai dietro al semantico e sulle concettuali il
   chunk giusto resta in top-3.
4. **Reveal e wrap-up (📊, 18')**: la tabella del docente a confronto con
   quelle degli studenti, con due o tre domande a una riga sul codice
   scritto; il costo dell'indice in più; il ponte alla prossima lezione
   (Modulo 3 · Lezione 5: in top-3 ma non primo → il re-ranking).

## Diagnosi rapida in aula (docente)

- Studente bloccato → `python scaffolding/check_lab04.py` dice quale TODO
  non è cablato e perché.
- Lo stesso id due volte nella colonna hybrid → `rrf()` ricostruisce i
  chunk con due cicli annidati e un `break` che chiude solo quello interno.
  Il main non si ferma: si vede solo leggendo l'output.
- `KeyError: 'bm25'` in `cerca_bm25()` → `costruisci_indice_bm25()` non
  riempie `INDICE` (ritorna qualcosa ma non assegna `INDICE["bm25"]` e
  `INDICE["chunks"]`).
- BM25 dà score tutti a zero → la query non è passata da `tokenizza()`
  (`get_scores` vuole la lista di token, non la stringa).
- L'hybrid è uguale al BM25 (o al semantico) → in `rrf()` si stanno usando
  gli score originali invece della posizione, oppure `cerca_hybrid()` passa
  a `rrf()` una lista sola.
- Il chunk giusto è primo nel semantico ma secondo o terzo nell'hybrid
  (il contributo, il codice sconto, metà corsa), oppure secondo in tutte e
  tre (SRV-02) → è RRF che funziona: i chunk presenti in entrambe le liste
  sommano due contributi. Non è un bug: è il costo dell'hybrid e il ponte
  alla prossima lezione (quali query lo fanno: `query-set.md`, fuori da
  questa cartella).
- Sulle concettuali il chunk giusto esce dalla top-3 → controllare
  `CONFIG["candidati"]` (a 3 le liste sono troppo corte) e che
  `cerca_hybrid()` chieda `candidati` chunk a entrambe le ricerche, non `k`.
