'use strict';
const $ = (id) => document.getElementById(id);
const telao = document.body.classList.contains('telao');
let estado = null;
let ultimoConteudo = '';
let pendente = false;
let selecionouModo = false;
let selecionouInterface = false;
let ultimaOperacao = null;
let proximaConsulta = null;

async function requisitar(url, dados) {
  const opcoes = dados ? {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(dados)} : {};
  const resposta = await fetch(url, {...opcoes, cache: 'no-store', signal: AbortSignal.timeout(10000)});
  const conteudo = await resposta.json();
  if (!resposta.ok) throw new Error(conteudo.erro || 'Não foi possível concluir a operação.');
  return conteudo;
}

async function confirmar(titulo, texto) {
  const dialogo = $('confirmacao');
  $('confirmacao-titulo').textContent = titulo;
  $('confirmacao-texto').textContent = texto;
  return new Promise((resolve) => {
    dialogo.addEventListener('close', () => resolve(dialogo.returnValue === 'confirmar'), {once: true});
    dialogo.showModal();
  });
}

async function acao(nome, dados = {}) {
  if (pendente || estado?.ocupado) return;
  pendente = true;
  atualizarBotoes();
  try {
    await requisitar('/api/acao', {acao: nome, ...dados});
    ultimaOperacao = nome;
    await consultar();
  } catch (erro) {
    $('erro').textContent = erro.message;
    $('erro').hidden = false;
  } finally {
    pendente = false;
    atualizarBotoes();
  }
}

function montarTabela(id, linhas, campos, mensagem, limite = 100) {
  const tabela = $(id);
  if (!tabela) return;
  tabela.replaceChildren();
  if (!linhas?.length) {
    const linha = tabela.insertRow();
    const celula = linha.insertCell();
    celula.colSpan = campos.length;
    celula.className = 'vazio';
    celula.textContent = mensagem;
    return;
  }
  const ultimas = linhas.slice(-limite);
  for (const item of ultimas) {
    const linha = tabela.insertRow();
    for (const campo of campos) {
      const celula = linha.insertCell();
      let valor = String(item[campo] || '—');
      if (campo === 'horario_utc' && item[campo]) valor = valor.replace('T', ' ').slice(0, 19);
      // Limita texto na projeção para preservar o espaço dos cinco registros.
      if (telao && campo === 'navegador') valor = valor.slice(0, 55);
      if (telao && campo === 'horario_utc') valor = String(item[campo]).slice(11, 19);
      if (telao) {
        const texto = document.createElement('span');
        texto.textContent = valor;
        celula.append(texto);
      } else celula.textContent = valor;
    }
  }
}

function atualizarBotoes() {
  if (telao || !estado) return;
  const travado = pendente || estado.ocupado;
  document.querySelectorAll('[data-acao], #iniciar, #anterior, #proximo, #revelar, #excluir, #enviar-notebook, #projetar-comparacao, #excluir-comparacao, #etapas button').forEach((b) => { b.disabled = travado; });
  $('configuracao').disabled = travado || estado.ativo || estado.limpeza_pendente;
  $('iniciar').disabled = travado || estado.ativo || estado.limpeza_pendente;
  $('encerrar').disabled = travado || (!estado.ativo && !estado.limpeza_pendente && !estado.comparacao.ativa);
  $('anterior').disabled = travado || estado.etapa === 0;
  $('proximo').disabled = travado || estado.etapa === ETAPAS.length - 1;
  $('excluir').disabled = travado || estado.ativo || estado.limpeza_pendente || (!estado.envios && !estado.arquivo && !estado.observados);
  $('atualizar').disabled = travado || !estado.ativo || estado.modo !== 'real';
  document.querySelectorAll('[data-acao^="simular"]').forEach((b) => { b.disabled = travado || !estado.ativo || estado.modo !== 'ensaio'; });
  $('abrir-pagina').disabled = !estado.servidor_ativo;
  $('preparar-comparacao').disabled = travado || estado.comparacao.ativa || estado.limpeza_pendente;
  $('encerrar-comparacao').disabled = travado || !estado.comparacao.ativa;
  $('enviar-notebook').disabled = travado || !estado.comparacao.ativa;
  $('mensagem-notebook').disabled = travado || !estado.comparacao.ativa;
  $('excluir-comparacao').disabled = travado || estado.comparacao.ativa || !estado.comparacao.fingerprint;
  $('projetar-comparacao').disabled = travado || !estado.comparacao.total;
  $('iniciar').textContent = travado && ultimaOperacao === 'iniciar' ? 'Iniciando…' : ($('modo').value === 'real' ? 'Iniciar demonstração real' : 'Iniciar ensaio');
}

function renderizarEquipe() {
  const e = estado;
  $('badge').textContent = e.modo === 'ensaio' ? 'Ensaio' : 'Demonstração real';
  $('badge').classList.toggle('real', e.modo === 'real');
  $('mensagem').textContent = e.ocupado ? 'Operação em andamento. Se aparecer uma janela do sistema, autorize para continuar.' : e.mensagem;
  $('erro').textContent = e.erro;
  $('erro').hidden = !e.erro;
  if (e.ativo || !selecionouModo) $('modo').value = e.modo;
  const seletor = $('interface');
  const atual = selecionouInterface ? seletor.value : e.interface;
  const opcoes = JSON.stringify(e.interfaces);
  if (seletor.dataset.opcoes !== opcoes) {
    seletor.replaceChildren();
    if (!e.interfaces.length) seletor.add(new Option('Verifique o equipamento', ''));
    e.interfaces.forEach((nome) => seletor.add(new Option(nome, nome)));
    seletor.dataset.opcoes = opcoes;
  }
  if (e.interfaces.includes(atual)) seletor.value = atual;
  $('status-rede').textContent = e.limpeza_pendente && !e.ativo ? 'Limpeza pendente' : (e.ativo ? (e.modo === 'ensaio' ? 'Ensaio ativo' : 'Rede ativa') : 'Parada');
  $('status-servidor').textContent = e.modo === 'ensaio' ? 'Simulada' : (e.servidor_ativo ? 'No ar' : 'Desligada');
  $('simulacao').hidden = $('modo').value !== 'ensaio';
  const etapa = ETAPAS[e.etapa];
  $('etapa-numero').textContent = `Etapa ${e.etapa + 1} de ${ETAPAS.length}`;
  $('previa-numero').textContent = String(e.etapa + 1).padStart(2, '0');
  $('previa-titulo').textContent = etapa.titulo;
  $('previa-resumo').textContent = etapa.resumo;
  $('nota').textContent = etapa.nota;
  document.querySelectorAll('#etapas button').forEach((b, i) => {
    if (i === e.etapa) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current');
  });
  $('observados').textContent = e.observados;
  $('envios').textContent = e.envios;
  $('revelar').textContent = e.revelado ? 'Ocultar dados na apresentação' : 'Revelar dados na apresentação';
  $('privacidade-texto').textContent = e.revelado ? 'Os detalhes da sessão estão visíveis na apresentação.' : 'A apresentação usa exemplos fictícios. Dados reais estão ocultos.';
  $('arquivo').textContent = e.arquivo ? `Arquivo desta sessão: ${e.arquivo}` : 'Ensaio: dados fictícios somente na memória.';
  const detalhes = JSON.stringify([e.vizinhos, e.registros]);
  if (detalhes !== ultimoConteudo) {
    montarTabela('vizinhos', e.vizinhos, ['ip', 'mac', 'estado'], 'Nenhum vizinho observado. Aguarde tráfego e atualize a consulta.');
    montarTabela('registros', e.registros, ['horario_utc', 'ip', 'navegador', 'apelido'], 'Nenhum envio registrado nesta sessão.');
    ultimoConteudo = detalhes;
  }
  const eventos = JSON.stringify(e.eventos);
  if ($('eventos').dataset.conteudo !== eventos) {
    $('eventos').replaceChildren(...e.eventos.map((item) => { const li = document.createElement('li'); li.textContent = `${item.hora} — ${item.texto}`; return li; }));
    $('eventos').dataset.conteudo = eventos;
  }
  renderizarComparacao();
  atualizarBotoes();
}

function ajustarPalco() {
  if (!telao) return;
  const area = document.querySelector('.viewport');
  const escala = Math.min(area.clientWidth / 1920, area.clientHeight / 1080);
  $('palco').style.transform = `scale(${escala})`;
}

function renderizarTelao() {
  const e = estado;
  $('conexao-telao').textContent = e.ativo ? 'Sincronizado com o painel da equipe' : 'Dinâmica parada · controle pelo painel da equipe';
  $('modo-telao').textContent = e.modo === 'ensaio' ? 'SIMULAÇÃO · DADOS FICTÍCIOS' : (e.ativo ? 'DEMONSTRAÇÃO AO VIVO' : 'DINÂMICA ENCERRADA');
  $('passo-telao').textContent = `${e.etapa + 1} / ${ETAPAS.length}`;
  const progresso = $('progresso-telao');
  if (progresso.children.length !== ETAPAS.length) progresso.replaceChildren(...ETAPAS.map(() => document.createElement('i')));
  [...progresso.children].forEach((ponto, i) => { ponto.className = i < e.etapa ? 'feito' : (i === e.etapa ? 'atual' : ''); });
  $('titulo-telao').textContent = ETAPAS[e.etapa].titulo;
  if ($('corpo-telao').dataset.etapa !== String(e.etapa)) {
    $('corpo-telao').innerHTML = ETAPAS[e.etapa].corpo;
    $('corpo-telao').dataset.etapa = e.etapa;
  }
  // Nome da rede e endereço reais (no macOS vêm do Compartilhamento de Internet).
  const nomeRede = $('corpo-telao').querySelector('.nome-rede');
  if (nomeRede && e.ssid && nomeRede.textContent !== e.ssid) nomeRede.textContent = e.ssid;
  const endereco = $('corpo-telao').querySelector('.endereco');
  if (endereco && e.url && endereco.firstChild?.nodeType === Node.TEXT_NODE && endereco.firstChild.nodeValue !== e.url) endereco.firstChild.nodeValue = e.url;
  $('totais-telao').textContent = `${e.observados} ${e.observados === 1 ? 'vizinho observado' : 'vizinhos observados'} · ${e.envios} ${e.envios === 1 ? 'envio' : 'envios'}`;
  $('dados-telao').hidden = !e.revelado || e.comparacao.telao;
  renderizarComparacao();
  // Remove também do DOM quando ocultos, inclusive após mudança de etapa.
  if (!e.revelado) {
    $('vizinhos').replaceChildren();
    $('registros').replaceChildren();
    ultimoConteudo = '';
  } else {
    $('dados-modo').textContent = e.modo === 'ensaio' ? 'EXEMPLOS FICTÍCIOS' : 'DADOS REAIS';
    const detalhes = JSON.stringify([e.vizinhos, e.registros]);
    if (detalhes !== ultimoConteudo) {
      montarTabela('vizinhos', e.vizinhos, ['ip', 'mac', 'estado'], 'Nenhum vizinho observado.', 5);
      montarTabela('registros', e.registros, ['horario_utc', 'ip', 'navegador', 'apelido'], 'Nenhum envio registrado.', 5);
      ultimoConteudo = detalhes;
    }
  }
}

function quadrosComparacao(container, envios) {
  const chave = JSON.stringify(envios);
  if (container.dataset.conteudo === chave) return;
  container.dataset.conteudo = chave;
  container.replaceChildren();
  for (const protocolo of ['http', 'https']) {
    const quadro = document.createElement('article');
    quadro.className = 'quadro-protocolo';
    const titulo = document.createElement('h3'); titulo.textContent = protocolo.toUpperCase(); quadro.append(titulo);
    const item = envios.filter(e => e.protocolo === protocolo).at(-1);
    const paragrafo = (texto, classe = '') => { const p = document.createElement('p'); p.textContent = texto; p.className = classe; quadro.append(p); };
    if (!item) paragrafo(`Aguardando envio por ${protocolo.toUpperCase()}.`);
    else {
      let veredito;
      if (protocolo === 'http') veredito = item.legivel ? 'Texto encontrado nos bytes da conexão' : 'Texto não localizado nesta amostra';
      else veredito = item.legivel ? 'Texto localizado: confira os bytes observados' : `Conteúdo protegido por ${item.tls || 'TLS'}`;
      paragrafo(veredito, 'veredito');
      paragrafo(`${item.origem === 'notebook' ? 'Notebook' : 'Participante'} · ${item.total_bytes} bytes observados${item.truncado ? ' (amostra limitada)' : ''}`);
      const codigo = document.createElement('pre');
      codigo.textContent = protocolo === 'http' ? item.texto : item.hex;
      quadro.append(codigo);
      paragrafo(`Recebido pelo servidor: ${item.recebido}`, 'recebido');
    }
    container.append(quadro);
  }
}

function renderizarComparacao() {
  const c = estado.comparacao;
  if (telao) {
    $('comparacao-telao').hidden = !c.telao;
    if (c.telao) {
      $('modo-telao').textContent = 'COMPARAÇÃO REAL · HTTP × HTTPS';
      quadrosComparacao($('quadros-telao'), c.envios || []);
    } else {
      $('quadros-telao').replaceChildren();
      $('quadros-telao').dataset.conteudo = '';
    }
    return;
  }
  $('status-comparacao').textContent = c.ativa ? (c.host === '127.0.0.1' ? 'Pronta no notebook. Os servidores atendem somente neste computador.' : 'Pronta para o notebook e os aparelhos da rede da atividade.') : 'Comparação encerrada ou ainda não preparada. Os resultados anteriores ficam disponíveis até a exclusão.';
  $('enderecos-comparacao').hidden = !c.ativa;
  for (const protocolo of ['http', 'https']) {
    const link = $(`url-comparacao-${protocolo}`);
    const host = c.host === '127.0.0.1' ? 'localhost' : c.host;
    const url = `${protocolo}://${host}:${c.portas[protocolo] || (protocolo === 'http' ? 8081 : 8443)}/`;
    link.textContent = url;
    link.href = url;
  }
  $('fingerprint').textContent = c.fingerprint;
  $('total-comparacao').textContent = `${c.total} ${c.total === 1 ? 'envio nesta comparação' : 'envios nesta comparação'}`;
  $('projetar-comparacao').textContent = c.telao ? 'Ocultar comparação na apresentação' : 'Mostrar comparação na apresentação';
  quadrosComparacao($('resultados-comparacao'), c.envios || []);
}

async function consultar() {
  try {
    estado = await requisitar(telao ? '/api/telao' : '/api/estado');
    if (telao) renderizarTelao();
    else { $('aviso-conexao').hidden = true; renderizarEquipe(); }
  } catch (erro) {
    if (telao) {
      $('conexao-telao').textContent = 'Sem conexão com o painel. Reabra pelo atalho se o app foi reiniciado.';
      $('dados-telao').hidden = true;
      $('comparacao-telao').hidden = true;
      $('quadros-telao').replaceChildren();
      $('quadros-telao').dataset.conteudo = '';
      $('vizinhos').replaceChildren(); $('registros').replaceChildren(); ultimoConteudo = '';
    } else {
      $('aviso-conexao').textContent = `Painel sem conexão: ${erro.message} Reabra pelo atalho se necessário.`;
      $('aviso-conexao').hidden = false;
    }
  }
}

async function iniciarInterface() {
  const parametros = new URLSearchParams(location.hash.slice(1));
  const token = parametros.get('sessao');
  if (token) {
    history.replaceState(null, '', location.pathname);
    try { await requisitar('/api/sessao', {token}); }
    catch (erro) { if (!telao) { $('mensagem').textContent = erro.message; return; } }
  }
  if (telao) {
    $('tela-cheia').onclick = async () => {
      try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); }
      catch { $('conexao-telao').textContent = 'Use F11 para entrar em tela cheia.'; }
    };
    window.addEventListener('resize', ajustarPalco);
    document.addEventListener('fullscreenchange', ajustarPalco);
    ajustarPalco();
  } else {
    ETAPAS.forEach((etapa, i) => {
      const botao = document.createElement('button'); botao.textContent = i + 1;
      botao.title = etapa.titulo; botao.setAttribute('aria-label', `Etapa ${i + 1}: ${etapa.titulo}`);
      botao.onclick = () => acao('etapa', {etapa: i}); $('etapas').append(botao);
    });
    $('modo').onchange = () => { selecionouModo = true; $('simulacao').hidden = $('modo').value !== 'ensaio'; atualizarBotoes(); };
    $('interface').onchange = () => { selecionouInterface = true; };
    document.querySelectorAll('[data-acao]').forEach((botao) => {
      botao.onclick = () => acao(botao.dataset.acao, {interface: $('interface').value});
    });
    $('iniciar').onclick = async () => {
      const real = $('modo').value === 'real';
      const aviso = estado?.plataforma === 'macos'
        ? `A página de participação vai abrir na rede do Compartilhamento de Internet (“${estado.ssid}”), em ${estado.url}. O app não muda ajustes do Mac. Avise o público sobre os dados observáveis antes de convidá-lo a conectar.`
        : 'A conexão Wi-Fi deste adaptador será substituída pelo ponto de acesso sem senha. Se houver internet em outra interface, ela poderá ser compartilhada. Avise o público sobre os dados observáveis antes de convidá-lo a conectar.';
      if (real && !await confirmar('Iniciar a rede da atividade?', aviso)) return;
      await acao('iniciar', {modo: $('modo').value, interface: $('interface').value, confirmar: real});
    };
    $('abrir-telao').onclick = () => {
      // O telão é a apresentação completa; nas etapas da demonstração ela mostra o telão ao vivo.
      const janela = window.open('/apresentacao', 'rede-aberta-apresentacao', 'popup,width=1280,height=760');
      if (!janela) { $('erro').textContent = 'Permita a abertura de janelas neste navegador para abrir a apresentação no projetor.'; $('erro').hidden = false; }
    };
    $('abrir-pagina').onclick = () => { if (estado?.servidor_ativo) window.open('http://127.0.0.1:8080', '_blank', 'noopener'); };
    $('anterior').onclick = () => acao('etapa', {etapa: estado.etapa - 1});
    $('proximo').onclick = () => acao('etapa', {etapa: estado.etapa + 1});
    $('revelar').onclick = async () => {
      if (estado.revelado) return acao('ocultar');
      const texto = estado.modo === 'ensaio' ? 'Os exemplos fictícios ficarão visíveis na apresentação. Você poderá ocultá-los a qualquer momento.' : 'IP, MAC e registros de participação ficarão visíveis para o público. Confirme que os participantes foram informados e que deseja projetar esses dados.';
      if (await confirmar('Revelar detalhes na apresentação?', texto)) await acao('revelar', {confirmar: true});
    };
    $('enviar-notebook').onclick = async () => {
      if (await confirmar('Enviar o texto fictício pelos dois protocolos?', 'O notebook enviará sua mensagem por HTTP e HTTPS e guardará o texto recebido, horário, IP e bytes de teste. Use somente texto fictício. A conexão HTTPS valida o certificado do laboratório.')) {
        await acao('enviar_notebook', {mensagem: $('mensagem-notebook').value, confirmar: true});
      }
    };
    $('projetar-comparacao').onclick = async () => {
      if (estado.comparacao.telao) return acao('ocultar_comparacao');
      if (await confirmar('Mostrar a comparação na apresentação?', 'As mensagens recebidas e as amostras HTTP/HTTPS ficarão visíveis ao público. Confirme que os envios são de demonstração e que os participantes foram informados.')) await acao('mostrar_comparacao', {confirmar: true});
    };
    $('excluir-comparacao').onclick = async () => {
      if (await confirmar('Excluir os dados desta comparação?', 'Apaga os fluxos observados, mensagens e certificados somente da comparação atual. Os registros da dinâmica original serão preservados.')) await acao('excluir_comparacao', {confirmar: true});
    };
    $('excluir').onclick = async () => {
      if (await confirmar('Excluir os dados desta sessão?', 'Esta ação é permanente e afeta somente a sessão atual. Registros anteriores não serão apagados.')) await acao('excluir', {confirmar: true});
    };
  }
  await consultar();
  // Uma consulta por vez, inclusive quando há lentidão ou suspensão do notebook.
  async function acompanhar() { await consultar(); proximaConsulta = setTimeout(acompanhar, 1000); }
  proximaConsulta = setTimeout(acompanhar, 1000);
}
iniciarInterface();

// No painel, as setas do teclado passam os slides da apresentação sem precisar clicar nela antes.
if (!telao && $('palestrante')) {
  const TECLAS = ['ArrowRight', 'ArrowLeft', 'PageDown', 'PageUp', 'Home', 'End'];
  document.addEventListener('keydown', (e) => {
    if (e.target.closest('input, select, textarea, dialog') || (e.target.closest('button') && e.key === ' ')) return;
    if (!TECLAS.includes(e.key) && !['r', 'c', 'd'].includes(e.key.toLowerCase())) return;
    try {
      $('palestrante').contentDocument.dispatchEvent(new KeyboardEvent('keydown', {key: e.key, shiftKey: e.shiftKey}));
      e.preventDefault();
    } catch (_) { /* apresentação ainda carregando */ }
  });
}

