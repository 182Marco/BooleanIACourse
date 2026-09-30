from rimborsi import controlla


def test_pranzo_torino_nel_massimale():
    assert controlla({"voce": "pranzo", "citta": "Torino", "giorno": "2026-03-10", "importo": "18.50"})


def test_taxi_roma_fuori_massimale():
    assert not controlla({"voce": "taxi", "citta": "Roma", "giorno": "2026-05-02", "importo": "52.00"})


def test_cena_milano_prima_di_luglio():
    assert not controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-06-12", "importo": "50.00"})


def test_cena_milano_dopo_luglio():
    # Nota 1043: dal 01/07/2026 il massimale cena a Milano è 55 € (circolare 7/2026)
    assert controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-07-14", "importo": "52.00"})


def test_cena_milano_primo_luglio():
    assert controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-07-01", "importo": "55.00"})
    assert not controlla({"voce": "cena", "citta": "Milano", "giorno": "2026-06-30", "importo": "55.00"})


def test_hotel_milano_dopo_luglio():
    assert controlla({"voce": "hotel", "citta": "Milano", "giorno": "2026-08-03", "importo": "145.00"})
    assert not controlla({"voce": "hotel", "citta": "Milano", "giorno": "2026-06-03", "importo": "145.00"})
