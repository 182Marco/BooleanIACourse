"""CHECKPOINT — stato del chatbot DOPO il Lab 3 (anti-cascata).

Se sei bloccato sul Lab 3, copia QUESTO file su `starter/chatbot.py` e prosegui col
Lab 4. Qui il chatbot è completo (parla, ricorda, loop) ma SENZA troncamento.
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
