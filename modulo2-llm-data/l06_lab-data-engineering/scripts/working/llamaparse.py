"""LlamaParse — il loader GESTITO, per i documenti dove pypdf & co. si arrendono.

Non sostituisce i loader nativi: si affianca. Stessa interfaccia (`list[Document]`),
quindi il resto della pipeline non si accorge di chi ha fatto il parsing. È il
punto del lab: un servizio esterno si INNESTA dietro la tua interfaccia.

Il servizio è un'API REST asincrona (v2) — lo stesso flusso che hai visto nella
webapp, ma via codice (docs: developers.llamaindex.ai). Tre passi:

  1. POST /api/v1/files                 → carichi il file, torna un file id
  2. POST /api/v2/parse                 → avvii il job scegliendo il TIER
  3. GET  /api/v2/parse/{id}?expand=markdown_full → poll finché COMPLETED

Il **tier** è la manopola qualità/costo — la stessa del playground:

  fast            1 credito/pagina   solo estrazione testo (niente struttura)
  cost_effective  3 crediti/pagina   testo + tabelle: il default ragionevole
  agentic        10 crediti/pagina   layout difficili (colonne, scansioni con tabelle)
  agentic_plus   45 crediti/pagina   i casi disperati

Serve LLAMA_CLOUD_API_KEY nel `.env` (free tier ~10k crediti/mese). Occhio: il
documento VIAGGIA NEL CLOUD — un trade-off da dire esplicitamente in aula.
"""
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit import Document

load_dotenv()

BASE = "https://api.cloud.llamaindex.ai"

# crediti per pagina, per tier (rilevati a luglio 2026 dal listino LlamaCloud)
TIERS = {"fast": 1, "cost_effective": 3, "agentic": 10, "agentic_plus": 45}


def _api_key() -> str:
    key = os.getenv("LLAMA_CLOUD_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "Manca LLAMA_CLOUD_API_KEY nel .env — creala su cloud.llamaindex.ai "
            "(free tier) e copiala nel file .env (vedi .env.example)."
        )
    return key


def load_llamaparse(path: str, tier: str = "cost_effective",
                    timeout: int = 240) -> list[Document]:
    """Parsa `path` con LlamaParse al `tier` scelto → `[Document]` (markdown).

    🎤 TODO 4 — NON si fa da soli: si scrive INSIEME al docente, replicando
    dal vivo (è il blocco di live coding, vedi la slide di switch). I tre
    passi (upload → job col tier → poll fino a COMPLETED) sono nel docstring
    in cima al file; l'autenticazione è un header Bearer con `_api_key()` su
    ogni richiesta. Due contratti da rispettare:

    - un tier che non sta in TIERS → ValueError, prima di qualunque altra
      cosa (controllo della chiave compreso)
    - ritorna [Document(markdown, {"source": path, "type": "llamaparse",
                                   "tier": tier, "format": "markdown"})]
    """
    raise NotImplementedError("TODO 4: load_llamaparse")
