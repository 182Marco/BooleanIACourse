# L15 · Consegna del lab — Chatbot con memoria e cost-tracking

> **La consegna completa è nelle slide della lezione**
> (`../lezione-15-chatbot-memoria-costi-slidev.pdf`): setup, cosa costruite, il
> contratto, gli obiettivi dei lab e il "fatto quando". Questo file è solo un
> promemoria operativo.

## In due righe

Lavorate in `starter/`. Il **client** lo scrive il docente dal vivo nella demo (lo
ritrovate nello starter). Voi scrivete **`chatbot.py`** — la classe `Chatbot`.

```bash
cd starter && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && cp .env.example .env   # incolla la chiave del corso
```

| Lab | Obiettivo | Fatto quando |
|---|---|---|
| 1 | il bot parla (senza memoria) | `python check_lab1.py` tutto `[OK]` |
| 2 | la memoria (accumula e rispedisce la storia) | `python check_lab2.py` tutto `[OK]` |
| 3 | il loop interattivo | `python check_lab3.py` OK + `python chatbot.py` ricorda davvero |
| 4 | streaming della risposta | provalo dal vivo (`python chatbot.py`) — la risposta "scorre" |
| 5 *(opzionale)* | restare nel budget di token (troncamento) | `python check_lab5.py` tutto `[OK]` — **se c'è tempo** |

**Le firme non si toccano:** `Chatbot`, `send`, `chat`, gli attributi `istruzioni`
e `storia` — i check e i lab successivi ci contano. Bloccato? Alza la mano: il
docente affianca.
