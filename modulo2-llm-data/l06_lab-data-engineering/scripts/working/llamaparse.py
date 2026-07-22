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
documento VIAGGIA NEL CLOUD — è il trade-off dello show & tell.
"""
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent / "scaffolding"))   # aikit vive lì

from aikit.loaders.base import Document

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

    TODO 4 — si scrive INSIEME al docente (tu replica nel tuo starter).
    I tre passi, con `httpx` e header `{"Authorization": f"Bearer {_api_key()}"}`:

    0. valida il tier: se non è in TIERS, solleva ValueError.
    1. upload — POST f"{BASE}/api/v1/files" con
         files={"upload_file": (nome_file, open(path, "rb"))}
       Il file id sta nel campo "id" del JSON di risposta.
    2. job — POST f"{BASE}/api/v2/parse" con
         json={"file_id": file_id, "tier": tier, "version": "latest"}
       L'id del job sta nel campo "id".
    3. poll — in loop: GET f"{BASE}/api/v2/parse/{job_id}" con
         params={"expand": "markdown_full"}
       leggi lo status (può stare in dati["job"]["status"] o dati["status"]);
       se "COMPLETED" esci, se "FAILED"/"CANCELLED" solleva RuntimeError,
       altrimenti `time.sleep(2)` e riprova rispettando `timeout` (è un job
       asincrono: decine di secondi sono normali).
       Il testo sta nel campo "markdown_full".

    Ritorna: [Document(markdown, {"source": path, "type": "llamaparse",
                                  "tier": tier, "format": "markdown"})]
    """
    raise NotImplementedError("TODO 4: load_llamaparse")
