# L17 — Text Cleaning & Pre-processing · guida agli script

Lezione di **live coding** (🎤): il docente costruisce dal vivo `aikit/clean.py` e
mostra il **before/after** su tre documenti *reali* e sporchi, poi verifica col
**chatbot** (`ask()`) che la risposta migliora sul testo pulito. Niente notebook,
solo script `.py`. Il cleaning gira **senza chiave**; solo `ask.py` chiama il modello.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (loader di L16 + `openai`/`dotenv` per il banco di prova). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` (serve solo a `ask.py`). |
| `download_samples.py` | 🧰 | (Ri)scarica i 3 documenti reali in `sample_docs/`. |
| `aikit/__init__.py` | 🧰 | Espone `load`, `Document`, `clean`. Il toolkit che cresce lezione dopo lezione. |
| `aikit/loaders/` | 🧰 | I loader di **L16** (riuso) + `txt.py`. Non si riscrivono oggi. |
| `aikit/clean.py` | 🎤 | **Il cuore della lezione.** Gli step di cleaning (`str→str`) + il runner `clean()` + **le `PIPELINES` per tipo di file** (`.txt`/`.pdf`/`.html`). Per un documento nuovo si tocca solo qui. |
| `ask.py` | 🎤 | **L'unico runner.** Senza argomenti: before/after (offline). Con una domanda: confronta la risposta del **chatbot** (L15/L16) su testo **sporco vs pulito**. |
| `llm_client.py` · `pricing.py` | 🧰 | Client LLM + costi, **riuso da L15/L16**. Dipendenze di `ask.py`, non si riscrivono. |
| `esercizio/mia_pulizia.py` | ⌨️ | **Stub studenti**: implementare `remove_urls` e agganciarla alla pipeline. |
| `esercizio/soluzione.py` | 🎤 | Soluzione di riferimento (docente). |
| `esercizio/check.py` | ⌨️ | Verifica `[OK]/[FAIL]` per requisito, **senza chiave API**. |
| `sample_docs/frankenstein.txt` | 📄 | Gutenberg #84 — boilerplate + righe a ~70 char. |
| `sample_docs/arxiv_1905.00075.pdf` | 📄 | arXiv — hyphenation + header ricorrenti + n° pagina. |
| `sample_docs/wikipedia_nlp.html` | 📄 | Wikipedia — sezioni di coda + note + whitespace. |

## Setup

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python download_samples.py     # opzionale: i sample sono già in sample_docs/
```

## Come si prova

```bash
python ask.py                                 # before/after sui 3 doc (offline)
python ask.py sample_docs/frankenstein.txt    # un doc, con estratto prima/dopo (offline)
python ask.py sample_docs/wikipedia_nlp.html "che cos'è l'NLP?"   # chatbot: sporco vs pulito (serve la chiave)
```

Per un **documento nuovo**: aggiungi la funzione-step in `aikit/clean.py` e registrala
nella mappa `PIPELINES`. `ask.py` la usa in automatico — nient'altro da toccare.

## L'idea da trasmettere

Una pipeline di cleaning **non è un framework**: è una **lista di funzioni pure
`str → str`** applicate in ordine (`clean(text, steps)`). Documenti diversi =
pipeline diverse (vedi `PIPELINES` in `aikit/clean.py`): un `.txt` di Gutenberg si
riflow-a, un PDF si de-sillaba, una pagina web si de-boilerplat-a. Il criterio per
decidere cosa è rumore: *«se dovessi rispondere io alla domanda, questo testo mi
servirebbe?»*.

Ordine di costruzione consigliato in aula (`clean.py`):

1. `normalize_whitespace`, `normalize_unicode`, `strip_control_chars` — le basi.
2. `reflow_paragraphs` → **Frankenstein** (7742 → ~1600 righe).
3. `dehyphenate`, `remove_repeated_lines`, `remove_page_numbers` → **PDF arXiv**.
4. `remove_citation_markers`, `drop_sections` → **Wikipedia**.

## Caso-limite reale (usalo, non nasconderlo)

Sul PDF, `remove_repeated_lines(3)` toglie 6 delle 7 occorrenze dell'header
"Published as a conference paper at ICLR 2019", ma **ne resta una**: su pagina 1
il numero di pagina è incollato all'header (`"1 Published as a conference…"`),
riga *unica* che sfugge al conteggio. Messaggio: il **cleaning è euristico**, non
esiste la pipeline perfetta.
