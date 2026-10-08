# Spiegazione — Modulo 4 · Lezione 3

Le risposte le scrivete voi, una sezione per obiettivo.

## 1. Orientarsi nel progetto

Per ogni risposta, il file e la riga che avete aperto voi.

- Le righe di `MAPPA.md` che avete controllato, e cosa avete corretto: i
  due modelli (`assistente.py:27`, `aikit/embeddings.py:27`), chi chiama
  `vectorstore` (`assistente.py:45`, `indicizza.py:46-47`), la sola lettura
  di `query_db` (`assistente.py:67`), il `.env` caricato (`assistente.py:19`:
  la mappa diceva `.env.example`, corretto), il materiale da non modificare
  (`AGENTS.md`: la mappa ci metteva anche `SPIEGAZIONE.md`, corretto).

1. Quali modelli chiama il progetto, e dove si scelgono?
   Due. `gpt-5.6-luna` per l'agente: `assistente.py:27` (`MODELLO`), passato
   all'`Agent` a riga 93. `text-embedding-3-small` per gli embedding:
   `aikit/embeddings.py:27`; lo usano `indicizza.py:47` per i chunk e
   `vectorstore.search` (`aikit/vectorstore.py:68`) per la domanda, a ogni
   `cerca_documenti`. `aikit/llm_client.py:35` ha `gpt-4.1-mini` come
   default, ma nel progetto nessuno usa `LLMClient`; `aikit/embeddings.py:28`
   ha `all-MiniLM-L6-v2` per il backend locale, che nessuno sceglie.
2. Da dove vengono i passaggi che restituisce `cerca_documenti`?
   Dalla collection `valtesa` in `indice/` (`assistente.py:24` e `45`,
   `aikit/vectorstore.py:29`). La costruisce `indicizza.py`: legge i sei
   documenti di `ufficio/`, li pulisce (riga 38, con `aikit/clean.py`), li
   divide in chunk da 500 caratteri (riga 39) e salva gli embedding (riga
   47). Sono i documenti com'erano all'ultimo `python indicizza.py`.
3. Cosa riceve il modello quando un tool fallisce, per tutti e due i
   tool?
   `query_db` intercetta l'errore da sé (`assistente.py:72-73`): con
   `SELECT data FROM note_spese` il modello riceve `Errore: no such column:
   data`. `cerca_documenti` non ha un `try`: l'errore lo trasforma in testo
   l'SDK, «An error occurred while running the tool. Please try again.
   Error: …», per esempio con la chiave sbagliata «… Error: Error code:
   401 - … Incorrect API key provided …». Con una collection che non
   c'è (o senza indice) non fallisce niente: `apri_collection()` usa
   `get_or_create_collection` (`aikit/vectorstore.py:35`), crea una
   collection vuota e il tool restituisce una stringa vuota.

## 2. La nota 1441

- I numeri di partenza (l'ultima riga, le note fuori massimale che non
  sono hotel, l'ultima riga con l'export di ottobre): 293; 188; 190 note,
  34 fuori massimale, 16 con massimale mancante.
- Atteso e ottenuto, nell'output di `python rimborsi.py`: atteso `ok` (390 €
  per tre notti sono 130 € a notte, il massimale di Roma è 140 €);
  ottenuto `FUORI MASSIMALE (140.00)`.
- La causa, in due righe: `controlla()` e `main()` confrontano l'importo
  del soggiorno con il massimale di una notte; la colonna `notti` c'è, ma
  il programma non la legge. La policy dice che il massimale dell'albergo è
  per notte e che l'albergo sta su una riga per soggiorno (art. 2 e 6).
- Come avete verificato la correzione: il test `test_hotel_roma_tre_notti`
  prima falliva e ora passa, gli altri test sono quelli di prima (in `git
  diff main tests/` solo righe aggiunte); `pytest` verde; l'ultima riga
  passa da 293 a 267; le note fuori massimale che non sono hotel restano
  188; la 1441 ora è `ok`; l'export di ottobre dà ancora 190, 34, 16.
  `AGENTS.md` aggiornato a 267.

## 3. Il report mensile

- I criteri del ticket, come li avete verificati: 1, `ls output`; 2-3, i
  numeri nella pagina contro il ticket (164, 8.963,53 €, Brescia 5.141,74 €,
  Padova 3.821,79 €, le voci); 4, le 20 righe della tabella, senza la 1441;
  5, `python report.py 2026-12`; 6, `grep -cE "https?://"` dà 0; 7, `git status
  --short dati/` vuoto, 20 passed.
- Una funzione del diff, spiegata riga per riga: `riepilogo(note,
  sede_di)`. Per ogni nota somma l'importo alla sua sede (cercata per
  `dipendente_id`, perché ci sono due Sara Conti) e alla sua voce; se
  `controlla()` dice che è fuori massimale, chiede a `limite_nota()` il
  massimale applicato e calcola l'eccedenza. Restituisce un dizionario con
  i numeri che `pagina()` mette nell'HTML.
- Cosa non avete verificato: la pagina l'abbiamo aperta nel browser con la
  rete, non senza; le proporzioni del grafico solo a occhio; un mese
  scritto male (`2026-7`) dà una pagina con zero note, senza errore; le
  note di una città senza massimale (nessuna a luglio) fermerebbero il
  report con `KeyError`.
