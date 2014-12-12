"""Inteligência artificial dos Pokémons. Em ordem de prioridade,
   as ideias são:
   1) Usar o golpe com melhor 'custo-benefício', não levando em
      conta a chance de crítico e com pior caso de aleatoriedade.
   2) Se mais de um golpe nocauteia o oponente, usar o que
      tem melhor acurácia (em caso de empate, escolher o que
      possui mais PP).
   3) Se HP < 20%, usar o golpe mais forte (em caso de empate,
      escolher o que possui mais acurácia).
   4) Se nenhum golpe possuir PP sobrando, usar Struggle."""

from pokemon import Pokemon, Ataque


def melhor_ataque(atacante, defensor):
    """Devolve o golpe do atacante que causa, em média, mais dano
       no defensor. Supõe que algum golpe tenha PP."""

    if atacante.todos_ataques_sem_pp:
        return 0  # Struggle

    if atacante.hp < atacante.hp_max/5:
        return mais_forte(atacante)

    eficiencia = []
    for ataque in atacante.ataques:
        if ataque.pp > 0:
            dano = calcula_dano(ataque, atacante, defensor, random=False)
            eficiencia.append(dano * ataque.acc/100)
        else:
            eficiencia.append(0)

    print(eficiencia)  # Debug

    suficiente = []
    for efc in eficiencia:
        if efc >= defensor.hp:
            suficiente.append(eficiencia.index(efc))

    if suficiente.length > 1:
        return mais_preciso(atacante, suficiente)
    else:
        maximo = max(eficiencia)
        return eficiencia.index(maximo) + 1


def mais_forte(poke):
    """Devolve o golpe mais forte do Poḱémon. O critério
       de desempate é o ataque com melhor acurácia."""
    id = -1
    pwr = -1

    for ataque in poke.ataques:
        if ataque.pwr > pwr:
            id = poke.ataques.index(ataque)
            pwr = ataque.pwr
        elif ataque.pwr == pwr:
            if ataque.acu > poke.get_ataque(id).acu:
                id = poke.ataques.index(ataque)

    return id + 1


def mais_preciso(poke, lista):
    """Devolve o golpe com maior acurácia do Pokémon.
       O critério de desempate é o ataque com mais PP."""
    id = -1
    acc = -1

    for i in lista:
        ataque = poke.get_ataque(i)
        if ataque.acu > acu:
            id = poke.ataques.index(ataque)
            acu = ataque.acu
        elif ataque.acc == acu:
            if ataque.pp > poke.get_ataque(id).pp:
                id = poke.ataques.index(ataque)

    return id + 1
