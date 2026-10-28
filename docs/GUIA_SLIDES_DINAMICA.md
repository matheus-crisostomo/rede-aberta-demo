# Guia de slides — dinâmica final sobre Wi-Fi aberto

Este roteiro foi pensado para uma atividade presencial de aproximadamente **10 a 13 minutos**, ao final da apresentação. Use os textos indicados na tela e deixe as explicações nas notas do apresentador. O conteúdo corresponde ao funcionamento de `servidor.py`, `iniciar.sh` e `clientes.sh`.

> **Telão do app:** as sete etapas projetadas pelo app seguem a identidade visual do deck do projeto (azul-marinho, amarelo, Montserrat) e usam os títulos “Por que não confiar em Wi-Fi aberto?”, “Entre na rede de teste”, “Leia e escolha participar”, “Ver e guardar são coisas diferentes”, “Um envio, quatro informações”, “O mesmo texto, duas conexões” e “Como se proteger”. Este guia serve para quem preferir montar slides próprios. Veja [CONTEXTO_PROJETO.md](CONTEXTO_PROJETO.md).

## Objetivo da atividade

Mostrar quais informações aparecem na comunicação entre um celular, a rede Wi-Fi e uma página local. Ao final, o público deverá distinguir informações observáveis na conexão de dados gravados após participação voluntária.

## Direção visual

- Monte em formato 16:9, no Canva, PowerPoint ou Google Slides.
- Use fundo claro com texto escuro, uma cor de destaque e bastante espaço livre.
- Como ponto de partida, use títulos de 36–44 pt e corpo de pelo menos 28 pt; confira a leitura do fundo da sala.
- Destaque o nome da rede e o endereço da página. Mantenha o endereço escrito mesmo se incluir QR code.
- Use ícones simples de celular, Wi-Fi e notebook. Reserve comandos e detalhes de configuração às notas da equipe.

## Slide 1 — Vamos observar uma conexão na prática

**Tempo:** 1 minuto.

**Texto na tela:**

> O que uma rede e uma página conseguem observar?
>
> Uma experiência com o seu celular e uma página local.
>
> Participação voluntária: você também pode apenas acompanhar.

**Visual:** celular → rede Wi-Fi → notebook com a página.

**Fala sugerida:**

“Vamos encerrar com uma demonstração. Antes de se conectar, saibam que a rede pode observar o IP e o endereço MAC apresentado pelo aparelho. Ao acessar a página, nosso servidor recebe o IP e informações técnicas que o navegador enviar. Nosso programa só grava horário, IP, identificação do navegador e apelido opcional quando vocês concordam e enviam o formulário. Quem preferir pode apenas observar.”

**Orientação para a equipe:** faça esse aviso antes de convidar o público a entrar na rede. Não apresente a coleta como uma surpresa ao final.

## Slide 2 — Conecte-se à rede da atividade

**Tempo:** 1 a 2 minutos.

**Texto na tela:**

> 1. Abra as configurações de Wi-Fi.
> 2. Conecte-se a **EXTENSAO-REDE-ABERTA**, sem senha.
> 3. No navegador, digite **http://10.42.0.1:8080**.

**Aviso em destaque:** “A rede pode aparecer como ‘sem internet’. Mantenha a conexão para abrir a página local.”

**Visual:** três passos numerados. Se houver QR code, ele deve conter exatamente `http://10.42.0.1:8080` e ser usado depois da conexão ao Wi-Fi.

**Fala sugerida:**

“A página está no notebook da equipe e funciona sem internet. Digitem o endereço completo na barra de endereços. Ela não abre automaticamente quando vocês entram na rede.”

**Orientação para a equipe:** teste o endereço e o eventual QR code em um celular antes da apresentação. Se houver dificuldade, prossiga com o aparelho de demonstração.

## Slide 3 — Leia e escolha participar

**Tempo:** 1 minuto.

**Texto na tela:**

> Leia a explicação da página.
>
> Se quiser, use um apelido fictício ou deixe o campo vazio.
>
> Marque a concordância e toque em **Participar**.

**Rodapé:** “Use apenas dados de demonstração. Não informe senhas nem nome real.”

**Visual:** captura da página com destaque no apelido opcional, na caixa de concordância e no botão. Use campos vazios ou dados fictícios na captura.

**Fala sugerida:**

“Abrir a página não gera um registro de participação neste programa. O registro acontece quando vocês marcam a concordância e enviam o formulário. A página usa HTTP, sem criptografia dessa comunicação; por isso, vamos usar apenas informações fictícias.”

**Resultado esperado:** a página mostra “Participação registrada. Obrigado!”. Cada envio válido acrescenta uma linha ao arquivo de registros; a quantidade de linhas representa envios, não necessariamente pessoas diferentes.

## Slide 4 — O que aparece em cada etapa?

**Tempo:** 2 minutos.

**Texto na tela:**

| Etapa | O que fica disponível nesta demonstração |
| --- | --- |
| Conexão e tráfego na rede | IP e MAC podem aparecer na tabela de vizinhos |
| Acesso à página | O servidor recebe IP e informações enviadas pelo navegador |
| Envio com concordância | O programa grava horário, IP, navegador e apelido opcional |

**Visual:** linha do tempo com as três etapas. Use uma cor para “observado” e outra para “gravado”, mantendo essas palavras escritas.

**Fala sugerida:**

“O IP identifica o endereço usado na rede local. O MAC é um endereço apresentado pela interface de rede e pode ser aleatório, conforme o aparelho. A identificação do navegador, chamada User-Agent, pode trazer informações sobre o aplicativo e o sistema; não comprova a identidade da pessoa. Nosso comando de vizinhos apenas consulta a tabela do sistema: ele não grava o MAC no arquivo de participação.”

**Nota de precisão:** os dados do User-Agent podem variar e ser reduzidos pelo navegador. Veja a [documentação do cabeçalho User-Agent na MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/User-Agent).

## Slide 5 — Veja um exemplo de registro

**Tempo:** 1 minuto.

**Texto na tela:**

> **Exemplo fictício de um envio**
>
> Horário: 18:30 UTC
>
> IP local: 10.42.0.23
>
> Navegador: informações técnicas enviadas pelo aplicativo
>
> Apelido: Visitante Azul

**Visual:** ficha simples com os quatro campos. Mantenha “exemplo fictício” visível.

**Fala sugerida:**

“Este exemplo mostra os campos que o programa guarda no notebook. O horário é registrado em UTC. O arquivo não inclui um campo MAC. Esses dados também não são uma lista de mensagens, fotos ou senhas do celular.”

**Orientação para a equipe:** use a ficha fictícia como padrão de projeção. Para confirmar o funcionamento ao vivo, consulte os registros no notebook fora da projeção; evite abrir o arquivo real na tela compartilhada.

## Slide 6 — O mesmo texto, duas conexões

**Tempo:** 2 a 3 minutos, com o aparelho HTTPS preparado antes da apresentação.

**Texto na tela:**

> **HTTP:** o formulário aparece legível nos bytes da conexão.
>
> **HTTPS:** o conteúdo da aplicação viaja em registros TLS criptografados.
>
> O servidor de destino recebe a mensagem nos dois casos.

**Visual:** dois quadros lado a lado. Use o botão **Mostrar comparação no telão** para apresentar os resultados reais, após confirmar a projeção. O quadro HTTP mostra o formulário observado; o quadro HTTPS mostra uma amostra hexadecimal de um registro TLS criptografado. Ambos indicam a mensagem recebida pelo servidor.

**Condução pelo público:**

1. Com a demonstração real ativa, clique em **Preparar comparação** no painel.
2. Oriente o participante a abrir `http://10.42.0.1:8081/`, usar `OLA_TURMA`, marcar a concordância e enviar.
3. No aparelho previamente preparado com o certificado do laboratório, abra `https://10.42.0.1:8443/` e repita a mensagem com concordância.
4. Confira que os dois quadros exibem a mesma mensagem recebida antes de comparar os bytes.

**Condução pelo notebook:**

1. Clique em **Preparar comparação**, mesmo que a rede real esteja desligada.
2. Mantenha o texto fictício e clique em **Enviar pelo notebook (HTTP + HTTPS)**.
3. Confirme o registro e mostre os resultados no telão. Esse envio é real e valida o certificado HTTPS; não utiliza exemplos de criptografia simulados.

**Fala sugerida:**

“Enviamos o mesmo texto por duas conexões. Aqui observamos os bytes na entrada dos nossos servidores de teste, antes da descriptografia TLS. No HTTP conseguimos localizar o formulário. No HTTPS vemos registros criptografados. Depois de receber e descriptografar, o servidor lê a mensagem normalmente. IPs, portas e tamanhos continuam observáveis na comunicação.”

**Preparação do certificado:** a página HTTP oferece o download do certificado público de laboratório, válido por dois dias, e sua impressão SHA-256. Prepare o aparelho antes da fala, conferindo a impressão no painel. A cada nova comparação o certificado muda. Siga as instruções de Android/iPhone no [README.md](../README.md#certificado-https-no-celular); remova o certificado após a atividade. O notebook utiliza confiança restrita ao cliente do teste e não precisa dessa instalação.

**Precisão da explicação:** a observação é de fluxos TCP nos servidores da atividade, não de pacotes de todos os usuários da rede. Os arquivos `.bin` não são PCAP. O texto “Recebido pelo servidor” representa os dados no destino, enquanto os bytes exibidos representam a entrada da conexão. Não use a aparência hexadecimal sozinha como prova de criptografia: destaque também a negociação TLS efetivamente realizada e a comparação com o HTTP.

## Slide 7 — O que levamos dessa experiência?

**Tempo:** 1 a 2 minutos.

**Texto na tela:**

> Antes de conectar, confirme qual é a rede.
>
> Antes de enviar, entenda quais dados serão usados.
>
> Observe o endereço do site e a proteção da conexão.

**Pergunta ao público:** “Qual informação vocês não imaginavam que apareceria nessa comunicação?”

**Fala sugerida:**

“Nesta atividade, observamos informações da conexão e do acesso à nossa própria página. HTTPS protege o conteúdo da comunicação entre navegador e servidor, embora o servidor de destino ainda receba os dados enviados a ele. Nossa demonstração usa HTTP para tornar essa diferença parte da explicação. Agora podem sair da rede da atividade e remover a conexão salva no celular.”

**Nota de precisão:** HTTPS usa TLS para criptografar a comunicação entre cliente e servidor. Referência: [HTTPS na MDN](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS). O módulo de comparação observa os bytes TCP somente dos servidores de teste, antes da descriptografia TLS. O projeto não captura tráfego de outros sites.

## Preparação e condução — notas da equipe

### Antes de apresentar

Além do Wi-Fi, teste OpenSSL e prepare o certificado do aparelho que participará do HTTPS. Ensaie também o botão de envio pelo notebook.

1. Identifique a interface com `nmcli device status`. Nos exemplos abaixo, substitua `wlan0` pela interface correta.
2. Verifique suporte ao modo AP com `nmcli -f WIFI-PROPERTIES.AP device show wlan0`.
3. Para uma demonstração isolada, desconecte outras conexões de internet do notebook. O modo de compartilhamento pode distribuir uma conexão ativa de outra interface.
4. Inicie com `bash iniciar.sh wlan0`. O script pede privilégio administrativo e troca a conexão usada por essa interface.
5. Teste a página com um celular, incluindo um envio com apelido fictício. Separe registros de ensaio dos resultados da atividade, conforme o procedimento de retenção definido pela equipe.
6. Prepare capturas da página e a ficha fictícia do slide 5 para usar caso a rede falhe. Informe ao público quando estiver mostrando um exemplo preparado.

### Durante a atividade

- Uma pessoa conduz a fala e outra auxilia quem precisar conectar.
- Consulte `bash clientes.sh wlan0` no notebook da equipe. A lista pode ficar vazia até haver tráfego e não representa necessariamente todos os participantes.
- Confira `registros.jsonl` fora da projeção. Esse arquivo recebe os envios válidos no diretório do projeto.
- Mantenha a participação opcional; quem acompanha sem conectar também participa da discussão.

### Ao encerrar

- Pelo app, clique em **Encerrar dinâmica**; isso também fecha a comparação HTTP/HTTPS. Ao usar apenas os scripts, pressione `Ctrl+C` no terminal que iniciou a demonstração. O script tenta desativar e remover o perfil temporário; confirme o encerramento da rede.
- Oriente as pessoas a se desconectarem e removerem a rede salva.
- Remova os registros da apresentação quando não houver necessidade de mantê-los. O app tem botões separados para excluir dados da sessão e da comparação, após encerramento e confirmação. Encerrar o servidor não apaga `registros.jsonl`.

## Se houver espaço para apenas um slide

Use o título **“Dinâmica final: o que uma conexão revela?”** e este conteúdo:

> **Participação voluntária.** A rede pode observar IP e MAC; o servidor recebe IP e informações do navegador ao abrir a página.
>
> **Conecte:** EXTENSAO-REDE-ABERTA — sem senha.
>
> **Acesse:** http://10.42.0.1:8080
>
> **Escolha participar:** leia o aviso, use apelido fictício se desejar e envie com concordância. Só então o programa grava horário, IP, navegador e apelido opcional.

Mantenha o passo a passo projetado durante a prática. Explique os resultados e faça a pergunta de encerramento oralmente, usando as notas dos slides 4 a 7.
