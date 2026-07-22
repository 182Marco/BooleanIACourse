"""Client LLM con anche lo STREAMING (soluzione del Lab 4).

Stesso client di prima + un secondo metodo `chat_stream`: lo streaming è una
chiamata diversa all'SDK (`responses.stream`), e il client è proprio il posto
dove vive ogni chiamata al modello — quindi si aggiunge qui, accanto a `chat`.
"""
from dotenv import load_dotenv
from openai import OpenAI, APIError, AuthenticationError

from pricing import cost_usd

load_dotenv()


class LLMClient:
    def __init__(self, model="gpt-4.1-mini", temperature=0.7):
        self.model = model
        self.temperature = temperature
        self._client = OpenAI(max_retries=3, timeout=30)
        self.costo_totale = 0.0
        self.n_chiamate = 0
        self.ultimo_uso = (0, 0, 0.0)        # (input, output, costo) dell'ultima chiamata

    def chat(self, messaggi, instructions=None):
        try:
            r = self._client.responses.create(
                model=self.model,
                instructions=instructions,
                input=messaggi,
                temperature=self.temperature,
            )
        except AuthenticationError:
            raise SystemExit("Chiave API non valida o assente: controlla il file .env")
        except APIError as e:
            self.ultimo_uso = (0, 0, 0.0)
            return f"[errore API: {type(e).__name__} — riprova tra poco]"

        u = r.usage
        costo = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.costo_totale += costo
        self.n_chiamate += 1
        self.ultimo_uso = (u.input_tokens, u.output_tokens, costo)
        return r.output_text

    def chat_stream(self, messaggi, instructions=None):
        """Come chat(), ma STAMPA la risposta a pezzi man mano che arriva.

        Accumula il testo, lo ritorna intero alla fine e aggiorna costo/uso come
        chat(). Lo streaming usa `responses.stream` (Responses API, L12).
        """
        testo = ""
        try:
            with self._client.responses.stream(
                model=self.model,
                instructions=instructions,
                input=messaggi,
                temperature=self.temperature,
            ) as stream:
                for event in stream:
                    if event.type == "response.output_text.delta":
                        print(event.delta, end="", flush=True)   # stampa subito il pezzo
                        testo += event.delta
                finale = stream.get_final_response()
        except AuthenticationError:
            raise SystemExit("Chiave API non valida o assente: controlla il file .env")
        except APIError as e:
            self.ultimo_uso = (0, 0, 0.0)
            return f"[errore API: {type(e).__name__} — riprova tra poco]"

        u = finale.usage
        costo = cost_usd(self.model, u.input_tokens, u.output_tokens)
        self.costo_totale += costo
        self.n_chiamate += 1
        self.ultimo_uso = (u.input_tokens, u.output_tokens, costo)
        return testo
