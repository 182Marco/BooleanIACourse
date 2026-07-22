"""Il chatbot del corso: una classe sola, da costruire nei tre lab.

Costruisci UN solo oggetto `Chatbot` e fallo crescere a strati. Cosa serve in ogni
lab è spiegato sulle slide e in CONSEGNA.md — qui ci sono solo le firme da riempire.

Verifica:    python check_lab1.py  /  check_lab2.py  /  check_lab3.py   (senza chiave)
Prova reale: python chatbot.py   (serve il .env con la chiave)
"""
from llm_client import LLMClient


class Chatbot:
    # Lab 1 — costruisci il bot e fagli mandare un messaggio (per ora senza memoria).
    def __init__(self, nome="Aiko", tono="cordiale e conciso"):
        raise NotImplementedError("Lab 1: costruisci il chatbot")

    def send(self, testo):
        # Lab 1: manda il messaggio al modello e torna la risposta.
        # Lab 2: fai in modo che il bot tenga la conversazione e la rimandi tutta.
        raise NotImplementedError("Lab 1: implementa send")

    # Lab 3 — il loop interattivo che usa send().
    def chat(self):
        raise NotImplementedError("Lab 3: implementa il loop chat")


if __name__ == "__main__":
    Chatbot().chat()
