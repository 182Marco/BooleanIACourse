"""LlamaParse — il loader GESTITO, per i documenti dove pypdf & co. si arrendono.

Non sostituisce i loader nativi: si affianca. Stessa interfaccia (`list[Document]`),
quindi il resto della pipeline non si accorge di chi ha fatto il parsing.

Il servizio è un'API REST asincrona (v2) — lo stesso flusso della webapp, via
codice (docs: developers.llamaindex.ai). Tre passi:

  1. POST /api/v1/files                 → carichi il file, torna un file id
  2. POST /api/v2/parse                 → avvii il job scegliendo il TIER
  3. GET  /api/v2/parse/{id}?expand=markdown_full → poll finché COMPLETED

Il **tier** è la manopola qualità/costo — la stessa che hai visto nel playground:

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
    """Parsa `path` con LlamaParse al `tier` scelto → `[Document]` (markdown)."""
    # si valida PRIMA di toccare la rete: un tier sbagliato non deve
    # costare una chiamata (né un upload)
    if tier not in TIERS:
        raise ValueError(f"tier {tier!r} non valido: scegli tra {sorted(TIERS)}")
    headers = {"Authorization": f"Bearer {_api_key()}"}

    # 1. upload del file → file id
    with open(path, "rb") as f:
        r = httpx.post(f"{BASE}/api/v1/files", headers=headers,
                       files={"upload_file": (Path(path).name, f)}, timeout=60)
    r.raise_for_status()
    file_id = r.json()["id"]

    # 2. avvio del job di parsing, scegliendo il tier
    r = httpx.post(f"{BASE}/api/v2/parse", headers=headers,
                   json={"file_id": file_id, "tier": tier, "version": "latest"},
                   timeout=60)
    r.raise_for_status()
    job_id = r.json()["id"]

    # 3. poll: è un job asincrono, decine di secondi sono normali
    scadenza = time.monotonic() + timeout
    while True:
        r = httpx.get(f"{BASE}/api/v2/parse/{job_id}", headers=headers,
                      params={"expand": "markdown_full"}, timeout=30)
        r.raise_for_status()
        dati = r.json()
        # lo status può stare annidato in dati["job"] o al livello alto,
        # a seconda dello stadio del job: le gestiamo entrambe
        status = (dati.get("job") or {}).get("status") or dati.get("status")
        if status == "COMPLETED":
            break
        if status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"LlamaParse job {job_id} fallito: {status}")
        if time.monotonic() > scadenza:
            raise TimeoutError(f"LlamaParse job {job_id} non pronto dopo {timeout}s")
        time.sleep(2)

    markdown = dati["markdown_full"]
    return [Document(markdown, {"source": path, "type": "llamaparse",
                                "tier": tier, "format": "markdown"})]
