# Modulo 2 · Lezione 6 · Consegna del lab — Data Engineering su dati sporchi

> **La consegna completa è nelle slide della lezione**: il dataset, il metodo,
> gli obiettivi dei lab e il "fatto quando". Questo file è solo un promemoria
> operativo.

## In due righe

Si lavora in `working/`. Il dataset sporco è in `dataset/` (9 file, trappole
diverse) e **non si modifica**: si impara a sopravvivergli. Il metodo del
giorno — **carica → guarda l'output → diagnostica → correggi** — lo mostra il
docente nel *primo giro*, che trovate già scritto in testa a
`working/triage.py`; le slide vi dicono quando si passa a ogni attività e su
quale file.

```bash
cd scripts && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # la chiave LlamaParse la creiamo IN CLASSE (blocco webapp)
# da qui in poi tutto si lancia da scripts/
```

Entrambi gli script del giorno girano anche coi TODO non ancora fatti:
stampano quello che c'è e dicono cosa manca. **Non serve finire tutto per
vedere qualcosa.**

| Attività | Obiettivo | Fatto quando |
|---|---|---|
| Lab 1 — Triage | tutto il dataset (9 file) caricato e classificato (`working/triage.py`: TODO 1–3) | `python working/triage.py` stampa la tabella completa e scrive `triage.md` |
| Caccia al tier (playground) | i tuoi 5 file candidati provati su **almeno 2 tier** ciascuno | `scheda_tier.md` compilata: difetto risolto?, crediti, tier scelto e perché |
| Loader (col docente) | `load_llamaparse(path, tier=...)` dietro l'interfaccia `Document` (TODO 4, si replica dal vivo) | il main di `pulisci_corpus.py` usa il TUO loader sui file instradati |
| Lab 2 — Routing | la mappa `ROUTING` file → nativo/tier (TODO 5) | `python working/pulisci_corpus.py` produce `corpus_pulito/` + `report.md` con tier e **crediti** per file, senza note di degrado |

Il Lab 2 **non dipende** dal Lab 1: se il triage non è chiuso, il pomeriggio
parte lo stesso.

**Le firme non si toccano:** `carica_testo`, `triaga_file`, `triage_dataset`,
`load_llamaparse` (col parametro `tier`), `ROUTING`. Il *come* è vostro.
Occhio ai crediti: ogni run di `pulisci_corpus.py` **con la chiave** richiama
LlamaParse sui file non nativi — sistemate il ROUTING con lo script offline
(senza chiave fa tutto coi loader nativi e lo scrive nel report), il giro vero
fatelo quando siete convinti. Al debrief portate `triage.md`,
`scheda_tier.md` e `report.md`. Bloccati? Alzate la mano: il docente affianca.
