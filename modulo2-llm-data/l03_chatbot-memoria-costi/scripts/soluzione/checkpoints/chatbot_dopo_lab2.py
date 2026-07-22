"""CHECKPOINT — stato del chatbot DOPO il Lab 2 (anti-cascata).

Se sei bloccato sul Lab 2, copia QUESTO file su `starter/chatbot.py` e prosegui col
Lab 3. Qui il bot ricorda la conversazione; manca solo il loop `chat` (Lab 3).
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
        risposta = self.client.chat(self.storia, instructions=self.istruzioni)
        self.storia.append({"role": "assistant", "content": risposta})
        return risposta

    def chat(self):
        raise NotImplementedError("Lab 3: implementa il loop chat")


if __name__ == "__main__":
    Chatbot().chat()
