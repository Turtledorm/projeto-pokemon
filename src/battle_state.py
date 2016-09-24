""" Funções que criam e traduzem um objeto battle_state de e para xml."""

from bs4 import BeautifulSoup

from pokemon import Pokemon
from ataque import Ataque
from entrada import le_pokemon


def cria_bs(poke1, poke2=None):
    """Cria um xml battle_state com dados de até dois Pokémons."""
    xml = ('<?xml version="1.0" encoding="utf-8"?>'
           + "<battle_state>"
           + poke1.to_xml())
    if poke2 is not None:
        xml += poke2.to_xml()
    xml += "</battle_state>"
    return xml


def bs_to_poke(battle_state, cpu=False):
    """Devolve até dois objetos Pokémon cujos dados estão no battle_state."""
    # Converte a primeira parte do xml em Pokémon
    xml = battle_state.split("</pokemon>", 1)
    poke1 = xml_to_poke(xml[0], cpu)

    # Faz a conversão do segundo Pokémon, se houver
    if xml[1] != "</battle_state>":
        poke2 = xml_to_poke(xml[1], cpu)
        return poke1, poke2
    return poke1


def xml_to_poke(xml, cpu):
    """Recebe uma string xml e devolve um objeto Pokémon."""
    # Objeto que representa o xml
    dados = BeautifulSoup(xml)

    # Pega todos os valores dos atributos do Pokémon e separa por linhas
    dados = dados.pokemon.get_text("\n").split("\n")

    # Remove ids dos ataques (inúteis)
    del dados[9::6]

    # Cria objeto com dados recebidos
    poke = le_pokemon(cpu, dados)

    return poke
