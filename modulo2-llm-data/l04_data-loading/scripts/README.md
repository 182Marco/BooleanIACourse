# L16 — Data Loading · materiale docente

Lezione di **live coding** (🎤): il docente costruisce dal vivo il modulo
`loaders/` e il banco di prova `ask()`. Niente notebook, solo script `.py`. Questo
è il **codice di riferimento** (completo e testato) che il docente replica a
schermo; gli studenti scrivono un solo pezzo nell'esercizio (`.txt`/`.csv`).

## Struttura

```
scripts/
├── README.md            # questa guida (docente)
├── requirements.txt
├── .env.example         # OPENAI_API_KEY (solo per ask())
├── loaders/             # IL CUORE — un file per formato, costruito dal vivo
│   ├── __init__.py          # espone load() + Document
│   ├── base.py              # la dataclass Document (text + metadata)
│   ├── pdf.py               # load_pdf      (pypdf)
│   ├── docx.py              # load_docx     (python-docx)
│   ├── html.py              # load_html     (BeautifulSoup) — toglie il noise
│   ├── markdown.py          # load_markdown (markdown-it-py)
│   └── dispatch.py          # load() — smista per estensione
├── llm_client.py        # = client della L15 (riuso, non si riscrive)
├── pricing.py           # = pricing della L15 (dipendenza di llm_client)
├── ask.py               # ask(doc, domanda) — banco di prova + CLI per le prove
├── make_samples.py      # (ri)genera i binari bilancio.pdf / cv.docx
├── sample_docs/         # documenti di esempio — un CONTENUTO diverso per formato
│   ├── bilancio.pdf         # relazione annuale (generato) — caso "report"
│   ├── cv.docx              # curriculum (generato) — caso "documento Word"
│   ├── ricetta.html         # ricetta CON noise (nav/footer/newsletter/script)
│   ├── readme.md            # README di un tool CLI
│   ├── note.txt             # per l'esercizio (.txt)
│   └── clienti.csv          # per l'esercizio (.csv)
└── esercizio/           # il pezzo che scrivono gli STUDENTI
    ├── txt_csv.py           # stub da completare (load_txt / load_csv)
    └── soluzione_txt_csv.py # soluzione (riferimento docente)
```

> **Perché un package `loaders/` e non file piatti** (la L15 usava file piatti):
> qui i moduli sono 5 e mappano 1:1 sui formati, ed è esattamente come le slide
> presentano la cosa (un `loaders/` con un loader per formato). Spezzare per
> formato rende ovvio dove si aggiunge il prossimo.

## Come fare le prove

Lo strumento è `ask.py`, usato da riga di comando:

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python make_samples.py        # genera bilancio.pdf / cv.docx (una volta)

# carica un documento e mostra metadata + testo — NESSUNA chiave necessaria
python ask.py sample_docs/bilancio.pdf

# + la risposta del modello — serve OPENAI_API_KEY nel .env
python ask.py sample_docs/bilancio.pdf "di quanto è cresciuto il fatturato?"
python ask.py sample_docs/cv.docx      "che ruolo ricopre Giulia?"
python ask.py sample_docs/ricetta.html "quali ingredienti servono?"
python ask.py sample_docs/readme.md    "a cosa serve MeteoCLI?"
```

Senza domanda, `ask.py` gira **offline**: carica il file e ne mostra `Document` +
metadata + anteprima (il client del modello si crea solo se passi una domanda).
Ogni formato ha un **contenuto diverso**, così le prove sono varie.

## L'arco della live demo (mappa sulle slide)

1. **`base.py` — il `Document`.** Si parte dal dolore (forme diverse a valle), poi
   la dataclass minima `text + metadata`. *(slide 6–8)*
2. **`ask.py` — il banco di prova, SUBITO.** Riusa `LLMClient` di L15. È naive di
   proposito: tutto il testo nel prompt. Lo si richiama dopo ogni loader. *(slide 11)*
3. **I loader, uno alla volta, ognuno seguito da `ask()`** *(slide 12–17)*:
   - `pdf.py` → pagina per pagina, `page` nei metadata. `ask()` funziona.
   - `docx.py` → join dei paragrafi. Stessa interfaccia, cambia solo il loader.
   - `html.py` → **il momento chiave**: chiedi gli ingredienti della `ricetta.html`;
     con tutto il testo `ask()` ci infila menu e newsletter, togliendo
     `nav`/`footer`/`script` migliora. "Pulire bene" è L17. *(seme)*
   - `markdown.py` → render → testo.
   - `dispatch.py` → `load()` li smista tutti per estensione.
4. **Esercizio studenti** *(slide 18)*: `esercizio/txt_csv.py` su `note.txt` /
   `clienti.csv`, verifica con `ask()`.
5. **Il muro** *(slide 20)*: prova `ask()` mentale su 300 pagine / 500 doc → non
   ci sta nel contesto, costa troppo → motiva il resto del modulo.

## Note didattiche

- **Il loading non ha bisogno dell'AI per essere mostrato:** `ask.py <file>` senza
  domanda gira senza chiave. L'AI (passare una domanda) è il *perché*, non il *cosa*.
- **HTML con noise è voluto:** `sample_docs/ricetta.html` ha `nav`/`footer`/`script`
  e una newsletter apposta, così il punto "il noise confonde il modello" si vede
  dal vivo. Per mostrarlo, commenta la riga `for tag in soup(NOISE)` in
  `loaders/html.py` e confronta l'output di `ask()` prima/dopo.
- **`llm_client.py`/`pricing.py` non si riscrivono:** vengono dalla L15. Qui si
  riusano per costruire `ask()` in poche righe.
- **`import docx` dentro `loaders/docx.py`** prende il pacchetto installato
  python-docx (import assoluto), non il file stesso (`loaders.docx`).

## Stack (testato)

Python 3.10+ (`list[Document]` ok da 3.9). `pypdf`, `python-docx`,
`beautifulsoup4`, `markdown-it-py`; `openai` + `python-dotenv` per `ask()`;
`reportlab` solo per `make_samples.py`. Modello `gpt-4.1-mini`, Responses API
(come L12/L15).
