# Specifica: l'approvazione nell'assistente

Da scrivere in `esecuzione.py`, che ha già `esegui_python` (finito) e le
firme con le docstring del ciclo di approvazione: le docstring dicono cosa
fa ogni funzione, e non si cambiano. `assistente.py` chiama già queste
funzioni quando `ESEGUI_PYTHON = True`, e non si cambia. Si lavora solo in
`esecuzione.py` e in `tests/test_approvazione.py`, che è nuovo.

## Cosa deve succedere

`esegui_python` ha `needs_approval=True`: prima di ogni esecuzione il run
si ferma e rimanda le chiamate da approvare. Per ognuna:

1. A schermo il codice scritto dal modello, riga per riga con il numero di
   riga; per un altro tool, il nome e gli argomenti (`mostra_richiesta`).
2. La domanda: `s` per sì, `n` per no, `e` per uscire. Tutto quello che non
   è `s` né `e` vale come no.
3. Dopo un no, la domanda del motivo, facoltativa: se l'utente scrive un
   motivo, il modello riceve quel testo al posto dell'output del tool; se
   preme Invio, riceve il testo di default dell'SDK.
4. Con `e` il run si interrompe: il suo stato va nel file dato da
   `file_stato(sessione)` e il programma finisce.
5. Al lancio dopo, se l'utente dà lo stesso nome di sessione,
   `assistente.py` chiama `riprendi_in_sospeso`: lo stato si ricarica dal
   file, le domande dei punti 1-3 si rifanno per le chiamate in sospeso e
   il run continua. Il file si cancella quando il run ripreso arriva alla
   risposta: se la ripresa si interrompe per un errore, al lancio dopo si
   riprova.

Dopo le decisioni il run riprende dallo stato, e si ferma di nuovo se il
modello chiede un'altra esecuzione.

## Criteri di accettazione

1. Il ciclo usa l'approvazione dell'SDK: le interruzioni del result, le
   decisioni prese sullo stato del run, la ripresa con
   `Runner.run(agente, stato)`.
2. Il file contiene lo stato del run, così che la ripresa riparta dallo
   stesso punto: le chiamate già fatte non si rifanno e il modello non
   viene richiamato prima della decisione.
3. Nessuna esecuzione parte senza un sì: `needs_approval=True` resta.
4. Il no con motivo manda al modello il motivo; il no senza motivo, il
   testo di default dell'SDK.
5. `esegui_python`, `file_stato`, le firme e le docstring restano quelle del
   file; nessuna dipendenza nuova, nessun file oltre quelli indicati.
6. `tests/test_approvazione.py` prova, senza API, con `modello_finto()` di
   `tests/test_esecuzione.py` e con `input()` sostituito da `monkeypatch`:
   il sì (il modello riceve l'output del programma), il no con e senza
   motivo (il testo che riceve il modello), l'uscita e la ripresa con un
   agente nuovo, il cui modello finto ha solo la risposta finale (il file
   c'è dopo l'uscita e non c'è più dopo la ripresa, la risposta arriva), una
   ripresa che si interrompe per un errore del modello (il file resta).
   Sessione e file di stato dei test stanno in `tmp_path`, mai nella
   cartella del progetto (`CARTELLA` di `esecuzione.py` si cambia con
   `monkeypatch.setattr`). `pytest` verde, compresi i test che c'erano.
