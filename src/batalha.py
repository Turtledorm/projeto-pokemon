#!/usr/bin/python3
# coding=utf-8

from pokemon import Pokemon

# ---------------------------------------------------------------------

def le_pokemon():
    base = []
    atributos = []

    base.append(input("Nome: "))
    base.append(int(input("Nível: ")))

    print("Leitura de atributos:")
    for i in range(5):
        atributo = int(input())
        atributos.append(atributo)

    print("Leitura de tipos:")
    for i in range(2):
        tipo = int(input())
        if tipo not in range(17):
            erro_leitura("tipo do Pokémon")
        base.append(tipo)

    pokemon = Pokemon(base, atributos)
    num_ataques = int(input())

    print("Leitura de ataques:")
    for i in range(num_ataques):
        pokemon.adiciona_ataque(le_ataque())

    print("'" + base[0] + "' lido com sucesso!")
    return pokemon

# ---------------------------------------------------------------------

def le_ataque():
    ataque = []

    ataque.append(input("Nome: "))

    tipo = int(input())
    if tipo not in range(16):
        erro_leitura("tipo de um ataque")
    ataque.append(tipo)

    for i in range(3):
        ataque.append(int(input()))

    return ataque

# ---------------------------------------------------------------------

def erro_leitura(mensagem):
    print("Erro ao ler " + mensagem + "!")
    exit(1)

# ---------------------------------------------------------------------
# MAIN

poke1 = le_pokemon()
poke1.mostra_pokemon()
poke1.mostra_ataques()

poke2 = le_pokemon()
poke2.mostra_pokemon()
poke2.mostra_ataques()
