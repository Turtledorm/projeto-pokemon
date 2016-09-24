"""Contém a classe do cliente."""

import requests

from entrada import le_pokemon
from batalha import mostra_pokemons, resultado, acabou
from battle_state import cria_bs, bs_to_poke


class Cliente:
    """Representa o cliente no jogo multiplayer."""

    def __init__(self, cpu):
        """Lê o Pokémon do cliente e o endereço do servidor."""
        self.poke_cliente = le_pokemon(cpu)
        self.cpu = cpu

        ip = input("Digite o endereço IP do servidor: ")
        if ip == "":
            ip = "127.0.0.1"
        try:
            porta = int(input("Digite a porta de conexão: "))
        except ValueError:
            porta = 5000
        self.servidor = ip + ":" + str(porta)
        print("Endereço do servidor:", self.servidor)

    def conecta_ao_servidor(self):
        """Envia um objeto battle_state com dados do cliente ao servidor."""
        bs = cria_bs(self.poke_cliente)

        try:
            # Faz uma requisição POST e recebe battle_state modificado
            resp = requests.post("http://" + self.servidor + "/battle/", bs)
            resp.raise_for_status()  # Verificação de erros HTTP
            bs = resp.text

        except requests.exceptions.ConnectionError:
            print("ERRO: Não foi possível se conectar ao servidor.")
            exit(1)

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 423:
                print("ERRO: [423] Já há uma partida em execução no servidor.")
            else:
                print("ERRO: Não foi possível completar a requisição.")
            exit(1)

        self.poke_cliente, self.poke_servidor = bs_to_poke(bs, self.cpu)

    def loop(self):
        """Executa o loop de batalha com o servidor."""
        while not acabou(self.poke_cliente, self.poke_servidor):
            self.jogada()
        self.finaliza()

    def jogada(self):
        """Envia a escolha de ataque do cliente ao servidor."""
        # Cliente escolhe seu ataque e obtém-se o id deste
        mostra_pokemons(self.poke_servidor, self.poke_cliente)
        id = self.poke_cliente.escolhe_ataque(self.poke_servidor)
        id = self.poke_cliente.ataques.index(id) + 1

        # Faz o envio da escolha ao servidor
        try:
            print("Esperando resposta do servidor...")
            resp = requests.post("http://" + self.servidor + "/battle/attack/"
                                 + str(id))
        except requests.exceptions.ConnectionError:
            print("ERRO: A conexão com o servidor foi desfeita.")
            exit(1)

        # Atualiza dados do cliente
        self.poke_cliente, self.poke_servidor = bs_to_poke(resp.text)

    def finaliza(self):
        """Mostra o resultado da batalha e fecha o servidor."""
        mostra_pokemons(self.poke_servidor, self.poke_cliente)
        resultado(self.poke_servidor, self.poke_cliente)

        # Envia pedido para fechar o servidor
        requests.post("http://" + self.servidor + "/shutdown/")
