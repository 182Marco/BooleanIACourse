# Modulo 2 · Lezione 4 — Data Loading · guida agli script

Infrasettimanale (📊 + 🎤 + ⌨️, 2h): si insegna al codice a leggere i file.
Il docente live-coda quattro loader — PDF, DOCX, HTML, Markdown — e la porta
unica `load()` che li smista; poi gli studenti aggiungono da soli `.txt` e
`.csv`. Tutto in **un unico file**, `working/loaders.py`. Niente notebook,
solo script `.py`.

È la lezione in cui nascono tre cose che restano per tutto il modulo: il
toolkit `aikit/`, la struttura a tre cartelle `scaffolding/` · `working/` ·
`solutions/`, e il criterio di "fatto" basato sull'**output osservabile**
invece che su un check da lanciare.

Il `check_lab04.py` è **strumento del docente**, fuori dal percorso studente:
serve per la regressione dei materiali (`--solutions`) e per la diagnosi
rapida di uno studente bloccato. Verifica i risultati leggendo il dataset,
istantaneo, zero rete e zero costi.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Le quattro librerie di parsing (`pypdf`, `python-docx`, `beautifulsoup4`, `markdown-it-py`) + `openai`/`python-dotenv`; `reportlab` serve solo a rigenerare il dataset. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 3**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti: setup, i sette TODO, il "fatto quando" di ciascuno. |
| `scaffolding/aikit/__init__.py` | 🧰 | Il docstring del package: che cosa il toolkit ha accumulato finora e perché da oggi ha un nome. |
| `scaffolding/aikit/llm_client.py` | 🧰 | Il client di Modulo 2 · Lezione 3, **verbatim**: cambia la cartella, non il codice (l'unica riga diversa è l'import di `pricing`, ora modulo del package). **Non si tocca.** |
| `scaffolding/aikit/pricing.py` | 🧰 | I prezzi e il calcolo del costo di Modulo 2 · Lezione 2, **verbatim**. |
| `scaffolding/ask.py` | 🧰 | Il banco di prova, già scritto: `ask()` fa la domanda al modello con tutto il testo nel prompt (`temperature=0`, così a ogni giro esce la stessa risposta); `mostra()` e `rispondi()` sono gli helper di stampa usati dal main. |
| `dataset/relazione-annuale.pdf` | 📄 | Relazione annuale di Lumen S.r.l., **3 pagine** con header e footer ripetuti e la numerazione "pagina N di 3": è quello che rende visibile un Document per pagina. |
| `dataset/verbale-consiglio.docx` | 📄 | Verbale di CdA in paragrafi e titoli — il caso "documento Word". |
| `dataset/faq-garanzia.html` | 📄 | La pagina di supporto del sito: il contenuto in `<main>`, e intorno promo, menu, sidebar e footer che parlano **dello stesso argomento con numeri diversi**. È il documento del momento chiave. |
| `dataset/guida-lumadesk.md` | 📄 | Guida rapida in Markdown: titoli, liste, tabella, codice, link. |
| `dataset/note-supporto.txt` · `ordini.csv` | 📄 | I due file dell'esercizio studenti. |
| `working/loaders.py` | 🎤⌨️ | **L'unico file della serata.** TODO 1-5 col docente (`load_pdf`, `load_docx`, `load_html`, `load_markdown`, `load`); TODO 6-7 da soli (`load_txt`, `load_csv` + l'aggancio a `load()`). Il main gira a ogni stadio: ogni TODO finito stampa il suo risultato, gli altri dicono «ancora da fare». |
| `solutions/loaders.py` | 🎤 | **Non distribuito agli studenti.** La versione completa dello stesso file (stesso nome, stessi import). Le docstring dei TODO 1-5 contengono **la frase da dire mentre si scrive**: il docente può narrarle leggendole. |
| `scaffolding/check_lab04.py` | 🧰 | **Strumento del docente**: `[OK]/[FAIL]` sui risultati, mai sulle firme interne; ogni TODO in isolamento; non scrive niente su disco; segnala se dataset o scaffolding sono stati modificati. `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `scaffolding/make_dataset.py` | 🧰 | (Ri)genera i sei documenti del `dataset/`, che è già versionato. Ogni trappola è documentata nel docstring. |
| `scaffolding/confronto_html.py` | 🧰 | Da qui escono **i numeri del momento chiave** in slide: caratteri con e senza `decompose()`, quali affermazioni del boilerplate finiscono alla lettera nel prompt, e con `--live` le risposte vere del modello nei due casi. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di Modulo 2 · Lezione 1 – Modulo 2 · Lezione 3
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env`, `.venv` e cache (git non li versiona), e **senza**
> `solutions/`. Il venv si crea in `scripts/`, non più dentro una cartella
> `starter/` come a Modulo 2 · Lezione 3: è il primo dei quattro cambi di
> abitudine che la slide di setup dichiara in aula.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/loaders.py                        # il giro della serata (~$0.002 a lancio)
python scaffolding/check_lab04.py                # verifica working/: istantanea, zero costi
python scaffolding/check_lab04.py --solutions    # per il docente: verifica le soluzioni
python scaffolding/confronto_html.py             # i numeri del boilerplate, zero rete
python scaffolding/confronto_html.py --live      # 10 chiamate vere, ~$0.004 a lancio
python scaffolding/make_dataset.py               # rigenera il dataset (non serve in aula)
```

## Dove sta il resto

Le **idee da trasmettere** coi numeri della serata, il **percorso in aula**
blocco per blocco e la **conduzione della live demo** (che cosa dire, quali
risposte aspettarsi, come diagnosticare uno studente bloccato) stanno in
`conduzione-docente.md`, nella cartella della lezione: contengono le risposte
dell'esercizio e non si distribuiscono.
