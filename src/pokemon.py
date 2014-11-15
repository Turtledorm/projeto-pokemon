"""Classes para representar Pokémons, ataques e tipos"""

import os

MAX_ATAQUES = 4  # Nº máximo de ataques que um Pokémon pode possuir
BARRA_MAX = 20   # Comprimento máximo da barra de vida

tabela_eff = []  # Tabela com multiplicadores de efetividade
tipos = []       # Lista de tipos

class Pokemon:

    """Representa um Pokémon, unidade de batalha no jogo."""

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
        self._tipo1 = tipos[dados.pop()]
        self._tipo2 = tipos[dados.pop()]

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
            if ataque.pp > 0:
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

    def get_ataque(self, n):
        """Retorna o n-ésimo ataque do Pokémon se existir e tiver PP > 0."""
        if n >= MAX_ATAQUES or self.ataques[n].pp <= 0:
            return None
        return self.ataques[n]

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
        
class Ataque:

    """Representa um ataque de Pokémon."""

    def __init__(self, _dados):
        """Recebe uma lista de dados e cria um ataque."""
        dados = list(_dados)
        dados.reverse()

        self._nome = dados.pop()
        self._typ = tipos[dados.pop()]
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


class Tipo:

    """Representa um tipo de Pokémon/ataque."""

    def __init__(self, numero, nome, is_especial):
        """Inicializa o tipo."""
        self._numero = numero
        self._nome = nome
        self._is_especial = is_especial

    def mostra(self):
        """Exibe informações do tipo."""
        print(str(self.numero) + ":", self.nome,
              "(Especial)" if self.is_especial else "")

    @property
    def numero(self):
        return self._numero

    @property
    def nome(self):
        return self._nome

    @property
    def is_especial(self):
        return self._is_especial


def le_tipos(nome_arquivo):
    """Lê tipos do arquivo, guarda-os e constrói a tabela de efetividade."""
    # Permite que o script leia o arquivo mesmo
    # se executado de fora do diretório de onde ele está.
    diretorio = os.path.join(os.getcwd(), os.path.dirname(__file__))
    caminho = (os.path.join(diretorio, nome_arquivo))

    with open(caminho) as arquivo:
        n = int(arquivo.readline())

        # Leitura dos nomes e categoria
        for i in range(n):
            nome, especial = arquivo.readline().split()
            tipos.append(Tipo(i, nome, bool(int(especial))))

        # Adiciona o tipo Blank ao final da lista
        tipos.append(Tipo(n, "Blank", False))

        # Leitura da tabela de tipos
        for i in range(n):
            linha = arquivo.readline().split()
            linha = list(map(float, linha))
            tabela_eff.append(linha)

    return n


def get_eff(i, j):
    """Devolve o valor da efetividade dos tipos 'i' contra 'j'."""
    return tabela_eff[i][j]


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    raise Exception("Erro ao ler " + mensagem + "!")
    exit(1)


# Função auxiliar de to_xml
def _tag(nome, valor):
    return "<" + nome + ">" + str(valor) + "</" + nome + ">"
