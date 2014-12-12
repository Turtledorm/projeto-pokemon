"""Eventos de batalha do jogo."""

import sys
import random
import subprocess

import pokemon


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
        struggle = pokemon.Ataque(["Struggle", 0, 100, 50, 10])
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


def calcula_dano(ataque, atacante, defensor, random=True):
    """Calcula o dano causado usando a fórmula da 1ª geração.
       Se random=False, aleatório e crítico não são contabilizados."""
    # Pega os valores básicos para calcular dano
    lvl = atacante.lvl
    base = ataque.pwr
    if ataque.typ.is_especial:
        atk = atacante.spc
        dfs = defensor.spc
    else:
        atk = atacante.atk
        dfs = defensor.dfs

    eff = efetividade(ataque, defensor)

    # Calcula o dano base, sem modificadores aleatórios
    dano = (2*lvl + 10)/250 * atk/dfs * base + 2
    dano *= stab(ataque, atacante) * eff

    # Aplica o modificador de crítico e aleatório
    if random:
        dano *= critico(atacante, eff) * aleatorio()

    return int(dano)


def stab(ataque, atacante):
    """Confere um bônus de dano se tipo do ataque e do atacante são iguais."""
    tipo1 = atacante.tipo1
    tipo2 = atacante.tipo2
    typ = ataque.typ

    if tipo1 == typ or tipo2 == typ:
        return 1.5
    return 1


def critico(atacante, eff):
    """Decide se o atacante causou um golpe crítico."""
    lvl = atacante.lvl
    chance = atacante.spd/512

    if random.uniform(0, 1) <= chance and eff > 0:
        print("> Golpe crítico!")
        return (2*lvl + 5)/(lvl + 5)
    return 1


def efetividade(ataque, defensor):
    """Aplica o multiplicador de efetividade presente na tabela."""
    # Calcula o multiplicador
    typ_ataque = ataque.typ.numero
    mult = pokemon.get_eff(typ_ataque, defensor.tipo1.numero)
    if defensor.tipo2.nome != "Blank":
        mult *= pokemon.get_eff(typ_ataque, defensor.tipo2.numero)

    # Exibe mensagem
    if mult > 1:
        print("> Foi super efetivo!")
    elif mult > 0 and mult < 1:
        print("> Não foi muito efetivo...")
    elif mult == 0:
        print("> Não teve efeito. :(")

    return mult


def aleatorio():
    """Gera um número aleatório a ser usado na fórmula de dano."""
    return random.uniform(0.85, 1)


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
