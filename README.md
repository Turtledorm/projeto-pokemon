MAC0242 - Relatório (Parte 1)
=============================

  - Integrantes:
    - (**7557797**) Gustavo Chicato Wandeur
    - (**8536065**) Leonardo Pereira Macedo
    - (**8536072**) Nikolai J. Kotsifas
    - (**4550300**) Rafael Tadaaki Higa

Introdução
----------
  O objetivo principal desta parte foi implementar um jogo (em modo texto) muito semelhante à primeira geração de Pokémon.

Resumo do que foi feito
-----------------------
  - Esboço do diagrama de classes com o objetivo de ter um planejamento inicial.
  - Iniciou-se o projeto com dois módulos:
      - **main**: Responsável por ler os Pokémons e ataques, inicializando o programa.
      - **pokemon**: Possui as classes *Pokemon* e *Ataque*.
  - Diretório "test" criado. Uso do Unittest em *test_pokemon*.
  - Criação do terceiro e último módulo, **batalha**.
  - Uso do arquivo "tipos.txt" para guardar os tipos e a tabela de efetividade.
  - Definição de uma nova classe *Tipo* no módulo **pokemon**.
  - Uso de **@properties** como getters mais eficientes.
  - Criação do script "exeggcute" para facilitar a execução do programa.
  - Implementação de *Struggle* como um "golpe extra" no módulo **batalha**.
  - Possibilidade de empate implementada devido ao *Struggle*.
  - Limpeza no código e no output.
  - Atualização e ênfase nos módulos de teste.
  - Atualização do diagrama de classes.
 
Simulação
---------
  - Ao executar o programa, a batalha começará após os 2 Pokémons serem lidos de acordo com a especificação do EP.
  - Supõe-se que os atributos digitados estejam de acordo com o jogo (o nível deve estar entre 1 e 100, a acurácia de um ataque deve ser > 0, etc.).
  - Nesta fase do projeto, o usuário tem controle sobre ambos os Pokémons ao digitar o número correspondente ao ataque desejado.
  - A batalha acaba quando pelo menos um dos Pokémons for nocauteado.
  - Pode haver empate devido ao *Struggle*, que foi implementado de acordo com a 1ª geração do jogo.

Uso
---
  - O programa é executado chamando o arquivo "main.py", localizado na pasta "src". Não há nenhum argumento por linha de comando.
  - Para evitar ter que escrever valores ao rodar o programa, criou-se o script "exeggcute".
  - Recomenda-se seu uso para simplificar a execução do programa. Veja como rodá-lo usando:

  **$ ./exeggcute -h**

Requirements
------------
  - Nenhum módulo externo do Python3 foi utilizado.
  - Por precaução, prefirimos incluir o arquivo **mock.py**, usado na pasta *test*, por ser utilizado pelo Unittest.
