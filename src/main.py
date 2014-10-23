#!/usr/bin/python3

from pokemon import Pokemon, Ataque, le_tipos

# Lê de arquivo tipos e tabela de efetividade
le_tipos("tipos.txt")

from batalha import batalha


def le_pokemon():
    """Recebe dados do Pokémon, guarda-os numa lista e devolve-a."""
    dados = [input()]  # Começa com o nome

    # Leitura de LVL, HP, ATK, DEF, SPD, SPC, Tipo 1 e Tipo 2
    for i in range(8):
        dados.append(int(input()))

    # Leitura dos ataques
    ataques = []
    num_ataques = int(input())
    for i in range(num_ataques):
        ataques.append(Ataque(le_ataque()))
    dados.append(ataques)

    return dados


def le_ataque():
    """Recebe dados de um ataque e devolve uma lista contendo-os."""
    dados = [input()]  # Começa com o nome

    # Leitura do tipo
    num_typ = int(input())
    if num_typ not in range(16):
        erro_leitura("tipo de um ataque")
    dados.append(num_typ)

    # Leitura de ACU, PWR e PP
    for i in range(3):
        dados.append(int(input()))

    return dados


poke1 = Pokemon(le_pokemon())
poke2 = Pokemon(le_pokemon())
batalha(poke1, poke2)
