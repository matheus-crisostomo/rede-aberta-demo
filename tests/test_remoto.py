"""Controle limitado ao celular, sem alterar a rede física."""

import http.client
import json
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from app import ServidorApp
from controle import Controle
from remoto import Apresentacao, ErroRemoto


class TestRemoto(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.controle = Controle(self.temp.name)
        self.app = ServidorApp(('127.0.0.1', 0), self.controle)
        self.thread = threading.Thread(target=self.app.serve_forever, daemon=True)
        self.thread.start()
        self.remoto = self.app.apresentacao
        self.remoto.registrar({'slides': [{'titulo': 'Capa'}, {'titulo': 'Wi-Fi aberto', 'etapa': 0},
                                         {'titulo': 'Encerramento'}]})
        self.remoto.ativar('127.0.0.1', 0)
        self.servidor = self.remoto.servidor
        self.cookie = ''

    def tearDown(self):
        self.app.shutdown()
        self.app.server_close()
        self.thread.join(2)
        self.controle.encerrar()
        self.temp.cleanup()

    def pedir(self, path, dados=None, headers=None, local=False):
        servidor = self.app if local else self.servidor
        cabecalhos = {'Origin': servidor.origem, 'Content-Type': 'application/json',
                      'Cookie': f'rede_sessao={self.app.token}' if local else self.cookie}
        cabecalhos.update(headers or {})
        conexao = http.client.HTTPConnection('127.0.0.1', servidor.server_port, timeout=3)
        conexao.request('GET' if dados is None else 'POST', path,
                       None if dados is None else json.dumps(dados), cabecalhos)
        resposta = conexao.getresponse()
        resultado = resposta.status, resposta.read(), dict(resposta.getheaders())
        conexao.close()
        return resultado

    def parear(self):
        codigo = self.remoto.codigo
        status, _, headers = self.pedir('/api/parear', {'codigo': codigo})
        self.assertEqual(status, 200)
        self.cookie = headers['Set-Cookie'].split(';')[0]
        return codigo

    def test_pareamento_uso_unico_rotacao_e_expiracao(self):
        self.assertEqual(self.pedir('/api/estado')[0], 401)
        codigo = self.parear()
        self.assertEqual(self.pedir('/api/parear', {'codigo': codigo})[0], 401)
        self.assertEqual(self.pedir('/api/estado')[0], 200)
        self.remoto.renovar()
        self.assertEqual(self.pedir('/api/estado')[0], 401)
        self.parear()
        self.remoto.expira = time.monotonic() - 1
        self.assertEqual(self.pedir('/api/estado')[0], 401)

    def test_limita_tentativas_e_recusa_entrada_invalida(self):
        for valor in (None, [], 'áááááá', 'x', '1234567'):
            self.assertEqual(self.pedir('/api/parear', {'codigo': valor})[0], 401)
        self.assertEqual(self.pedir('/api/parear', {'codigo': self.remoto.codigo})[0], 429)
        self.remoto.renovar()
        self.parear()
        self.assertEqual(self.pedir('/api/comando', [1])[0], 400)

    def test_recusa_origens_hosts_e_acoes_administrativas(self):
        self.parear()
        self.assertEqual(self.pedir('/api/estado', headers={'Host': 'evil.example'})[0], 403)
        self.assertEqual(self.pedir('/api/comando', {'acao': 'proximo'}, {'Origin': 'http://evil.example'})[0], 403)
        for acao in ('iniciar', 'encerrar', 'excluir', 'enviar_notebook', 'executar', []):
            self.assertEqual(self.pedir('/api/comando', {'acao': acao})[0], 409)
        for caminho in ('/api/acao', '/api/telao', '/apresentacao', '/dados/app.json', '/registros.jsonl', '/../app.py'):
            self.assertEqual(self.pedir(caminho)[0], 404)
        self.assertEqual(self.app.server_address[0], '127.0.0.1')

    def test_navegacao_limites_e_confirmacao_vinculada_ao_slide(self):
        self.parear()
        self.controle.iniciar({'modo': 'ensaio'})
        self.controle._acao('simular_envio', {})
        self.assertEqual(self.pedir('/api/comando', {'acao': 'proximo'})[0], 200)
        self.assertEqual(self.remoto.indice, 1)
        self.assertEqual(self.controle.etapa, 0)
        self.remoto.ultimo_comando = 0
        self.assertEqual(self.pedir('/api/comando', {'acao': 'revelar', 'revisao': 1})[0], 409)
        self.assertFalse(self.controle.revelado)
        self.assertEqual(self.pedir('/api/comando', {'acao': 'revelar', 'revisao': 1, 'confirmar': True})[0], 200)
        self.assertTrue(self.controle.revelado)
        estado = json.loads(self.pedir('/api/estado')[1])
        for segredo in ('vizinhos', 'registros', 'codigo', 'token', 'url', 'envios'):
            self.assertNotIn(segredo, estado)
        self.remoto.mudar(2)
        self.assertFalse(self.controle.revelado)
        self.remoto.ultimo_comando = 0
        self.assertEqual(self.pedir('/api/comando', {'acao': 'revelar', 'revisao': 1, 'confirmar': True})[0], 409)
        self.assertEqual(self.pedir('/api/comando', {'acao': 'proximo'})[0], 200)
        self.assertEqual(self.remoto.indice, 2)
        self.remoto.visto = time.monotonic() - 10
        self.remoto.ultimo_comando = 0
        self.assertEqual(self.pedir('/api/comando', {'acao': 'anterior'})[0], 409)

    def test_api_local_protege_codigo_e_qr(self):
        self.assertEqual(self.pedir('/api/remoto', {'acao': 'desativar'}, local=True, headers={'Cookie': ''})[0], 401)
        estado = json.loads(self.pedir('/api/estado', local=True)[1])
        self.assertEqual(estado['remoto']['codigo'], self.remoto.codigo)
        self.assertNotIn('remoto', json.loads(self.pedir('/api/telao', local=True)[1]))
        self.assertEqual(self.pedir('/api/remoto/qr', local=True, headers={'Cookie': ''})[0], 401)
        status, svg, _ = self.pedir('/api/remoto/qr', local=True)
        self.assertEqual(status, 200)
        self.assertIn(b'<svg', svg)
        self.assertNotIn(self.remoto.codigo.encode(), svg)
        self.assertEqual(self.pedir('/api/apresentacao', {'indice': True}, local=True)[0], 409)
        self.assertEqual(self.pedir('/api/apresentacao', {'indice': 2}, local=True)[0], 200)
        self.assertEqual(self.remoto.indice, 2)
        self.assertEqual(self.pedir('/api/remoto', {'acao': 'desativar'}, local=True)[0], 200)
        self.assertFalse(self.remoto.autenticado(self.cookie.removeprefix('rede_remoto=')))

    def test_configuracao_local_e_catalogo_validado(self):
        # A escolha automática de outra porta do painel deve continuar funcionando.
        with self.assertRaises(OSError):
            ServidorApp(('127.0.0.1', self.app.server_port), self.controle)
        for slides in (None, [], [None], [{'titulo': 'a', 'etapa': True}], [{'titulo': 'a' * 141}]):
            with self.assertRaises(ErroRemoto):
                Apresentacao(self.controle).registrar({'slides': slides})
        self.controle.ativo = True
        self.controle.modo = 'real'
        self.controle.host_rede = '192.168.2.1'
        self.assertEqual(self.remoto.endereco(), '192.168.2.1')
        self.controle.ativo = False
        with patch('remoto.socket.socket', side_effect=OSError):
            with self.assertRaises(ErroRemoto):
                self.remoto.endereco()


if __name__ == '__main__':
    unittest.main()
