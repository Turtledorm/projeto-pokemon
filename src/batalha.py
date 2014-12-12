"""Eventos de batalha do jogo."""

import sys
import random
import subprocess

from ataque import Ataque
from ia import melhor_ataque


def batalha(poke1, poke2):
    """Simula uma batalha entre dois Pokémons até decidir o vencedor."""
    atacante = quem_comeca(poke1, poke2)
    defensor = poke2 if atacante == poke1 else poke1

    # Loop principal da batalha e do jogo
    while not acabou(poke1, poke2):
        mostra_pokemons(poke1, poke2)
        ataque = escolhe_ataque(atacante, defensor)
        atacante.realiza_ataque(ataque, defensor)
        atacante, defensor = defensor, atacante

    mostra_pokemons(poke1, poke2)

    # Define Pokémon vencedor e perdedor
    resultado(poke1, poke2)


def quem_comeca(poke1, poke2):
    """Compara o SPD dos dois Pokémons e decide quem inicia a batalha."""
    if poke1.spd > poke2.spd:
        return poke1
    if poke1.spd < poke2.spd:
        return poke2

    # Se o SPD for igual, a escolha é aleatória
    if random.randint(1, 2) == 1:
        return poke1
    return poke2


def mostra_pokemons(poke1, poke2):
    """Limpa a tela e exibe informação dos pokémons."""
    limpa_tela()
    poke1.mostra()
    poke2.mostra()


def limpa_tela():
    """Limpa a tela após a escolha do ataque pelo usuário."""
    if sys.platform == "linux":
        subprocess.call("clear")
    elif sys.platform == "win32":
        subprocess.call("cls", shell=True)


def escolhe_ataque(atacante, defensor):
    """Mostra a lista de ataques do Pokémon e lê a escolha do usuário."""
    print("* Turno de", atacante.nome, "*\n")
    n = atacante.mostra_ataques()

    # Se não tiver mais com o que atacar, usa Struggle
    if atacante.todos_ataques_sem_pp():
        print(atacante.nome, "não tem golpes sobrando...", end="")
        input()
        struggle = Ataque(["Struggle", 0, 100, 50, 10])
        return struggle

    if atacante.cpu is True:
        x = melhor_ataque(atacante, defensor)
    else:
        while True:
            try:
                x = int(input("Digite o nº do ataque: "))
            except ValueError:
                continue
            if x in range(n+1) and atacante.get_ataque(x-1) is not None:
                break

    return atacante.get_ataque(x-1)


def acabou(poke1, poke2):
    """Verifica se algum dos Pokémons foi nocauteado."""
    return poke1.hp <= 0 or poke2.hp <= 0


def resultado(poke1, poke2):
    """Imprime o resultado da batalha baseado no HP dos Pokémons"""
    vencedor = poke1 if poke1.hp > 0 else poke2
    perdedor = poke2 if poke1 == vencedor else poke1

    print(">", perdedor.nome + " foi nocauteado!")
    if vencedor.hp <= 0:
        print(">", vencedor.nome + " foi nocauteado!")
        print("> A batalha terminou em empate!")
    else:
        print(">", vencedor.nome + " vence a batalha! :D")
