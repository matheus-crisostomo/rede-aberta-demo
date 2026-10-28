'use strict';
const $ = id => document.getElementById(id);
let estado = null, pendente = false, confirmando = false;

async function requisitar(caminho, dados) {
  const resposta = await fetch(caminho, {cache: 'no-store', signal: AbortSignal.timeout(5000),
    ...(dados ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(dados)} : {})});
  const corpo = await resposta.json();
  if (resposta.status === 401) {
    estado = null;
    $('pareamento').hidden = false;
    $('controle').hidden = true;
  }
  if (!resposta.ok) throw new Error(corpo.erro || 'Não foi possível executar o comando.');
  return corpo;
}

function renderizar() {
  if (!estado) return;
  $('pareamento').hidden = true;
  $('controle').hidden = false;
  $('conexao').textContent = estado.conectada ? 'Conectado ao notebook' : 'Abra a apresentação no notebook para continuar.';
  $('numero').textContent = `Slide ${estado.total ? estado.indice + 1 : 0} de ${estado.total}`;
  $('titulo').textContent = estado.titulo;
  const travado = pendente || confirmando || !estado.conectada || estado.ocupado;
  $('voltar').disabled = travado || estado.indice === 0;
  $('avancar').disabled = travado || estado.indice >= estado.total - 1;
  $('paineis').hidden = estado.etapa === null;
  for (const tipo of ['dados', 'comparacao']) {
    const aberto = estado[tipo];
    $(tipo).textContent = `${aberto ? 'Ocultar' : 'Mostrar'} ${tipo === 'dados' ? 'MAC e mensagens' : 'HTTP × HTTPS'}`;
    $(tipo).setAttribute('aria-pressed', String(aberto));
    $(tipo).disabled = travado || (tipo === 'comparacao' && !aberto && !estado.tem_comparacao);
  }
  $('dica-comparacao').hidden = estado.tem_comparacao;
}

async function consultar() {
  try { estado = await requisitar('/api/estado'); renderizar(); }
  catch (erro) {
    $('conexao').textContent = estado ? 'Sem conexão. Confira o Wi-Fi e o notebook.' : 'Digite o código do notebook para conectar.';
    if (estado) {
      estado.conectada = false;
      renderizar();
      $('conexao').textContent = 'Sem conexão. Confira o Wi-Fi e o notebook.';
    }
  }
}

async function comando(acao, dados = {}) {
  if (pendente) return;
  pendente = true; renderizar(); $('erro').hidden = true;
  try { estado = await requisitar('/api/comando', {acao, ...dados}); }
  catch (erro) { $('erro').textContent = erro.message; $('erro').hidden = false; }
  finally { pendente = false; renderizar(); }
}

$('pareamento').onsubmit = async e => {
  e.preventDefault();
  if (pendente) return;
  pendente = true; $('erro').hidden = true;
  try {
    await requisitar('/api/parear', {codigo: $('codigo').value.trim()});
    $('codigo').value = ''; await consultar();
  } catch (erro) { $('erro').textContent = erro.message; $('erro').hidden = false; }
  finally { pendente = false; renderizar(); }
};
$('voltar').onclick = () => comando('anterior');
$('avancar').onclick = () => comando('proximo');
for (const tipo of ['dados', 'comparacao']) $(tipo).onclick = async () => {
  if (!estado || pendente || confirmando) return;
  const aberto = estado[tipo], revisao = estado.revisao;
  const acao = tipo === 'dados' ? (aberto ? 'ocultar' : 'revelar') : (aberto ? 'ocultar_comparacao' : 'mostrar_comparacao');
  if (!aberto) {
    confirmando = true; renderizar();
    $('confirmacao-texto').textContent = tipo === 'dados'
      ? 'IP, MAC e mensagens desta sessão ficarão visíveis ao público. Confirme que os participantes foram informados.'
      : 'As mensagens recebidas e os bytes HTTP/HTTPS ficarão visíveis ao público. Confirme que são envios de demonstração e que os participantes foram informados.';
    const dialogo = $('confirmacao'); dialogo.returnValue = '';
    const confirmou = await new Promise(resolve => {
      dialogo.addEventListener('close', () => resolve(dialogo.returnValue === 'confirmar'), {once: true});
      dialogo.showModal();
    });
    confirmando = false; renderizar();
    if (!confirmou) return;
  }
  await comando(acao, {confirmar: !aberto, revisao});
};
async function acompanhar() { await consultar(); setTimeout(acompanhar, 700); }
acompanhar();
