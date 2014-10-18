#!/usr/bin/python3
# coding=utf-8

from Pokemon import Pokemon

# ---------------------------------------------------------------------

def lePokemon():
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
        if tipo not in range(16):
            erroLeitura("tipo do Pokémon")
        base.append(tipo)

    pokemon = Pokemon(base, atributos)
    numAtaques = int(input())

    print("Leitura de ataques:")
    for i in range(numAtaques):
        pokemon.adicionaAtaque(leAtaque())

    print("'" + base[0] + "' lido com sucesso!")
    return pokemon

# ---------------------------------------------------------------------

def leAtaque():
    ataque = []

    ataque.append(input("Nome: "))

    tipo = int(input())
    if tipo not in range(16):
        erroLeitura("tipo de um ataque")
    ataque.append(tipo)

    for i in range(3):
        ataque.append(int(input()))

    return ataque

# ---------------------------------------------------------------------


def erroLeitura(mensagem):
    print("Erro ao ler " + mensagem + "!")
    exit(1)

# ---------------------------------------------------------------------
# MAIN

poke1 = lePokemon()
poke2 = lePokemon()
