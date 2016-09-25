"""Inteligência artificial para jogo automatizado."""


def melhor_ataque(atacante, defensor):
    """Devolve o golpe do atacante que causa maior dano esperado ao
       defensor, levando em conta, dano total, acurácia e condição
       de HP de atacante e defensor. Supõe que algum golpe tenha PP."""
    melhor, melhor_efc, melhor_acu = None, -1, -1

    # Condição especial para caso Pokémon esteja à beira do nocaute
    estado_critico = True if atacante.hp < atacante.hp_max/3 else False

    # Procura pelo ataque com melhor custo-benefício
    for ataque in atacante.ataques:
        if not ataque.com_pp():
            continue
        # Calcula-se o dano sem bônus aleatórios (como crítico)
        efc = ataque.calcula_dano(atacante, defensor, ia=True)
        if efc >= defensor.hp:
            # Se houver mais de um ataque que nocauteie o adversário,
            # procurar por aquele que possuir maior acurácia.
            # Caso persista o empate, escolhe o com menor PP.
            if (ataque.acu > melhor_acu or
               (ataque.acu == melhor_acu and ataque.pp > melhor.pp)):
                melhor_efc, melhor_acu = efc, ataque.acu
                melhor = ataque
        elif melhor_acu == -1:
            # Se não foi descoberto ainda um 1 hit K.O, procura-se
            # o com maior efetividade, segundo a fórmula abaixo.
            # Caso HP < 33%, usar logo golpe com maior dano (esqueça acurácia).
            if not estado_critico:
                efc *= (ataque.acu * ataque.acu)/10000
            if efc > melhor_efc:
                melhor_efc = efc
                melhor = ataque

    return melhor
