MAC0242 - Relatório (Parte 2)
=============================

  - Integrantes:
    - (**7557797**) Gustavo Chicato Wandeur
    - (**8536065**) Leonardo Pereira Macedo
    - (**8536072**) Nikolai José Eustatios Kotsifas
    - (**4550300**) Rafael Tadaaki Higa

### Introdução

  A segunda parte deste projeto teve como objetivo a implementação de batalhas online com base no que já foi desenvolvido. Dois jogadores podem ter uma partida de 1x1 via web no modelo Cliente/Servidor.

### Visão geral

  Cita-se aqui os arquivos novos ou que sofreram grandes mudanças em relação à Etapa 1.

###### doc/

  - ***Etapa2.pdf***: O enunciado da segunda etapa.
  - ***requirements.txt***: Dependências do programa a serem instaladas pelo pip.
  - ***uml/Classes2.dia***: Diagrama de classes desta fase do projeto. Feito no programa Dia. É importante notar que, embora alguns módulos (*batalha* e *entrada*) contenham funções sem classes, eles em si foram, por clareza, considerados como classes não instanciáveis.
  - ***uml/Classes2.png***: Versão em imagem do anterior.

###### src/

  - ***main.py***: Módulo principal onde o programa é iniciado. Apenas trata os argumentos por linha de comando, isto é, a escolha de rodar o programa como cliente ou servidor.
  - ***entrada.py***: Faz a leitura dos Pokémons e de seus respectivos ataques, dos tipos e da tabela de efetividade. Era o antigo *main.py* da Etapa 1.
  - ***pokemon.py***: Praticamente igual à Etapa 1. As adições mais importantes foram duas funções para converter um objeto Pokémon em uma string xml.
  - ***batalha.py***: Por si só, cuida do loop de batalhas *locais*. No entanto, suas funções são utilizadas para partidas *online*, como verificar quem deve começar, receber a escolha de ataque do usuário, etc.
  - ***multiplayer.py***: O astro do show nessa Etapa 2. Cuida de batalhas online, administrando a partida entre servidor (métodos POST) e cliente (requisições). Também possui funções adicionais para lidar com as conversões XML.

###### test/

  - ***teste_multiplayer.py***: Testa execução do cliente e do servidor, bem como verificação das strings XML.

### Simulação

  Explicaremos aqui a execução como cliente-servidor, já que as batalhas locais são idênticas à Etapa 1.
  - ***Inicialização como servidor***: O servidor é aberto, aguardando pelo cliente.
  - ***Inicialização como cliente***: O Pokémon do jogador é recebido via entrada padrão. Após ler o IP do servidor, o Pokémon do cliente é convertido em uma string correspondente ao battle_state e enviado por uma requisição POST ao servidor.
  - Ao receber os dados do cliente, o servidor tem seu Pokémon lido e, se for mais rápido, já contabiliza seu ataque.
  - O battle_state atualizado contendo os dois Pokémons é retornando ao cliente. Este escolhe seu ataque e o envia para o servidor.
  - Tal processo continua até um dos Pokémons ser nocauteado.
  - Imprime-se uma mensagem para os jogadores, informando o resultado da partida. O servidor é encerrado e ambos os programas terminam.

  Se houver algum erro durante a conexão do cliente ao servidor, imprime-se uma notificação e o cliente é encerrado.

### Uso

  - Primeiramente, recomenda-se executar o ***pyenv***:

  **$ ./pyenv**

  - Este script automaticamente cria um virtualenv na pasta principal e instala as dependências citadas em *doc/requirements.txt*. Portanto, os diretórios *bin*, *include* e *lib* são resultado desse proceso.

  - O programa pode ser executado de diferentes formas dependendo do argumento passado ao script ***exeggcute***. Este também recebe nomes de Pokémon como argumento ou simplesmente sorteia-os aleatoriamente, caso não seja informado nenhum. Para melhores detalhes de como executar o script, faça:

  **$ ./exeggcute -h**
