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

```
description: Fa il report mensile delle note spese (la pagina HTML di report.py e una sintesi di poche righe per l'ufficio del personale) per un mese AAAA-MM, controllando i dati e gli export. Usala quando si chiede il report, il riepilogo o la sintesi delle note spese o dei rimborsi di un mese.
```

## Criteri di accettazione

Non usare la skill se esite già il report di questo mese

Quando si carica (si vede nella sessione):

- «fammi il report delle note spese di luglio 2026» e «mi serve il riepilogo
  dei rimborsi di settembre» caricano `report-mensile`;
- «quante note ha presentato Luca Ferri?», «aggiungi un test a rimborsi.py» e
  «qual è il massimale della cena a Milano?» non la caricano.

Cosa produce, con un mese tutto in `dati/note_spese.csv` (2026-07):

- `dati_del_mese.py 2026-07` stampa 164 note e 8.963,53 € per
  `note_spese.csv`, 0 note per `export-ottobre.csv`, nessuna città senza
  massimale;
- `output/report-2026-07.html` esiste e dice 164 note e 8.963,53 €;
- `output/sintesi-2026-07.md` ha al massimo sei righe e riporta 164 note,
  8.963,53 €, la sede che spende di più e il numero di note fuori massimale,
  uguali a quelli del report;
- nella sessione l'agente confronta note e totale del report con quelli dello
  script prima di scrivere la sintesi.

Quando i dati non tornano:

- con 2026-09 lo script trova le note solo in `export-ottobre.csv`: 190 note,
  9.934,75 €, la colonna `notti` che manca e la città Bologna senza
  massimale; il report finale dice 190 note e 9.934,75 €, non un report vuoto;
- se per farlo cambia `report.py`, c'è un test nuovo in `tests/` e `pytest`
  passa; i report di 2026-07 escono uguali a prima;
- la sintesi di 2026-09 segnala Bologna senza massimale e gli hotel senza
  notti come cose da verificare, citando il documento di `ufficio-completo/`
  che ha guardato; le note di Bologna non sono date per fuori massimale né per
  regolari senza dirlo;
- con un mese senza note (2026-12) l'agente si ferma e lo dice: nessun file in
  `output/` per quel mese;
- `git status dati/ ufficio-completo/` non mostra modifiche;
- la sessione finisce con l'esito di `pytest` e un riepilogo di cosa è
  cambiato negli script (o «nessuna modifica»).

## Cosa l'ha fatta caricare

<!-- Da scrivere voi, alla fine: due righe. Cosa, nel nome e nella
descrizione, ha fatto caricare la skill, confrontato con la richiesta. -->
