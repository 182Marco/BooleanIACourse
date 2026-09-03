"""aikit — il toolkit del corso, cresce di un pezzo a lezione.

    Modulo 2 · Lezione 3   llm_client.py, pricing.py   parlare col modello
    Modulo 2 · Lezione 4   loaders.py                  portare dentro i documenti
    Modulo 2 · Lezione 5   clean.py                    ← lo scrivete stasera,
                                                        entra qui la prossima volta

Quello che c'è dentro non si tocca: si importa.
"""
from .loaders import Document, load

__all__ = ["Document", "load"]
