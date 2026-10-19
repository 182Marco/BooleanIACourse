"""I test di skill_agente.py che non chiamano il modello: l'indice nelle istruzioni, il corpo
solo con apri_skill."""
from skill_agente import ISTRUZIONI_SKILL, SKILL, apri_skill, indice, leggi_skill
from tests.test_assistente import chiama


def test_nell_indice_ci_sono_solo_nome_e_descrizione():
    campi, corpo = leggi_skill(SKILL / "rimborso-trasferta" / "SKILL.md")
    assert f"- rimborso-trasferta: {campi['description']}" in indice()
    assert corpo.splitlines()[0] not in ISTRUZIONI_SKILL      # il corpo non è nelle istruzioni


def test_apri_skill_rimanda_il_corpo_senza_frontmatter():
    corpo = chiama(apri_skill, nome="rimborso-trasferta")
    assert corpo.startswith("# Indicazioni per una trasferta")
    assert "description:" not in corpo


def test_apri_skill_con_un_nome_sbagliato_rimanda_l_elenco():
    assert "Nessuna skill «ferie»" in chiama(apri_skill, nome="ferie")


def test_apri_skill_non_esce_dalla_cartella_delle_skill():
    # lo stesso SKILL.md, raggiunto con un percorso: si rifiuta, come leggi_file con ../.env
    assert "Nessuna skill" in chiama(apri_skill, nome="../skill-assistente/rimborso-trasferta")
