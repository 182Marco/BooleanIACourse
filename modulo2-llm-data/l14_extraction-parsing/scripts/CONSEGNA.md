# L26 — Extraction & Parsing · consegna

Il pattern di martedì (schema Pydantic + structured outputs) si punta stasera
su un documento vero: una fattura Lumen, letta da file — non scritta per
l'occasione. Un solo file per tutta la serata: `working/extract.py`. Tutto
si lancia dalla cartella `scripts/`.

## Setup (una volta sola, nei primi minuti)

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env    # dentro: la STESSA chiave OpenAI di L13-L25
```

> Chiave persa? **Alzate la mano**: il docente ha una chiave di riserva.

I documenti sono già in `dataset/` (due fatture Lumen + una terza per la
Tappa 4 + un CV per l'esercizio): non serve rigenerarli, ma se volete
`python scaffolding/make_dataset.py` li ricrea da zero.

## Live coding col docente (🎤 si replica) — `working/extract.py`

| TODO | Cosa | Fatto quando |
|---|---|---|
| 1 | `carica(nome_file)`: lettura diretta del file (testo già pulito) | il testo grezzo stampato mostra intestazione e footer della fattura |
| 2 | `RigaFattura` + `Fattura` (Pydantic, due campi **nullable**: `sconto`, `note`) + `estrai_fattura(testo)` | sulla Fattura 1: `imponibile + iva - sconto == totale`; sulla Fattura 2 (senza sconto): `sconto` e `note` tornano `None`, non un errore |

Poi la Tappa 4: si lancia sulla Fattura 3, che ha un omaggio scritto in
prosa (non come riga "Nx prodotto @ prezzo") — verificato che l'estrazione
lo perde SEMPRE: un caso vero di recall basso, non solo descritto.

## Esercizio breve (⌨️ da soli) — in fondo allo stesso file

Un CV (`dataset/cv_marta_colombo.txt`, già presente): scrivete uno schema
Pydantic proprio (nome, esperienze, competenze) con almeno un campo che il
CV potrebbe non menzionare — es. le certificazioni — dichiaratelo
`nullable`, e fatelo popolare dal modello.

**Fatto quando:** il record ha i campi giusti popolati, e il campo
eventualmente assente è `None` — non un errore, non un valore inventato.

```bash
python working/extract.py
```

## Cosa portate a casa

`extract.py` con lo schema `Fattura` (nullable sul serio) e il vostro
schema per il CV. Sabato (L27) tutto il modulo confluisce nel Progetto
Modulo 2, dove l'output strutturato entra "dove serve" nella pipeline.
