"""Funções que cuidam dos eventos de batalha do jogo."""

import sys
import random
import subprocess

# Indicador de debug
debug = False


def batalha_local(poke1, poke2):
    """Simula uma batalha entre dois Pokémons, no modo offline."""
    atacante = quem_comeca(poke1, poke2)
    defensor = poke2 if atacante == poke1 else poke1

    # Loop principal da batalha e do jogo
    while not acabou(poke1, poke2):
        mostra_pokemons(poke1, poke2)
        ataque = atacante.escolhe_ataque(defensor)
        atacante.realiza_ataque(ataque, defensor)
        atacante, defensor = defensor, atacante

    # Define Pokémon vencedor e perdedor
    mostra_pokemons(poke1, poke2)
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
    """Exibe informação dos pokémons."""
    limpa_tela()
    poke1.info()
    poke2.info()


def limpa_tela():
    """Limpa a tela com um comando."""
    if sys.platform == "linux":
        subprocess.call("clear")
    elif sys.platform == "win32":
        subprocess.call("cls", shell=True)


def acabou(poke1, poke2):
    """Verifica se algum dos Pokémons foi nocauteado."""
    return poke1.hp <= 0 or poke2.hp <= 0


def resultado(poke1, poke2):
    """Imprime o resultado da batalha baseado no HP dos Pokémons"""
    vencedor, perdedor = (poke1, poke2) if poke1.hp > 0 else (poke2, poke1)

    print(">", perdedor.nome + " foi nocauteado!")
    if vencedor.hp <= 0:
        print(">", vencedor.nome + " foi nocauteado!")
        print("> A batalha terminou em empate!")
    else:
        print(">", vencedor.nome + " vence a batalha! :D")


def set_debug():
    """Ativa modo debug."""
    global debug
    debug = True


def is_debug():
    """Verifica se está em modo debug."""
    return debug