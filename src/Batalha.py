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

    i = 0
    while i < 5:
        lido = int(input())
        atributos.append(lido)
        i += 1

    i = 0
    while i < 2:
        lido = int(input())
        if lido < 0 or lido > 16:
            erroLeitura("tipo do Pokémon")
        base.append(lido)
        i += 1

    pokemon = Pokemon(base, atributos)
    numAtaques = int(input())

    i = 0
    while i < numAtaques:
        pokemon.adicionaAtaque(leAtaque())
        i += 1

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

    i = 0
    while i < 3:
        ataque.append(int(input()))
        i += 1

    return ataque

#---------------------------------------------------------------------

def erroLeitura(mensagem):
    print("Erro ao ler " + mensagem + "!")
    exit(1)

#---------------------------------------------------------------------
# MAIN

poke1 = lePokemon()
poke2 = lePokemon()
