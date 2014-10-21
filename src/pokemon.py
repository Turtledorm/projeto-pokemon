# coding=utf-8

tabela_eff = [] # Tabela com multiplicadores de efetividade
tipos = []      # Lista de tipos


class Pokemon:

    def __init__(self):
        """Recebe dados, atributos e ataques e cria um Pokémon."""
        self.nome = input()
        self.lvl = int(input())

        # Leitura dos atributos
        self.hp = self.hp_max = int(input())
        self.atk = int(input())
        self.dfs = int(input())
        self.spd = int(input())
        self.spc = int(input())

        # Leitura dos tipos
        self.tipo1 = tipos[int(input())]
        self.tipo2 = tipos[int(input())]

        # Leitura dos ataques
        self.ataques = []
        num_ataques = int(input())
        if num_ataques > 4:
            raise Exception(self.nome + " tem mais de 4 ataques!")
        for i in range(num_ataques):
            self.ataques.append(Ataque())

        print("'" + self.nome + "' lido com sucesso!")

    def __call__(self):
        """Exibe informações do Pokémon."""
        print("==== " + self.nome + " ====")

        print("(" + self.tipo1.nome + (("/" + self.tipo2.nome) if self.tipo2.nome != "Blank" else "") + ")")

        print("Nível", self.lvl, "\n")
        print(str(self.hp) + "/" + str(self.hp_max), "HP")
        print("ATK =", self.atk)
        print("DEF =", self.dfs)
        print("SPD =", self.spd)
        print("SPC =", self.spc, "\n")

    def exibe_ataques(self):
        """Mostra lista de ataques do Pokémon."""
        print("<<< Ataques >>>")
        for ataque in self.ataques:
            ataque()
        return len(self.ataques)

    def remove_hp(self, dano):
        self.hp -= dano

    def get_tipos(self):
        return self.tipo1, self.tipo2

    def get_ataque(self, num):
        return self.ataques[num]

    def todos_ataques_sem_pp(self):
        """Verifica se todos os ataques estão com PP 0."""
        for ataque in self.ataques:
            if ataque.pp > 0:
                return False
        return True

class Ataque:

    def __init__(self):
        """Recebe dados e atributos do ataque."""
        self.nome = input()

        # Leitura do tipo
        num_typ = int(input())
        if num_typ not in range(16):
            erro_leitura("tipo de um ataque")
        self.typ = tipos[num_typ]

        # Leitura dos atributos do ataque
        self.acu = int(input())
        self.pwr = int(input())
        self.pp = self.pp_max = int(input())

    def __call__(self):
        """Exibe informações do ataque."""
        print(self.nome, "(" + str(self.typ.nome) + ")")
        print(str(self.pp) + "/" + str(self.pp_max), "PP")
        print("Poder:", self.pwr)
        print("Acurácia:", self.acu, "\n")

    def usa_pp(self):
        self.pp -= 1


class Tipo:

    def __init__(self, numero, nome, is_especial):
        self.numero = numero
        self.nome = nome
        self.is_especial = is_especial

    def __call__(self):
        print(str(self.numero) + ":", self.nome,
            "(Especial)" if self.is_especial else "")
        return self.numero()


def le_tipos(nome_arquivo):
    """Lê tipos do arquivo, guarda-os e constrói a tabela de efetividade."""
    with open(nome_arquivo) as arquivo:
        n = int(arquivo.readline())

        # Leitura dos nomes e categoria
        for i in range(n):
            nome, flag = arquivo.readline().split()
            is_especial = bool(int(flag))
            tipos.append(Tipo(i, nome, is_especial))

        # Adiciona o tipo Blank no final da lista
        tipos.append(Tipo(n, "Blank", False))

        # Leitura da tabela de tipos
        for i in range(n):
            linha = arquivo.readline().split()
            linha = list(map(float, linha))
            tabela_eff.append(linha)

    # DEBUG
    for tipo in tipos:
        tipo()
    for line in tabela_eff:
        print(line)


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    raise Exception("Erro ao ler " + mensagem + "!")
    exit(1)
