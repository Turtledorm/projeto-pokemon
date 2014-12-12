"""Funções de leitura para criar objetos de uma classe."""

from pokemon import Pokemon
from ataque import Ataque
from tipo import le_tipos

# Lê de arquivo tipos e tabela de efetividade
num_tipos = le_tipos("tipos.txt")


def le_pokemon():
    """Recebe dados do Pokémon e cria um objeto dessa classe."""
    dados = [input()]  # Começa com o nome

    # Leitura de LVL, HP, ATK, DEF, SPD, SPC
    for i in range(6):
        dados.append(int(input()))

    # Leitura de Tipo 1 e Tipo 2
    for i in range(2):
        n = int(input())
        if n not in range(num_tipos + 1):
            erro_leitura("tipo de um Pokémon")
        dados.append(n)

    # Leitura dos ataques
    ataques = []
    num_ataques = int(input())
    for i in range(num_ataques):
        ataques.append(le_ataque())
    dados.append(ataques)

    print("'" + dados[0] + "' lido com sucesso!")
    return Pokemon(dados)


def le_ataque():
    """Recebe dados de um ataque e cria um objeto dessa classe."""
    dados = [input()]  # Começa com o nome

    # Leitura do tipo
    n = int(input())
    if n not in range(num_tipos):
        erro_leitura("tipo de um ataque")
    dados.append(n)

    # Leitura de ACU, PWR e PP
    for i in range(3):
        dados.append(int(input()))

    return Ataque(dados)


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    raise Exception("Erro ao ler " + mensagem + "!")
    exit(1)
