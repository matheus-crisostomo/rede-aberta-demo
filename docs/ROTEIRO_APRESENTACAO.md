# Roteiro para conduzir a apresentação

Use este roteiro na transição da explicação teórica para a dinâmica final. Reserve **13 a 15 minutos**. As sete etapas já estão no telão do app; os textos para criar slides estão no [guia de slides](GUIA_SLIDES_DINAMICA.md); o encaixe com o deck do projeto está em [CONTEXTO_PROJETO.md](CONTEXTO_PROJETO.md).

## Antes de o público chegar

Uma pessoa pode conduzir a fala e outra operar o painel e ajudar nas conexões. Se estiver sozinho, mantenha o painel no notebook e o telão no projetor.

1. Abra **Rede aberta** e configure o projetor para **estender a tela**.
2. Ensaie o fluxo. Depois, encerre o ensaio e selecione **Demonstração real**.
3. Clique em **Verificar equipamento**, selecione o adaptador e use **Iniciar demonstração real**. Confirme a operação e autorize pela janela do sistema, se necessário.
4. Clique em **Preparar comparação** e configure o certificado no celular de demonstração. Siga o [tutorial do certificado](../README.md#certificado-https-no-celular).
5. Teste no celular o formulário original e os envios HTTP/HTTPS usando apenas dados fictícios. Teste também **Enviar pelo notebook (HTTP + HTTPS)**.
6. Mantenha essa comparação preparada até o fim da apresentação. Preparar outra comparação gera outro certificado; iniciar outra dinâmica encerra a comparação anterior.
7. Clique em **Abrir telão**, mova essa janela para o projetor e use **Tela cheia**. Selecione a etapa **1** no painel e confira que os detalhes reais estão ocultos.

Os envios de teste podem permanecer nos totais dessa sessão. Apresente os números como quantidade de envios, incluindo a preparação, e não como quantidade de participantes. Prepare também capturas com dados fictícios para usar se algum equipamento falhar.

## Sequência durante a apresentação

| Tempo aproximado | Etapa do app | Sua ação principal |
| --- | --- | --- |
| 0–1 min | 1. Por que não confiar em Wi-Fi aberto? | Explicar o objetivo e a participação voluntária |
| 1–3 min | 2. Entre na rede de teste | Ajudar o público a conectar e abrir a página |
| 3–4 min | 3. Leia e escolha participar | Orientar o envio com apelido fictício |
| 4–6 min | 4. Ver e guardar são coisas diferentes | Explicar IP, MAC e informações do navegador |
| 6–7 min | 5. Um envio, quatro informações | Relacionar o formulário ao registro |
| 7–11 min | 6. O mesmo texto, duas conexões | Comparar HTTP/HTTPS pelo celular e pelo notebook |
| 11–13 min | 7. Como se proteger | Ouvir o público e encerrar a dinâmica |

Use **Próximo**, **Anterior** ou os números para mudar de etapa. Cada mudança oculta os detalhes que estavam projetados.

## 1. Faça a transição para a prática

**Fala sugerida:**

> “Agora vamos observar como essas informações aparecem em uma conexão real. Vamos usar uma rede e uma página criadas para esta atividade. A participação é voluntária; quem preferir pode apenas acompanhar.”

Antes de convidar as pessoas a conectar, explique:

> “A rede pode observar IP e MAC apresentados pelo aparelho. Ao abrir a página, o servidor recebe IP e informações enviadas pelo navegador. Nosso programa só grava a participação depois da concordância e do envio do formulário. Usem apenas apelidos e mensagens fictícias.”

## 2. Convide o público a entrar na rede

Avance para a etapa **2** e mantenha as instruções projetadas:

- Rede: **EXTENSAO-REDE-ABERTA**, sem senha.
- Página inicial: **http://10.42.0.1:8080**.

**Fala sugerida:**

> “Conectem-se à rede indicada e digitem o endereço completo no navegador. A página funciona no notebook da equipe, mesmo sem internet. Se o celular avisar que a rede está sem internet, mantenham a conexão.”

Espere uma ou duas pessoas confirmarem que abriram a página. Prossiga com quem conseguiu; o restante pode acompanhar o aparelho de demonstração.

## 3. Oriente a participação

Na etapa **3**, peça que leiam o aviso, escolham um apelido fictício ou deixem o campo vazio, marquem a concordância e toquem em **Participar**.

**Fala sugerida:**

> “Primeiro leiam quais dados serão gravados. Quem quiser participar pode enviar o formulário. A mensagem de agradecimento confirma que o envio foi recebido.”

Confira os resultados no painel. Um novo envio aumenta o total de participações; não prometa que todos os aparelhos aparecerão na tabela de vizinhos.

## 4. Explique os dados observados

Na etapa **4**, clique em **Atualizar aparelhos**. Se precisar examinar os valores, abra **Consultar detalhes nesta janela**, mantendo o painel fora da projeção.

**Fala sugerida:**

> “O IP é um endereço usado nesta rede. O MAC é o endereço apresentado pela interface do aparelho e pode ser aleatório. As informações do navegador ajudam a descrever o aplicativo que fez o acesso, mas não comprovam quem é a pessoa.”

Destaque a diferença: a tabela de vizinhos mostra IP e MAC observados; o arquivo de participação guarda horário, IP, navegador e apelido opcional.

## 5. Mostre como um envio vira registro

Avance para a etapa **5** e use o exemplo fictício do telão para explicar os quatro campos.

Se houver motivo para mostrar detalhes reais, clique em **Revelar dados no telão**, leia a confirmação e prossiga somente com os participantes informados. Use **Ocultar dados no telão** ao terminar.

**Fala sugerida:**

> “Este é o tipo de registro que o formulário produz. Uma pessoa pode enviar mais de uma vez, então o contador representa envios. O MAC consultado na rede não é gravado nesse registro.”

## 6. Compare HTTP e HTTPS

Avance para a etapa **6**. A comparação deve continuar preparada desde a configuração do certificado.

### Primeiro, deixe o participante enviar

1. No celular de demonstração, abra **http://10.42.0.1:8081/**. A página inicial também oferece o link **Participar da comparação HTTP × HTTPS**.
2. Use a mensagem **OLA_TURMA**, marque a concordância e toque em **Enviar por HTTP**.
3. No mesmo aparelho, com o certificado já configurado, abra **https://10.42.0.1:8443/**.
4. Repita **OLA_TURMA**, marque a concordância e toque em **Enviar por HTTPS**.
5. Confira no painel que os quadros dos dois protocolos mostram a mesma mensagem recebida. Clique em **Mostrar comparação no telão** e confirme.

**Fala sugerida:**

> “Aqui observamos os bytes TCP na entrada dos nossos servidores de teste, antes da descriptografia HTTPS. No HTTP conseguimos localizar o formulário enviado. No HTTPS vemos registros TLS criptografados. O servidor recebe a mensagem nos dois casos.”

Aponte a versão TLS indicada no quadro HTTPS e o campo **Recebido pelo servidor**. A aparência hexadecimal sozinha não demonstra criptografia: relacione os bytes à conexão TLS efetivamente estabelecida.

### Depois, repita pelo notebook

1. Clique em **Ocultar comparação no telão** enquanto opera.
2. No campo do notebook, mantenha **OLA_TURMA**.
3. Clique em **Enviar pelo notebook (HTTP + HTTPS)** e confirme.
4. Aguarde os dois resultados e use **Mostrar comparação no telão** novamente.

**Fala sugerida:**

> “Agora o notebook repetiu os dois envios automaticamente. O resultado é o mesmo: o HTTP permite localizar o texto na conexão, enquanto o HTTPS protege o conteúdo durante o transporte. O destino continua recebendo o que enviamos.”

O notebook valida o certificado no próprio cliente do teste. Esse envio funciona também sem rede Wi-Fi ativa. Cada quadro mostra o envio mais recente daquele protocolo, portanto os envios do notebook substituem os resultados do celular na visualização.

**Controle direto no slide:** na parte Wi-Fi aberto, use **Exibir → Mostrar HTTP × HTTPS**, ou o botão de mesmo nome no modo palestrante. A tecla **C** alterna essa comparação; **D** alterna MAC e mensagens. Com o app, confirme a projeção dos envios da sessão. O botão só fica disponível após um envio HTTP/HTTPS. Para a versão independente, os exemplos são fictícios e identificados na tela.

## 7. Feche com uma pergunta

Avance para a etapa **7**, ocultando os resultados da comparação.

Pergunte:

> “Qual informação vocês não imaginavam que apareceria nessa comunicação?”

Após uma ou duas respostas, conclua:

> “Antes de conectar, confirmem qual é a rede. Antes de enviar, entendam quais dados serão usados. HTTPS protege o conteúdo entre o navegador e o servidor, enquanto informações da conexão continuam observáveis. Essa é a diferença que vimos na prática.”

## Encerramento da equipe

- Peça que as pessoas se desconectem e removam a rede salva.
- Clique em **Encerrar dinâmica**. Isso fecha a página e a comparação, remove o perfil criado pelo app e tenta restaurar a conexão anterior, preservando uma conexão diferente que você tenha escolhido manualmente.
- Confira eventuais mensagens de limpeza pendente no painel.
- Remova do celular o certificado de laboratório instalado para a demonstração.
- Quando os dados não forem mais necessários, use **Excluir dados da sessão** e **Excluir dados da comparação**, confirmando cada operação. Encerrar os serviços preserva os arquivos até essa exclusão.

## Se algo falhar durante a fala

| Situação | Como continuar |
| --- | --- |
| Parte do público não conecta | Continue com o celular de demonstração e mantenha as instruções na tela |
| O celular informa “sem internet” | Oriente a manter a conexão ao Wi-Fi e abrir o endereço completo |
| O HTTPS mostra aviso de certificado | Confira a preparação do aparelho com a equipe; prossiga com o envio pelo notebook enquanto isso |
| A tabela de vizinhos está vazia | Gere tráfego abrindo a página e atualize; explique que a tabela pode omitir aparelhos |
| Os quadros mostram mensagens diferentes | Repita a mesma mensagem nos dois protocolos ou use o envio duplo do notebook |
| O ponto de acesso falha | Encerre a dinâmica e prepare a comparação no próprio notebook; os envios HTTP/HTTPS locais continuam sendo reais |
| O app fica indisponível | Use as capturas preparadas, identificando-as como exemplos do ensaio |

**Lembrete para quem apresenta:** o projeto observa os fluxos dos próprios servidores de teste. Ele não demonstra leitura de tráfego de outros sites, mensagens ou arquivos dos celulares.
