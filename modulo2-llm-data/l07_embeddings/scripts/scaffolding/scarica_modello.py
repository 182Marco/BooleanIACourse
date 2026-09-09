"""scarica_modello.py — scarica il modello locale degli embedding (una tantum).

~88 MB nella cache di Hugging Face: dopo questo giro il backend "local"
funziona offline e gratis. Si lancia una volta, durante il setup:

    python scaffolding/scarica_modello.py
"""
from sentence_transformers import SentenceTransformer

print("Scarico all-MiniLM-L6-v2 (~88 MB, solo la prima volta)...")
SentenceTransformer("all-MiniLM-L6-v2")
print("Fatto: il backend \"local\" ora funziona offline.")
