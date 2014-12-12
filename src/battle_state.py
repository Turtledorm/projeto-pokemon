""" Funções que criam e traduzem um objeto battle_state de e para xml."""

from bs4 import BeautifulSoup
from pokemon import Pokemon
from ataque import Ataque


def cria_bs(poke1, poke2=None):
    """Cria um xml battle_state com dados de até dois Pokémons."""
    xml = ('<?xml version="1.0" encoding="utf-8"?>'
           + "<battle_state>"
           + poke1.to_xml())
    if poke2 is not None:
        xml += poke2.to_xml()
    xml += "</battle_state>"

    return xml


def bs_to_poke(battle_state):
    """Devolve até dois objetos Pokémon cujos dados estão no battle_state."""
    # Converte a primeira parte do xml em Pokémon
    xml = battle_state.split("</pokemon>", 1)
    data_poke1 = xml_to_poke(xml[0])

    # Faz a conversão do segundo Pokémon, se houver
    if xml[1] != "</battle_state>":
        data_poke2 = xml_to_poke(xml[1])
        return Pokemon(data_poke1), Pokemon(data_poke2)

    return Pokemon(data_poke1)


def xml_to_poke(xml):
    """Recebe uma string xml e devolve uma lista de dados do Pokémon."""
    # Objeto que representa o xml
    data = BeautifulSoup(xml)

    # Pega todos os atributos do Pokémon e separa por linhas
    data = data.pokemon.get_text("\n")
    data = data.split("\n")

    # Converte o que for número de str para int
    data = [int(n) if n.isdigit() else n for n in data]

    # Agora vamos criar os objetos Ataque:
    # Contém todos os campos de cada ataque (nome, ACU, PWR, PP etc)
    ataques = data[9:]

    for i in range(0, len(ataques) - 5, 5):
        ataques.pop(i)  # Remove o id
        # Troca as posições do ACU e PWR para ficar como o esperado por Ataque
        aux = ataques[2+i]
        ataques[2+i] = ataques[3+i]
        ataques[3+i] = aux

    # Contém todo o resto que não é ataque
    data = data[:9]
    num_atributos_ataque = 5  # Cada ataque tem 5 itens na lista
    num_atks = len(ataques)/num_atributos_ataque
    lista_ataques = []
    for i in range(int(num_atks)):
        ataque = []
        for j in range(num_atributos_ataque):
            ataque.append(ataques.pop(0))
        lista_ataques.append(Ataque(ataque))
    data.append(lista_ataques)

    return data
