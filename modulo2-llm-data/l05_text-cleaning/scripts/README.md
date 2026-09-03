# Modulo 2 · Lezione 5 — Text Cleaning & Pre-processing · guida agli script

Infrasettimanale (📊 + 🎤 + ⌨️, 2h). Il documento della serata è un manuale
LumaDesk in PDF: estratto com'è fa rispondere **male** al modello, perché il
piede di pagina ricorrente parla di un altro prodotto e le sue parole
somigliano alla domanda più di quelle del contenuto vero. Gli studenti scrivono
gli step che lo ripuliscono, in **un solo file**: `working/clean.py`.

Niente notebook, solo script `.py`.

Il `check_lab05.py` è **strumento del docente**, fuori dal percorso studente: il
"fatto quando" degli esercizi è l'output osservabile del main.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze. `reportlab` serve solo a rigenerare il PDF. |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave** di Modulo 2 · Lezione 1-4. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/aikit/loaders.py` | 🧰 | I loader **scritti a Modulo 2 · Lezione 4**, promossi nel toolkit come modulo piatto. Non si tocca: si importa. |
| `scaffolding/aikit/llm_client.py`, `pricing.py` | 🧰 | Eredità di Modulo 2 · Lezione 3, invariati. |
| `scaffolding/ask.py` | 🧰 | Il banco di prova, già scritto: `rispondi()` fa la domanda al modello (`temperature=0`, così due risposte diverse vengono dal testo e non dal caso), `mostra_confronto()` stampa i numeri del prima/dopo. |
| `scaffolding/make_dataset.py` | 🧰 | Genera `dataset/manuale-lumadesk.pdf`. Il docstring documenta la trappola e perché scatta. Non serve in aula. |
| `scaffolding/check_lab05.py` | 🧰 | **Strumento del docente**: non a cascata, non distruttivo, verifica esiti. `--solutions` per la regressione, `--live` per il giro vero (~$0.001), `--manifest` dopo un rework. |
| `dataset/manuale-lumadesk.pdf` | 📄 | Il banco di prova: 4 pagine, piede ricorrente della Mini, numeri di pagina, righe spezzate. |
| `dataset/frankenstein.txt` | 📄 | Gutenberg #84 — boilerplate di testa e coda, righe a ~70 caratteri. Il caso "libro". |
| `dataset/arxiv_1905.00075.pdf` | 📄 | arXiv — sillabazione (15 parole spezzate) e header ricorrente su 7 pagine. Il caso "paper". |
| `working/clean.py` | 🎤⌨️ | **L'unico file della serata.** TODO 1-3 col docente, TODO 4-6 da soli. Il main gira a stadi: ogni step stampa appena è finito. |
| `solutions/clean.py` | 🎤 | La versione completa, stesso nome e stessi import: è **una** soluzione possibile, non l'unica. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Come si prova

```bash
python working/clean.py                          # il giro degli studenti
python solutions/clean.py                        # il riferimento completo
python scaffolding/check_lab05.py --solutions    # docente: regressione, zero costi
python scaffolding/check_lab05.py --live         # docente: il giro vero (~$0.001)
python scaffolding/make_dataset.py               # rigenera il PDF del manuale
```

## Le idee da trasmettere

Sono nel materiale di conduzione della lezione (`conduzione-docente.md`, nella
cartella della lezione), insieme ai numeri misurati e alle soglie: non stanno
qui perché questa cartella arriva agli studenti.
