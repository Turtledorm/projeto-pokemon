"""Funções relacionadas à interação cliente-servidor"""

import requests
from flask import Flask, request, abort

from entrada import le_pokemon
from batalha import batalha, escolhe_ataque, realiza_ataque
from pokemon import Pokemon, Ataque
from bs4 import BeautifulSoup

app = Flask(__name__)

# Cria Pokémon inicial
poke_server  = None
poke_cliente = None


@app.route("/battle/", methods=["POST"])
def inicia_servidor():
    # Convertemos o xml para um objeto Pokémon
    poke_cliente = bs_to_poke(request.data)
    
    #Afim de não criar uma nova poke_server só no escopo dessa função 
    global poke_server, poke_cliente
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
        xml += poke2.to_xml()
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
    global poke_cliente
    ataque = escolhe_ataque(poke_server)
    realiza_ataque(poke_server, poke_cliente, ataque)

"""Se battle_state tem um pokemon representado em xml, retorna esse pokemon,
   se tem dois, retorna uma tupla com os pokemons.""" 
def bs_to_poke(battle_state):
    battle_state = str(battle_state)
    xml = battle_state.split('</pokemon>', 1) #O primeiro poke no xml[0].
    data_poke1 = xml_to_poke(xml[0])
    if len(xml[1]) > 100: #Caso tenha vindo 2 pokes no battle_state.
        data_poke2 = xml_to_poke(xml[1])
        return Pokemon(data_poke1), Pokemon(data_poke2)
    return Pokemon(data_poke1)

"""Recebe uma string xml e devolve uma lista de dados que pokemon.Pokemon 
   usará para criar o pokemon representado na string"""
def xml_to_poke(xml):
    data = BeautifulSoup(xml) #Objeto que representa o xml
    #Pega todos os atributos do pokemon e separa por linhas
    data = data.pokemon.get_text("\n") 
    data = data.split("\n")
    #Converte o que for número de str para int
    data = [int(n) if n.isdigit() else n for n in data] 
    
    #Agora vamos criar os objetos Ataque: 
    
    #Contém todos os campos de cada ataque (nome, acu, pwr, pp etc)
    ataques = data[9:]
    
    i = 0
    while i < len(ataques) - 5:
        ataques.pop(i) #Remove o id
        #Troca as posições do acu e pwr para ficar como o esperado por Ataque 
        aux = ataques[2 + i]
        ataques[2 + i] = ataques[3 + i]
        ataques[3 + i] = aux
        i += 5
        
    #Contém todo o resto que não é ataque 
    data = data[:9] 
    num_atributos_ataque = 5  #Cada ataque tem 5 itens na lista
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
    global poke_cliente
    poke_cliente = le_pokemon()
    cliente_init(poke_cliente)


def programa_server():
    app.debug = True
    app.run()
