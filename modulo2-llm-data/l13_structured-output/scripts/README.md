# L25 — Structured Output · guida agli script

Serata infrasettimanale (📊 + 🎤 + ⌨️, 2h): dal testo libero al dato che un
programma può usare. Col docente si scrive `working/structured.py` — schema
Pydantic `PersonaEstratta`, chiamata con `client.responses.parse(...,
text_format=PersonaEstratta)`, retry su `ValidationError` — poi, da soli,
si applica lo stesso pattern su un secondo caso (un botanico e le sue
piante), con un campo `enum` e una lista di oggetti annidati. Niente
notebook, solo script `.py`.

Il `check_lab25.py` è **strumento del docente**, fuori dal percorso
studente: verifica la forma del codice (schema giusto, chiamata cablata
bene, retry che non è un loop) senza spendere un token — mocka
`client.responses.parse`, non chiama davvero OpenAI. Il giro reale (con
chiave vera, su Giulia e sul botanico) sta dietro `--live`.

## Ruolo di ogni file

Legenda: 🧰 ambiente/toolkit riusabile · 🎤 codice di riferimento che il
docente live-coda · ⌨️ da completare dagli studenti · 📄 documenti/dati di
esempio.

| File | Ruolo | Cosa fa |
|---|---|---|
| `requirements.txt` | 🧰 | Dipendenze (`openai`, `pydantic`, `python-dotenv`). |
| `.env.example` | 🧰 | Template per `OPENAI_API_KEY` — la **stessa chiave di L13-L24**, nessuna registrazione nuova. |
| `CONSEGNA.md` | 🧰 | Promemoria operativo della serata per gli studenti. |
| `working/structured.py` | 🎤⌨️ | L'unico file della serata. **TODO 1-2 col docente** (schema + chiamata, poi retry — si replica); **TODO 3 da soli** (schema del botanico, in fondo allo stesso file). Riferimento in `solutions/`. |
| `scaffolding/check_lab25.py` | 🧰 | **Strumento del docente**: `[OK]/[FAIL]` su schema, chiamata e retry (base: istantaneo, zero rete — mocka il client); `--live` fa chiamate vere a OpenAI su Giulia e sul botanico; `--solutions` verifica le soluzioni. Non compare nel percorso studente. |
| `solutions/structured.py` | 🎤 | La versione **completa** del file di `working/` (stesso nome, stessi import), incluso l'esercizio del botanico. |

## Setup

```bash
cd scripts
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # dentro: la stessa chiave OpenAI di L13-L24
```

> **Nota per chi distribuisce (docente):** agli studenti la cartella arriva
> **senza** `.env` e `.venv` (git non li versiona).

## Come si prova

Tutto si lancia dalla cartella `scripts/`:

```bash
python working/structured.py                    # Giulia + il botanico, con chiave vera
python scaffolding/check_lab25.py                # verifica working/: istantaneo, zero costi
python scaffolding/check_lab25.py --live         # chiamate vere a OpenAI (Giulia + botanico)
python scaffolding/check_lab25.py --solutions    # per il docente: verifica solutions/
```

## Percorso in aula (le slide sono la regia: ogni switch ha la sua slide)

1. **Teoria (📊, 45')**: il problema (esempio guida), la storia (JSON mode →
   Structured Outputs, con date vere e l'esempio di rottura), come funziona
   davvero (decodifica vincolata), il JSON Schema (deep dive sui tipi di
   campo), Pydantic vs JSON Schema, l'API universale, i due usi dello schema.
2. **Live coding (🎤, 50')**: `working/structured.py` — Tappa 1 (schema +
   prima chiamata + `model_dump_json()`), Tappa 2 (retry), poi il payoff
   (il ciclo `for interesse in persona.interessi` finalmente scrivibile).
3. **Esercizio guidato (⌨️, 20')**: il metodo in quattro passi, poi lo
   schema del botanico applicato sullo stesso file.
4. **Wrap-up (📊, 5')**: recap, ponte a L26 (lo stesso pattern su documenti
   veri).
