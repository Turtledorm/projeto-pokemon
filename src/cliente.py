"""Classe que representa o cliente na parte multiplayer."""

import requests

from entrada import le_pokemon
from pokemon import Pokemon, Ataque
from batalha import escolhe_ataque, mostra_pokemons, resultado, acabou
from battle_state import cria_bs, bs_to_poke


class Cliente:
    """ ??? """

    def __init__(self):
        """Lê o Pokémon do cliente o endereço do servidor."""
        self.poke_cliente = le_pokemon()

        ip = input("Digite o endereço IP do servidor: ")
        if ip == "":
            ip = "localhost"
        try:
            port = int(input("Digite a porta de conexão: "))
        except ValueError:
            port = 5000
        self.servidor = ip + ":" + str(port)

    def conecta_servidor(self):
        """Envia um objeto battle_state com dados do cliente ao servidor."""
        battle_state = cria_bs(self.poke_cliente)

        try:
            bs = requests.post("http://" + self.servidor + "/battle/",
                               data=battle_state)
            bs.raise_for_status()

        except requests.exceptions.ConnectionError:
            print("Não foi possível se conectar ao servidor!")
            exit(1)

        except requests.exceptions.HTTPError:
            print("Já existe um jogo em andamento no servidor!")
            exit(1)

        cliente_temp, self.poke_servidor = bs_to_poke(bs.text)
        self.poke_cliente.hp = cliente_temp.hp

    def jogada(self):
        """Envia a escolha de ataque do cliente ao servidor."""

        # Cliente escolhe seu ataque
        mostra_pokemons(self.poke_servidor, self.poke_cliente)
        id = escolhe_ataque(self.poke_cliente, self.poke_servidor)
        if id not in self.poke_cliente.ataques:
            id = 0
        else:
            id = self.poke_cliente.ataques.index(id) + 1

        # Tenta mandar a escolha ao servidor
        try:
            print("Esperando resposta do servidor...")
            bs = requests.post("http://" + self.servidor + "/battle/attack/"
                               + str(id))
        except requests.exceptions.ConnectionError:
            print("A conexão com o servidor caiu!")
            exit(1)

        # Atualiza dados do cliente
        cliente_temp, servidor_temp = bs_to_poke(bs.text)
        self.poke_cliente.hp = cliente_temp.hp
        self.poke_servidor.hp = servidor_temp.hp
        if id > 0:
            self.poke_cliente.get_ataque(id-1).usa_pp()

    def acabou_batalha(self):
        """Verifica se algum dos Pokémons foi nocauteado."""
        return acabou(self.poke_servidor, self.poke_cliente)

    def finaliza(self):
        """Mostra o resultado da batalha e fecha o servidor."""
        mostra_pokemons(self.poke_servidor, self.poke_cliente)
        resultado(self.poke_servidor, self.poke_cliente)

        # Envia pedido para fechar o servidor
        requests.post("http://" + self.servidor + "/shutdown/")
