"""Contém a classe que representa um Pokémon."""

import os
import random

from dano import calcula_dano
from tipo import get_tipo

MAX_ATAQUES = 4  # Nº máximo de ataques de um Pokémon
BARRA_MAX = 20   # Comprimento máximo da barra de vida


class Pokemon:

    def __init__(self, _dados):
        """Recebe uma lista contendo dados e cria um Pokémon."""
        dados = list(_dados)  # Faz uma cópia bruta da lista original
        dados.reverse()

        self._nome = dados.pop()
        self._lvl = dados.pop()
        self._hp = self._hp_max = dados.pop()
        self._atk = dados.pop()
        self._dfs = dados.pop()
        self._spd = dados.pop()
        self._spc = dados.pop()
        self._tipo1 = get_tipo(dados.pop())
        self._tipo2 = get_tipo(dados.pop())
        self._cpu = False

        self._ataques = dados.pop()

    def mostra(self, full=False):
        """ Exibe nome, tipo(s) e HP atual/máximo do Pokémon.
            Se full=True, mostra também os atributos restantes."""
        print(">>>", self.nome, "{Lv " + str(self.lvl) + "} <<<")
        print("(" + self.tipo1.nome +
              (("/" + self.tipo2.nome) if self.tipo2.nome != "Blank" else "")
              + ")")
        self.imprime_barra()

        if full:
            print("ATK =", self.atk)
            print("DEF =", self.dfs)
            print("SPD =", self.spd)
            print("SPC =", self.spc)

        print()

    def imprime_barra(self):
        """Imprime uma barra para facilitar a leitura do HP do Pokémon."""
        # Pega o comprimento relativo à vida atual
        length = int(BARRA_MAX * self.hp/self.hp_max)
        if length == 0 and self.hp > 0:
            length = 1

        # Imprime a barra
        print("[", end="")
        print("=" * length, end="")
        print(" " * (BARRA_MAX - length), end="")
        print("]  " + str(self.hp) + "/" + str(self.hp_max), "HP")

    def mostra_ataques(self, full=False):
        """Mostra lista de ataques do Pokémon e devolve quantos são."""
        print("<<< Ataques >>>")
        i = 1
        for ataque in self.ataques:
            print(i, "-", end=" ")
            ataque.mostra(full)
            i += 1
        print()
        return len(self.ataques)

    def remove_hp(self, dano):
        """Reduz quantidade de HP equivalente ao dano."""
        self._hp -= dano
        if self._hp < 0:
            self._hp = 0

    def todos_ataques_sem_pp(self):
        """Verifica se todos os ataques estão com PP 0."""
        for ataque in self.ataques:
            if not ataque.sem_pp():
                return False
        return True

    @property
    def nome(self):
        return self._nome

    @property
    def lvl(self):
        return self._lvl

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, valor):
        self._hp = valor

    @property
    def hp_max(self):
        return self._hp_max

    @property
    def atk(self):
        return self._atk

    @property
    def dfs(self):
        return self._dfs

    @property
    def spd(self):
        return self._spd

    @property
    def spc(self):
        return self._spc

    @property
    def tipo1(self):
        return self._tipo1

    @property
    def tipo2(self):
        return self._tipo2

    @property
    def ataques(self):
        return self._ataques

    @property
    def cpu(self):
        return self._cpu    

    def get_ataque(self, n):
        """Retorna o n-ésimo ataque do Pokémon se existir e tiver PP > 0."""
        if n >= MAX_ATAQUES or self.ataques[n].sem_pp():
            return None
        return self.ataques[n]

    def realiza_ataque(self, ataque, defensor):
        """Realiza um ataque contra outro Pokémon."""
        ataque.usa_pp()
        print("\n>", self.nome + " usa " + ataque.nome + "!")

        if ataque.acertou():
            dano = calcula_dano(ataque, self, defensor)

            if dano > 0:
                defensor.remove_hp(dano)
                print(">", defensor.nome, "perdeu", dano, "HP!")

                if ataque.is_struggle():
                    dano //= 2
                    print(">", self.nome, "perdeu", dano, "HP pelo recuo!")
                    self.remove_hp(dano)
        else:
            print("> O ataque de " + self.nome + " errou!")

        input()  # Aguarda por usuário antes de limpar a tela

    def to_xml(self):
        """Gera uma string XML contendo as informações do Pokémon."""
        xml = "<pokemon>"
        xml += _tag("name", self.nome)
        xml += _tag("level", self.lvl)

        xml += "<attributes>"
        xml += _tag("health", self.hp)
        xml += _tag("attack", self.atk)
        xml += _tag("defense", self.dfs)
        xml += _tag("speed", self.spd)
        xml += _tag("special", self.spc)
        xml += "</attributes>"

        xml += _tag("type", self.tipo1.numero)
        if self.tipo2 != "Blank":
            xml += _tag("type", self.tipo2.numero)

        xml += "<attacks>"
        for ataque in self.ataques:
            xml += _tag("id", self.ataques.index(ataque) + 1)
            xml += _tag("name", ataque.nome)
            xml += _tag("type", ataque.typ.numero)
            xml += _tag("power", ataque.pwr)
            xml += _tag("accuracy", ataque.acu)
            xml += _tag("power_points", ataque.pp)
        xml += "</attacks>"
        xml += "</pokemon>"

        return xml


# Função auxiliar de to_xml
def _tag(nome, valor):
    return "<" + nome + ">" + str(valor) + "</" + nome + ">"
