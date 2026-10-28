# Rede aberta — demonstração de Wi-Fi aberto

> Parte do projeto de intervenção **Inclusão Digital e Segurança da Informação** (Unit · Sistemas de Informação), com a EMEF Prof. Diomedes Santos Silva, Aracaju/SE. Esta é a **demonstração ao vivo** do deck: “Por que não confiar em Wi-Fi aberto”. Veja como ela se encaixa na palestra em [docs/CONTEXTO_PROJETO.md](docs/CONTEXTO_PROJETO.md).

## Mapa do repositório

| Pasta ou arquivo | Para que serve |
| --- | --- |
| `app.py`, `controle.py` | Painel da equipe, controle da rede e das etapas |
| `servidor.py` | Página de participação (`http://10.42.0.1:8080`) |
| `comparacao.py` | Laboratório HTTP × HTTPS |
| `remoto.py`, `interface/remoto.*` | Controle dos slides pelo celular, com pareamento e QR code local |
| `interface/` | Painel (`index.html`, `app.js`, `estilo.css`), **telão** (`telao.html`, `telao.css`) e textos das etapas (`conteudo.js`) |
| `docs/` | Contexto do projeto, roteiro de fala, guia de slides, `previa_telao.html` e `apresentacao_completa.html` |
| `ver_telao.py` | Abre só a prévia do telão no navegador, sem rodar o app |
| `tests/` | Testes automatizados e verificação da interface |
| `iniciar.sh`, `clientes.sh`, `abrir_app.sh`, `instalar_atalho.py` | Scripts de linha de comando e atalho do app |


Este projeto cria um ponto de acesso **sem senha** para uma atividade presencial e oferece uma página educativa em `http://10.42.0.1:8080`. A página só grava dados depois que a pessoa marca a caixa de concordância e envia o formulário: horário, IP, identificação do navegador e apelido opcional. O comando `clientes.sh` mostra os endereços IP e MAC presentes na tabela de vizinhos do sistema; essa consulta não grava arquivo.

Para conduzir a fala, os cliques e a participação do público, consulte o [roteiro de apresentação](docs/ROTEIRO_APRESENTACAO.md).

## Apresentação completa da palestra

Abra `docs/apresentacao_completa.html` com duplo clique. São 37 slides para uma palestra de 45 minutos: abertura, informática básica, ferramentas digitais, internet consciente, senhas seguras, golpes virtuais (com a dinâmica “Verdadeiro ou golpe?”), dados pessoais e LGPD, a demonstração de Wi-Fi aberto e o encerramento com questionário. O tempo sugerido de cada parte está no slide de roteiro e nas notas. Setas ← → ou toque na tela mudam de slide, **P** abre o modo palestrante (uma segunda janela com o roteiro de fala, o tempo sugerido de cada slide, o relógio de 45 minutos e o próximo slide, sincronizada com a do público), **N** mostra as notas do apresentador, **R** revela as respostas da dinâmica, **F** entra em tela cheia; nas etapas da demonstração, **D** e **C** funcionam como na prévia. O arquivo é independente (estilos, textos das etapas e imagens embutidos); se mudar `interface/conteudo.js` ou `interface/telao.css`, gere-o de novo.

### Mostrar HTTP × HTTPS no próprio slide

Na parte **Wi-Fi aberto**, abra **Exibir** na barra da apresentação e escolha **Mostrar HTTP × HTTPS**. No modo palestrante, use o botão **Mostrar HTTP × HTTPS** abaixo do título do slide. **Mostrar MAC e mensagens** alterna para a tabela de aparelhos e registros. As teclas **C** e **D** fazem as mesmas ações, inclusive quando o foco está no painel da equipe.

Com o app aberto, faça primeiro um envio em **Compare HTTP e HTTPS**. O botão do slide ficará disponível assim que houver resultados; confirme a exibição para projetar os bytes HTTP/HTTPS e as mensagens recebidas. Use o mesmo botão para ocultar. As duas visualizações são exclusivas e os detalhes ficam ocultos ao trocar a etapa da demonstração.

Ao abrir `docs/apresentacao_completa.html` ou `docs/previa_telao.html` diretamente, os controles mostram exemplos identificados como fictícios. A apresentação e o painel ao vivo usam os registros da sessão, com confirmação antes de revelá-los.

### Controlar os slides pelo celular

1. Abra o app no notebook e clique em **Abrir apresentação no projetor**. Este recurso controla os 37 slides servidos pelo app; o arquivo HTML aberto com duplo clique funciona de forma independente.
2. Conecte o celular à **mesma rede do notebook**. Na demonstração real, inicie primeiro a rede da atividade e conecte o celular a ela. Funciona sem internet.
3. No painel da equipe, em **Controle pelo celular**, clique em **Ativar controle do celular**. Leia o QR code com a câmera ou abra o endereço exibido. Digite no celular o **código de seis dígitos**, mostrado somente no painel da equipe.
4. Use **Anterior** e **Próximo** para passar os slides. Notebook, projetor e celular acompanham a posição atual. Nas sete etapas de Wi-Fi aberto também aparecem **Mostrar MAC e mensagens** e **Mostrar HTTP × HTTPS**. A comparação fica disponível após um envio pelo notebook; a exibição dos dados exige confirmação no celular.
5. **Gerar novo código** desconecta o controle anterior. **Desativar controle** fecha o acesso pelo celular. O código é de uso único e a sessão dura até duas horas. Fechar a página do notebook não encerra o app; mantenha a apresentação aberta para os comandos funcionarem.

Se não abrir, confira o Wi-Fi, mantenha a conexão mesmo com o aviso “sem internet” e permita conexões de entrada do Python no firewall do notebook (normalmente porta **8766**, ou a indicada no endereço). Redes com isolamento entre clientes podem impedir o acesso. Depois de trocar a rede do notebook, desative e ative o controle novamente para gerar o endereço correto.

O controle usa HTTP local e permite somente navegação e exibição dos painéis; não libera o painel administrativo nem mostra os registros no celular. O código evita acesso casual, mas não criptografa a conexão em uma rede aberta. O QR code é gerado no próprio notebook, sem serviços externos. A biblioteca incluída em `vendor/qrcodegen.py` é do [Project Nayuki](https://github.com/nayuki/QR-Code-generator), sob licença MIT preservada no arquivo.

## Ver só o telão (sem rodar o app)

```bash
python3 ver_telao.py
```

Ou abra `docs/previa_telao.html` com duplo clique. Setas ← → mudam de etapa, **D** mostra a tabela de resultados, **C** a comparação HTTP × HTTPS (dados fictícios) e **F** entra em tela cheia. Edite `interface/telao.css` e `interface/conteudo.js` e recarregue com F5. Funciona em qualquer sistema com navegador.

## Baixar e iniciar

Em um computador Linux com Python 3 e OpenSSL:

```bash
git clone https://github.com/matheus-crisostomo/rede-aberta-demo.git
cd rede-aberta-demo
python3 instalar_atalho.py
bash abrir_app.sh
```

Depois da instalação, abra **Rede aberta** pelo menu de aplicativos ou pelo atalho na área de trabalho. A comparação HTTP/HTTPS pelo notebook funciona sem criar uma rede Wi-Fi. Para conectar celulares, confira os requisitos de NetworkManager e adaptador AP abaixo.

### No macOS

No Mac funcionam o painel, o ensaio, a apresentação, a comparação HTTP × HTTPS e também a **Demonstração real**. Nela o Mac vira o ponto de acesso pelo **Compartilhamento de Internet**, que a equipe liga nos Ajustes; o app não muda ajustes do sistema e só usa essa rede (interface `bridge100`), para observar apenas os aparelhos que entraram na rede da demonstração.

```bash
cd rede-aberta-demo
python3 instalar_atalho.py
bash abrir_app.sh
```

O instalador cria **Rede Aberta.command** na pasta do projeto e na Mesa: dê dois cliques para abrir o painel. Se o macOS bloquear na primeira vez, clique com o botão direito, escolha **Abrir** e confirme.

**Antes da demonstração real no Mac:**

1. Abra **Ajustes do Sistema › Geral › Compartilhamento** e clique no **ⓘ** ao lado de **Compartilhamento de Internet**.
2. Em **Compartilhar sua conexão de**, troque **Wi-Fi** por **USB do iPhone**, **Ponte Thunderbolt** ou um **Adaptador Ethernet**. Com **Wi-Fi** nesse campo, a opção **Wi-Fi** não aparece na lista de baixo, porque o Mac não recebe e distribui pelo Wi-Fi ao mesmo tempo. A demonstração funciona mesmo sem internet nessa fonte (com USB do iPhone, ligue o Acesso Pessoal no iPhone e conecte o cabo).
3. Em **Para dispositivos que usam**, ative **Wi-Fi**. Clique em **Opções de Wi-Fi** e defina o nome da rede (por exemplo, `EXTENSAO-REDE-ABERTA`) e, se o macOS oferecer, a segurança **Nenhuma**; se não oferecer, use uma senha simples e mostre-a ao público.
4. Ative **Compartilhamento de Internet** no topo da janela e clique em **OK**. O Mac sai da rede Wi-Fi em que estava enquanto ele estiver ativo.
5. No painel, escolha **Demonstração real**, clique em **Verificar equipamento** e depois em **Iniciar demonstração real**. O nome da rede e o endereço da página (por exemplo, `http://192.168.2.1:8080`) aparecem sozinhos na apresentação.
6. Na primeira vez, o macOS pode perguntar se o Python pode aceitar conexões de entrada: clique em **Permitir**, senão os celulares não abrem a página.
7. Ao terminar, clique em **Encerrar dinâmica** e desligue o Compartilhamento de Internet.

Para rodar os testes: `python3 -m unittest discover -s tests -v`.

## Usar o aplicativo por botões

Abra **Rede aberta** pelo menu de aplicativos do Linux ou pelo atalho **Rede Aberta** na área de trabalho. O navegador abre o painel da equipe; durante a apresentação não é necessário usar o terminal. Se o sistema perguntar, escolha **Permitir iniciar** no atalho da área de trabalho.

1. Comece em **Ensaio com dados fictícios** e clique em **Iniciar ensaio**. Os botões **Simular aparelho** e **Simular envio** criam exemplos somente na memória, sem alterar o Wi-Fi.
2. O painel já mostra a **Apresentação**: o slide, o roteiro de fala, o tempo sugerido, o relógio de 45 minutos e o próximo slide, ao lado dos controles da dinâmica. Clique em **Abrir apresentação no projetor**, mova a nova janela para o projetor e use **Tela cheia** (configure o projetor para **estender** a tela). Passe os slides pelo painel ou pelo projetor: os dois andam juntos. Na parte “Wi-Fi aberto”, a apresentação mostra o telão ao vivo do app e segue as **Etapas da demonstração**; depois da última etapa, volta aos slides.
3. Avance as sete etapas pelos botões **Anterior**, **Próximo** ou pelos números. As notas de fala aparecem apenas no painel. O roteiro completo está em [GUIA_SLIDES_DINAMICA.md](docs/GUIA_SLIDES_DINAMICA.md).
4. Para usar aparelhos reais, encerre o ensaio, selecione **Demonstração real**, clique em **Verificar equipamento**, escolha o adaptador e clique em **Iniciar demonstração real**. Confirme a troca de conexão; se necessário, autorize pela janela do sistema. A página fica em `http://10.42.0.1:8080`.
5. Os resultados atualizam automaticamente. **Atualizar aparelhos** refaz a consulta de vizinhos. **Consultar detalhes nesta janela** mostra os dados à equipe. **Revelar dados no telão** pede confirmação antes de projetá-los. **Ocultar dados no telão** ou mudar de etapa os esconde novamente.
6. Clique em **Encerrar dinâmica** para desligar a página, remover o perfil criado pelo app e tentar restaurar a conexão Wi-Fi anterior. Se aparecer **Limpeza pendente**, clique novamente após resolver o erro indicado.

Cada atividade real usa seu próprio arquivo em `dados/sessoes/`. O `registros.jsonl` anterior é preservado. Encerrar mantém os dados; **Excluir dados da sessão**, disponível após o encerramento e com confirmação, apaga somente a sessão atual. O telão mostra até cinco linhas por tabela, com textos abreviados; o painel mostra até os cem envios mais recentes. Quantidade de envios não equivale a pessoas diferentes.

O painel atende apenas no endereço local `127.0.0.1` e exige a sessão aberta pelo atalho. Os participantes acessam somente a página educativa. Fechar o navegador não encerra uma dinâmica: reabra o app para retomar os controles. Em caso de interrupção do processo, o app recupera a identificação da rede criada e oferece a limpeza na próxima abertura.

### Comparar HTTP e HTTPS pelo notebook

1. Abra o painel e localize **Compare HTTP e HTTPS**. Clique em **Preparar comparação**. Isso funciona mesmo sem iniciar o Wi-Fi ou um ensaio.
2. Mantenha `OLA_TURMA` ou digite outro texto fictício e clique em **Enviar pelo notebook (HTTP + HTTPS)**. Confirme o registro da mensagem e dos bytes de teste.
3. Compare os dois quadros: no HTTP, o formulário aparece legível; no HTTPS, aparecem bytes de registros TLS. **Recebido pelo servidor** mostra o texto entregue nos dois casos. O notebook verifica o certificado de laboratório com uma confiança restrita a esse cliente, sem alterar os certificados do sistema.
4. Clique em **Mostrar comparação no telão** e confirme a projeção. O telão identifica esses envios como reais mesmo que o roteiro esteja em ensaio. Use **Ocultar comparação no telão** ou avance de etapa para esconder os detalhes.
5. Termine com **Encerrar comparação**. Para remover os arquivos dessa comparação, use **Excluir dados da comparação** e confirme.

### Manter o envio pelo celular

A página original em `http://10.42.0.1:8080` e seu formulário continuam funcionando.

1. Inicie a **Demonstração real** e, depois, **Preparar comparação**. Se a comparação estava preparada apenas para o notebook, iniciar outra dinâmica a encerra; prepare-a novamente com a rede ativa.
2. No celular, conecte-se a `EXTENSAO-REDE-ABERTA`. Abra a página original e toque em **Participar da comparação HTTP × HTTPS**, ou acesse diretamente `http://10.42.0.1:8081/`.
3. Leia a explicação, use uma mensagem fictícia, marque a concordância e toque em **Enviar por HTTP**. Apenas a visita ou um envio sem concordância não grava participação na comparação.
4. No aparelho de demonstração com o certificado de laboratório já instalado e conferido, abra `https://10.42.0.1:8443/`, repita a mesma mensagem e envie com concordância.
5. A equipe verá os envios no painel e poderá projetá-los mediante confirmação. O quadro de cada protocolo mostra o envio mais recente, sua origem e o texto recebido; mensagens diferentes devem ser reenviadas com o mesmo texto para uma comparação direta.

### Certificado HTTPS no celular

Antes da apresentação, a equipe deve preparar um aparelho para a versão HTTPS. O certificado é gerado localmente, vale dois dias e muda a cada nova comparação. Portanto, prepare a comparação definitiva antes de instalar o certificado no aparelho. Os demais participantes podem usar HTTP e acompanhar o HTTPS pelo notebook.

Na página HTTP da comparação, escolha **Baixar certificado do laboratório**. Confira a impressão **SHA-256** com a exibida no painel, em **Certificado de laboratório**; faça essa conferência com a equipe antes de confiar no certificado.

- **Android:** nas configurações de segurança/credenciais, procure a instalação de **certificado de CA** e selecione `Rede-Aberta-Laboratorio.crt`. Os nomes dos menus e a aceitação de certificados do usuário variam por fabricante e navegador. Consulte as orientações do aparelho; a [ajuda oficial do Google](https://support.google.com/pixelphone/answer/2844832?hl=pt-BR) também explica a remoção de credenciais do usuário.
- **iPhone/iPad:** instale o perfil baixado pelos Ajustes. Depois, em **Geral → Sobre → Confiança em Certificados**, ative a confiança na autoridade **Rede Aberta Laboratorio**. A confiança em certificados instalados manualmente exige essa etapa adicional, conforme a [documentação da Apple](https://support.apple.com/en-us/102390).

Se o navegador ainda mostrar aviso de certificado, confira a instalação, o endereço, a impressão e a validade com a equipe. O envio automático pelo notebook continua disponível e valida o certificado sem configuração do celular. Ao terminar, remova apenas o certificado/perfil instalado para esta atividade.

### O que a comparação observa e guarda

A comparação usa duas pontes TCP que encaminham somente para os servidores HTTP/HTTPS locais da atividade. Observamos os bytes recebidos antes da descriptografia TLS no destino. É uma observação real do fluxo TCP; não é captura passiva de pacotes da rede inteira, nem leitura de outros sites. Não exige `tcpdump`, Wireshark ou privilégios de captura.

Após consentimento e envio, cada registro guarda horário UTC, IP, mensagem, protocolo, origem, versão TLS e uma amostra dos bytes. Os arquivos ficam em `dados/comparacoes/<sessão>/`, separados dos registros originais. Arquivos `.bin` contêm bytes do fluxo TCP, sem cabeçalhos IP/TCP; não são PCAP. São guardados até 64 KiB por envio, com limite de 100 envios por comparação. A interface mostra os últimos dez resultados e o quadro mais recente de cada protocolo. No HTTPS, o trecho hexadecimal vem de um registro TLS criptografado; o texto **Recebido pelo servidor** vem do processamento feito no destino.

Em comparação local, as portas 8081 e 8443 atendem somente em `127.0.0.1`. Quando preparada com a rede real ativa, a comparação atende também aos participantes. **Encerrar dinâmica** fecha igualmente os servidores de comparação. Fechar o navegador mantém os serviços ativos; reabra o atalho para encerrar pelos botões.

### Instalar ou recriar o atalho

Após mover ou copiar esta pasta, execute uma única vez:

```bash
python3 instalar_atalho.py
```

O instalador cria atalhos para o usuário atual, sem `sudo`. Alternativamente, inicie com `bash abrir_app.sh`. O app usa Python 3, OpenSSL e recursos do sistema; não depende de Node, npm ou internet. A pasta `dados/` contém os arquivos locais de execução e deve ficar fora do controle de versão. O log técnico fica em `dados/app.log`.

### Verificar a implementação

```bash
python3 -m unittest discover -s tests -v
bash -n abrir_app.sh iniciar.sh clientes.sh
```

Os testes usam rede Wi-Fi simulada, diretórios temporários e servidores em portas locais efêmeras. A comparação HTTP/HTTPS é exercitada com conexões TCP e TLS reais no próprio computador. Não criam pontos de acesso nem leem registros reais. Para verificar a interface com Playwright instalado em um ambiente de desenvolvimento, inicie o app e execute `node tests/verificar_interface.cjs`; esse teste executa e limpa um ensaio, por isso use-o sem outra atividade em andamento. A operação física do ponto de acesso deve ser ensaiada com um celular antes da apresentação.

## Equipamentos

- Notebook ou mini PC com Linux e NetworkManager (`nmcli`), Python 3 e comando `ip` (`iproute2`).
- Placa ou adaptador Wi-Fi compatível com **modo AP**. Um adaptador USB extra pode ser necessário se a placa integrada já estiver sendo usada para acessar outra rede Wi-Fi.
- Um celular ou outro aparelho para se conectar e abrir a página.
- Fonte de energia e, se desejado, um cartaz ou QR code com o endereço da página.

**Arduino não é necessário.** A internet também não é necessária para abrir a página local. Se o computador tiver uma conexão de internet ativa em outra interface, o modo `shared` do NetworkManager pode compartilhá-la com os participantes; para um teste isolado, desconecte essa outra interface.

## Executar

1. Identifique a interface Wi-Fi com `nmcli device status` (por exemplo, `wlan0`). Confira se o adaptador oferece modo AP com `nmcli -f WIFI-PROPERTIES.AP device show wlan0`.
2. Na pasta do projeto, execute `bash iniciar.sh wlan0`. O comando pede permissão administrativa para criar o ponto de acesso temporário. A interface deixa de usar a conexão Wi-Fi anterior enquanto a demonstração estiver ativa.
3. No celular, conecte-se ao SSID `EXTENSAO-REDE-ABERTA` e abra **manualmente** `http://10.42.0.1:8080`. Alguns aparelhos avisam que a rede não tem internet; mantenha a conexão para acessar a página local.
4. Em outro terminal, execute `bash clientes.sh wlan0` para observar IP e MAC. A lista pode aparecer vazia até que o aparelho troque tráfego com o ponto de acesso.
5. Após o envio do formulário, consulte `registros.jsonl`. Um registro ocupa uma linha JSON. Para encerrar, pressione `Ctrl+C` no terminal do servidor; o perfil de rede criado pelo script será removido.

Use apenas aparelhos dos participantes informados. O endereço MAC pode ser temporário ou aleatório, conforme a configuração do aparelho. Apague `registros.jsonl` depois da apresentação se não precisar manter os dados.

## Referência técnica

O modo `ap`, o isolamento entre clientes e o método IPv4 `shared` são propriedades documentadas pelo [NetworkManager](https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/nm-settings-nmcli.html).
