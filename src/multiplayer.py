"""Funções relacionadas à interação cliente-servidor"""

import requests
from flask import Flask, request, abort

from entrada import le_pokemon
from batalha import batalha, escolhe_ataque, realiza_ataque, \
    quem_comeca, mostra_pokemons, resultado
from pokemon import Pokemon, Ataque
from bs4 import BeautifulSoup

app = Flask(__name__)

poke_server = None
poke_cliente = None
server_ip = None

@app.route("/battle/", methods=["POST"])
def inicia_servidor():
    global poke_server, poke_cliente

    # Convertemos o xml para um objeto Pokémon
    poke_cliente = bs_to_poke(request.data)

    poke_server = le_pokemon()

    # Se servidor for jogar primeiro, já contabilizamos o ataque
    if quem_comeca(poke_server, poke_cliente) == poke_server:
        server_ataque()
        if poke_cliente.hp <= 0 or poke_server.hp <= 0:
            resultado(poke_cliente, poke_server)
    else:
        mostra_pokemons(poke_cliente, poke_server)

    # Atualizamos o battle_state com os dados do Pokémon do cliente
    battle_state = cria_bs(poke_cliente, poke_server)

    # Descobrir qual condição devemos colocar aqui
    if False:
        abort(423)

    return battle_state


@app.route("/battle/attack/<int:id>", methods=["POST"])
def ataque(id):
    global poke_cliente, poke_server

    # Realiza os ataques do cliente e do servidor
    realiza_ataque(poke_cliente, poke_server, poke_cliente.get_ataque(id))
    if poke_cliente.hp > 0 and poke_server.hp > 0:
        server_ataque()
        # Modificamos o battle_state com ambos os ataques contabilizados
        battle_state = cria_bs(poke_cliente, poke_server)
    else:
        resultado(poke_cliente, poke_server)

    if poke_cliente.hp <= 0 or poke_server.hp <= 0:
        resultado(poke_cliente, poke_server)

    return battle_state


def cria_bs(poke1, poke2=None):
    xml = ('<?xml version="1.0" encoding="utf-8"?>'
           + "<battle_state>"
           + poke1.to_xml())
    if poke2 is not None:
        xml += poke2.to_xml()
    xml += "</battle_state>"
    return xml


def cliente_init(poke):
    global poke_cliente, poke_server
    battle_state = cria_bs(poke)

    try:
        
        bs = requests.post("http://" + ip + ":5000/battle/", data=battle_state)
    except requests.exceptions.ConnectionError:
        print("Não foi possível se conectar ao servidor!")
        exit(1)

    cliente_temp, poke_server = bs_to_poke(bs.text)
    poke_cliente.hp = cliente_temp.hp


def cliente_ataque():
    global poke_cliente, poke_server

    # Cliente escolhe seu ataque
    mostra_pokemons(poke_server, poke_cliente)
    id = escolhe_ataque(poke_cliente)
    id = poke_cliente.ataques.index(id)

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
    poke_cliente.get_ataque(id).usa_pp()


def server_ataque():
    global poke_cliente, poke_server

    mostra_pokemons(poke_cliente, poke_server)
    ataque = escolhe_ataque(poke_server)
    realiza_ataque(poke_server, poke_cliente, ataque)


def bs_to_poke(battle_state):
    """Retorna até dois objetos Pokémon cujos dados estão no battle_state"""
    battle_state = str(battle_state)
    xml = battle_state.split('</pokemon>', 1)  # O primeiro poke no xml[0]
    data_poke1 = xml_to_poke(xml[0])
    if len(xml[1]) > 100:  # Caso tenha vindo 2 pokes no battle_state
        data_poke2 = xml_to_poke(xml[1])
        return Pokemon(data_poke1), Pokemon(data_poke2)
    return Pokemon(data_poke1)


def xml_to_poke(xml):
    """Recebe uma string xml e devolve uma lista de dados do Pokémon"""
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
    global poke_cliente, poke_server, ip
    poke_cliente = le_pokemon()
    ip = input("Digite o endereço IP do servidor: ")
    cliente_init(poke_cliente)

    while True:
        if poke_cliente.hp <= 0 or poke_server.hp <= 0:
            break
        cliente_ataque()

    mostra_pokemons(poke_server, poke_cliente)
    resultado(poke_cliente, poke_server)


def programa_server():
    app.debug = True
    app.run(host="0.0.0.0")


