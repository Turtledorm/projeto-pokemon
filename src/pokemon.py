import os

max_ataques = 4
tabela_eff = []  # Tabela com multiplicadores de efetividade
tipos = []       # Lista de tipos


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
        if num_ataques > max_ataques:
            raise Exception(self.nome + " tem mais de 4 ataques!")
        for i in range(num_ataques):
            self.ataques.append(Ataque())

        print("'" + self.nome + "' lido com sucesso!")

    def __call__(self):
        """Exibe informações do Pokémon."""
        print("==== " + self.nome + " ====")

        print("(" + self.tipo1.nome +
              (("/" + self.tipo2.nome) if self.tipo2.nome != "Blank" else "")
              + ")")

        print("Nível", self.lvl, "\n")
        print(str(self.hp) + "/" + str(self.hp_max), "HP")
        print("ATK =", self.atk)
        print("DEF =", self.dfs)
        print("SPD =", self.spd)
        print("SPC =", self.spc, "\n")

    def exibe_ataques(self):
        """Mostra lista de ataques do Pokémon e devolve quantos são."""
        print("<<< Ataques >>>")
        i = 1
        for ataque in self.ataques:
            print(str(i) + ")", end=" ")
            ataque()
            i += 1
        return len(self.ataques)

    def remove_hp(self, dano):
        self.hp -= dano

    def get_nome(self):
        return self.nome

    def get_lvl(self):
        return self.lvl

    def get_hp(self):
        return self.hp

    def get_hp_max(self):
        return self.hp_max

    def get_atk(self):
        return self.atk

    def get_dfs(self):
        return self.dfs

    def get_spd(self):
        return self.spd

    def get_spc(self):
        return self.spc

    def get_tipo1(self):
        return self.tipo1

    def get_tipo2(self):
        return self.tipo2

    def get_ataque(self, n):
        "Retorna o n-ésimo ataque do Pokémon se exister e tiver PP > 0"
        if n > max_ataques-1 or self.ataques[n].get_pp() <= 0:
            return None
        return self.ataques[n]

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

    def get_nome(self):
        return self.nome

    def get_typ(self):
        return self.typ

    def get_acu(self):
        return self.acu

    def get_pwr(self):
        return self.pwr

    def get_pp(self):
        return self.pp

    def usa_pp(self):
        self.pp -= 1


class Tipo:

    def __init__(self, numero, nome, especial):
        self.numero = numero
        self.nome = nome
        self.especial = especial

    def __call__(self):
        print(str(self.numero) + ":", self.nome,
              "(Especial)" if self.is_especial() else "")

    def get_nome(self):
        return self.nome

    def get_numero(self):
        return self.numero

    def is_especial(self):
        return self.especial


def le_tipos(nome_arquivo):
    """Lê tipos do arquivo, guarda-os e constrói a tabela de efetividade."""
    # Permite que o script leia o arquivo mesmo
    # se executado de fora do diretório de onde ele está.
    __diretorio = os.path.join(os.getcwd(), os.path.dirname(__file__))
    caminho = (os.path.join(__diretorio, nome_arquivo))

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


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    raise Exception("Erro ao ler " + mensagem + "!")
    exit(1)
