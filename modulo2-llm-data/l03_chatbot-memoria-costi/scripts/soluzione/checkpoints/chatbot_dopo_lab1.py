"""CHECKPOINT — stato del chatbot DOPO il Lab 1 (anti-cascata).

Se sei bloccato sul Lab 1, copia QUESTO file su `starter/chatbot.py` e prosegui col
Lab 2. Qui il bot parla ma SENZA memoria; `chat` è ancora da scrivere (Lab 3).
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
        # Lab 1: senza memoria — manda solo il messaggio corrente
        return self.client.chat([{"role": "user", "content": testo}],
                                instructions=self.istruzioni)

    def chat(self):
        raise NotImplementedError("Lab 3: implementa il loop chat")


if __name__ == "__main__":
    Chatbot().chat()
