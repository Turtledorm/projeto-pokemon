"""Inteligência artificial dos Pokémons."""

def melhor_ataque(atacante, defensor):
    """ ??? """
    if atacante.todos_ataques_sem_pp()
        return 0  # Struggle

    lista_eficiencia = []
    for ataque in atacante.ataques:
        if ataque.pp > 0:
            dano = calcula_dano(ataque, atacante, defensor, random=False)
            eficiencia = dano * ataque.acc/100
        else:
            eficiencia = 0
        lista_eficiencia.append(eficiencia)

    if defensor.hp < efc for efc in lista_eficiencia:
        pass  # Pegar o golpe com melhor acurácia e melhor pp
