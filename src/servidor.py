"""Classe que representa o servidor na parte multiplayer."""

from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException

from entrada import le_pokemon
from battle_state import cria_bs, bs_to_poke
from batalha import quem_comeca, mostra_pokemons, escolhe_ataque, \
    acabou, resultado
from pokemon import Pokemon, Ataque


class Trancado(HTTPException):
    """Exception para o erro 423: Locked"""
    code = 423
    description = "Locked"


class Servidor:
    """ ??? """

    def __init__(self):
        """Executa o programa no modo servidor."""
        self.conectado = False
        self.app = Flask(__name__)

        @self.app.route("/battle/", methods=["POST"])
        def recebe_cliente():
            """Recebe um objeto battle_state com o Pokémon do cliente
            e atualiza-o com os dados do servidor."""

            # Verifica se outra batalha está em andamento
            if self.conectado is True and \
               self.app.config['TESTING'] is not True:
                return Trancado()

            # Indica que a conexão está estabelecida
            self.conectado = True

            # Lê o Ṕokémon do servidor
            self.poke_servidor = le_pokemon()

            # Convertemos o xml para um objeto Pokémon (do cliente)
            self.poke_cliente = bs_to_poke(request.data)

            # Se servidor for jogar primeiro, já contabilizamos o ataque
            if quem_comeca(self.poke_servidor, self.poke_cliente) == \
               self.poke_servidor:
                self.servidor_ataque()
                if acabou(self.poke_cliente, self.poke_servidor):
                    resultado(self.poke_cliente, self.poke_servidor)
            else:
                mostra_pokemons(self.poke_cliente, self.poke_servidor)

            # Atualizamos o battle_state com os dados do Pokémon do cliente
            battle_state = cria_bs(self.poke_cliente, self.poke_servidor)

            return battle_state

        @self.app.route("/battle/attack/<int:id>", methods=["POST"])
        def contabiliza_ataques(id):
            """Recebe um id correspondente ao ataque do cliente.
               Contabiliza os ataques de cliente e servidor,
               devolvendo o resultado em um objeto battle_state."""

            if id != 0:
                self.poke_cliente.realiza_ataque(self.poke_cliente.get_ataque(id-1), self.poke_servidor)
            else:
                # Caso especial: Struggle
                struggle = Ataque(["Struggle", 0, 100, 50, 10])
                self.poke_cliente.realiza_ataque(struggle, self.poke_servidor)

            if not acabou(self.poke_cliente, self.poke_servidor):
                self.servidor_ataque()

            # Modificamos o battle_state com ambos os ataques contabilizados
            battle_state = cria_bs(self.poke_cliente, self.poke_servidor)

            if acabou(self.poke_cliente, self.poke_servidor):
                resultado(self.poke_cliente, self.poke_servidor)

            return battle_state

        @self.app.route("/shutdown/", methods=["POST"])
        def shutdown():
            """Fecha o servidor."""
            func = request.environ.get("werkzeug.server.shutdown")
            if func is None:
                raise RuntimeError("Não é um servidor Werkzeug!")
            func()
            return "Servidor finalizado!"

    def servidor_ataque(self):
        """Contabiliza o ataque escolhido pelo servidor na batalha."""
        mostra_pokemons(self.poke_cliente, self.poke_servidor)
        ataque = escolhe_ataque(self.poke_servidor, self.poke_cliente) 
        self.poke_servidor.realiza_ataque(ataque, self.poke_cliente)
        mostra_pokemons(self.poke_cliente, self.poke_servidor)
