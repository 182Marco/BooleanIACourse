"""documenti.py — i documenti del tuo tema in un vector DB (obiettivo 2).

Qui ci sono solo il prologo e gli import: il resto lo scrivi tu.

Uso (dalla cartella scripts/):  python working/documenti.py
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent              # la cartella scripts/: i percorsi si costruiscono da qui
sys.path.insert(0, str(SCRIPTS / "scaffolding"))    # per importare aikit

from dotenv import load_dotenv
load_dotenv(SCRIPTS / ".env")                       # la chiave: servono gli embedding

from aikit.loaders import load                      # Modulo 2 · Lezione 4
from aikit.clean import clean, pipeline_for         # Modulo 2 · Lezione 5
from aikit.chunk import chunk_recursive             # Modulo 2 · Lezione 10
from aikit.embeddings import embed                  # Modulo 2 · Lezione 7
from aikit import vectorstore                       # Modulo 2 · Lezione 9
