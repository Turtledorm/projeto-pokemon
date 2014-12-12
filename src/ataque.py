"""Contém a classe que representa um ataque."""

import random
from tipo import get_tipo


class Ataque:

    """Representa um ataque de Pokémon."""

    def __init__(self, _dados):
        """Recebe uma lista de dados e cria um ataque."""
        dados = list(_dados)
        dados.reverse()

        self._nome = dados.pop()
        self._typ = get_tipo(dados.pop())
        self._acu = dados.pop()
        self._pwr = dados.pop()
        self._pp = self.pp_max = dados.pop()

    def mostra(self, full=False):
        """Exibe nome e PP atual/máximo do ataque.
        Se full=True, mostra também os atributos restantes."""
        if not full:
            print(self.nome, "(" + str(self.typ.nome) + ")",
                  "[" + str(self.pp) + "/" + str(self.pp_max) + "]")
        else:
            print(self.nome, "(" + str(self.typ.nome) + ")")
            print(str(self.pp) + "/" + str(self.pp_max), "PP")
            print("Acurácia:", self.acu)
            print("Poder:", self.pwr)

    @property
    def nome(self):
        return self._nome

    @property
    def typ(self):
        return self._typ

    @property
    def acu(self):
        return self._acu

    @property
    def pwr(self):
        return self._pwr

    @property
    def pp(self):
        return self._pp

    def usa_pp(self):
        self._pp -= 1

    def sem_pp(self):
        return self.pp <= 0

    def acertou(self):
        """Verifica se o ataque resultou em acerto ou erro."""
        chance = (self.acu * self.acu)/10000
        return random.uniform(0, 1) <= chance

    def is_struggle(self):
        """Verifica se o ataque em questão é o Struggle."""
        return (self.nome == "Struggle"
                and self.typ.nome == "Normal"
                and self.acu == 100
                and self.pwr == 50)
