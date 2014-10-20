import random
from pokemon import *


def realiza_batalha(poke1, poke2):
    """Simula uma batalha entre dois Pokémons até decidir o vencedor"""
    atacante, defensor = quem_comeca(poke1, poke2)

    while poke1.get_hp() > 0 and poke2.get_hp() > 0:
        defensor()
        atacante()
        calcula_dano(atacante, defensor, escolhe_ataque(atacante))
        atacante, defensor = defensor, atacante

    print(atacante.get_nome() + " foi nocauteado!")
    print(defensor.get_nome() + " vence a batalha! :D")


def quem_comeca(poke1, poke2):
    """Compara o SPD dos dois Pokémons e decide quem começa a batalha"""
    if poke1.get_spd() > poke2.get_spd():
        return (poke1, poke2)
    if poke1.get_spd() < poke2.get_spd():
        return (poke2, poke1)

    # Se o SPD for igual, a escolha é aleatória
    if random_randint(1, 2) == 1:
        return (poke1, poke2)
    return (poke2, poke1)


def escolhe_ataque(atacante):
    """Mostra os ataques do Pokémon para o usuário escolher"""
    n = atacante.exibe_ataques()

    if atacante.sem_pp():
        return None  # Struggle
    else:
        while True:
            escolha = int(input("Digite o número do ataque escolhido: "))
            if escolha >= 1 and escolha <= n:
                break

    return atacante.get_ataque(escolha-1)


def calcula_dano(atacante, defensor, ataque):
    """Calcula o dano causado usando a fórmula da 1ª geração"""
    if ataque is None:
        return  # Implementar Struggle!

    ataque.usa_pp()
    print(atacante.get_nome() + " usa " + ataque.get_nome() + "!")

    if acertou(ataque):
        # Pega os valores básicos para calcular dano
        lvl = atacante.get_lvl()
        base = ataque.get_pwr()
        if ataque.get_typ() < fisico:
            atk = atacante.get_atk()
            dfs = defensor.get_dfs()
        else:
            atk = atacante.get_spc()
            dfs = defensor.get_spc()

        dano = (2*lvl + 10)/250 * atk/dfs * base + 2
        dano *= stab(atacante, ataque) * critico(atacante)
        dano *= aleatorio()  # Colocar efetividade aqui!

        defensor.dano(int(dano))
    else:
        print("O ataque de " + atacante.get_nome() + " errou!")


def acertou(ataque):
    chance = (ataque.get_acu() * ataque.get_acu())/10000
    if random.uniform(0, 1) <= chance:
        return True
    return False


def stab(atacante, ataque):
    """Confere um bônus de dano se o tipo do ataque e do atacante são iguais"""
    tipo1, tipo2 = atacante.get_tipos()
    typ = ataque.get_typ

    if tipo1 == typ or tipo2 == typ:
        return 1.5
    return 1


def critico(atacante):
    """Decide se o atacante causou um golpe crítico"""
    lvl = atacante.get_lvl()
    chance = atacante.get_spd()/512

    if random.uniform(0, 1) <= chance:
        print("Golpe crítico!")
        return (2*lvl + 5)/(lvl + 5)
    return 1


def aleatorio():
    """Gera um número aleatório a ser usado na fórmula de dano"""
    return random.uniform(0.85, 1)
