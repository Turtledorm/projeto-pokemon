"""Funções relacionadas ao cálculo de dano."""

import os
import random

from tipo import get_eff


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
    mult = get_eff(typ_ataque, defensor.tipo1.numero)
    if defensor.tipo2.nome != "Blank":
        mult *= get_eff(typ_ataque, defensor.tipo2.numero)

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
