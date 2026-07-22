"""Client LLM: parla col modello, tiene il conto della spesa, regge gli errori.

Modulo a sé, separato dal chatbot: ogni chiamata al modello passa di qui.
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
