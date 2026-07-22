"""Chatbot con risposta in STREAMING (soluzione del Lab 4).

Parte dal chatbot base (Lab 1–3) e cambia una cosa sola: nel loop usa
`client.chat_stream(...)` invece di `client.chat(...)`, così la risposta compare
a pezzi man mano. Niente troncamento qui (è il Lab 5).

Eseguire dalla cartella (con il .env pronto):  python chatbot.py
"""
from llm_client import LLMClient


class Chatbot:
    def __init__(self, nome="Aiko", tono="cordiale e conciso"):
        self.client = LLMClient()
        self.istruzioni = (
            f"Sei {nome}, un assistente {tono}. "
            "Rispondi sempre in italiano. "
            "Se non conosci la risposta, dillo invece di inventare."
        )
        self.storia = []

    def send(self, testo):
        self.storia.append({"role": "user", "content": testo})
        risposta = self.client.chat_stream(self.storia, instructions=self.istruzioni)
        self.storia.append({"role": "assistant", "content": risposta})
        return risposta

    def chat(self):
        print("Chatbot — scrivi 'exit' per uscire.\n")
        while True:
            testo = input("Tu> ").strip()
            if testo.lower() in {"exit", "quit"}:
                break
            if not testo:
                continue
            print("Bot> ", end="", flush=True)
            self.send(testo)                  # la risposta viene stampata in streaming
            inp, out, costo = self.client.ultimo_uso
            print(f"\n   [{inp}+{out} token, ${costo:.5f} · totale: ${self.client.costo_totale:.5f}]\n")


if __name__ == "__main__":
    Chatbot().chat()
