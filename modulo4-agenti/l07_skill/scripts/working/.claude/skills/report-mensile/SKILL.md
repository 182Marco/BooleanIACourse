---
name: report-mensile
description: Fa il report mensile delle note spese (la pagina HTML di report.py e una sintesi di poche righe per l'ufficio del personale) per un mese AAAA-MM, controllando i dati e gli export. Usala quando si chiede il report, il riepilogo o la sintesi delle note spese o dei rimborsi di un mese.
---

# Il report mensile delle note spese

Il mese è AAAA-MM. Se dalla richiesta manca l'anno o il mese, chiedilo in una
riga e fermati. Python è quello del venv del modulo: `../../../.venv/bin/python`.

0. **Il report c'è già?** Se `output/report-AAAA-MM.html` esiste, non rifarlo:
   dillo, con il percorso del file, e fermati. Si rifà solo se lo chiedono
   esplicitamente.
1. **I dati del mese.** Dalla cartella del progetto:
   `../../../.venv/bin/python .claude/skills/report-mensile/scripts/dati_del_mese.py AAAA-MM`.
   Lo script dice, file per file, quante note ci sono del mese e il totale, le
   colonne che mancano e le città senza massimale. Se stampa «nessuna nota per
   AAAA-MM», fermati e dillo: non scrivere niente in `output/`.
2. **Il report.** `../../../.venv/bin/python report.py AAAA-MM`. Oggi
   `report.py` legge solo `dati/note_spese.csv`. Se le note del mese stanno in
   un export, o lo script si ferma con un errore:
   - capisci il perché, leggendo il codice e il messaggio;
   - adatta `report.py`, per esempio con il file come argomento, come fa
     `rimborsi.py`. Aggiungi un test in `tests/test_report.py`;
     `test_i_numeri_di_luglio` deve continuare a passare;
   - una nota di una città senza massimale non è né fuori massimale né
     regolare. Contala a parte, come fa `rimborsi.py` con «MASSIMALE
     MANCANTE», e non lasciare che il report si fermi con un `KeyError`;
   - se mancano dati che il codice non può ricavare, fermati e chiedi.
3. **Il controllo.** Note e totale stampati da `report.py` devono essere quelli
   dello script del passo 1 (la riga «In tutto»). Se non tornano, non andare
   avanti: dillo e spiega la differenza.
4. **Quello che i dati non dicono.** Con `cerca` e `leggi_file` (o leggendo i
   file), nei documenti di `ufficio-completo/`:
   - per una città senza massimale, la policy trasferte
     (`policy-trasferte-note-spese.docx`, art. 3: i massimali si fissano
     nell'autorizzazione della trasferta);
   - per un export senza `notti`, gli hotel contati come una notte, la
     stessa policy (art. 2 e 6).

   Segnalalo come cosa da verificare, citando il documento. Non correggere i
   dati e non inventare massimali o notti.
5. **La sintesi.** Scrivi `output/sintesi-AAAA-MM.md`, al massimo sei righe,
   con i numeri del report:

   ```
   # Note spese AAAA-MM
   - N note, totale X €.
   - La sede che spende di più: <sede>, X € (N note).
   - Fuori massimale: N note, X € di eccedenza.
   - Da verificare: <città senza massimale, hotel senza notti, …> [documento]
   ```

   Se non c'è niente da verificare, scrivi «Da verificare: niente».
6. **La chiusura.** Lancia `../../../.venv/bin/python -m pytest` e riporta
   l'esito. Poi elenca cosa è cambiato negli script e quali test sono nuovi,
   oppure scrivi «nessuna modifica agli script». Finisci con i percorsi del
   report e della sintesi.

I file di `dati/` e di `ufficio-completo/` non si modificano.
