"""Client LLM: parla col modello, tiene il conto della spesa, regge gli errori.

Modulo a sé, separato dal chatbot: ogni chiamata al modello passa di qui.
"""
from dotenv import load_dotenv
from openai import OpenAI, APIError, AuthenticationError

from .pricing import cost_usd            # stesso file, ora dentro il package aikit

load_dotenv()


class LLMClient:
    def __init__(self, model="gpt-4.1-mini", temperature=0.7):
        # salva modello e temperatura
        self.model = model
        self.temperature = temperature
        # crea il client OpenAI (con retry e timeout)
        self._client = OpenAI(max_retries=3, timeout=30)
        # inizializza il contatore della spesa totale
        self.costo_totale = 0.0
        # inizializza il contatore delle chiamate
        self.n_chiamate = 0
        # inizializza l'ultimo uso: (input_tokens, output_tokens, costo)
        self.ultimo_uso = (0, 0, 0.0)

    def chat(self, messaggi, instructions=None):
        """Manda i messaggi al modello, aggiorna i costi, gestisce gli errori."""
        # --- chiamata al modello (con gestione errori) ---
        try:
            r = self._client.responses.create(
                model=self.model,
                instructions=instructions,
                input=messaggi,
                temperature=self.temperature,
            )
        # chiave non valida → esci con messaggio chiaro
        except AuthenticationError:
            raise SystemExit("Chiave API non valida o assente: controlla il file .env")
        # altro errore API → restituisci un messaggio di errore, senza bloccare il chatbot
        except APIError as e:
            self.ultimo_uso = (0, 0, 0.0)
            return f"[errore API: {type(e).__name__} — riprova tra poco]"

        # --- aggiorna i contatori ---
        # leggi l'usage dalla risposta
        u = r.usage
        # calcola il costo con cost_usd
        costo = cost_usd(self.model, u.input_tokens, u.output_tokens)
        # aggiorna il totale e il numero di chiamate
        self.costo_totale += costo
        self.n_chiamate += 1
        # salva l'ultimo uso
        self.ultimo_uso = (u.input_tokens, u.output_tokens, costo)
        # restituisci il testo della risposta
        return r.output_text
