# Modulo 2 · Lezione 6 — Lab Data Engineering · guida agli script

Lab (⌨️, 4h): gli studenti mettono insieme **Modulo 2 · Lezione 4 (load) + Modulo 2 ·
Lezione 5 (clean)** su un **dataset volutamente sporco** (9 file), scoprono dove il parsing nativo
non basta e imparano a usare **LlamaParse** da professionisti: prima la **caccia
al tier** nel playground (fast 1 · cost_effective 3 · agentic 10 · agentic_plus
45 crediti/pagina), poi il loader via REST v2 dietro la stessa interfaccia
`Document`, con la mappa di **routing** file → parser/tier. Il metodo del
giorno: **carica → guarda l'output → diagnostica → correggi**. Niente notebook,
solo script `.py`.

Il `check_lab06.py` è **strumento del docente**, fuori dal percorso studente:
il "fatto quando" dei lab è l'output osservabile dei due main
(`working/triage.py` e `working/pulisci_corpus.py`), che girano a stadi anche
coi TODO non finiti.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il docente
live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (loader Modulo 2 · Lezione 4 e Modulo 2 · Lezione 5 + `httpx`/`dotenv` per LlamaParse; `reportlab`/`pillow` solo per rigenerare il dataset). |
| `.env.example` | 🧰 | Template per `LLAMA_CLOUD_API_KEY` (si crea **in classe**, free tier). |
| `CONSEGNA.md` | 📄 | Promemoria operativo del lab per gli studenti. |
| `scaffolding/make_dataset.py` | 🧰 | (Ri)genera il dataset. Attrezzo del docente: leggerlo prima del Lab 1 rovina la scoperta. |
| `dataset/guida_smartworking.pdf` | 📄 | Regolamento smart working Lumen, **3 pagine**. |
| `dataset/listino_prezzi.pdf` | 📄 | Listino 2026, 2 pagine con la **tabella dei prezzi** (27 righe). |
| `dataset/verbale_scansionato.pdf` | 📄 | Verbale **scansionato**, 2 pagine. |
| `dataset/fattura_scansionata.pdf` | 📄 | Fattura **scansionata**, con tabella. |
| `dataset/rassegna_stampa.pdf` | 📄 | Ritaglio di rassegna stampa **scansionato**, a 2 colonne. |
| `dataset/report_trimestrale.pdf` | 📄 | Report trimestrale in PDF. |
| `dataset/faq_prodotto.html` | 📄 | Le FAQ prodotto dal sito Lumen — il file della demo. |
| `dataset/contratto_fornitura.docx` | 📄 | Contratto di fornitura in DOCX, 8 articoli con 2 tabelle. |
| `dataset/note_interne.txt` | 📄 | Note interne dell'ufficio acquisti, in `.txt`. |
| `scaffolding/aikit/` | 🧰 | Il toolkit: `loaders.py` (**scritto a Modulo 2 · Lezione 4**) e `clean.py` (**scritto a Modulo 2 · Lezione 5**), promossi come moduli piatti, più `__init__.py`. Non si tocca: si importa. |
| `working/triage.py` | 🎤⌨️ | **Lab 1**. In testa il "primo giro" già scritto (carica → guarda → diagnostica → correggi su `faq_prodotto.html`, la demo del docente); sotto, i TODO 1–3: caricare tutto il dataset, gestire l'encoding, classificare OK/VUOTO/ERRORE, scrivere `triage.md`. |
| `working/llamaparse.py` | 🎤⌨️ | Il loader **gestito** col parametro `tier`: flusso REST v2 (files → parse col tier → poll), via `httpx` puro (TODO 4, si scrive col docente). |
| `working/scheda_tier.md` | ⌨️ | La **scheda della caccia al tier**: per ogni file candidato, tier provati, crediti, difetto risolto?, tier scelto e perché. Si compila nel playground. (Unico file di `working/` senza controparte in `solutions/`, per scelta: la "soluzione" è la vostra sperimentazione.) |
| `working/pulisci_corpus.py` | ⌨️ | **Lab 2**: lo script riproducibile con la mappa **`ROUTING`** file → nativo/tier (TODO 5). Il cleaning di Modulo 2 · Lezione 5 è **fornito**. Scrive `corpus_pulito/` + `report.md` con tier e crediti per file. |
| `scaffolding/check_lab06.py` | 🧰 | **Strumento del docente**: non a cascata (TODO non iniziato = `[--]`), non distruttivo (il giro di prova scrive in una tmp), verifica esiti + integrità dello scaffolding via `manifest.json`. `--solutions` per la regressione, `--live` per un parse vero (~6 crediti), `--manifest` dopo un rework. |
| `solutions/` | 🎤 | Le versioni **complete dei soli file di `working/`** (stesso nome, stessi import): quelle che il docente mostra a fine blocco. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # la chiave LlamaParse si crea in classe
python scaffolding/make_dataset.py   # opzionale: il dataset è già versionato
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env` e `.venv` (git non li versiona). Se la zippi a mano,
> escludili: un `.env` con una chiave dentro contraddice il "la chiave si crea
> in classe" — e fa consumare crediti veri al primo `pulisci_corpus.py`.
> `scaffolding/make_dataset.py` documenta le trappole file per file (la skill
> di preparazione lo richiede): chi lo legge prima del Lab 1 si rovina la
> scoperta, con lo stesso patto di `solutions/` — si può, ma l'esercizio
> perde senso.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/triage.py                      # Lab 1: primo giro + stato dei TODO
python working/pulisci_corpus.py              # Lab 2: corpus_pulito/ + report.md
python solutions/triage.py                    # il riferimento completo del Lab 1
python scaffolding/check_lab06.py             # docente: verifica working/ (offline, zero crediti)
python scaffolding/check_lab06.py --solutions # docente: regressione sulle solutions
python scaffolding/check_lab06.py --live      # docente: un parse vero (~6 crediti)
```

Senza `LLAMA_CLOUD_API_KEY` nel `.env`, `pulisci_corpus.py` gira comunque:
tutto coi loader nativi, e il report annota quali file sono usciti degradati.

Nota: leggendo il PDF corrotto, `pypdf` stampa su stderr l'avviso
`EOF marker not found` — è atteso, fa parte della diagnosi.

## Le idee da trasmettere

Sono nel materiale di conduzione della lezione (`conduzione-docente.md`, nella
cartella della lezione), insieme al reveal del debrief Lab 1 e ai numeri
misurati: non stanno qui perché questa cartella arriva agli studenti.

## E l'SDK ufficiale? (domanda legittima in aula)

Stato verificato a luglio 2026, con parse reali:

- **`llama-cloud-services`** (quello citato da quasi tutti i tutorial) è
  **deprecato** (manutenzione terminata a maggio 2026) e llama-index lì è
  **inscindibile**: `llama-index-core` è dipendenza hard e i metodi
  restituiscono oggetti `llama_index.core.schema.Document` (66 pacchetti,
  ~240 MB di venv).
- Il successore **`llama-cloud >= 1.0`** è invece un client **pulito**: 17
  pacchetti, ~38 MB, dipende solo da `httpx` + `pydantic` — zero llama-index.
  Una chiamata fa tutto: `client.parsing.parse(tier="cost_effective",
  version="latest", upload_file=f, expand=["markdown"])` (upload + poll +
  risultato).
- **Nel lab restiamo sul REST a mano**: le tre chiamate mostrano il job
  asincrono, che è il punto didattico. In produzione il nuovo SDK va
  benissimo — e dopo il lab gli studenti sanno esattamente cosa fa sotto.

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Demo guida (docente, 🎤)**: il "primo giro" su `faq_prodotto.html`, in
   testa a `triage.py` — load, ispezione (4515 char che si aprono col cookie
   banner), diagnosi, primo fix mirato. I file che si *rompono* restano da
   scoprire agli studenti.
2. **Lab 1 (studenti, ⌨️)**: stesso file, TODO 1–3 su tutto il dataset.
3. **LlamaParse webapp (🌐🎤)**: registrazione in classe + demo del giro nel
   playground (tier, markdown, crediti in dashboard).
4. **Caccia al tier (studenti, ⌨️🌐)**: i 5 file candidati su ≥2 tier ciascuno
   nel playground → `scheda_tier.md`.
5. **Loader via codice (🎤, si replica)**: `llamaparse.py` con
   il parametro `tier` (TODO 4).
6. **Lab 2 (studenti, ⌨️)**: la mappa `ROUTING` (TODO 5) → `corpus_pulito/` +
   `report.md` con tier e crediti.
7. **Debrief (📊)**: schede e report a confronto; il tier che ripaga e quello
   che no; trade-off finale.
