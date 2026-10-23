"""login_mcp.py — il login OAuth a un server MCP remoto, come lo fanno Claude Code e il connettore di claude.ai.

La prima volta: il programma si registra presso il fornitore dell'app (registrazione dinamica
del client), apre il browser sulla pagina di login, riceve il codice su
http://localhost:8765/callback e salva il token in .mcp-token/<app>.json. Le volte dopo usa il
token salvato, e lo rinnova quando scade. Il token è una chiave del vostro account: la cartella
.mcp-token/ è nel .gitignore, e non va copiata altrove.

Lo usano assistente.py e il login da solo:  python assistente.py --app trello --login  (lo rifà sempre)
"""
import asyncio
import json
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx2
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.shared.auth import (AuthorizationCodeResult, OAuthClientInformationFull,
                             OAuthClientMetadata, OAuthToken)

CARTELLA_TOKEN = Path(__file__).parent / ".mcp-token"
PORTA = 8765
RITORNO = f"http://localhost:{PORTA}/callback"


class TokenInFile(TokenStorage):
    """Il token e la registrazione del client in un file JSON, leggibile solo da voi."""

    def __init__(self, percorso):
        self.percorso = Path(percorso)

    def _leggi(self):
        return json.loads(self.percorso.read_text()) if self.percorso.exists() else {}

    def _scrivi(self, chiave, valore):
        dati = self._leggi()
        dati[chiave] = valore.model_dump(mode="json", exclude_none=True)
        self.percorso.parent.mkdir(exist_ok=True)
        self.percorso.write_text(json.dumps(dati, indent=2))
        self.percorso.chmod(0o600)

    async def get_tokens(self):
        dati = self._leggi().get("token")
        return OAuthToken(**dati) if dati else None

    async def set_tokens(self, tokens):
        self._scrivi("token", tokens)

    async def get_client_info(self):
        dati = self._leggi().get("client")
        return OAuthClientInformationFull(**dati) if dati else None

    async def set_client_info(self, client_info):
        self._scrivi("client", client_info)


async def apri_browser(url):
    print(f"\nApri questo indirizzo nel browser e fai il login:\n{url}\n", flush=True)
    webbrowser.open(url)


async def aspetta_ritorno():
    """Un server web minimo su localhost: aspetta che il browser torni con il codice del login."""
    loop = asyncio.get_running_loop()
    risultato = loop.create_future()

    class Ritorno(BaseHTTPRequestHandler):
        def do_GET(self):
            parametri = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            if "code" in parametri:
                self.wfile.write("Login fatto: puoi chiudere questa finestra.".encode())
            else:                                       # consenso negato, o un errore del fornitore
                self.wfile.write(f"Login non riuscito: {parametri.get('error', 'nessun codice')}.".encode())
            if not risultato.done():
                loop.call_soon_threadsafe(risultato.set_result, parametri)

        def log_message(self, *args):                   # niente righe di log nel terminale
            pass

    try:
        server = HTTPServer(("127.0.0.1", PORTA), Ritorno)
    except OSError:
        raise SystemExit(f"La porta {PORTA} è occupata, forse da un altro login aperto: chiudetelo e riprovate.")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        parametri = await risultato
    finally:
        server.shutdown()
    if "code" not in parametri:
        raise SystemExit(f"Login non riuscito: {parametri.get('error_description') or parametri.get('error', 'nessun codice')}.")
    return AuthorizationCodeResult(code=parametri["code"], state=parametri.get("state"), iss=parametri.get("iss"))


def file_token(app):
    return CARTELLA_TOKEN / f"{app}.json"


def autenticazione(app, url):
    """L'oggetto da passare come auth a MCPServerStreamableHttp: aggiunge il token a ogni richiesta,
    e se il server risponde 401 fa il login."""
    return OAuthClientProvider(
        server_url=url,
        client_metadata=OAuthClientMetadata(client_name="Assistente Valtesa", redirect_uris=[RITORNO],
                                            grant_types=["authorization_code", "refresh_token"],
                                            response_types=["code"], token_endpoint_auth_method="none"),
        storage=TokenInFile(file_token(app)),
        redirect_handler=apri_browser,
        callback_handler=aspetta_ritorno,
    )


async def fai_login(app, url, di_nuovo=False):
    """Solo il login, prima di aprire la sessione MCP. Dentro la sessione la prima richiesta ha un
    timeout di circa un minuto, e scadrebbe mentre siete nel browser. Se il token c'è già, niente;
    con di_nuovo=True il token salvato si butta e il login si rifà (un token revocato, un altro account)."""
    if di_nuovo:
        file_token(app).unlink(missing_ok=True)
    if await TokenInFile(file_token(app)).get_tokens():
        return
    richiesta = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                 "params": {"protocolVersion": "2025-11-25", "capabilities": {},
                            "clientInfo": {"name": "login", "version": "1"}}}
    async with httpx2.AsyncClient(auth=autenticazione(app, url), timeout=900) as client:
        await client.post(url, json=richiesta, headers={"Accept": "application/json, text/event-stream"})
