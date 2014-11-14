"""Funções de leitura para criar objetos de uma classe."""

from pokemon import Pokemon, Ataque, le_tipos, erro_leitura

# Lê de arquivo tipos e tabela de efetividade
num_tipos = le_tipos("tipos.txt")


def le_pokemon():
    """Recebe dados do Pokémon e cria um objeto dessa classe."""
    dados = [input()]  # Começa com o nome

    # Leitura de LVL, HP, ATK, DEF, SPD, SPC, Tipo 1 e Tipo 2
    for i in range(8):
        dados.append(int(input()))

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
    if n not in range(16):
        erro_leitura("tipo de um ataque")
    dados.append(n)

    # Leitura de ACU, PWR e PP
    for i in range(3):
        dados.append(int(input()))

    return Ataque(dados)
