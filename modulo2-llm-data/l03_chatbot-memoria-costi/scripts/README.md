# L15 — Chatbot con memoria e cost-tracking · materiale docente

Materiale per il lab del sabato (coding studenti). Gli studenti costruiscono
**una sola classe `Chatbot`** e la fanno crescere a strati, partendo da
`starter/`; il docente tiene la `soluzione/` testata e affianca. Niente notebook:
solo script `.py`.

Lab: i primi **3 sono il core** (chatbot funzionante); **Lab 4 = streaming**
(prova dal vivo); **Lab 5 = troncamento per budget di token** (opzionale, se c'è
tempo). Il codice di ciascun lab è poche righe: il tempo è capire, testare e — al
Lab 1 — scrivere **bene** il system prompt, non battere righe.

## Struttura

```
scripts/
├── CONSEGNA.md            # promemoria operativo — la consegna completa è nelle slide
├── README.md             # questa guida (docente)
├── starter/              # punto di partenza STUDENTI
│   ├── pricing.py            # risultato della demo (prezzi/costo, da L14)
│   ├── llm_client.py         # risultato della demo (classe LLMClient)
│   ├── chatbot.py            # STUB ← la classe Chatbot, cresce nei lab
│   ├── check_lab1.py         # il bot parla, senza memoria (no chiave)
│   ├── check_lab2.py         # la memoria (no chiave)
│   ├── check_lab3.py         # il loop chat() (no chiave)
│   ├── check_lab5.py         # troncamento per budget di token (no chiave) — Lab 5
│   ├── .env.example
│   └── requirements.txt
└── soluzione/            # riferimento DOCENTE (tutto completo, testato)
    ├── pricing.py
    ├── llm_client.py
    ├── chatbot.py            # la classe Chatbot completa (con troncamento, stato dopo Lab 5)
    ├── checkpoints/          # stati intermedi (anti-cascata, li fornisce il docente SOLO se serve)
    │   ├── chatbot_dopo_lab1.py   # parla, senza memoria
    │   ├── chatbot_dopo_lab2.py   # + memoria
    │   └── chatbot_dopo_lab3.py   # + loop (chatbot completo, senza troncamento)
    ├── lab4_streaming/       # soluzione del Lab 4 (runnable): client con chat_stream + loop a pezzi
    │   ├── pricing.py
    │   ├── llm_client.py          # = client + metodo chat_stream
    │   └── chatbot.py             # = base + loop che stampa in streaming
    ├── .env.example
    └── requirements.txt
```

> **Lab 4 (streaming)**: soluzione runnable a sé in `lab4_streaming/` (logica
> validata offline con un mock; l'effetto "a pezzi" si vede con la chiave).
> Niente check automatico né checkpoint per questo lab.
> **`pricing.py` e `llm_client.py` li scrive il docente dal vivo** nella live demo
> (non sono "materiale dato"); nello `starter/` ci sono come risultato della demo,
> così i lab girano per tutti. Moduli piatti accanto a `chatbot.py` (`from
> llm_client import ...`): niente package, niente nome da ricordare.

## Come funziona il lab (il modello didattico)

Un solo oggetto `Chatbot` che cresce metodo dopo metodo: **parla → ricorda →
loop** (core), poi streaming e budget come extra. La sequenza concettuale della
lezione resa tangibile.

Lo stub e la consegna sono volutamente **all'osso e concettuali**: la spiegazione
di *cosa* costruire vive sulle slide, non come hint nei file. Ogni lab core ha
**quattro appoggi** (la lezione della L12, dove il coding senza scaffolding saltò):

1. **Stub di partenza** — la classe con le sole firme + TODO concettuali (`starter/chatbot.py`).
2. **Contratto d'interfaccia fissato** — i nomi pubblici (`Chatbot`, `send`,
   `chat`, gli attributi `istruzioni`/`storia`) NON cambiano.
3. **Check eseguibile per "done"** — `python check_labN.py` dà `[OK ]/[FAIL]`;
   girano **senza chiave** (iniettano un `chat` finto, niente API).
4. **Checkpoint anti-cascata** — bloccato sul lab N? Gli dai
   `soluzione/checkpoints/chatbot_dopo_labN.py` (lab 1–3) e prosegue. **Gli
   studenti non sanno che esistono**: li fornisci solo se servono davvero.

> ⚠️ **Check vs stato giusto.** `check_lab1` verifica lo stato *Lab 1* (il bot NON
> ricorda): passa su `dopo_lab1`, non sul finale. Per validare ogni check usa lo
> stato corrispondente (vedi "Verificare").

Prima di iniziare: **pre-check setup** (venv + `.env` con la chiave pronti).

## Tempi e mappatura (~275', con margine sulle 4h; il Lab 5 è opzionale)

| Blocco | Durata | Cosa si scrive |
|---|---|---|
| Intro | 25' | cosa costruiamo, perché senza framework |
| Live demo 🎤 | 35' | il docente scrive `pricing.py` + `llm_client.py` dal vivo |
| Lab 1 ⌨️ | 45' | `__init__` + `send` senza memoria → `check_lab1.py` |
| ☕ Pausa | 15' | |
| Lab 2 ⌨️ | 30' | `send` tiene e rispedisce la `storia` → `check_lab2.py` |
| Lab 3 ⌨️ | 40' | il loop `chat()` → `check_lab3.py` + prova reale |
| Lab 4 ⌨️ | 35' | streaming della risposta — prova dal vivo (no check) |
| Lab 5 ⌨️ *(opz.)* | 35' | troncamento per budget di token → `check_lab5.py` |
| Wrap-up | 15' | recap |

> Le stime hanno **margine**: il piano somma ~275' contro le ~240' nominali, così
> setup/debug/varianza non mandano fuori tempo. Se si è indietro si comprime/salta
> il **Lab 5** (opzionale) e parte del recap. Il tempo dei lab non è battitura
> (poche righe): è capire, testare e — Lab 1 — la cura del system prompt.

## Verificare (docente)

```bash
# la soluzione gira davvero (serve il .env con la chiave del corso):
cd soluzione && cp .env.example .env   # incolla la chiave
python chatbot.py                      # "mi chiamo Marco" / "come mi chiamo?"

# ogni check PASSA sullo stato giusto (copialo su chatbot.py accanto a check + pricing/llm_client):
#   check_lab1 → checkpoints/chatbot_dopo_lab1.py
#   check_lab2 → checkpoints/chatbot_dopo_lab2.py
#   check_lab3 → checkpoints/chatbot_dopo_lab3.py
#   check_lab5 → chatbot.py (stato finale, con troncamento)
# (Lab 4 streaming: soluzione runnable in soluzione/lab4_streaming/ — cd lì e `python chatbot.py` con la chiave)
```

## La classe `Chatbot` completa (riferimento docente)

Stato finale, con il troncamento del Lab 5 (uguale a `soluzione/chatbot.py`).

```python
import tiktoken

from llm_client import LLMClient

_encoder = tiktoken.get_encoding("o200k_base")


def conta_token(messaggi):                       # Lab 5
    return sum(len(_encoder.encode(m["content"])) for m in messaggi)


class Chatbot:
    def __init__(self, nome="Aiko", tono="cordiale e conciso", budget_token=2000):
        self.client = LLMClient()
        self.istruzioni = (
            f"Sei {nome}, un assistente {tono}. "
            "Rispondi sempre in italiano. "
            "Se non conosci la risposta, dillo invece di inventare."
        )
        self.storia = []
        self.budget_token = budget_token         # Lab 5

    def send(self, testo):
        self.storia.append({"role": "user", "content": testo})
        self._tronca()                           # Lab 5 (al Lab 2 questa riga non c'è)
        risposta = self.client.chat(self.storia, instructions=self.istruzioni)
        self.storia.append({"role": "assistant", "content": risposta})
        return risposta

    def _tronca(self):                           # Lab 5
        while len(self.storia) > 1 and conta_token(self.storia) > self.budget_token:
            self.storia.pop(0)

    def chat(self):                              # Lab 3
        print("Chatbot — scrivi 'exit' per uscire.\n")
        while True:
            testo = input("Tu> ").strip()
            if testo.lower() in {"exit", "quit"}:
                break
            if not testo:
                continue
            risposta = self.send(testo)
            inp, out, costo = self.client.ultimo_uso
            print(f"\nBot> {risposta}")
            print(f"   [{inp}+{out} token, ${costo:.5f} · totale: ${self.client.costo_totale:.5f}]\n")


if __name__ == "__main__":
    Chatbot().chat()
```

> **Lab 1** (`send` senza memoria): `return self.client.chat([{"role": "user", "content": testo}], instructions=self.istruzioni)`
> · **Lab 2 / Lab 3** = il `send` qui sopra **senza** la riga `self._tronca()` (il troncamento arriva al Lab 5).

## Lab 4 · streaming — soluzione

Soluzione completa e runnable in **`soluzione/lab4_streaming/`** (`cd` lì e
`python chatbot.py` con la chiave). Lo streaming è una chiamata diversa all'SDK
(`responses.stream`), quindi **si aggiunge un metodo `chat_stream` al client**: è
il client a possedere le chiamate al modello, perciò estenderlo è il suo mestiere,
non una violazione. Il loop poi usa `chat_stream` al posto di `chat`.

> ⚠️ La **logica è validata offline con un mock** (testo accumulato, stampa a
> pezzi, costo/uso aggiornati); l'effetto reale "a pezzi" si vede solo con la
> chiave — provalo dal vivo prima di proporlo.

Il cuore è il metodo aggiunto al client (Responses API, L12):

```python
# in LLMClient — un secondo metodo accanto a chat()
def chat_stream(self, messaggi, instructions=None):
    testo = ""
    with self._client.responses.stream(
        model=self.model, instructions=instructions,
        input=messaggi, temperature=self.temperature,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)   # stampa man mano
                testo += event.delta
        finale = stream.get_final_response()
    u = finale.usage
    costo = cost_usd(self.model, u.input_tokens, u.output_tokens)
    self.costo_totale += costo
    self.ultimo_uso = (u.input_tokens, u.output_tokens, costo)
    return testo

# nel loop di Chatbot.chat(): al posto di stampare la risposta tutta in fondo,
#   print("\nBot> ", end="")
#   risposta = self.client.chat_stream(self.storia, instructions=self.istruzioni)
#   (appendendo il messaggio utente PRIMA e la risposta DOPO, come in send)
```

## Stack (testato)

Python 3.12 · `openai==2.44.0` · `tiktoken==0.13.0` · `python-dotenv==1.1.1`.
Modello `gpt-4.1-mini`, **Responses API** (`responses.create`, `input` = lista
messaggi), coerente con L12/L13. Il costo si legge da `response.usage`.

> **Smoke test API:** la chiamata reale richiede la chiave nel `.env`. La logica
> offline (memoria, troncamento, struttura del loop e dello streaming via mock) è
> testata senza chiave; l'**effetto reale dello streaming** (Lab 4) va visto dal vivo.

## Note didattiche

- **Due pezzi, non cinque file.** Il client (`LLMClient`) + il chatbot (`Chatbot`).
  Il system prompt è una stringa nell'`__init__`, la memoria è `self.storia`.
- **Perché il client resta separato.** Ha uno **stato** (`costo_totale`,
  `ultimo_uso`, config) e una **policy** (errori): il punto da cui passa ogni
  chiamata, comodo per logging/cache/altri provider.
- **Core = Lab 1–3.** Streaming (Lab 4) e troncamento (Lab 5, opzionale) sono
  extra: il chatbot dei primi tre lab funziona già.
- **Continuità:** `.env`+dotenv e Responses API (L12), "il modello non ha memoria"
  (L12), token/costi (L14), streaming (L12).
