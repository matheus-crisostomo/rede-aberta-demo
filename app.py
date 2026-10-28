#!/usr/bin/env python3
"""Painel local da dinâmica. Abra pelo atalho ou execute python3 app.py."""

import argparse
import fcntl
import hmac
import json
import os
import secrets
import signal
import threading
import time
import webbrowser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from controle import Controle, ErroOperacao


BASE = Path(__file__).resolve().parent
CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; "
       "frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
# O telão aparece dentro da apresentação, e a apresentação aparece dentro do painel da equipe.
CSP_TELAO = CSP.replace("frame-ancestors 'none'", "frame-ancestors 'self'")
# A apresentação é um arquivo único com estilos e scripts embutidos e a fonte do Google Fonts.
# Ela não exibe dados de participantes: na demonstração mostra o /telao, que segue com a política estrita.
CSP_APRESENTACAO = ("default-src 'self'; script-src 'self' 'unsafe-inline'; "
                    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; "
                    "img-src 'self' data:; frame-src 'self'; connect-src 'self'; frame-ancestors 'self'; "
                    "base-uri 'none'; form-action 'none'")


class ServidorApp(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, endereco, controle):
        super().__init__(endereco, HandlerApp)
        self.controle = controle
        self.token = secrets.token_urlsafe(32)
        self.porta = self.server_address[1]
        self.origem = f"http://127.0.0.1:{self.porta}"


class HandlerApp(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, format, *args):
        pass

    def enviar(self, status, conteudo, tipo="application/json; charset=utf-8", cookie=False, csp=CSP):
        corpo = conteudo if isinstance(conteudo, bytes) else json.dumps(conteudo, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", csp)
        if cookie:
            self.send_header("Set-Cookie", f"rede_sessao={self.server.token}; HttpOnly; SameSite=Strict; Path=/")
        self.end_headers()
        self.wfile.write(corpo)

    def host_valido(self):
        return self.headers.get("Host") == f"127.0.0.1:{self.server.porta}"

    def autenticado(self):
        try:
            cookie = SimpleCookie(self.headers.get("Cookie", ""))
            item = cookie.get("rede_sessao")
            return bool(item and hmac.compare_digest(item.value, self.server.token))
        except Exception:
            return False

    def do_GET(self):
        if not self.host_valido():
            self.enviar(403, {"erro": "Endereço de acesso inválido."})
            return
        path = urlsplit(self.path).path
        if path == "/health":
            self.enviar(200, {"app": "rede-aberta", "versao": 1})
            return
        if path.startswith("/api/"):
            if not self.autenticado():
                self.enviar(401, {"erro": "Abra o aplicativo pelo atalho para iniciar sua sessão."})
                return
            if path in ("/api/estado", "/api/telao"):
                self.enviar(200, self.server.controle.estado(publico=path.endswith("telao")))
            else:
                self.enviar(404, {"erro": "Recurso não encontrado."})
            return
        if path == "/apresentacao":
            self.enviar(200, (BASE / "docs" / "apresentacao_completa.html").read_bytes(),
                        "text/html; charset=utf-8", csp=CSP_APRESENTACAO)
            return
        arquivos = {"/": ("index.html", "text/html; charset=utf-8"),
                    "/telao": ("telao.html", "text/html; charset=utf-8"),
                    "/estilo.css": ("estilo.css", "text/css; charset=utf-8"),
                    "/telao.css": ("telao.css", "text/css; charset=utf-8"),
                    "/app.js": ("app.js", "text/javascript; charset=utf-8"),
                    "/conteudo.js": ("conteudo.js", "text/javascript; charset=utf-8"),
                    "/icone.svg": ("icone.svg", "image/svg+xml")}
        if path not in arquivos:
            self.enviar(404, {"erro": "Recurso não encontrado."})
            return
        nome, tipo = arquivos[path]
        self.enviar(200, (BASE / "interface" / nome).read_bytes(), tipo, csp=CSP_TELAO if path == "/telao" else CSP)

    def do_POST(self):
        if not self.host_valido() or self.headers.get("Origin") != self.server.origem:
            self.enviar(403, {"erro": "Origem não autorizada."})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.enviar(415, {"erro": "Envie JSON."})
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if not 0 < tamanho <= 4096:
                raise ValueError()
            dados = json.loads(self.rfile.read(tamanho).decode("utf-8"))
            if not isinstance(dados, dict):
                raise ValueError()
        except (ValueError, UnicodeDecodeError):
            self.enviar(400, {"erro": "Requisição inválida."})
            return
        path = urlsplit(self.path).path
        if path == "/api/sessao":
            token = dados.get("token")
            if not isinstance(token, str) or not hmac.compare_digest(token, self.server.token):
                self.enviar(401, {"erro": "Sessão inválida. Reabra pelo atalho."})
                return
            self.enviar(200, {"ok": True}, cookie=True)
            return
        if not self.autenticado():
            self.enviar(401, {"erro": "Sessão encerrada. Reabra o aplicativo pelo atalho."})
            return
        if path != "/api/acao":
            self.enviar(404, {"erro": "Recurso não encontrado."})
            return
        try:
            self.server.controle.solicitar(dados.get("acao", ""), dados)
        except (ErroOperacao, TypeError) as erro:
            self.enviar(409, {"erro": str(erro)})
            return
        self.enviar(202, {"ok": True})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sem-navegador", action="store_true")
    args = parser.parse_args()
    pasta = BASE / "dados"
    pasta.mkdir(exist_ok=True, mode=0o700)
    trava = (pasta / "app.lock").open("a+")
    try:
        fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        # Um segundo clique abre a instância existente, sem criar outro servidor.
        try:
            sessao = json.loads((pasta / "app.json").read_text())
            webbrowser.open(f"http://127.0.0.1:{sessao['porta']}/#sessao={sessao['token']}")
        except (OSError, ValueError, KeyError):
            print("O app está iniciando. Tente abrir novamente em alguns segundos.")
        return
    controle = Controle(BASE)
    try:
        servidor = ServidorApp(("127.0.0.1", 8765), controle)
    except OSError:
        # Se outro programa ocupa 8765, o atalho usa uma porta local disponível.
        servidor = ServidorApp(("127.0.0.1", 0), controle)
    configuracao = pasta / "app.json"
    descritor = os.open(configuracao, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(descritor, "w") as arquivo:
        json.dump({"porta": servidor.porta, "token": servidor.token}, arquivo)
    url = f"{servidor.origem}/#sessao={servidor.token}"
    encerrar = threading.Event()
    for sinal in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sinal, lambda *_: encerrar.set())
    thread = threading.Thread(target=servidor.serve_forever, daemon=True)
    thread.start()
    if not args.sem_navegador:
        webbrowser.open(url)
    print(f"Painel pronto em {servidor.origem}. Use o atalho para abrir a sessão.", flush=True)
    proxima_consulta = 0
    try:
        while not encerrar.wait(1):
            if controle.ativo and controle.modo == "real" and time.monotonic() >= proxima_consulta:
                try:
                    controle.solicitar("atualizar", {})
                except ErroOperacao:
                    pass
                proxima_consulta = time.monotonic() + 5
    finally:
        with controle.lock:
            controle.fechando = True
        if controle.worker:
            controle.worker.join()
        try:
            controle.encerrar()
        except Exception as erro:
            print(f"Limpeza pendente: {erro}", flush=True)
        servidor.shutdown()
        servidor.server_close()
        configuracao.unlink(missing_ok=True)
        trava.close()


if __name__ == "__main__":
    main()
