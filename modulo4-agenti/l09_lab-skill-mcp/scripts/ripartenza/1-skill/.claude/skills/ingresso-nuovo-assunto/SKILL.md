---
name: ingresso-nuovo-assunto
description: Prepara l'ingresso dei nuovi assunti di Valtesa con la procedura PR-PER-04 - le attività del loro ruolo, con chi le fa e la scadenza, in un task per persona nell'app dell'ufficio. Da usare quando si chiede di preparare un ingresso, un nuovo assunto o un onboarding.
---

# Ingresso di un nuovo assunto

Preparare gli ingressi: mettere nell'app le attività di ogni persona. I nuovi
ingressi sono in `dati/assunzioni.csv`; la procedura è
`ufficio-completo/procedura-ingresso-dotazioni.pdf`. Non modificare i file di
`dati/` e di `ufficio-completo/`.

## Preparare gli ingressi

1. **Date e indirizzo.** Lancia `python scadenze.py ID` per una persona,
   `python scadenze.py --tutti` per tutte: dice ruolo, reparto, contratto,
   note, l'indirizzo di posta e le date. Le date e l'indirizzo li prendi da
   lì, senza ricalcolarli.
2. **Le attività.** Dalla tabella sotto prendi solo quelle che valgono per la
   persona, guardando reparto, contratto e note. Per un caso che la tabella
   non copre leggi la procedura; se non basta, segnalalo invece di inventare.
3. **Leggi l'app prima di scrivere.** Cerca lo spazio «Valtesa · nuovi
   ingressi» e, dentro, un task con lo stesso nome e la stessa data di
   ingresso, tra quelli aperti (gli archiviati non contano). Se c'è, l'ingresso
   è già preparato: non rifarlo e non modificarlo. Per saperlo basta il
   titolo: le attività dei task che ci sono già non servono, e nel riepilogo
   non dire niente di quello che non hai letto. Se lo spazio non c'è, crealo.
   Non toccare niente fuori da quello spazio.
4. **Un task per persona**, nel formato dell'app (sotto), con tutte le sue
   attività. Nelle righe dei documenti e delle dotazioni scrivi solo quelli che
   valgono per la persona, non le condizioni.
5. **Riepilogo**: per ogni persona se l'hai preparata o c'era già, quante
   attività, e cosa non torna.

| Attività | Chi la fa | Scadenza | Per chi |
|---|---|---|---|
| Lettera di benvenuto: data, ora e sede, referente, documenti da portare | Ufficio del Personale | 10 giorni lavorativi prima | tutti tranne gli stagisti |
| Richiesta delle dotazioni nel portale | Responsabile di reparto | 10 giorni lavorativi prima | tutti |
| Visita medica preventiva | Ufficio del Personale, con il medico competente | ultimo giorno lavorativo prima | Produzione e Logistica |
| Account aziendale (l'indirizzo di posta) e dotazioni del ruolo | IT | primo giorno | tutti |
| Badge | Ufficio del Personale | primo giorno | tutti |
| Accoglienza: contratto, informative, regolamenti | Ufficio del Personale | primo giorno | tutti tranne gli stagisti |
| Documenti da consegnare (elenco sotto) | il nuovo assunto, all'Ufficio del Personale | primo giorno | tutti tranne gli stagisti |
| Dispositivi di protezione e istruzioni per i reparti | Servizio di prevenzione e protezione | primo giorno | Produzione e Logistica |
| Presentazione del gruppo e piano di affiancamento | Responsabile di reparto | primo giorno | tutti tranne gli stagisti |
| Corso sicurezza, formazione generale (4 ore) | Ufficio del Personale, iscrizione | 30 giorni dall'ingresso | tutti tranne chi ha già l'attestato |
| Corso sicurezza, rischio basso (4 ore) | Ufficio del Personale, iscrizione | 60 giorni dall'ingresso | uffici e Commerciale |
| Corso sicurezza, rischio alto (12 ore, in aula) | Ufficio del Personale, iscrizione | prima di essere adibito alla mansione | Produzione e Logistica |
| Corso privacy (2 ore) | Ufficio del Personale, iscrizione | 30 giorni dall'ingresso | tutti |
| Corso carrelli elevatori (12 ore) | Ufficio del Personale, iscrizione | prima dell'uso del carrello | chi usa il carrello elevatore |
| Corso codice etico (1 ora) | Ufficio del Personale, iscrizione | 90 giorni dall'ingresso | tutti |
| Colloquio di verifica | Responsabile di reparto | fine della quarta settimana | tutti tranne gli stagisti |
| Scelta sulla destinazione del TFR | il nuovo assunto | 6 mesi dall'ingresso | tutti tranne gli stagisti |

- **Stagisti** (contratto `stage`): per loro valgono solo account, dotazioni
  e formazione (art. 2 della procedura), cioè sette attività: richiesta delle
  dotazioni, account e dotazioni, badge, i corsi generale, di rischio del
  reparto, privacy e codice etico.
- **Uffici**: Amministrazione, Personale e IT.
- **Documenti**: documento d'identità e codice fiscale, IBAN, modulo per le
  detrazioni; in più il permesso di soggiorno se previsto, gli attestati di
  sicurezza se ne ha, la patente se usa auto aziendali o il carrello.
- **Dotazioni**: uffici, portatile, cuffie con microfono e monitor;
  Commerciale, portatile e cellulare, più la carta di credito aziendale con
  trasferte frequenti; Produzione, le postazioni condivise di reparto;
  Logistica, le postazioni condivise e il terminale palmare; responsabili di
  reparto e capoturno, in più portatile e cellulare.

**Il formato nell'app.** Il titolo di un task è «Nome Cognome · ingresso
GG/MM/AAAA». Un'attività è una riga «Attività · chi la fa · entro
GG/MM/AAAA», o «· prima della mansione» e «· prima dell'uso del carrello»
quando la data non c'è.

- **Trello**: la board «Valtesa · nuovi ingressi», la lista «Ingressi», una
  card per persona con ruolo, reparto, sede, contratto e indirizzo di posta
  nella descrizione, e una checklist «Attività» con una riga per attività. Le
  attività di una card si leggono dalle sue checklist: la card da sola non le
  mostra.
- **Notion**: la pagina «Valtesa · nuovi ingressi», una sottopagina per
  persona con le stesse righe in testa e le attività come caselle da
  spuntare.
- **Airtable**: la base «Valtesa · nuovi ingressi», la tabella «Attività»,
  un record per attività con i campi Persona (il titolo del task),
  Attività, Chi, Scadenza e Fatto (una casella).

