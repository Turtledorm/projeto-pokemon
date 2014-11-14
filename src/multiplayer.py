"""Funções relacionadas à interação cliente-servidor"""

import requests
from flask import Flask, request, abort

from entrada import le_pokemon
from batalha import batalha, escolhe_ataque, realiza_ataque
from pokemon import Pokemon

app = Flask(__name__)

# Cria Pokémon inicial
poke_server = poke_cliente = None


@app.route("/battle/", methods=["POST"])
def inicia_servidor():
    # Convertemos o xml para um objeto Pokémon
    # poke_cliente = xml_to_poke(request.data)

    poke_server = le_pokemon()

    # Se servidor for jogar primeiro, já contabilizamos o ataque
    server_ataque()

    # Atualizamos o battle_state com os dados do Pokémon do cliente
    battle_state = cria_bs(poke_server, poke_cliente)

    # Descobrir qual condição devemos colocar aqui
    if False:
        abort(423)

    return battle_state


@app.route("/battle/attack/<int:id>", methods=["POST"])
def ataque(id):
    # Realiza os ataques do cliente e do servidor
    realiza_ataque(poke_cliente, poke_server, poke_cliente.get_ataque(id))
    server_ataque()

    # Modificamos o battle_state com ambos os ataques contabilizados
    battle_state = cria_bs(poke1, poke2)

    return battle_state


def cria_bs(poke1, poke2=None):
    xml = ('<?xml version="1.0" encoding="utf-8"?>'
           + "<battle_state>"
           + poke1.to_xml())
    if poke2 is not None:
        xml += poke2.to_xml
    xml += "</battle_state>"
    return xml


def cliente_init(poke):
    # payload = {'key1': 'value1', 'key2': 'value2'}
    battle_state = cria_bs(poke)
    requests.post("http://127.0.0.1:5000/battle/", data=battle_state)


def cliente_ataque():
    id = escolhe_ataque(poke_cliente)
    bs = requests.post("http://127.0.0.1:5000/battle/attack/" + str(id))
    # atualiza_pokemons(bs)


def server_ataque():
    ataque = escolhe_ataque(poke_server)
    realiza_ataque(poke_server, poke_cliente, ataque)

# -------------------------------------------------------------------


def programa_cliente():
    poke_cliente = le_pokemon()
    cliente_init(poke_cliente)


def programa_server():
    app.debug = True
    app.run()
