"""Contém a classe do servidor."""

from flask import Flask, request
from werkzeug.exceptions import HTTPException

from entrada import le_pokemon
from battle_state import cria_bs, bs_to_poke
from batalha import quem_comeca, mostra_pokemons, acabou, resultado
from ataque import Ataque, get_struggle


class Trancado(HTTPException):
    """Exception para o erro 423: Locked."""
    code = 423
    description = "Locked"


class Servidor:
    """Representa o servidor na parte multiplayer."""

    def __init__(self, cpu):
        """Executa o programa no modo servidor."""
        self.conectado = False
        self.app = Flask(__name__)

        #-----------------------------------------
        # A seguir estão contidos os métodos POST
        #-----------------------------------------

        @self.app.route("/battle/", methods=["POST"])
        def recebe_cliente():
            """Recebe um objeto battle_state com o Pokémon
               do cliente e atualiza-o com os dados do servidor."""
            # Devolve erro 423 se outra batalha já está em andamento
            if self.conectado is True:
                return Trancado()

            # Indica que a conexão está estabelecida
            self.conectado = True

            # Lê o Pokémon do servidor
            self.poke_servidor = le_pokemon(cpu)

            # Convertemos o xml para um objeto Pokémon (do cliente)
            battle_state = request.data.decode("UTF-8")
            self.poke_cliente = bs_to_poke(battle_state)

            # Se servidor for jogar primeiro, já contabilizamos o ataque
            if quem_comeca(self.poke_servidor, self.poke_cliente) == \
                    self.poke_servidor:
                self.servidor_ataque()
            else:
                mostra_pokemons(self.poke_cliente, self.poke_servidor)

            return self.atualiza_bs()

        @self.app.route("/battle/attack/<int:id>", methods=["POST"])
        def contabiliza_ataques(id):
            """Recebe um id correspondente ao ataque do cliente.
               Contabiliza os ataques de cliente e servidor,
               devolvendo o resultado em um objeto battle_state."""
            self.poke_cliente.realiza_ataque(
                self.poke_cliente.get_ataque(id-1), self.poke_servidor)

            if not acabou(self.poke_cliente, self.poke_servidor):
                self.servidor_ataque()

            return self.atualiza_bs()

        @self.app.route("/shutdown/", methods=["POST"])
        def shutdown():
            """Fecha o servidor, encerrando a conexão."""
            func = request.environ.get("werkzeug.server.shutdown")
            if func is None:
                raise RuntimeError("ERRO: Não é um servidor Werkzeug.")
            func()
            return "Servidor finalizado."

    def servidor_ataque(self):
        """Contabiliza o ataque escolhido pelo servidor na batalha."""
        mostra_pokemons(self.poke_cliente, self.poke_servidor)
        ataque = self.poke_servidor.escolhe_ataque(self.poke_cliente)
        self.poke_servidor.realiza_ataque(ataque, self.poke_cliente)
        mostra_pokemons(self.poke_cliente, self.poke_servidor)

    def atualiza_bs(self):
        """Atualiza battle_state com estado atual dos Pokémons e o devolve.
           Caso batalha tenha terminado, exibe o resultado, """
        battle_state = cria_bs(self.poke_cliente, self.poke_servidor)

        if acabou(self.poke_cliente, self.poke_servidor):
            resultado(self.poke_cliente, self.poke_servidor)

        return battle_state
