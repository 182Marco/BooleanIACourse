"""I test dello script della skill report-mensile, sui veri export (in sola lettura)."""
import subprocess
import sys
from pathlib import Path

CARTELLA = Path(__file__).parent.parent
SCRIPT = CARTELLA / ".claude" / "skills" / "report-mensile" / "scripts" / "dati_del_mese.py"


def lancia(mese, tmp_path):
    # da un'altra cartella: lo script trova dati/ da solo
    return subprocess.run([sys.executable, str(SCRIPT), mese],
                          capture_output=True, text=True, encoding="utf-8", cwd=tmp_path)


def test_luglio_sta_in_note_spese(tmp_path):
    esito = lancia("2026-07", tmp_path)
    assert esito.returncode == 0, esito.stderr
    assert "dati/note_spese.csv: 164 note di 2026-07, 8.963,53 €" in esito.stdout
    assert "In tutto: 164 note di 2026-07, 8.963,53 €" in esito.stdout
    assert "città senza massimale" not in esito.stdout


def test_settembre_sta_solo_nell_export(tmp_path):
    esito = lancia("2026-09", tmp_path)
    assert esito.returncode == 0, esito.stderr
    assert "dati/note_spese.csv: 0 note di 2026-09" in esito.stdout
    assert "dati/export-ottobre.csv: 190 note di 2026-09, 9.934,75 €" in esito.stdout
    assert "colonne mancanti: notti" in esito.stdout
    assert "città senza massimale: Bologna" in esito.stdout


def test_un_mese_senza_note(tmp_path):
    esito = lancia("2026-12", tmp_path)
    assert esito.returncode == 1
    assert "nessuna nota per 2026-12" in esito.stdout
