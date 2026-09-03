"""aikit — il toolkit del corso, cresce di un pezzo a lezione.

    Modulo 2 · Lezione 3   llm_client.py, pricing.py   parlare col modello
    Modulo 2 · Lezione 4   loaders.py                  portare dentro i documenti
    Modulo 2 · Lezione 5   clean.py                    ripulire il testo estratto

Quello che c'è dentro non si tocca: si importa. Oggi lo si mette alla prova su
documenti veri — e si vede dove non basta.

    from aikit import load, Document
    from aikit.clean import normalize_whitespace, remove_repeated_lines
"""
from .loaders import Document, load

__all__ = ["Document", "load"]
