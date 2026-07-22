# L26 — Extraction & Parsing · guida agli script

Serata infrasettimanale (📊 + 🎤 + ⌨️, 2h): il pattern di L25 (Pydantic +
structured outputs) si punta su documenti veri. Col docente si scrive
`working/extract.py` — lettura diretta della fattura, schema `Fattura` con
due campi **nullable** (`sconto`, `note`), `client.responses.parse(...,
text_format=Fattura)` — poi, da soli, lo stesso pattern su un CV, con un
proprio schema e un campo nullable (le certificazioni). Niente notebook,
solo script `.py`.

Il `check_lab26.py` è **strumento del docente**, fuori dal percorso
studente: verifica dataset (I/O locale, reale) e la forma del codice
(schema giusto, nullable rispettato, chiamata cablata bene) senza spendere
un token — mocka `client.responses.parse`. Il giro reale (chiamate vere su
tutte e tre le fatture + il CV) sta dietro `--live`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il
docente live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di
esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `pydantic`, `python-dotenv`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L25**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `scaffolding/make_dataset.py` | 🧰 | Genera le fatture Lumen e il CV in `dataset/`. Calcola imponibile/iva/sconto/totale e **verifica che tornino** prima di scrivere il file — niente numeri buttati lì a mano. Deterministico. |
| `dataset/fattura_2026-0143.txt` | 📄 | Fattura completa (con sconto e nota) — Tappe 1-2. Imponibile 1.840,00 · IVA 404,80 · sconto 92,00 · totale 2.152,80. |
| `dataset/fattura_2026-0158.txt` | 📄 | Fattura senza sconto né nota — Tappa 3 (il nullable in azione). Imponibile 340,00 · IVA 74,80 · totale 414,80. |
| `dataset/fattura_2026-0171.txt` | 📄 | Fattura con un omaggio scritto in prosa (non come riga) — Tappa 4: verificato che produce sempre un recall basso, la riga sparisce dall'estrazione. |
| `dataset/cv_marta_colombo.txt` | 📄 | Il CV dell'esercizio breve — non menziona certificazioni (il campo nullable naturale). |
| `working/extract.py` | 🎤⌨️ | L'unico file della serata. **TODO 1-2 col docente** (lettura file, schema `Fattura`, chiamata — si replica); **TODO 3 da soli** (schema del CV, in fondo allo stesso file). Riferimento in `solutions/`. |
| `scaffolding/check_lab26.py` | 🧰 | **Strumento del docente**: `[OK]/[FAIL]` su dataset, schema, nullable e chiamate (base: istantaneo, zero rete — mocka il client); `--live` fa chiamate vere a OpenAI su tutte e tre le fatture + il CV; `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `solutions/extract.py` | 🎤 | La versione **completa** del file di `working/` (stesso nome, stessi import), incluso l'esercizio del CV. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L25
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env` e `.venv` (git non li versiona). I file di `dataset/`
> sono già generati e versionati: non serve rigenerarli in aula.

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/extract.py                        # le 3 fatture + il CV, con chiave vera
python scaffolding/check_lab26.py                 # verifica working/: istantaneo, zero costi
python scaffolding/check_lab26.py --live          # chiamate vere a OpenAI (3 fatture + CV)
python scaffolding/check_lab26.py --solutions     # per il docente: verifica solutions/
python scaffolding/make_dataset.py                # rigenera dataset/ (se serve) + verifica i conti
```

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 35')**: estrazione vs RAG, casi d'uso, perché i documenti
   sporchi vanno bene lo stesso, campi mancanti (nullable sul serio),
   precisione e recall (TP/FP/FN, poi i due errori).
2. **Live coding (🎤, 65')**: `working/extract.py` — Tappa 1 (carico la
   fattura), Tappa 2 (schema + estrazione), Tappa 3 (il nullable in
   azione sulla Fattura 2), Tappa 4 (il caso impreciso sulla Fattura 3).
3. **Esercizio breve (⌨️, 15')**: lo schema del CV, con un campo nullable.
4. **Wrap-up (📊, 5')**: recap, ponte al Progetto Modulo 2 (sabato).
