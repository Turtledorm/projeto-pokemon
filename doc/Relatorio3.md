MAC0242 - Relatório (Parte 3)
=============================

  - Integrantes:
    - (**7557797**) Gustavo Chicato Wandeur
    - (**8536065**) Leonardo Pereira Macedo
    - (**8536072**) Nikolai José Eustatios Kotsifas
    - (**4550300**) Rafael Tadaaki Higa

### Introdução

  A terceira e última parte deste projeto buscou criar uma inteligência artificial para os Pokémons. A forma de implementação era livre e deveria ser usada tanto em batalhas locais quanto online.

### Visão geral

  Cita-se aqui os arquivos novos ou que sofreram grandes mudanças em relação à Etapa 2.

###### doc/

  - ***Etapa3.pdf***: O enunciado da terceira etapa.
  - ***requirements.txt***: Não foi usada nenhuma dependência nova em relação à fase anterior.
  - ***uml/Classes3.dia***: Diagrama de classes desta fase do projeto. Feito no programa Dia. É importante notar que, embora alguns módulos (*batalha* e *entrada*) contenham funções sem classes, eles em si foram, por clareza, considerados como classes não instanciáveis.
  - ***uml/Classes3.png***: Versão em imagem do anterior.

###### src/

  - ***main.py***: Módulo principal onde o programa é iniciado. Foram adicionados argumentos por linha de comando para tratar a inteligência artificial.
  - ***pokemon.py***: Sofreu uma boa refatoração, contendo agora apenas a classe Pokémon. As funções de escolher e realizar um ataque foram movidas do *batalha.py* para este módulo com o objetivo de reforçar a Orientação a Objetos.
  - ***batalha.py***: Por si só, cuida do loop de batalhas *locais*. Sofreu uma boa refatoração.
  - ***ataque.py***: Contém a classe Ataque (que pertencia antes a *pokemon.py*) e as funções anteriormente do módulo *batalha.py* relacionadas ao cálculo de dano.
  - ***tipo.py***: Possui a classe Tipo e a tabela de efetividade. Estava antes no *pokemon.py*.
  - ***cliente.py*** e ***servidor.py***: Juntos, eram o antigo *multiplayer.py* da Etapa 2. Administram, respectivamente, o lado *cliente* e *servidor* numa batalha online.
  - ***battle_state.py***: Contém as funções que criam e traduzem um objeto battle_state (XML). Na Etapa 2, faziam parte do *multiplayer.py*.
  - ***ia.py***: É o módulo mais inédito desta Etapa do projeto. Trata da inteligência artificial através de funções que determinam o melhor ataque a ser usado.

###### test/

  - ???

### Simulação

  Explicaremos aqui a lógica utilizada na inteligência artificial, já que as batalhas locais e online são idênticas às Etapas anteriores. A prioridade de ações da IA é a seguinte:

  1. Se todos os golpes estiverem sem PP, a única opção é Struggle.

  2. Quando o usuário estiver com menos de 1/5 do HP total, escolhe-se o golpe com maior potencial de dano, desconsiderando a acurácia (afinal, a chance de perder está próxima!). Fatores aleatórios como chance de crítico são desconsiderados, e o número aleatório usado na fórmula de dano será o mais baixo (0.85).

  3. Se **2** não ocorrer, então calcula-se o dano que cada golpe do usuário causará no defensor. A acurácia entra nas contas para determinar o "custo-benefício" dos golpes. Novamente, fatores aleatórios são ignorados. Depois disso, usa-se o melhor ataque analisado.

  4. Se o "custo-benefício" de mais de um ataque em **3** tem chance de nocautear o oponente, então escolhe-se o que possui maior acurácia. O critério de desempate, se necessário, é o golpe com maior PP.

  Durante a partida local/online, aparecerá *(CPU)* quando um Pokémon for controlado pela IA. Infelizmente, em batalhas pela Internet, não é possível saber se o oponente é humano ou máquina, pois o *battle_state* não possui um campo para tratar isso.

### Uso

  - Primeiramente, recomenda-se executar o ***pyenv***:

  **$ ./pyenv**

  - Este script automaticamente cria um virtualenv na pasta principal e instala as dependências citadas em *doc/requirements.txt*. Portanto, os diretórios *bin*, *include* e *lib* são resultado desse proceso.

  - O programa pode ser executado de diferentes formas dependendo do argumento passado ao script ***exeggcute***. Este também recebe nomes de Pokémon como argumento ou simplesmente sorteia-os aleatoriamente, caso não seja informado nenhum. Para melhores detalhes de como executar o script, faça:

  **$ ./exeggcute -h**
