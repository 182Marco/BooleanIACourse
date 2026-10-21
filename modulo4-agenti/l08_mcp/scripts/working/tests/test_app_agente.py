"""Test di app_agente.py e login_mcp.py, senza rete: il function tool e il file del token."""
import asyncio
import os

from app_agente import APP, testo_fuori_massimale
from login_mcp import TokenInFile
from mcp.shared.auth import OAuthToken


def test_le_note_fuori_massimale_di_luglio():
    testo = testo_fuori_massimale("2026-07")
    righe = testo.split("\n")
    assert righe[0] == "20 note fuori massimale in 2026-07, su 164."
    assert len(righe) == 21
    assert any(r.startswith("nota 2377: Luca Ferri, cena a Roma il 2026-07-28, 46.42 €, massimale 45.00 €") for r in righe)


def test_un_mese_senza_note():
    assert testo_fuori_massimale("2026-09") == "0 note fuori massimale in 2026-09, su 0."


def test_le_tre_app():
    assert {"trello", "notion", "airtable"} <= set(APP)
    for nome in ("trello", "notion", "airtable"):
        assert APP[nome]["url"].startswith("https://") and APP[nome]["tool"]


def test_il_token_resta_nel_file(tmp_path):
    archivio = TokenInFile(tmp_path / "prova.json")
    assert asyncio.run(archivio.get_tokens()) is None
    asyncio.run(archivio.set_tokens(OAuthToken(access_token="finto", refresh_token="finto-anche-lui")))
    assert asyncio.run(archivio.get_tokens()).access_token == "finto"
    if os.name != "nt":                                 # su Windows chmod non toglie la lettura agli altri
        assert oct((tmp_path / "prova.json").stat().st_mode)[-3:] == "600"
