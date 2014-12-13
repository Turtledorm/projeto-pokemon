"""Inteligência artificial dos Pokémons."""


def melhor_ataque(atacante, defensor):
    """Devolve o golpe do atacante que causa, em média, mais dano
       no defensor. Supõe que algum golpe tenha PP."""
    estado_critico = False
    eficiencias = []

    # Caso HP < 20%, usar o golpe que causa mais dano (esqueça acurácia)
    if atacante.hp < atacante.hp_max/5:
        estado_critico = True

    # Procura pelo ataque com melhor custo-benefício,
    # levando em conta dano total e acurácia do mesmo.
    for ataque in atacante.ataques:
        if ataque.pp > 0:
            efc = ataque.calcula_dano(atacante, defensor, is_basico=True)
            if not estado_critico:
                efc *= (ataque.acu*ataque.acu)/10000
            eficiencias.append(efc)
        else:
            eficiencias.append(0)

    # Cria, se existir, uma lista de ataques que podem
    # nocautear o inimigo num acerto só.
    suficientes = []
    for efc in eficiencias:
        if efc >= defensor.hp:
            suficientes.append(efc)

    # Encontra o melhor ataque
    if len(suficientes) > 1:
        return mais_preciso(atacante, suficientes)
    else:
        return atacante.get_ataque(eficiencias.index(max(eficiencias)))


def mais_preciso(atacante, suficientes):
    """Devolve o golpe com maior acurácia do Pokémon.
       O critério de desempate é a quantidade de PP."""
    melhor = None
    acu = -1

    for efc in suficientes:
        ataque = atacante.get_ataque(suficientes.index(efc))
        if ataque.acu > acu:
            melhor = ataque
            acu = ataque.acu
        elif ataque.acu == acu:
            if ataque.pp > melhor.pp:
                melhor = ataque

    return melhor
