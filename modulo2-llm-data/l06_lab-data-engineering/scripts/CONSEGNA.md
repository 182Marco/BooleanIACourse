# L18 · Consegna del lab — Data Engineering su dati sporchi

> **La consegna completa è nelle slide della lezione**
> (`../lezione-18-lab-data-engineering-slidev.pdf`): il dataset, il metodo, gli
> obiettivi dei lab e il "fatto quando". Questo file è solo un promemoria
> operativo.

## In due righe

Si lavora in `working/`. Il dataset sporco è in `../dataset/` (9 file, trappole
diverse e **tier diversi**) e **non si modifica**: si impara a sopravvivergli.
Il metodo del giorno —
**carica → guarda l'output → diagnostica → correggi** — lo mostra il docente
nella demo guida (`primo_giro.py`: replicatelo pure mentre guardate); le slide
vi dicono quando si passa a ogni attività e su quale file.

```bash
cd scripts && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # la chiave LlamaParse la creiamo IN CLASSE (blocco webapp)
# da qui in poi tutto si lancia da scripts/
```

| Attività | Obiettivo | Fatto quando |
|---|---|---|
| Lab 1 — Triage | tutto il dataset (9 file) caricato e classificato (`triage.py`: TODO 1–3) | `python working/triage.py` stampa la tabella e scrive `triage.md`; il check dà `[OK]` sul blocco Lab 1 |
| Caccia al tier (playground) | i tuoi 5 file candidati provati su **almeno 2 tier** ciascuno | `scheda_tier.md` compilata: difetto risolto?, crediti, tier scelto e perché |
| Loader (col docente) | `load_llamaparse(path, tier=...)` dietro l'interfaccia `Document` (TODO 4, si replica dal vivo) | `python scaffolding/check_lab18.py --live` ricostruisce la tabella del listino |
| Lab 2 — Routing | la mappa `ROUTING` file → nativo/tier (TODO 5) + corpus + report | `python working/pulisci_corpus.py` produce `corpus_pulito/` + `report.md` con tier e crediti; `python scaffolding/check_lab18.py` tutto `[OK]` |

**Le firme non si toccano:** `carica_robusto`, `triaga_file`, `triage_dataset`,
`load_llamaparse` (col parametro `tier`), `ROUTING`, `pulisci` — il check ci
conta. Il check base è **istantaneo e non consuma crediti**: lanciatelo a ogni
salvataggio; `--live` fa un parse vero (≈6 crediti), usatelo quando il loader
vi sembra pronto. Allo show & tell portate `triage.md`, `scheda_tier.md` e
`report.md`. Bloccati? Alzate la mano: il docente affianca.
