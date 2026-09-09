# Modulo 3 · Lezione 5 — Advanced Retrieval II: Re-ranking · guida agli script

Lezione infrasettimanale (📊 teoria + 🎤 codice spiegato + ⌨️ esercizio, 2h):
`hybrid.cerca_hybrid()` (Modulo 3 · Lezione 4, da stasera in `aikit/`) porta
il chunk giusto in top-3 su tutte le query con un codice, ma non sempre al
primo posto, e su tre domande concettuali lo fa scendere. Stasera si
aggiunge un **secondo stadio**: la top-10 dell'hybrid viene **riordinata**
da un modello che legge domanda e chunk insieme. Due backend dietro la
stessa firma: **Cohere Rerank** (un cross-encoder servito via API, chiave
Trial gratuita creata in aula) e **l'LLM come reranker** (`gpt-4o-mini`
con lo structured output di Modulo 2 · Lezione 13). Tutto in **un solo
file**, `working/rerank.py`: `rerank_cohere()` arriva **già scritta** e il
docente la spiega (leggendola o live-codandola: la scelta è di chi eroga),
`rerank_llm()` e `cerca_due_stadi()` (TODO 2-3) le scrivono gli studenti.

Il query set è lo stesso della lezione scorsa: tredici domande, stasera
con una colonna per backend e i secondi di ogni chiamata. La chiave di
lettura (chunk atteso, esiti, tempi) **non è in questa cartella**: sta in
`query-set-rerank.md`, nella cartella della lezione (docente).

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 live coding del docente ·
⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le dipendenze di Modulo 3 · Lezione 4 più `cohere`. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2) e `COHERE_API_KEY` (facoltativa, creata in aula da chi vuole). |
| `CONSEGNA.md` | ⌨️ | La spiegazione della funzione già scritta, la consegna dei TODO 2-3 e il criterio di "fatto". |
| `scaffolding/aikit/` | 🧰 | Il toolkit: i sette moduli del Modulo 2 + `rag.py` (identico a Modulo 3 · Lezione 3-4) + **`hybrid.py`**, la soluzione di Modulo 3 · Lezione 4 promossa stasera (cambiano la riga `SCRIPTS` e le intestazioni delle funzioni 3-4, non più «TODO», come fu per `rag.py`). Stasera `rerank.py` usa `hybrid.costruisci_indice_bm25()` e `hybrid.cerca_hybrid()` (il primo stadio), `rag.CONFIG` e `vectorstore.apri_collection()` (per la collection). `chat.py` resta fuori: single-turn. |
| `scaffolding/make_dataset.py` | 🧰 | Il generatore del corpus (Modulo 3 · Lezione 2). Il corpus è già generato e non cambia: serve al check per verificare che lo scaffolding sia intatto. |
| `scaffolding/check_lab05.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura + le tre funzioni con i client finti); `--solutions` per la versione completa; `--live` con le due chiavi vere verifica le tre query che il rerank porta in testa e la query RMA che Cohere non deve rompere. Non compare nel percorso studente. |
| `working/rerank.py` | 🎤⌨️ | **L'unico file della serata**: `CONFIG`, `DOMANDA_DEMO`, `QUERY_SET`, la funzione 1 `rerank_cohere()` **già scritta** (codice spiegato), il modello Pydantic `Ordine` dato, TODO 2-3 (esercizio), gli helper di stampa, il main con la pausa per il free tier e la tabella da compilare in fondo (colonna del chunk giusto già scritta). |
| `solutions/rerank.py` | 🧰 | La versione completa di `working/rerank.py`, stesso nome file: differisce solo nei TODO 2-3. Se il docente live-coda la funzione 1 invece di leggerla, è il riferimento da replicare. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen, identici a Modulo 3 · Lezione 2 (82 chunk). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la chiave OpenAI del Modulo 2 e la chiave Cohere creata stasera
```

**La chiave Cohere è facoltativa per gli studenti** (in aula, 8 minuti,
slide dedicata) e serve invece al **docente**, per la demo del codice
spiegato: `dashboard.cohere.com`
→ account gratuito → *API keys* → chiave **Trial**. Limiti misurati il
09/09/2026: **10 chiamate al minuto** (la undicesima risponde 429) e
**1.000 al mese**. Un giro del query set sono 14 chiamate: il main aspetta
sei secondi tra una domanda e l'altra. Non c'è una chiave di riserva e non
va promessa: chi non fa la chiave lavora col solo backend LLM, e con
`COHERE_API_KEY` vuota il main salta la colonna cohere («senza
COHERE_API_KEY in .env: si salta») e non aspetta tra le domande.

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). La collection
> `lumen_m3` NON viaggia con la cartella: al primo avvio `rerank.py` la
> ricostruisce da solo (82 chunk, ~2 minuti, meno di un centesimo).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/rerank.py         # il file della serata: demo del codice spiegato, poi il query set con e senza rerank (~2 minuti per la pausa Cohere)

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab05.py                       # struttura + le tre funzioni con i client finti: istantaneo, zero costi
python scaffolding/check_lab05.py --solutions           # regressione sulla versione completa
python scaffolding/check_lab05.py --solutions --live    # chiamate vere (~40 s per la pausa Cohere): le tesi della serata
```

Numeri di riferimento (misurati il 09/09/2026, `misura_rerank.py` nella
cartella della lezione): un giro del main fa 14 chiamate Cohere (1 search
unit ciascuna, fino a 100 documenti per unità) e 13 chiamate `gpt-4o-mini`
da circa 1.000-1.300 token in ingresso e 11-25 in uscita l'una (frazioni
di centesimo in tutto). Cohere risponde in circa un secondo (da 0.3 a 3), l'LLM
in circa due (da 0.9 a 3.6): i tempi variano con l'ora.

> **Prima dell'aula (docente):** le posizioni in `query-set-rerank.md` e
> nelle slide sono misurate il 09/09/2026. Se il corpus, il modello di
> embedding o i modelli di rerank cambiano, si rimisura: `python
> scaffolding/check_lab05.py --solutions --live` (tutto `[OK]`) e, dalla
> cartella della lezione, `scripts/.venv/bin/python misura_rerank.py`. Il
> reranker LLM **oscilla** da un giro all'altro (la query RMA cambia posto
> quasi sempre, altre di rado): le slide lo dicono come comportamento, non
> come numero fisso. Lancia una volta `python solutions/rerank.py` per
> vedere l'output completo che gli studenti avranno a schermo.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Apertura (📊, 5')**: la tabella della lezione scorsa con le quattro
   righe dove l'hybrid non è primo; agenda.
2. **Registrazione Cohere (🖥️ facoltativa, 8')**: dashboard, chiave
   Trial, `.env`. La fa chi vuole provare quel backend; chi non la fa
   apre intanto il file. Nessuna chiave di riserva da promettere.
3. **Teoria (📊, 32')**: bi-encoder vs cross-encoder col disegno, i due
   stadi e quanto largo il primo, Cohere vs LLM come reranker (costo,
   latenza, privacy), il cross-encoder locale in una riga, dove il rerank
   non ripaga, la mappa dei pezzi.
4. **Codice spiegato (🎤, 12')**: `rerank_cohere()` è già in
   `working/rerank.py`; il docente la spiega, gli studenti seguono. Si
   lancia e si vede la demo su «Cosa copre SRV-02?»: il listino da secondo
   a primo.
5. **Esercizio (⌨️, 45')**: TODO 2-3 da soli, consegna in `CONSEGNA.md`;
   il main passa il query set nelle tre modalità e si compila la tabella.
6. **Reveal e wrap-up (📊, 18')**: la tabella del docente, il caso RMA
   con l'LLM, tempi e costi, dove il rerank non ripaga, il ponte al lab
   (Modulo 3 · Lezione 6) e a Modulo 3 · Lezione 10.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → `python scaffolding/check_lab05.py` dice quale TODO
  non è cablato e perché.
- `UnauthorizedError` o `401` da Cohere → `COHERE_API_KEY` copiata male in
  `.env`. Se manca del tutto il main la salta da solo («senza
  COHERE_API_KEY in .env: si salta») e si lavora col solo LLM.
- `TooManyRequestsError` / `429` da Cohere → più di dieci chiamate in un
  minuto: la pausa in `CONFIG["pausa"]` è stata tolta o abbassata, oppure
  lo studente ha rilanciato il main due volte di fila. Si aspetta un
  minuto.
- Lo stesso id due volte nella colonna llm, o una colonna più corta →
  `rerank_llm()` prende gli indici del modello così come arrivano: vanno
  tolti i doppi e aggiunti in coda i mancanti.
- `ValidationError` o il modello risponde con testo → `text_format=Ordine`
  non è passato a `responses.parse()`, oppure si sta usando
  `responses.create()`.
- La colonna llm ha lo stesso ordine dell'hybrid su tutte le query → il
  prompt non contiene i testi dei chunk (solo gli indici), o gli indici
  della risposta non vengono usati per riordinare.
- La colonna cohere è identica alla colonna hybrid → `cerca_due_stadi()`
  ritorna i candidati senza passare dal reranker, o `rerank_cohere()` non
  usa `r.index` per rimappare i chunk.
- RMA primo nell'hybrid e quarto-settimo con l'LLM, o l'estero che cambia
  posto → non è un bug: il reranker generico oscilla. È il caso del reveal
  (`query-set-rerank.md`, fuori da questa cartella).
- «La scrivania non sta ferma» fuori in tutte e tre → giusto così: è 17ª
  nel semantico, con dieci candidati non arriva al secondo stadio. Con
  `k_largo` 30 entra e Cohere la porta nona: il rerank riordina solo ciò
  che riceve.
