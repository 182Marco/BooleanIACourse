"""aikit — il toolkit che cresce lezione dopo lezione.

L15: client + prompts + conversation (chatbot).
L16: loaders/ (leggere file eterogenei → Document).
L17: clean (ripulire il testo grezzo prima di chunk/embed).   ← questa lezione

    from aikit import load, Document, clean

Ogni lezione aggiunge un mattone riusabile: al Progetto Modulo 2 gli studenti
hanno già in mano l'intera pipeline load → clean → chunk → embed → search.
"""
from .clean import clean, clean_file, pipeline_for
from .loaders import Document, load

__all__ = ["load", "Document", "clean", "clean_file", "pipeline_for"]
