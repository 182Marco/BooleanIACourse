# Lezione 12 — Prima Applicazione AI — script per il live coding

Script **pronti e testati** da cui fare live coding: il docente li **riscrive a
mano dal vivo**, tenendo questi file nascosti come riferimento. Ogni script è
**indipendente** (riscrive da capo client, modello, ecc.): si possono mostrare
in qualsiasi ordine senza dipendenze tra loro. I commenti `#` suggeriscono cosa
dire all'aula.

> Testati con `openai==2.42.0`, `python-dotenv==1.1.1`, Python 3.12, modello `gpt-4.1-mini`.

## La chiave API (dotenv)
La chiave sta nel file `.env` (già nel `.gitignore`, non va su Git):
```
OPENAI_API_KEY=sk-...
```
Ogni script fa `load_dotenv()` e poi `OpenAI()`, che legge la chiave dall'ambiente.
Per partire: `cp .env.example .env` e incolla la chiave del corso.

## Gli script (in ordine di lezione)

| File | Mostra |
|------|--------|
| `01_prima_chiamata.py` | `responses.create`, `instructions`+`input`, `output_text`; classifica "il collo" -> spedizione |
| `02_parametri.py` | `temperature` 0 (3x identico) vs alta (3x diverso); `max_output_tokens` |
| `03_conversazione.py` | senza vs con cronologia (la lista di messaggi la passiamo noi) |
| `04_errori.py` | `try/except`; chiave finta -> `AuthenticationError`; `max_retries`/`timeout` |
| `05_streaming.py` | `stream=True`, eventi `response.output_text.delta` |
| `06_chatbot.py` | chatbot multi-turno: contesto + streaming + try/except |
| `07_classificatore.py` | `Ticket` (Pydantic), classifica seriale vs `asyncio.gather` (parallelo) |

Si **discutono soltanto** (niente script), perché il deep dive è la prossima lezione: la struttura della response e i token/costi (slide del Cap 3) e i tool integrati `web_search`/`file_search`/... (Cap 8).

`tickets.json` sono i ticket d'esempio (usati da `07_classificatore.py`).

## Setup dell'ambiente (a inizio lezione, tutti insieme, da zero)
Apri un terminale nella cartella `scripts`. Verifica prima che Python ci sia con
`python --version` (o `python3 --version`). Poi:

### Windows (PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1          # se bloccato: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
pip install -r requirements.txt
```

### WSL / Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
(Per WSL la prima volta, da PowerShell come amministratore: `wsl --install` e riavvia.)

### macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Poi `cp .env.example .env`, incolla la chiave, e lancia il primo script:
`python 01_prima_chiamata.py`.

## Fallback senza setup: Google Colab
Chi ha problemi col setup usa `prima_applicazione_ai_colab.ipynb` (cartella della
lezione) su <https://colab.research.google.com> (File > Carica blocco note).
