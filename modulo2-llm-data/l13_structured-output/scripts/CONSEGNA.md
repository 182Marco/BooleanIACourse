# L25 — Structured Output · consegna

Stasera la LLM smette di rispondere con frasi e comincia a rispondere con
**dati**: uno schema Pydantic vincola esattamente la forma dell'output. Un
solo file per tutta la serata: `working/structured.py`. Tutto si lancia
dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti)

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L24
```

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

## Live coding col docente (🎤 si replica) — `working/structured.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `PersonaEstratta` (schema Pydantic) + `estrai_persona(testo)`: la prima chiamata con structured outputs | lanciando lo script su Giulia, `persona.interessi` è già una LISTA, non una stringa da spezzare |
| 2 | `estrai_persona_con_retry(testo)`: un secondo tentativo su `ValidationError`, non un loop | il codice ha un solo `try/except` con un retry, niente `while True` |

## Esercizio guidato (⌨️ da soli) — in fondo allo stesso file

Applicate il metodo appena visto sul testo del botanico (`TESTO_BOTANICO`,
già nel file): schema `PersonaBotanica` con una lista di `Pianta` annidate,
e un campo `enum` per l'esposizione alla luce (non testo libero: un insieme
chiuso di valori).

**Fatto quando:** lanciando lo script, `botanico.piante` contiene le tre
piante del testo, coi campi giusti — incluso l'`enum` rispettato, non tre
stringhe diverse a caso.

Insight: se volete, aggiungete anche altri campi oltre al minimo (es. altre
informazioni sul botanico) — purché seguano lo stesso schema dichiarato, e
i campi che potrebbero mancare dal testo siano `nullable` (`| None = None`),
non obbligatori a tutti i costi.

```bash
python working/structured.py
```

## Cosa portate a casa

`structured.py` con il pattern schema Pydantic → `responses.parse` →
oggetto validato, il retry su `ValidationError`, e il vostro schema del
botanico. Giovedì (L26) lo stesso pattern si punta su documenti veri.
