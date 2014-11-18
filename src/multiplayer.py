"""Funções relacionadas à interação cliente-servidor."""

import requests
from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException
from bs4 import BeautifulSoup

from entrada import le_pokemon
from batalha import batalha, escolhe_ataque, realiza_ataque, \
    quem_comeca, mostra_pokemons, resultado, struggle
from pokemon import Pokemon, Ataque

poke_cliente = None
poke_servidor = None

# Instância do Flask
app = Flask(__name__)


@app.route("/battle/", methods=["POST"])
def inicia_servidor():
    """Recebe um objeto battle_state com o Pokémon do cliente
    e atualiza-o com os dados do servidor."""
    global poke_servidor, poke_cliente

    # Verifica se outra batalha está em andamento
    if poke_servidor is not None and app.config['TESTING'] is not True:
        return Trancado()

    # Recebe por entrada o Pokémon do servidor
    poke_servidor = le_pokemon()

    # Convertemos o xml para um objeto Pokémon
    poke_cliente = bs_to_poke(request.data)

    # Se servidor for jogar primeiro, já contabilizamos o ataque
    if quem_comeca(poke_servidor, poke_cliente) == poke_servidor:
        servidor_ataque()
        if poke_cliente.hp <= 0 or poke_servidor.hp <= 0:
            resultado(poke_cliente, poke_servidor)
    else:
        mostra_pokemons(poke_cliente, poke_servidor)

    # Atualizamos o battle_state com os dados do Pokémon do cliente
    battle_state = cria_bs(poke_cliente, poke_servidor)

    return battle_state


@app.route("/battle/attack/<int:id>", methods=["POST"])
def ataque(id):
    """Contabiliza os ataques escolhidos dos dois jogadores,
       retornando o resultado em um objeto battle_state."""
    global poke_cliente, poke_servidor

    if id != 0:
        realiza_ataque(poke_cliente, poke_servidor,
                       poke_cliente.get_ataque(id-1))
    else:
        # Caso especial: Struggle
        realiza_ataque(poke_cliente, poke_servidor, struggle)

    if poke_cliente.hp > 0 and poke_servidor.hp > 0:
        servidor_ataque()

    # Modificamos o battle_state com ambos os ataques contabilizados
    battle_state = cria_bs(poke_cliente, poke_servidor)

    if poke_cliente.hp <= 0 or poke_servidor.hp <= 0:
        resultado(poke_cliente, poke_servidor)

    return battle_state


@app.route("/shutdown/", methods=["POST"])
def shutdown():
    """Fecha o servidor."""
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Não é um servidor Werkzeug!")
    func()
    return "Servidor finalizado!"


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
    global poke_cliente, poke_servidor

    battle_state = cria_bs(poke)

    try:
        bs = requests.post("http://" + servidor + "/battle/",
                           data=battle_state)
        bs.raise_for_status()

    except requests.exceptions.ConnectionError:
        print("Não foi possível se conectar ao servidor!")
        exit(1)

    except requests.exceptions.HTTPError:
        print("Já existe um jogo em andamento no servidor!")
        exit(1)

    cliente_temp, poke_servidor = bs_to_poke(bs.text)
    poke_cliente.hp = cliente_temp.hp


def cliente_ataque():
    """Envia a escolha de ataque do cliente ao servidor."""
    global poke_cliente, poke_servidor

    # Cliente escolhe seu ataque
    mostra_pokemons(poke_servidor, poke_cliente)
    id = escolhe_ataque(poke_cliente)
    if id not in poke_cliente.ataques:
        id = 0
    else:
        id = poke_cliente.ataques.index(id) + 1

    # Tenta mandar a escolha ao servidor
    try:
        print("Esperando resposta do servidor...")
        bs = requests.post("http://" + servidor + "/battle/attack/" + str(id))
    except requests.exceptions.ConnectionError:
        print("A conexão com o servidor caiu!")
        exit(1)

    # Atualiza dados do cliente
    cliente_temp, servidor_temp = bs_to_poke(bs.text)
    poke_cliente.hp = cliente_temp.hp
    poke_servidor.hp = servidor_temp.hp
    if id > 0:
        poke_cliente.get_ataque(id-1).usa_pp()


def servidor_ataque():
    """Contabiliza o ataque escolhido pelo servidor na batalha."""
    global poke_cliente, poke_servidor

    mostra_pokemons(poke_cliente, poke_servidor)
    ataque = escolhe_ataque(poke_servidor)
    realiza_ataque(poke_servidor, poke_cliente, ataque)
    mostra_pokemons(poke_cliente, poke_servidor)


# -----------------------------------------------------------------------------


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
    # Objeto que representa o xml
    data = BeautifulSoup(xml)

    # Pega todos os atributos do pokemon e separa por linhas
    data = data.pokemon.get_text("\n")
    data = data.split("\n")

    # Converte o que for número de str para int
    data = [int(n) if n.isdigit() else n for n in data]

    # Agora vamos criar os objetos Ataque:
    # Contém todos os campos de cada ataque (nome, ACU, PWR, PP etc)
    ataques = data[9:]

    i = 0
    while i < len(ataques) - 5:
        ataques.pop(i)  # Remove o id
        # Troca as posições do ACU e PWR para ficar como o esperado por Ataque
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


# -----------------------------------------------------------------------------


def programa_cliente():
    """Executa o programa no modo cliente."""
    global poke_cliente, poke_servidor, servidor

    poke_cliente = le_pokemon()
    ip = input("Digite o endereço IP do servidor: ")
    try:
        port = int(input("Digite a porta de conexão: "))
    except ValueError:
        port = 5000
    servidor = ip + ":" + str(port)

    cliente_init(poke_cliente)
    while poke_cliente.hp > 0 and poke_servidor.hp > 0:
        cliente_ataque()

    mostra_pokemons(poke_servidor, poke_cliente)
    resultado(poke_cliente, poke_servidor)

    # Envia pedido para fechar o servidor
    requests.post("http://" + servidor + "/shutdown/")


def programa_servidor():
    """Executa o programa no modo servidor."""
    try:
        app.run(host="0.0.0.0")
    except OSError:
        print("Endereço do servidor já em uso!")
