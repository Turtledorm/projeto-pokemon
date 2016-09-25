"""Contém a classe Ataque."""

import random

from tipo import get_tipo, get_num_tipos
from batalha import is_debug


class Ataque:
    """Representa um ataque de Pokémon."""

    def __init__(self, dados):
        """Recebe uma lista de dados e cria um ataque."""
        dados.reverse()

        # Nome
        self._nome = dados.pop()

        # Tipo do ataque
        t = int(dados.pop())
        if t not in range(get_num_tipos()):
            print("ERRO: Valor inválido (" + str(t) + ") para tipo de ataque.")
            exit(1)
        self._typ = get_tipo(t)

        # Atributos
        self._acu = int(dados.pop())
        self._pwr = int(dados.pop())
        self._pp = self.pp_max = int(dados.pop())

    def info(self):
        """Exibe nome e PP atual/máximo do ataque.
           Se debug, mostra também os atributos restantes."""
        print(self.nome, " (", self.typ.nome, ")", sep="", end=" ")
        print("[", self.pp, "/", self.pp_max, "]", sep="")
        if is_debug():
            print("    { Acurácia:", self.acu, "/", "Poder:", self.pwr, "}")

    def acertou(self):
        """Verifica se o ataque resultou em acerto ou erro."""
        chance = (self.acu * self.acu)/10000
        return random.uniform(0, 1) <= chance

    def calcula_dano(self, atacante, defensor, ia=False):
        """Calcula o dano causado pelo ataque usando a fórmula da 1ª geração.
           Se ia=True, aleatório e crítico não são contabilizados."""
        if self.typ.especial:
            atk = atacante.spc
            dfs = defensor.spc
        else:
            atk = atacante.atk
            dfs = defensor.dfs

        # Calcula o dano base, sem modificadores aleatórios
        eff = self.efetividade(defensor, ia)
        dano = (2*atacante.lvl + 10)/250 * atk/dfs * self.pwr + 2
        dano *= self.stab(atacante) * eff

        # Aplica o modificador de crítico e aleatório
        if not ia:
            dano *= self.critico(atacante, eff) * self.aleatorio()

        return int(dano)

    def efetividade(self, defensor, ia):
        """Aplica o multiplicador de efetividade presente na tabela."""
        # Calcula o multiplicador
        mult = self.typ.get_eff_contra(defensor.tipo1)
        if defensor.tipo2.nome != "Blank":
            mult *= self.typ.get_eff_contra(defensor.tipo2)

        # Exibe mensagem
        if not ia:
            if mult > 1:
                print("> Foi super efetivo!")
            elif 0 < mult < 1:
                print("> Não foi muito efetivo...")
            elif mult == 0:
                print("> Não teve efeito. :(")

        return mult

    def stab(self, atacante):
        """Confere bônus de dano se tipo de ataque e atacante são iguais."""
        typ = self.typ
        if atacante.tipo1 == typ or atacante.tipo2 == typ:
            return 1.5
        return 1

    def critico(self, atacante, eff):
        """Confere bônus de dano se for causado um golpe crítico."""
        lvl = atacante.lvl
        chance = atacante.spd/512

        if random.uniform(0, 1) <= chance and eff > 0:
            print("> Golpe crítico!")
            return (2*lvl + 5)/(lvl + 5)
        return 1

    def aleatorio(self):
        """Gera um número aleatório a ser usado na fórmula de dano."""
        return random.uniform(0.85, 1)

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

    def com_pp(self):
        return self.pp > 0


def get_struggle():
    """Devolve um ataque struggle."""
    return Ataque(["Struggle", 0, 100, 50, 10])
