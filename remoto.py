"""Controle de apresentação na LAN, separado do painel administrativo local."""

import hmac
import ipaddress
import json
import secrets
import socket
import threading
import time
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from vendor.qrcodegen import QrCode

BASE = Path(__file__).resolve().parent
CSP = ("default-src 'self'; frame-ancestors 'none'; base-uri 'none'; "
       "object-src 'none'; form-action 'self'")


class ErroRemoto(ValueError):
    pass


class Apresentacao:
    def __init__(self, controle):
        self.controle = controle
        self.lock = threading.RLock()
        self.slides = []
        self.indice = 0
        self.revisao = 0
        self.visto = 0
        self.servidor = None
        self.url = ""
        self.codigo = ""
        self.token = ""
        self.expira = 0
        self.telefone_visto = 0
        self.tentativas = []
        self.ultimo_comando = 0
        self.qr = b""

    def registrar(self, dados):
        slides = dados.get("slides")
        if (not isinstance(slides, list) or not 1 <= len(slides) <= 100 or
                any(not isinstance(s, dict) or not isinstance(s.get("titulo"), str) or
                    not 1 <= len(s["titulo"]) <= 140 or
                    (s.get("etapa") is not None and
                     (type(s["etapa"]) is not int or not 0 <= s["etapa"] < 7)) for s in slides)):
            raise ErroRemoto("Lista de slides inválida.")
        with self.lock:
            if not self.slides:
                self.slides = [{"titulo": s["titulo"], "etapa": s.get("etapa")} for s in slides]
            self.visto = time.monotonic()
        return self.estado()

    def estado(self, presenca=False):
        with self.lock:
            if presenca:
                self.visto = time.monotonic()
            slide = self.slides[self.indice] if self.slides else {}
            return {"indice": self.indice, "total": len(self.slides), "revisao": self.revisao,
                    "titulo": slide.get("titulo", "Abra a apresentação no notebook"),
                    "etapa": slide.get("etapa"), "conectada": bool(self.visto and time.monotonic() - self.visto < 8)}

    def mudar(self, indice):
        # A ordem das travas é sempre controle -> apresentação.
        with self.controle.lock, self.lock:
            if type(indice) is not int or not 0 <= indice < len(self.slides):
                raise ErroRemoto("Slide inválido.")
            if indice != self.indice:
                self.indice = indice
                self.revisao += 1
                self.controle.revelado = False
                self.controle.comparacao.telao = False
                etapa = self.slides[indice]["etapa"]
                if etapa is not None:
                    self.controle.etapa = etapa
        return self.estado()

    def endereco(self):
        if self.controle.ativo and self.controle.modo == "real":
            return self.controle.host_rede
        try:
            # Consulta apenas a rota local; não envia pacotes nem exige internet.
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as conexao:
                conexao.connect(("192.0.2.1", 9))
                host = conexao.getsockname()[0]
            if not ipaddress.ip_address(host).is_loopback:
                return host
        except OSError:
            pass
        raise ErroRemoto("Conecte o notebook a uma rede Wi-Fi ou inicie a rede da atividade e tente novamente.")

    def ativar(self, host=None, porta=8766):
        self.desativar()
        host = host or self.endereco()
        try:
            servidor = ServidorRemoto((host, porta), self)
        except OSError:
            try:
                servidor = ServidorRemoto((host, 0), self)
            except OSError as erro:
                raise ErroRemoto("Não foi possível abrir o controle nesta rede. Confira a conexão do notebook.") from erro
        with self.lock:
            self.servidor = servidor
            self.url = f"http://{host}:{servidor.server_port}"
            self.renovar()
            codigo = QrCode.encode_text(self.url + "/", QrCode.Ecc.MEDIUM)
            tamanho = codigo.get_size()
            caminho = " ".join(f"M{x+4},{y+4}h1v1h-1z" for y in range(tamanho)
                               for x in range(tamanho) if codigo.get_module(x, y))
            self.qr = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {tamanho+8} {tamanho+8}" '
                       f'shape-rendering="crispEdges"><rect width="100%" height="100%" fill="white"/>'
                       f'<path d="{caminho}" fill="black"/></svg>').encode()
        threading.Thread(target=servidor.serve_forever, daemon=True).start()

    def renovar(self):
        with self.lock:
            if not self.servidor:
                raise ErroRemoto("Ative o controle primeiro.")
            self.codigo = f"{secrets.randbelow(1000000):06d}"
            self.token = ""
            self.expira = time.monotonic() + 7200
            self.telefone_visto = 0
            self.tentativas = []

    def desativar(self):
        with self.lock:
            servidor = self.servidor
            self.servidor = None
            self.token = self.codigo = self.url = ""
            self.qr = b""
        if servidor:
            servidor.shutdown()
            servidor.server_close()

    def privado(self):
        with self.lock:
            return {"ativo": bool(self.servidor), "url": self.url,
                    "codigo": self.codigo if time.monotonic() < self.expira else "",
                    "pareado": bool(self.token and time.monotonic() < self.expira),
                    "conectado": bool(self.token and time.monotonic() < self.expira and
                                      time.monotonic() - self.telefone_visto < 8)}

    def parear(self, codigo):
        with self.lock:
            agora = time.monotonic()
            self.tentativas = [t for t in self.tentativas if agora - t < 60]
            if len(self.tentativas) >= 5:
                return 429, "Muitas tentativas. Aguarde um minuto ou gere novo código no notebook."
            if (not isinstance(codigo, str) or not codigo.isascii() or not self.codigo or
                    agora >= self.expira or not hmac.compare_digest(codigo, self.codigo)):
                self.tentativas.append(agora)
                return 401, "Código inválido ou já utilizado. Confira o painel do notebook."
            self.codigo = ""  # Um único telefone; outro pareamento exige novo código local.
            self.token = secrets.token_urlsafe(32)
            self.telefone_visto = agora
            return 200, self.token

    def autenticado(self, token):
        with self.lock:
            ok = bool(self.servidor and self.token and time.monotonic() < self.expira and
                      hmac.compare_digest(token, self.token))
            if ok:
                self.telefone_visto = time.monotonic()
            return ok

    def estado_telefone(self):
        # Não expor IP, MAC, mensagens, código de pareamento ou sessão administrativa.
        with self.controle.lock:
            estado = self.estado()
            estado.update(dados=self.controle.revelado, comparacao=self.controle.comparacao.telao,
                          tem_comparacao=bool(self.controle.comparacao.estado(detalhes=False)["total"]),
                          ocupado=self.controle.ocupado)
            return estado

    def comandar(self, dados):
        with self.controle.lock, self.lock:
            if not self.estado()["conectada"]:
                raise ErroRemoto("Abra a apresentação no notebook e mantenha a janela aberta.")
            if self.controle.ocupado:
                raise ErroRemoto("Aguarde a operação em andamento.")
            agora = time.monotonic()
            if agora - self.ultimo_comando < 0.15:
                raise ErroRemoto("Aguarde um instante antes do próximo toque.")
            acao = dados.get("acao")
            if acao in ("anterior", "proximo"):
                self.mudar(max(0, min(len(self.slides) - 1, self.indice + (1 if acao == "proximo" else -1))))
            elif acao in ("revelar", "ocultar", "mostrar_comparacao", "ocultar_comparacao"):
                if dados.get("revisao") != self.revisao or self.slides[self.indice]["etapa"] is None:
                    raise ErroRemoto("O slide mudou. Confira a apresentação antes de exibir os dados.")
                if acao in ("revelar", "mostrar_comparacao") and dados.get("confirmar") is not True:
                    raise ErroRemoto("Confirme a exibição dos dados no celular.")
                if acao == "mostrar_comparacao" and not self.controle.comparacao.estado(detalhes=False)["total"]:
                    raise ErroRemoto("Faça primeiro um envio HTTP/HTTPS pelo notebook.")
                # Ações curtas de exibição executadas sob a mesma trava da navegação.
                self.controle._acao(acao, dados)
            else:
                raise ErroRemoto("Ação não permitida no controle do celular.")
            self.ultimo_comando = agora
        return self.estado_telefone()


class ServidorRemoto(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, endereco, apresentacao):
        super().__init__(endereco, HandlerRemoto)
        self.apresentacao = apresentacao
        self.origem = f"http://{self.server_address[0]}:{self.server_port}"


class HandlerRemoto(BaseHTTPRequestHandler):
    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, *args):
        pass

    def enviar(self, status, corpo, tipo="application/json; charset=utf-8", token=None):
        corpo = corpo if isinstance(corpo, bytes) else json.dumps(corpo, ensure_ascii=False).encode()
        self.send_response(status)
        for nome, valor in {"Content-Type": tipo, "Content-Length": str(len(corpo)),
                            "Cache-Control": "no-store", "Content-Security-Policy": CSP,
                            "X-Content-Type-Options": "nosniff", "Referrer-Policy": "no-referrer"}.items():
            self.send_header(nome, valor)
        if token:
            self.send_header("Set-Cookie", f"rede_remoto={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=7200")
        self.end_headers()
        self.wfile.write(corpo)

    def host_valido(self):
        return self.headers.get("Host") == self.server.origem.removeprefix("http://")

    def autenticado(self):
        try:
            item = SimpleCookie(self.headers.get("Cookie", "")).get("rede_remoto")
            return bool(item and self.server.apresentacao.autenticado(item.value))
        except (CookieError, ValueError, TypeError):
            return False

    def do_GET(self):
        if not self.host_valido():
            self.enviar(403, {"erro": "Endereço inválido."})
            return
        path = urlsplit(self.path).path
        arquivos = {"/": ("remoto.html", "text/html"), "/remoto.js": ("remoto.js", "text/javascript"),
                    "/remoto.css": ("remoto.css", "text/css")}
        if path in arquivos:
            arquivo, tipo = arquivos[path]
            self.enviar(200, (BASE / "interface" / arquivo).read_bytes(), tipo + "; charset=utf-8")
        elif path == "/api/estado":
            if not self.autenticado():
                self.enviar(401, {"erro": "Digite o código exibido no notebook."})
            else:
                self.enviar(200, self.server.apresentacao.estado_telefone())
        else:
            self.enviar(404, {"erro": "Recurso não encontrado."})

    def do_POST(self):
        if not self.host_valido() or self.headers.get("Origin") != self.server.origem:
            self.enviar(403, {"erro": "Origem não autorizada."})
            return
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            self.enviar(415, {"erro": "Envie JSON."})
            return
        try:
            tamanho = int(self.headers.get("Content-Length", "0"))
            if not 0 < tamanho <= 1024:
                raise ValueError()
            dados = json.loads(self.rfile.read(tamanho).decode())
            if not isinstance(dados, dict):
                raise ValueError()
        except (ValueError, UnicodeDecodeError):
            self.enviar(400, {"erro": "Requisição inválida."})
            return
        path = urlsplit(self.path).path
        if path == "/api/parear":
            status, valor = self.server.apresentacao.parear(dados.get("codigo"))
            self.enviar(status, {"ok": True} if status == 200 else {"erro": valor},
                        token=valor if status == 200 else None)
        elif not self.autenticado():
            self.enviar(401, {"erro": "Sessão encerrada. Gere novo código no notebook."})
        elif path == "/api/comando":
            try:
                self.enviar(200, self.server.apresentacao.comandar(dados))
            except ErroRemoto as erro:
                self.enviar(409, {"erro": str(erro)})
        else:
            self.enviar(404, {"erro": "Recurso não encontrado."})
