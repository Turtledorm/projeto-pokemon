import sys
import random
import subprocess

import pokemon

# Define Struggle como um possível ataque
struggle = pokemon.Ataque(["Struggle", 0, 100, 50, 10])


def batalha(poke1, poke2):
    """Simula uma batalha entre dois Pokémons até decidir o vencedor."""
    atacante, defensor = ordem_inicio(poke1, poke2)

    # Loop principal da batalha e do jogo
    while poke1.hp > 0 and poke2.hp > 0:
        mostra_pokemons(poke1, poke2)
        print("* Turno de", atacante.nome, "*\n")
        ataque = escolhe_ataque(atacante)
        realiza_ataque(atacante, defensor, ataque)
        atacante, defensor = defensor, atacante

    mostra_pokemons(poke1, poke2)

    # Define Pokémon vencedor e perdedor
    vencedor = poke1 if poke1.hp > 0 else poke2
    perdedor = poke2 if poke1 == vencedor else poke1

    print(perdedor.nome + " foi nocauteado!")
    if vencedor.hp <= 0:
        print(vencedor.nome + " foi nocauteado!")
        print("A batalha terminou em empate!")
    else:
        print(vencedor.nome + " vence a batalha! :D")


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
        subprocess.call("cls")


def escolhe_ataque(atacante):
    """Mostra a lista de ataques do Pokémon e lê a escolha do usuário."""
    n = atacante.mostra_ataques()

    # Se não tiver mais com o que atacar, usa Struggle
    if atacante.todos_ataques_sem_pp():
        print(atacante.nome, "não tem golpes sobrando...", end="")
        input()
        return struggle

    while True:
        try:
            x = int(input("Digite o nº do ataque: "))
        except ValueError:
            continue
        if x in range(n+1) and atacante.get_ataque(x-1) is not None:
            break

    return atacante.get_ataque(x-1)


def realiza_ataque(atacante, defensor, ataque):
    """Calcula o dano causado usando a fórmula da 1ª geração."""
    ataque.usa_pp()
    print("\n>", atacante.nome + " usa " + ataque.nome + "!")

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

        # Calcula o dano, aplicando os modificadores
        dano = (2*lvl + 10)/250 * atk/dfs * base + 2
        eff = efetividade(ataque, defensor)
        dano *= (stab(ataque, atacante) * critico(atacante, eff)
                 * eff * aleatorio())
        dano = int(dano)

        if dano > 0:
            defensor.remove_hp(dano)
            print(">", defensor.nome, "perdeu", dano, "HP!")

            if ataque == struggle:
                dano //= 2
                print(">", atacante.nome, "perdeu", dano, "HP pelo recuo!")
                atacante.remove_hp(dano)
    else:
        print("> O ataque de " + atacante.nome + " errou!")

    input()  # Aguarda por usuário antes de limpar a tela


def acertou(ataque):
    """Verifica se o ataque resultou em acerto ou erro."""
    chance = (ataque.acu * ataque.acu)/10000
    if random.uniform(0, 1) <= chance:
        return True
    return False


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
