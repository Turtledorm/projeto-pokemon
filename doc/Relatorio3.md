MAC0242 - Relatório (Parte 3)
=============================

  - Integrantes:
    - (**7557797**) Gustavo Chicato Wandeur
    - (**8536065**) Leonardo Pereira Macedo
    - (**8536072**) Nikolai José Eustatios Kotsifas
    - (**4550300**) Rafael Tadaaki Higa

### Introdução

  A terceira e última parte deste tão aguardado (nem por todos) projeto buscou criar uma inteligência artificial que simulasse satisfatoriamente a ação humana numa batalha entre Pokémons. A forma de implementação seria livre e deveria ser montada de modo a funcionar tanto em batalhas locais quanto online.

### Visão geral

  Citaremos aqui um resumo geral dos arquivos do projeto, bem como as principais modificações ocorridas na etapa 3.

###### doc/

  - ***Etapa{1,2,3}.pdf***: Enunciados das etapas.
  - ***requirements.txt***: Dependências das quais o programa necessita. Não foi usada nenhuma nova em relação à fase anterior.
  - ***uml/Classes{1,2,3}.dia***: Diagramas de classes das fases do projeto. Feitas no programa Dia. É importante notar que, embora alguns módulos (*batalha* e *entrada*, por exemplo) contenham funções sem classes, eles em si foram, por clareza, considerados como classes não instanciáveis.
  - ***uml/Classes{1,2,3}.png***: Versão em imagem dos diagramas.

###### src/

  - ***main.py***: Módulo principal onde o programa é iniciado. Recebe argumentos por linha de comando que possibilitam escolher entre jogo local, cliente ou servidor, bem como entre jogadores humanos e CPU.
  - ***pokemon.py***: Sofreu uma boa refatoração, contendo agora apenas a classe Pokémon. As funções de escolher e realizar um ataque foram movidas do *batalha.py* para este módulo com o objetivo de reforçar a POO.
  - ***ataque.py***: Contém a classe Ataque (que pertencia antes a *pokemon.py*) e as funções anteriormente do módulo *batalha.py* relacionadas ao cálculo de dano.
  - ***tipo.py***: Possui a classe Tipo e a tabela de efetividades.
  - ***batalha.py***: Cuida do desenrolar da batalha, decidindo quem começa, imprimindo resultados na tela, verificando se o jogo terminou, etc.
  - ***cliente.py*** e ***servidor.py***: Juntos, eram o antigo *multiplayer.py* da Etapa 2. Administram, respectivamente, o lado *cliente* e *servidor* numa batalha online.
  - ***battle_state.py***: Contém as funções que criam e traduzem um objeto battle_state (XML).
  - ***ia.py***: Atração principal desta etapa do projeto. Trata da inteligência artificial (IA) do CPU, determinando de forma inteligente o melhor ataque a ser usado. Para mais detalhes, ver a seção logo abaixo.

###### test/

  - <to be continued> ???

### Inteligência Artificial

  Explicaremos aqui a lógica utilizada na inteligência artificial, já que as batalhas locais e online entre seres humanos são idênticas às etapas anteriores. Para as ações da IA são levados em conta os seguintes detalhes:

  - O dano total *esperado* será o dano base do ataque (*PWR*), aplicado os modificadores de efetividade e STAB.
  - Serão desconsiderados fatores randômicos, ou seja, a chance de crítico, e o modificador aleatório será estipulado como o mínimo possível (0.85)

  Tendo isso em mente, a escolha do melhor ataque segue a seguinte ordem de prioridade:

  **1.** Se todos os golpes estiverem sem PP, a única opção é Struggle.

  **2.** Quando o usuário estiver com menos de 1/5 do HP total, escolhe-se o golpe com maior potencial de dano, desconsiderando a acurácia (afinal, a chance de perder no próximo turno é grande!).

  **3.** Se ***2*** não ocorrer, então calcula-se o dano que cada golpe do usuário causará no defensor. O produto do dano pela acurácia de cada ataque resultará no "custo-benefício" do golpe. Assim, escolher-se-á o que possuir maior valor.

  **4.** Se o "custo-benefício" de mais de um ataque em **3** tem chance de nocautear o oponente, então será usado o que possuir maior acurácia. O critério de desempate, se necessário, é o golpe com maior PP.

### Uso

  - Primeiramente, recomenda-se executar o ***pyenv***:

  **$ ./pyenv**

  - Este script automaticamente cria um virtualenv na pasta principal e instala as dependências citadas em *doc/requirements.txt*. Portanto, os diretórios *bin*, *include* e *lib* são resultado deste processo.

  - O programa pode ser executado de diferentes formas dependendo do argumento passado ao script ***exeggcute***. Este também recebe nomes de Pokémon como argumento ou simplesmente sorteia-os aleatoriamente, caso não seja informado nenhum. Para melhores detalhes de como executar o script, faça:

  **$ ./exeggcute -h**
