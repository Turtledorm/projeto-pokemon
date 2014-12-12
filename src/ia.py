"""Inteligência artificial dos Pokémons."""


def melhor_ataque(atacante, defensor):
    """Devolve o golpe do atacante que causa, em média, mais dano
       no defensor. Supõe que algum golpe tenha PP."""
    estado_critico = False
    eficiencia = []

    # Caso HP < 20%, usar o golpe que causa mais dano (esqueça acurácia)
    if atacante.hp < atacante.hp_max/5:
        estado_critico = True

    # Procura pelo ataque com melhor custo-benefício,
    # levando em conta dano total e acurácia do mesmo.
    for ataque in atacante.ataques:
        if ataque.pp > 0:
            efc = ataque.calcula_dano(atacante, defensor, is_basico=True)
            if not estado_critico:
                efc *= ataque.acu/100
            eficiencia.append(efc)

    # Cria, se existir, uma lista de ataques que podem
    # nocautear o inimigo num acerto só.
    suficiente = []
    for efc in eficiencia:
        if efc >= defensor.hp:
            suficiente.append(efc)

    # Encontra o melhor ataque
    if len(suficiente) > 1:
        return mais_preciso(atacante, suficiente)
    else:
        return max(eficiencia)


def mais_preciso(poke, lista):
    """Devolve o golpe com maior acurácia do Pokémon.
       O critério de desempate é a quantidade de PP."""
    melhor = None
    acu = -1

    for ataque in lista:
        if ataque.acu > acu:
            melhor = ataque
            acu = ataque.acu
        elif ataque.acu == acu:
            if ataque.pp > melhor.pp:
                melhor = ataque

    return melhor
