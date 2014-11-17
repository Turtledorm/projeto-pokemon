"""Funções relacionadas à interação cliente-servidor."""

import requests
from flask import Flask, request, abort

from entrada import le_pokemon
from batalha import batalha, escolhe_ataque, realiza_ataque, \
    quem_comeca, mostra_pokemons, resultado, struggle
from pokemon import Pokemon, Ataque
from bs4 import BeautifulSoup

# Instância do Flask
app = Flask(__name__)

# Variáveis globais para os Pokémons do cliente e servidor
poke_server = None
poke_cliente = None


@app.route("/battle/", methods=["POST"])
def inicia_servidor():
    """Recebe um objeto battle_state com o Pokémon do cliente
    e atualiza-o com os dados do servidor."""
    global poke_server, poke_cliente

    poke_server = le_pokemon()

    # Convertemos o xml para um objeto Pokémon
    poke_cliente = bs_to_poke(request.data)

    # Se servidor for jogar primeiro, já contabilizamos o ataque
    if quem_comeca(poke_server, poke_cliente) == poke_server:
        server_ataque()
        mostra_pokemons(poke_cliente, poke_server)
        if poke_cliente.hp <= 0 or poke_server.hp <= 0:
            resultado(poke_cliente, poke_server)

    # Atualizamos o battle_state com os dados do Pokémon do cliente
    battle_state = cria_bs(poke_cliente, poke_server)

    # Descobrir qual condição devemos colocar aqui
    if False:
        abort(423)

    return battle_state


@app.route("/battle/attack/<int:id>", methods=["POST"])
def ataque(id):
    """Contabiliza os ataques escolhidos dos dois jogadores,
       retornando o resultado em um objeto battle_state."""
    global poke_cliente, poke_server

    if id != 0:
        realiza_ataque(poke_cliente, poke_server,
                       poke_cliente.get_ataque(id-1))
    else:
        # Caso especial: Struggle
        realiza_ataque(poke_cliente, poke_server, struggle)

    if poke_cliente.hp > 0 and poke_server.hp > 0:
        server_ataque()

    # Modificamos o battle_state com ambos os ataques contabilizados
    battle_state = cria_bs(poke_cliente, poke_server)

    if poke_cliente.hp <= 0 or poke_server.hp <= 0:
        resultado(poke_cliente, poke_server)

    return battle_state


@app.route("/shutdown/", methods=["POST"])
def shutdown():
    """Fecha o servidor."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Não é um servidor Werkzeug!")
    func()
    return "Server finalizado!"


def cria_bs(poke1, poke2=None):
    """Cria um xml battle_state com dados de até dois Pokémons."""
    xml = ('<?xml version="1.0" encoding="utf-8"?>'
           + "<battle_state>"
           + poke1.to_xml())
    if poke2 is not None:
        xml += poke2.to_xml()
    xml += "</battle_state>"
    return xml


def cliente_init(poke):
    """Envia um objeto battle_state com dados do cliente ao servidor."""
    global poke_cliente, poke_server

    battle_state = cria_bs(poke)
    try:
        bs = requests.post("http://" + ip + ":5000/battle/", data=battle_state)
        bs.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Não foi possível se conectar ao servidor!")
        exit(1)

    cliente_temp, poke_server = bs_to_poke(bs.text)
    poke_cliente.hp = cliente_temp.hp


def cliente_ataque():
    """Envia a escolha de ataque do cliente ao servidor."""
    global poke_cliente, poke_server

    # Cliente escolhe seu ataque
    mostra_pokemons(poke_server, poke_cliente)
    id = escolhe_ataque(poke_cliente)
    if id not in poke_cliente.ataques:
        print("id = struggle")
        id = 0
    else:
        id = poke_cliente.ataques.index(id) + 1

    # Tenta mandar a escolha ao servidor
    try:
        print("Esperando resposta do servidor...")
        bs = requests.post("http://" + ip + ":5000/battle/attack/" + str(id))
    except requests.exceptions.ConnectionError:
        print("A conexão com o servidor caiu!")
        exit(1)

    # Atualiza dados do cliente
    cliente_temp, server_temp = bs_to_poke(bs.text)
    poke_cliente.hp = cliente_temp.hp
    poke_server.hp = server_temp.hp
    if id > 0:
        poke_cliente.get_ataque(id-1).usa_pp()


def server_ataque():
    """Contabiliza o ataque escolhido pelo servidor na batalha."""
    global poke_cliente, poke_server

    mostra_pokemons(poke_cliente, poke_server)
    ataque = escolhe_ataque(poke_server)
    realiza_ataque(poke_server, poke_cliente, ataque)


def bs_to_poke(battle_state):
    """Retorna até dois objetos Pokémon cujos dados estão no battle_state."""
    battle_state = str(battle_state)

    # Converte o primeiro Pokémon em xml[0]
    xml = battle_state.split("</pokemon>", 1)
    data_poke1 = xml_to_poke(xml[0])

    # Segundo Pokémon
    if len(xml[1]) > 100:
        data_poke2 = xml_to_poke(xml[1])
        return Pokemon(data_poke1), Pokemon(data_poke2)

    return Pokemon(data_poke1)


def xml_to_poke(xml):
    """Recebe uma string xml e devolve uma lista de dados do Pokémon."""
    data = BeautifulSoup(xml)  # Objeto que representa o xml
    # Pega todos os atributos do pokemon e separa por linhas
    data = data.pokemon.get_text("\n")
    data = data.split("\n")
    # Converte o que for número de str para int
    data = [int(n) if n.isdigit() else n for n in data]

    # Agora vamos criar os objetos Ataque:

    # Contém todos os campos de cada ataque (nome, acu, pwr, pp etc)
    ataques = data[9:]

    i = 0
    while i < len(ataques) - 5:
        ataques.pop(i)  # Remove o id
        # Troca as posições do acu e pwr para ficar como o esperado por Ataque
        aux = ataques[2 + i]
        ataques[2 + i] = ataques[3 + i]
        ataques[3 + i] = aux
        i += 5

    # Contém todo o resto que não é ataque
    data = data[:9]
    num_atributos_ataque = 5  # Cada ataque tem 5 itens na lista
    num_atks = len(ataques) / num_atributos_ataque
    lista_ataques = []
    for i in range(int(num_atks)):
        ataque = []
        for j in range(num_atributos_ataque):
            ataque.append(ataques.pop(0))
        lista_ataques.append(Ataque(ataque))
    data.append(lista_ataques)
    return data


# -------------------------------------------------------------------


def programa_cliente():
    """Executa o programa no modo cliente."""
    global poke_cliente, poke_server, ip

    poke_cliente = le_pokemon()
    ip = input("Digite o endereço IP do servidor: ")

    cliente_init(poke_cliente)
    while poke_cliente.hp > 0 and poke_server.hp > 0:
        cliente_ataque()

    mostra_pokemons(poke_server, poke_cliente)
    resultado(poke_cliente, poke_server)

    # Envia pedido para fechar o servidor
    requests.post("http://" + ip + ":5000/shutdown/")


def programa_server():
    """Executa o programa no modo servidor."""
    try:
        app.run(host="0.0.0.0", debug=True)
    except OSError:
        print("Endereço do server já em uso!")
