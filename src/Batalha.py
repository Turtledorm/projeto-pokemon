#!/usr/bin/python3

from Pokemon import Pokemon

#---------------------------------------------------------------------

def lePokemon():
    base = []
    atributos = []

    # Lê o nome
    base.append(input())

    # Lê o nível
    base.append(int(input()))

    for i in range(5):
        lido = int(input())
        atributos.append(lido)

    for i in range(2):
        lido = int(input())
        if lido < 0 or lido > 16:
            erroLeitura("tipo do Pokémon")
        base.append(lido)

    pokemon = Pokemon(base, atributos)
    numAtaques = int(input())

    for i in range(numAtaques):
        pokemon.adicionaAtaque(leAtaque())

    print("'" + base[0] + "' lido com sucesso!")
    return pokemon

#---------------------------------------------------------------------

def leAtaque():
    ataque = []

    # Lê o nome
    ataque.append(input())

    typ = int(input())
    if typ < 0 or typ > 16:
        erroLeitura("tipo de um ataque")
    ataque.append(typ)

    for i in range(3):
        ataque.append(int(input()))

    return ataque

#---------------------------------------------------------------------

def erroLeitura(mensagem):
    print("Erro ao ler " + mensagem + "!")
    exit(1)

#---------------------------------------------------------------------
# MAIN

poke1 = lePokemon()
poke2 = lePokemon()
