MAC0242 - Relatório (Parte 1)
=============================

  - Integrantes:
    - (**7557797**) Gustavo Chicato Wandeur
    - (**8536065**) Leonardo Pereira Macedo
    - (**8536072**) Nikolai José Eustatios Kotsifas
    - (**4550300**) Rafael Tadaaki Higa


### Introdução

  A primeira parte deste projeto visou implementar um jogo (em modo texto) muito semelhante à primeira geração de Pokémon. A exibição se dá todo pelo terminal, sem interface gráfica, onde são recebidos ataques do usuário e exibidas mensagens com o resultado dos mesmos: qual foi o dano, se foi crítico, efetividade, etc. É possível selecionar alguns Pokémons (com atributos fiéis ao jogo original) e usá-los na batalha. Por meio do script de execução, também é possível sorteá-los aleatoriamente.


### Visão geral

  Por organização, naturalmente separamos o projeto em alguns diretórios.

###### doc/

  - ***Classes.dia***: Diagrama de classes desta fase do projeto. Feito no programa Dia. É importante notar que, embora alguns módulos (*batalha* e *main*) contenham funções sem classes, eles em si foram, por clareza, considerados como classes não instanciávels.
  - ***Classes.png***: Versão em imagem do anterior.
  - ***Etapa1.pdf***: O enunciado da primeira etapa.

###### pokemon/

  - Arquivos contendo dados de Pokémons a serem usados no jogo. Seguem o formato da especificação descrita pelo enunciado.
  
###### src/

  - ***main.py***: Módulo principal onde o programa é iniciado. Faz a leitura dos Pokémons e seus respectivos ataques, dos tipos e tabela de efetividade e, por fim, chama a batalha.
  - ***pokemon.py***: Contém as três principais classes desta fase. É importante notar que, ao invés de getters, estamos usando com o mesmo intuito nas classes a sintaxe *@property* do python, que permite acessar atributos de maneira direta e sem perder o encapsulamento.
    - *Pokemon*: Representa um Pokémon com seus atributos.
    - *Ataque*: Representa um ataque de Pokémon.
    - *Tipo*: Representa um dos possíveis tipos de ataque/Pokémon do jogo.
  - ***batalha.py***: Onde a magia acontece. Cuida do loop de batalha, verifica quem deve começar, recebe a escolha de ataque do usuário, checa se o ataque acertou e, finalmente, faz o cálculo do dano aplicando todos os bônus possíveis: *STAB*, crítico e efetividade. Por fim, também cuida de Struggle (se isso por alguma raridade vier a acontecer).
  - ***tipos.txt***: Arquivo contendo os tipos e tabela de efetividades.

###### test/

  - ***teste_pokemon.py***: Verifica se os Pokémons e seus respectivos ataques estão sendo gerados automaticamente, sem nenhuma anomalia nos atributos.
  - ***teste_batalha.py***: Simula uma batalha pelo recebimento um input "falso". Verifica se a batalha decorre normalmente e se não há nenhuma irregularidade com o dano, os ataques e efeitos subsequentes.
  - ***random_poke.py***: Gera um Pokémon aleatoriamente. Auxiliar dos outros módulos de teste.

  
### Simulação

  - Ao executar o programa, dois Pokémons são lidos conforme especificação do EP. Supõe-se que os atributos digitados estejam de acordo com o jogo (o nível deve estar entre 1 e 100, a acurácia de um ataque deve ser > 0, etc).
  - Logo em seguida, a batalha começa.
  - Nesta fase do projeto, o usuário tem controle sobre ambos os Pokémons. Solicita-se que digite o número correspondente ao ataque desejado. O ataque é feito, verifica-se se acertou e, caso positivo, calcula-se dano e bônus. As respectivas mensagens são exibidas na tela.
  - A batalha acaba quando um dos Pokémons for nocauteado. Ainda que raramente, pode haver empate devido ao *Struggle*, caso ocorra do Pokémon derrotar o oponente e perder o resto de seu HP usando-o.

#### Uso

  - O programa é executado chamando o script ***exeggcute***. Veja como executá-lo usando-o:

  **$ ./exeggcute -h**

#### Requerimentos

  - Nenhum módulo externo do Python3 foi utilizado.
  - Por precaução, prefirimos incluir o arquivo **mock.py**, dentro da pasta *test*, por ser utilizado pelo *Unittest*.
