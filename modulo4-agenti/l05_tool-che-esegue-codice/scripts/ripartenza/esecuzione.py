"""esecuzione.py — il tool che esegue codice Python, e la sua approvazione.

esegui_python lancia un programma scritto dal modello in un processo a parte, nella cartella
dell'ufficio, con un timeout, e rimanda al modello quello che il programma stampa: testa e coda
se è lungo, come mini-swe-agent (Modulo 4 · Lezione 1). Non c'è sandbox: il programma può
fare tutto quello che può fare chi lancia l'assistente, anche uscire da ufficio/. Per questo il
tool ha needs_approval=True: il run si ferma prima di ogni esecuzione, e una persona legge il
codice e dice sì o no.

Le altre funzioni sono il ciclo di approvazione: a ogni interruzione il codice a schermo, sì o
no, un motivo facoltativo per il no; se si esce, lo stato del run va su file e al lancio dopo,
nella stessa sessione, si riprende da lì. L'assistente le usa quando ESEGUI_PYTHON = True.

La versione del docente, scritta da specifica-approvazione.md: è il punto di ripartenza.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

from agents import Runner, RunState, function_tool

from strumenti_cartella import RADICE

TIMEOUT = 30            # secondi, come mini-swe-agent
MAX_OUTPUT = 10_000     # caratteri; oltre, i primi e gli ultimi 5.000
CARTELLA = Path(__file__).parent

ISTRUZIONI_CODICE = """Hai anche esegui_python, che esegue un programma Python nella cartella dell'ufficio: usalo per i conti su molte righe dei CSV (somme, conteggi, incroci tra due file), invece di leggere i file interi. Scrivi programmi brevi, al massimo 20 righe, con la sola libreria standard; apri i file con il percorso che dà elenca_file e stampa solo i risultati. Prima di ogni esecuzione una persona legge il codice e la approva o la rifiuta."""


def testa_e_coda(testo: str) -> str:
    """Il testo com'è, se non supera MAX_OUTPUT; se no l'inizio e la fine, con quanti
    caratteri mancano in mezzo."""
    if len(testo) <= MAX_OUTPUT:
        return testo
    meta = MAX_OUTPUT // 2
    tolti = len(testo) - MAX_OUTPUT
    return (f"Output troppo lungo: {tolti} caratteri tolti in mezzo.\n"
            f"{testo[:meta]}\n[… {tolti} caratteri tolti …]\n{testo[-meta:]}")


@function_tool(needs_approval=True)
def esegui_python(codice: str) -> str:
    """Esegue un programma Python nella cartella dell'ufficio e rimanda quello che stampa (output
    ed errori), con il codice di uscita. Prima di ogni esecuzione una persona legge il codice e la
    approva o la rifiuta.

    Args:
        codice: il programma completo, con la sola libreria standard; i file si aprono con il
            percorso che dà elenca_file; i risultati si stampano con print.
    """
    ambiente = dict(os.environ, PYTHONUTF8="1")   # UTF-8 anche su Windows
    ambiente.pop("OPENAI_API_KEY", None)          # il programma non vede la chiave
    try:
        processo = subprocess.run(
            [sys.executable, "-c", codice], cwd=RADICE, env=ambiente,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"Il programma è stato fermato dopo {TIMEOUT} s: non era ancora finito."
    return f"codice di uscita {processo.returncode}\n{testa_e_coda(processo.stdout)}"


def file_stato(sessione) -> Path:
    """Il file in cui si salva il run lasciato a metà: uno per sessione, così si riprende nella
    stessa conversazione."""
    return CARTELLA / f"stato-{sessione.session_id}.json"


def mostra_richiesta(interruzione) -> None:
    """Stampa la chiamata che aspetta l'approvazione: il codice, riga per riga, se è esegui_python;
    se no il nome del tool e i suoi argomenti."""
    argomenti = json.loads(interruzione.arguments or "{}")
    print(f"\n   Il modello vuole chiamare {interruzione.name}.")
    if interruzione.name == "esegui_python":
        for numero, riga in enumerate(argomenti["codice"].splitlines(), start=1):
            print(f"   {numero:3} | {riga}")
    else:
        print(f"   argomenti: {json.dumps(argomenti, ensure_ascii=False)}")


def decidi(stato, interruzioni) -> bool:
    """Per ogni interruzione: la richiesta a schermo, poi sì, no (con un motivo facoltativo) o
    esci. Le decisioni vanno nello stato. Ritorna False se l'utente vuole uscire."""
    for interruzione in interruzioni:
        mostra_richiesta(interruzione)
        risposta = input("   Eseguo? [s = sì, n = no, e = esci e riprendi dopo] ").strip().lower()
        if risposta == "e":
            return False
        if risposta == "s":
            stato.approve(interruzione)
        else:                                       # tutto quello che non è «s» è un no
            motivo = input("   Perché no? (Invio per non dirlo) ").strip()
            stato.reject(interruzione, rejection_message=motivo or None)   # None: il testo dell'SDK
    return True


async def esegui_con_approvazione(agente, domanda_o_stato, sessione, max_turni):
    """Il run con l'approvazione: finché si ferma su chiamate da approvare, chiede e riprende
    dallo stato. Riceve la domanda, o lo stato di un run da riprendere (Runner.run accetta tutti
    e due). Ritorna il result finale, o None se l'utente esce: allora lo stato va su file."""
    result = await Runner.run(agente, domanda_o_stato, session=sessione, max_turns=max_turni)
    while result.interruptions:
        stato = result.to_state()
        if not decidi(stato, result.interruptions):
            file_stato(sessione).write_text(stato.to_string(), encoding="utf-8")
            print(f"   Stato salvato in {file_stato(sessione).name}: rilanciate con la stessa sessione per riprendere.")
            return None
        result = await Runner.run(agente, stato, session=sessione, max_turns=max_turni)
    return result


async def riprendi_in_sospeso(agente, sessione, max_turni):
    """Riprende il run lasciato a metà in questa sessione: carica lo stato dal file e continua
    con l'approvazione, che chiede di nuovo le decisioni in sospeso. Il file si cancella solo
    quando il run ripreso arriva alla risposta: se la ripresa si interrompe (un errore, il
    limite di turni), al lancio dopo si riprova."""
    file = file_stato(sessione)
    stato = await RunState.from_string(agente, file.read_text(encoding="utf-8"))
    print("   Riprendo il run lasciato a metà.")
    result = await esegui_con_approvazione(agente, stato, sessione, max_turni)
    if result is not None:                          # None: l'utente è uscito di nuovo, il file è già riscritto
        file.unlink()
    return result
