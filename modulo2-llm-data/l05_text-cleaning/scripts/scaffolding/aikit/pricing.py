"""Prezzi dei modelli e calcolo del costo (riusa la logica costi di Modulo 2 · Lezione 2).

I prezzi sono in dollari per 1 milione di token. ATTENZIONE: cambiano nel tempo,
vanno verificati sulla pagina ufficiale. Rilevazione: giugno 2026, fonte
openai.com/api/pricing.
"""

# prezzo input / output in USD per 1.000.000 di token
PRICING = {
    # "nome-modello": {"input": prezzo_input, "output": prezzo_output},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1":      {"input": 2.00, "output": 8.00},
}


def cost_usd(model, input_tokens, output_tokens):
    """Costo in dollari di una chiamata, dati i token consumati."""
    # prendi i prezzi del modello dal dizionario
    prezzi = PRICING[model]
    # calcola il costo dell'input (token / 1M * prezzo)
    costo_input = input_tokens / 1_000_000 * prezzi["input"]
    # calcola il costo dell'output (token / 1M * prezzo)
    costo_output = output_tokens / 1_000_000 * prezzi["output"]
    # restituisci la somma
    return costo_input + costo_output
