# Scheda della caccia al tier — Lab L18 (playground)

Per ognuno dei 5 file "candidati LlamaParse" del tuo triage: caricalo nel
playground di cloud.llamaindex.ai, provalo su **almeno 2 tier**, e annota se il
difetto è risolto e quanti crediti ha consumato (li vedi nella dashboard).

Regola d'oro: il tier giusto è **il più basso che risolve il difetto di QUEL
file** — non il più potente. E ricorda i prezzi: fast 1 · cost_effective 3 ·
agentic 10 · agentic_plus 45 crediti/pagina.

| File | Difetto (dal triage) | Tier provati (crediti) | Difetto risolto? | Tier scelto | Perché |
|---|---|---|---|---|---|
| `verbale_scansionato.pdf` | scansione, 0 char estratti | | | | |
| `fattura_scansionata.pdf` | scansione + tabella | | | | |
| `rassegna_stampa.pdf` | scansione a 2 colonne | | | | |
| `listino_prezzi.pdf` | tabella alla rinfusa | | | | |
| `contratto_fornitura.docx` | 2 tabelle sparite | | | | |

Domande per lo show & tell:

1. C'è un file dove il tier più economico basta? E uno dove NON basta?
2. Passare al tier superiore, dove ha cambiato davvero il risultato — e dove
   hai solo pagato di più per lo stesso esito?
3. Con questi prezzi, quanto costerebbe processare 10.000 documenti come i
   tuoi? Il gioco vale la candela per tutti i file?

Il tier scelto qui diventa la mappa `ROUTING` in `pulisci_corpus.py` (TODO 5).
