# Modulo 3 · Lezione 6 — Lab RAG: debugging del retrieval · guida agli script

Lab da 4 ore (📊 brief + ⌨️ tre blocchi pratici): le leve del retrieval ci sono
tutte — k, soglia, chunk size, prompt (Modulo 2 · Lezione 12), hybrid
(Modulo 3 · Lezione 4), rerank (Modulo 3 · Lezione 5, da oggi in
`aikit/`) — e oggi si impara a **capire quale serve**, partendo da dove
la pipeline si è rotta. Tre domande in ordine — il chunk giusto esiste
nel corpus? è nel top-k del retrieval? la risposta lo usa? — e sei casi
(A-F) da mettere in griglia, dal più comune (esiste, ma non è nel top-k)
ai rari (il modello inventa dove non c'è niente, o ignora un chunk che
ha nel prompt). Il codice sta tutto in **un file**, `working/debug.py`: le leve
in `CONFIG` e tre TODO, le tre domande in codice: la frase nel corpus
(`trova_nel_corpus()`), le tre domande su una query (`diagnostica()`), il
giro su tutto il set (`giro()`). I tre blocchi pratici sono scrivere lo
strumento (Lab 1), usarlo per trovare i failure (Lab 2), cercare la cura
girando le leve (Lab 3, nessun TODO). I failure si annotano in
`working/griglia.md`, la scheda della giornata.

I failure già trovati sul corpus, le query avversarie di riserva e gli
esiti delle leve **non sono in questa cartella** e non arrivano agli
studenti: stanno in `failure-docente.md`, un livello sopra `scripts/`,
nella cartella della lezione (materiale docente).

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · ⌨️ da completare dagli studenti
· 📄 documenti/dati di esempio. (Oggi non c'è live coding del docente:
tutti e tre i blocchi pratici sono ⌨️.)

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le stesse dipendenze di Modulo 3 · Lezione 5. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (la stessa del Modulo 2) e `COHERE_API_KEY` (facoltativa: serve solo con `CONFIG["backend"] = "cohere"`). |
| `CONSEGNA.md` | ⌨️ | La frase attesa, i TODO 1-3 del Lab 1, la caccia del Lab 2, la tabella caso → leve del Lab 3, i criteri di "fatto". |
| `MAPPA.md` (+ `MAPPA.pdf`) | 📄 | **Dove sta cosa**, per lo studente: l'albero della cartella, i tre file su cui si lavora, i moduli di `aikit/` usati oggi e cosa `debug.py` prende da ognuno, `chroma/` e quando nasce. La prima cosa da aprire. |
| `scaffolding/aikit/` | 🧰 | Il toolkit: i sette moduli del Modulo 2 + `rag.py` + `hybrid.py` (identici a Modulo 3 · Lezione 5) + **`rerank.py`**, la soluzione di Modulo 3 · Lezione 5 promossa oggi (cambiano la riga `SCRIPTS` e le intestazioni delle funzioni 2-3, non più «TODO», come fu per `hybrid.py`). `debug.py` usa `rag.recupera()` / `rag.genera()` / `rag.CONFIG` / `rag.ISTRUZIONI`, `hybrid.cerca_hybrid()` / `hybrid.INDICE`, `rerank.cerca_due_stadi()`, `vectorstore.apri_collection()`. Oggi non si toccano: le leve si girano da `CONFIG` (in `rerank.py` il numero di candidati si chiama ancora `k_largo`, come alla lezione scorsa: è lo stesso numero). |
| `scaffolding/make_dataset.py` | 🧰 | Il generatore del corpus (Modulo 3 · Lezione 2). Il corpus è già generato e non cambia: serve al check per verificare che lo scaffolding sia intatto. |
| `scaffolding/check_lab06.py` | 🧰 | **Strumento del docente**: base istantaneo senza rete (struttura + i tre TODO con retrieval e modello finti); `--solutions` per la versione completa; `--live` con la chiave vera verifica la baseline (TCK-1152 fuori dal top-k, la scrivania fuori dai candidati, il contrassegno rifiutato) e la cura con hybrid. Non compare nel percorso studente. |
| `working/debug.py` | ⌨️ | **Il file di lavoro della giornata**: `CONFIG` con le leve (più `candidati`, quanti chunk guarda la diagnosi), `SOLO` per provare una domanda, `QUERY_SET` con le frasi attese, `LE_MIE_QUERY`, `prepara()`, `cerca()`, TODO 1-3 (`trova_nel_corpus()`, `diagnostica()`, `giro()`), gli helper di stampa, il main. |
| `working/griglia.md` | ⌨️ | **La scheda dei failure**, da compilare a mano: la legenda dei sei casi, una tabella per il Lab 2 (domanda, frase attesa, le tre risposte, il caso), una per il Lab 3 (leva, dopo, regressioni) e la `CONFIG` finale. Non ha una copia in `solutions/`: è personale, e le cure misurate stanno in `failure-docente.md`. |
| `solutions/debug.py` | 🧰 | La versione completa di `working/debug.py`, stesso nome file: differisce solo nei TODO 1-3. |
| `dataset/lumen_m3/` | 📄 | I sei documenti Lumen, identici a Modulo 3 · Lezione 2 (82 chunk a chunk size 500). |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la chiave OpenAI del Modulo 2 (e la Cohere, se c'è)
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e `chroma/` (git non li versiona). La collection
> `lumen_m3` NON viaggia con la cartella: al primo avvio `debug.py` la
> ricostruisce da solo (82 chunk, ~2 minuti, meno di un centesimo). Con
> `CONFIG["chunk_size"]` diverso da 500 ne costruisce un'altra
> (`lumen_m3_<size>`), stesso costo.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/debug.py          # il file della giornata: il giro sul set (13 domande, ~1 minuto), o la domanda in SOLO

# solo docente, non fa parte del percorso studente
python scaffolding/check_lab06.py                       # struttura + i tre TODO con retrieval e modello finti: istantaneo, zero costi
python scaffolding/check_lab06.py --solutions           # regressione sulla versione completa
python scaffolding/check_lab06.py --solutions --live    # chiamate vere (~20 s): la baseline e la cura con hybrid
```

Un giro del set sono 13 chiamate a `gpt-4o-mini` (frazioni di centesimo)
più, con `retrieval = "rerank"`, 13 chiamate al reranker: con `"llm"`
altre 13 al modello, con `"cohere"` 13 chiamate Cohere e 6 secondi di
pausa tra una domanda e l'altra (il free tier fa 10 chiamate al minuto:
il giro dura circa un minuto e mezzo).

> **Se vuoi mostrare la prima indicizzazione (docente):** sulla tua copia
> `chroma/` esiste già, quindi il primo avvio parte subito e non si vede
> la collection nascere. Per farla vedere dal vivo, cancella `chroma/`
> prima della lezione: si ricostruisce in un paio di minuti.

> **Prima dell'aula (docente):** i numeri in `failure-docente.md` e nelle
> slide sono misurati il 10/09/2026 con `misura_failure.py` (cartella della
> lezione). La generazione non è deterministica: le risposte giuste sono
> date come «in N giri su M». Se il corpus, il modello di embedding o
> `gpt-4o-mini` cambiano, si rimisura: `python scaffolding/check_lab06.py
> --solutions --live` (tutto `[OK]`) e, dalla cartella della lezione,
> `scripts/.venv/bin/python misura_failure.py leve --ripeti 3`.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Brief (📊, 25')**: il caso comune (il chunk giusto non è nel top-k);
   tre domande in ordine; la frase attesa; quanto è lontano; i sei casi e
   le leve per caso; la regola anti-regressione; il file; agenda.
2. **Lab 1 — il banco di prova (⌨️, 70')**: i tre TODO in
   `working/debug.py`, provati con `SOLO`; si chiude quando il giro
   stampa la tabella (10/13 sulla baseline).
3. **Pausa (☕, 15')**.
4. **Lab 2 — caccia ai failure (⌨️, 55')**: le tre risposte sbagliate
   della baseline, poi le query proprie in `LE_MIE_QUERY` scambiate col
   vicino; ogni failure in `working/griglia.md` con la lettera del caso.
   Rientro sulle slide con i casi trovati.
5. **Lab 3 — cura mirata (⌨️, 75')**: nessun TODO, si gira una leva in
   `CONFIG`, si rilancia il giro, si annotano «dopo» e regressioni.
   Rientro finale: le leve misurate, i casi che non si curano, il
   confronto delle griglie.

## Diagnosi rapida in aula (docente; gli studenti possono leggerla)

- Studente bloccato → `python scaffolding/check_lab06.py` dice quale TODO
  non è cablato e perché.
- `KeyError: 'chunks'` in `trova_nel_corpus()` → `hybrid.INDICE` è vuoto:
  la funzione è stata chiamata prima di `prepara()` (che costruisce
  l'indice), per esempio in cima al file invece che nel main. Succede a
  chi la usa a mano per cercare la frase attesa di una domanda propria.
- «la frase … non c'è» su una query propria → la frase attesa non è
  scritta come nel documento (accenti, trattini lunghi, spazi): si copia
  dal file in `dataset/lumen_m3/`, o si sceglie un pezzo più corto.
- Posizione `None` su tutte le query → in `diagnostica()` il confronto è
  sul testo del candidato invece che sul suo `id`, o con la frase invece
  che con gli id di `trova_nel_corpus()`.
- `nel top-k: sì` con posizione 7 → il confronto con `CONFIG["k"]` è
  sbagliato (o manca): nel prompt entrano solo i primi k candidati. Se la
  posizione parte da 0, il primo chunk risulta 0° e tutto slitta.
- «la usa? no» con la risposta giusta a occhio → il modello ha citato
  con una forma diversa da `[id]` (senza parentesi quadre, o solo il nome
  del file): si legge la risposta, si annota a mano. È il limite del
  criterio automatico, e si dice.
- Il giro dà 9/13 o 11/13 invece di 10/13 sulla baseline → la generazione
  oscilla (nelle nostre misure la baseline ha dato 10/13 in tutti i giri,
  ma con hybrid o chunk 300 «metà corsa» cambia in un giro su tre). Non è
  un bug: si rilancia e si annota «in N giri su M».
- Una query resta «Non lo trovo» anche con la leva giusta per il suo
  caso → non è per forza un bug dello studente: gli esiti misurati di
  ogni leva, query per query, sono in `failure-docente.md` (docente).
- `TooManyRequestsError` / `429` da Cohere → più di dieci chiamate in un
  minuto: la pausa in `cerca()` è stata tolta, o il giro è stato
  rilanciato due volte di fila. Si aspetta un minuto.
- Il giro con `"rerank"` e `"llm"` dà posizioni diverse da un lancio
  all'altro → il reranker LLM oscilla (Modulo 3 · Lezione 5): si annota
  come comportamento, non come regressione.
- `chunk_size` cambiato e il giro dura due minuti in più → sta indicizzando
  la collection `lumen_m3_<size>`: è normale, la seconda volta parte subito.
  Le frasi attese valgono ancora; gli id dei chunk no.
