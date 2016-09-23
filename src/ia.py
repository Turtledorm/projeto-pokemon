"""Inteligência artificial para jogo automatizado."""


def melhor_ataque(atacante, defensor):
    """Devolve o golpe do atacante que causa maior dano 
       esperado ao defensor. Supõe que algum golpe tenha PP."""
    estado_critico = False
    melhor, melhor_efc, melhor_acu = None, -1, -1

    # Condição especial para caso Pokémon esteja à beira do nocaute
    if atacante.hp < atacante.hp_max/5:
        estado_critico = True

    # Procura pelo ataque com melhor custo-benefício, levando em conta
    # dano total e acurácia do mesmo. Se houver mais de um ataque que
    # nocauteie o adversário, procurar por aquele que possuir maior acurácia.
    for ataque in atacante.ataques:
        if ataque.pp > 0:
            efc = ataque.calcula_dano(atacante, defensor, ia=True)
            if efc >= defensor.hp:
                # Se ACU for igual, usa maior PP como critério de desempate
                if (ataque.acu > melhor_acu or
                   (ataque.acu == melhor_acu and ataque.pp > melhor.pp)):
                    melhor_efc, melhor_acu = efc, ataque.acu
                    melhor = ataque
            else:
                # Caso HP < 20%, usar golpe com maior dano (esqueça acurácia)
                if not estado_critico:
                    efc *= (ataque.acu*ataque.acu)/10000
                if efc > melhor_efc:
                    melhor_efc = efc
                    melhor = ataque

    return melhor
