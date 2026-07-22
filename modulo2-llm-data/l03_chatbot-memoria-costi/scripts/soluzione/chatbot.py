"""Il chatbot del corso: una classe sola, costruita nei lab. Sta sopra LLMClient.

Stato finale dopo il Lab 5 (con troncamento della storia per budget di token).
Eseguire dalla cartella (con il .env pronto):  python chatbot.py
"""
import tiktoken

from llm_client import LLMClient

_encoder = tiktoken.get_encoding("o200k_base")


def conta_token(messaggi):
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
        self.budget_token = budget_token

    def send(self, testo):
        self.storia.append({"role": "user", "content": testo})
        self._tronca()
        risposta = self.client.chat(self.storia, instructions=self.istruzioni)
        self.storia.append({"role": "assistant", "content": risposta})
        return risposta

    def _tronca(self):
        while len(self.storia) > 1 and conta_token(self.storia) > self.budget_token:
            self.storia.pop(0)

    def chat(self):
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
