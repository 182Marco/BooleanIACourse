# Specifica: la skill `report-mensile`

## A cosa serve

Ogni mese l'ufficio del personale vuole il report delle note spese: la pagina
HTML di `report.py` (Modulo 4 · Lezione 3) e due righe da leggere senza
aprirla. Lanciare `report.py` non basta: le note di un mese possono stare in
un export appena arrivato invece che in `dati/note_spese.csv`, un export può
avere colonne in meno o città senza massimale, e lo script può fermarsi o,
peggio, dare un report vuoto senza errori. La skill dà al coding agent la
procedura per fare il report come lo farebbe una persona attenta: trovare i
dati, lanciare gli script, controllare i numeri, adattare lo script quando
serve, dire cosa non torna.

## Dove sta

- `.claude/skills/report-mensile/SKILL.md`: la procedura;
- `.claude/skills/report-mensile/scripts/dati_del_mese.py`: lo script.

## Cosa produce

Per il mese chiesto (AAAA-MM):

- `output/report-AAAA-MM.html`, la pagina di `report.py`;
- `output/sintesi-AAAA-MM.md`, al massimo sei righe per l'ufficio: note e
  totale, la sede che spende di più, le note fuori massimale, cosa va
  verificato.

## La procedura

1. trovare in quali file di `dati/` ci sono le note del mese, con lo script;
   se non ci sono, fermarsi e dirlo;
2. fare il report con `report.py`; se le note stanno in un altro file o lo
   script si ferma con un errore, capire perché e adattare `report.py`, con
   un test, oppure fermarsi e chiedere se mancano dati;
3. controllare che note e totale del report siano quelli dello script;
4. per quello che i dati non dicono (una città senza massimale, gli hotel
   senza notti) guardare i documenti di `ufficio-completo/` e segnalarlo,
   senza correggere i dati;
5. scrivere la sintesi;
6. chiudere con `pytest` e un riepilogo di cosa è cambiato negli script.

I file di `dati/` e di `ufficio-completo/` non si modificano.

## Lo script

`dati_del_mese.py AAAA-MM` guarda `dati/note_spese.csv` e gli export
(`dati/export-*.csv`) e stampa, per ogni file, quante note ci sono di quel
mese e il totale, le colonne che mancano rispetto a `note_spese.csv` e le
città che non hanno massimali in `dati/massimali.csv`. Si lancia dalla
cartella del progetto:
`python .claude/skills/report-mensile/scripts/dati_del_mese.py 2026-07`.

## La descrizione

<!-- Da scrivere voi: una o due frasi, su una riga, nel campo description di
SKILL.md. Cosa fa la skill e quando usarla. Con il nome, è l'unica parte che il
coding agent legge prima di decidere se aprire la skill: usate le parole con
cui chiederete un report. -->

## Criteri di accettazione

<!-- Da scrivere voi: quando la skill si deve caricare e quando no, cosa deve
produrre, cosa deve fare quando i dati non tornano. Ogni criterio si verifica
guardando la sessione, aprendo un file o lanciando un comando. Un esempio:
«output/report-2026-07.html dice 164 note». -->

## Cosa l'ha fatta caricare

<!-- Da scrivere voi, alla fine: due righe. Cosa, nel nome e nella
descrizione, ha fatto caricare la skill, confrontato con la richiesta. -->
