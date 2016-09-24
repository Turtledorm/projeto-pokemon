"""Contém a classe Pokemon."""

import os
import sys
import time

from tipo import get_tipo
from ataque import Ataque, get_struggle
from batalha import is_debug
from ia import melhor_ataque


class Pokemon:
    """Representa um Pokémon que batalha no jogo."""

    def __init__(self, dados, cpu=False):
        """Recebe uma lista contendo dados e cria um Pokémon."""
        aux = dados[9:]     # Dados dos ataques
        dados = dados[:9]   # Dados do Pokémon
        dados.reverse()     # Revertido para facilitar pop()

        # Atributos iniciais
        self._nome = dados.pop()
        self._lvl = int(dados.pop())
        self._hp = self._hp_max = int(dados.pop())
        self._atk = int(dados.pop())
        self._dfs = int(dados.pop())
        self._spd = int(dados.pop())
        self._spc = int(dados.pop())

        # Tipos do Pokémon
        t = int(dados.pop()), int(dados.pop())
        for i in range(2):
            if t[i] not in range(17):
                print("ERRO: Valor inválido para tipo de Pokémon.")
                exit(1)
        self._tipo1 = get_tipo(t[0])
        self._tipo2 = get_tipo(t[1])

        # Ataques
        self._ataques = []
        while aux:
            ataque = Ataque(aux[:5])
            self.ataques.append(ataque)
            aux = aux[5:]

        self._cpu = cpu

        print("'" + self.nome + "' lido com sucesso!")

    def info(self):
        """ Exibe nome, tipo(s) e HP atual/máximo do Pokémon.
            Se debug, mostra também os atributos restantes."""
        print(">>>", self.nome, "{Lv " + str(self.lvl) + "} <<<", end=" ")
        print("(" + self.tipo1.nome +
              (("/" + self.tipo2.nome) if self.tipo2.nome != "Blank" else "")
              + ")" + ((" [CPU]") if self.cpu is True else ""))
        self.imprime_barra()

        if is_debug():
            print("{ ATK =", self.atk, "/", "DEF =", self.dfs, "/",
                    "SPD =", self.spd, "/", "SPC =", self.spc, "}")
        print()

    def imprime_barra(self):
        """Imprime uma barra para facilitar a leitura do HP do Pokémon."""
        BARRA_MAX = 20   # Comprimento máximo da barra de vida

        # Pega o comprimento relativo à vida atual
        length = int(BARRA_MAX * self.hp/self.hp_max)
        if length == 0 and self.hp > 0:
            length = 1

        # Imprime a barra
        print("[" + "=" * length + " " * (BARRA_MAX - length) + "] ", end="")
        print("[", self.hp, "/", self.hp_max, "] HP", sep="")

    def escolhe_ataque(self, defensor):
        """Mostra a lista de ataques do Pokémon e lê a escolha do usuário."""
        print("* Turno de", self.nome, "*\n")
        self.info_ataques()

        # Se não tiver mais com o que atacar, usa Struggle
        if self.todos_ataques_sem_pp():
            print(self.nome, "não tem golpes sobrando...", end="")
            input()
            return get_struggle()

        ataque = None
        if self.cpu:
            ataque = melhor_ataque(self, defensor)
        else:
            while True:
                try:
                    i = int(input("Digite o nº do ataque: "))
                    if i <= 0 or i > len(self.ataques):
                        continue
                except ValueError:
                    continue
                ataque = self.get_ataque(i-1)
                if ataque.com_pp():
                    break

        return ataque

    def info_ataques(self):
        """Mostra lista de ataques do Pokémon."""
        print("<<< Ataques >>>")
        i = 1
        for ataque in self.ataques:
            print(i, "-", end=" ")
            ataque.info()
            i += 1
        print()

    def get_ataque(self, i):
        """Retorna o i-ésimo ataque do Pokémon.
           Caso especial para struggle em batalhas multiplayer."""
        if i == -1:
            return get_struggle()
        return self.ataques[i]

    def todos_ataques_sem_pp(self):
        """Verifica se todos os ataques estão com PP 0."""
        for ataque in self.ataques:
            if ataque.com_pp():
                return False
        return True

    def realiza_ataque(self, ataque, defensor):
        """Realiza um ataque contra outro Pokémon."""
        ataque.usa_pp()
        print("\n>", self.nome + " usa " + ataque.nome + "!")

        if ataque.acertou():
            dano = ataque.calcula_dano(self, defensor)
            if dano > 0:
                defensor.remove_hp(dano)
                print(">", defensor.nome, "perdeu", dano, "HP!")
                if ataque.nome == "Struggle":
                    dano //= 2
                    print(">", self.nome, "perdeu", dano, "HP pelo recuo!")
                    self.remove_hp(dano)
        else:
            print("> O ataque de " + self.nome + " errou!")

        input()  # Aguarda por usuário antes de limpar a tela

    def remove_hp(self, dano):
        """Reduz quantidade de HP equivalente ao dano."""
        self.hp -= dano
        if self.hp < 0:
            self.hp = 0

    def to_xml(self):
        """Gera uma string XML contendo as informações do Pokémon."""
        xml = "<pokemon>"
        xml += tag("name", self.nome)
        xml += tag("level", self.lvl)

        xml += "<attributes>"
        xml += tag("health", self.hp)
        xml += tag("attack", self.atk)
        xml += tag("defense", self.dfs)
        xml += tag("speed", self.spd)
        xml += tag("special", self.spc)
        xml += "</attributes>"

        xml += tag("type", self.tipo1.numero)
        if self.tipo2 != "Blank":
            xml += tag("type", self.tipo2.numero)

        xml += "<attacks>"
        for ataque in self.ataques:
            xml += tag("id", self.ataques.index(ataque) + 1)
            xml += tag("name", ataque.nome)
            xml += tag("type", ataque.typ.numero)
            xml += tag("power", ataque.pwr)
            xml += tag("accuracy", ataque.acu)
            xml += tag("power_points", ataque.pp)
        xml += "</attacks>"
        xml += "</pokemon>"

        return xml

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


def tag(nome, valor):
    """Função auxiliar de to_xml para escrever tags."""
    return "<" + nome + ">" + str(valor) + "</" + nome + ">"
