# Specifica: l'assistente dell'ufficio, versione 1.0

## La richiesta dell'ufficio

L'assistente prepara in Trello l'ingresso di Davide Russo come fa Claude
Code, e risponde a chi entra: cosa portare il primo giorno, e cosa è già
pronto.

## I fatti

- `assistente.py` è la versione 0.9 (`CHANGELOG.md`): un programma solo, con
  le skill, il function tool `note_fuori_massimale` e, con `--app trello`, i
  tool di Trello. Non sa le date e non conosce la procedura di ingresso.
- Le date le fa `scadenze.py`, quello dell'obiettivo 1.
- Le skill dell'assistente stanno in `skill-assistente/`, una cartella per
  skill con il suo `SKILL.md`. I tool dell'assistente sono `elenca_file`,
  `cerca`, `leggi_file`, `apri_skill`, i function tool e quelli di Trello:
  non `Skill` né `Bash`. I file li legge solo in `ufficio-completo/`, dove ci
  sono la procedura e una copia di `assunzioni.csv`.
- `tests/test_assistente.py` controlla l'elenco esatto dei tool
  dell'assistente.
- `pytest` resta verde e `python valuta.py --solo 1,2,3,4,7,9,10` dà tutte le
  risposte giuste. La versione nuova va in `CHANGELOG.md`.

## Cosa aggiungere

<!-- Da scrivere voi: cosa serve all'assistente per preparare un ingresso e
rispondere a chi entra, e dove sta ogni pezzo (in quale file, con quale
nome). -->

## Cosa non cambia

<!-- Da scrivere voi: cosa resta com'è, perché l'assistente di sempre non si
rompa. -->

## Criteri di accettazione

<!-- Da scrivere voi: da tre a cinque, verificabili con pytest, con un
comando o guardando la traccia. -->
