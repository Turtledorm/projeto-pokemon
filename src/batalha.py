import random
from pokemon import *


def batalha(poke1, poke2):
    """Simula uma batalha entre dois Pokémons até decidir o vencedor."""
    atacante, defensor = ordem_inicio(poke1, poke2)

    while poke1.hp > 0 and poke2.hp > 0:
        defensor()
        atacante()
        ataque = escolhe_ataque(atacante)
        realiza_ataque(atacante, defensor, ataque)
        atacante, defensor = defensor, atacante

    print(atacante.nome + " foi nocauteado!")
    print(defensor.nome + " vence a batalha! :D")


def ordem_inicio(poke1, poke2):
    """Compara o SPD dos dois Pokémons e decide quem inicia a batalha."""
    if poke1.spd > poke2.spd:
        return poke1, poke2
    if poke1.spd < poke2.spd:
        return poke2, poke1

    # Se o SPD for igual, a escolha é aleatória
    if random.randint(1, 2) == 1:
        return poke1, poke2
    return poke2, poke1


def escolhe_ataque(atacante):
    """Mostra a lista de ataques do Pokémon e lê a escolha do usuário."""
    n = atacante.exibe_ataques()

    if atacante.todos_ataques_sem_pp():
        return  # TODO: Struggle
    
    while True:
        escolha = int(input("Digite o nº do ataque: "))
        if escolha in range(1, n+1):
            break

    return atacante.get_ataque(escolha-1)


def realiza_ataque(atacante, defensor, ataque):
    """Calcula o dano causado usando a fórmula da 1ª geração."""
    if ataque is None:
        pass  # TODO: Implementar Struggle!

    ataque.usa_pp()
    print(atacante.nome + " usa " + ataque.nome + "!")

    if acertou(ataque):
        # Pega os valores básicos para calcular dano
        lvl = atacante.lvl
        base = ataque.pwr
        if ataque.typ.is_especial:
            atk = atacante.spc
            dfs = defensor.spc
        else:
            atk = atacante.atk
            dfs = defensor.dfs

        dano = (2*lvl + 10)/250 * atk/dfs * base + 2
        dano *= stab(ataque, atacante) * critico(atacante) \
                * efetividade(ataque, defensor) * aleatorio()
        defensor.remove_hp(int(dano))

    else:
        print("O ataque de " + atacante.nome + " errou!")


def acertou(ataque):
    chance = (ataque.acu * ataque.acu)/10000
    if random.uniform(0, 1) <= chance:
        return True
    return False


def stab(ataque, atacante):
    """Confere um bônus de dano se o tipo do ataque e do atacante são iguais."""
    tipo1, tipo2 = atacante.get_tipos()
    typ = ataque.typ

    if tipo1 == typ or tipo2 == typ:
        return 1.5
    return 1


def critico(atacante):
    """Decide se o atacante causou um golpe crítico."""
    lvl = atacante.lvl
    chance = atacante.spd/512

    if random.uniform(0, 1) <= chance:
        print("Golpe crítico!")
        return (2*lvl + 5)/(lvl + 5)
    return 1


def efetividade(ataque, defensor):
    """Aplica o multiplicador de efetividade presente na tabela."""

    # Calcula o multiplicador
    mult = tabela_eff[ataque.typ()][defensor.tipo1()]
    if (defensor.tipo2.nome != "Blank"):
        mult *= tabela_eff[ataque.typ()][defensor.tipo2()]

    # Exibe mensagem
    if mult > 1:
        print("Foi super efetivo!")
    elif mult > 0:
        print("Não foi muito efetivo...")
    else:
        print("Não teve efeito. :(")

    return mult


def aleatorio():
    """Gera um número aleatório a ser usado na fórmula de dano."""
    return random.uniform(0.85, 1)
