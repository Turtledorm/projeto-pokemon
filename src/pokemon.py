import os

max_ataques = 4  # Nº máximo de ataques que um Pokémon pode possuir
tabela_eff = []  # Tabela com multiplicadores de efetividade
tipos = []       # Lista de tipos


class Pokemon:

    def __init__(self, dados):
        """Recebe uma lista contendo dados e cria um Pokémon."""
        dados.reverse()

        self.nome = dados.pop()
        self.lvl = dados.pop()
        self.hp = self.hp_max = dados.pop()
        self.atk = dados.pop()
        self.dfs = dados.pop()
        self.spd = dados.pop()
        self.spc = dados.pop()
        self.tipo1 = tipos[dados.pop()]
        self.tipo2 = tipos[dados.pop()]

        self.ataques = dados.pop()

        print("'" + self.nome + "' lido com sucesso!")

    def mostra(self):
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

    def mostra_ataques(self):
        """Mostra lista de ataques do Pokémon e devolve quantos são."""
        print("<<< Ataques >>>")
        i = 1
        for ataque in self.ataques:
            print(i, "-", end=" ")
            ataque.mostra()
            i += 1
        print()
        return len(self.ataques)

    def remove_hp(self, dano):
        self.hp -= dano

    def todos_ataques_sem_pp(self):
        """Verifica se todos os ataques estão com PP 0."""
        for ataque in self.ataques:
            if ataque.pp > 0:
                return False
        return True

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
        """Retorna o n-ésimo ataque do Pokémon se existir e tiver PP > 0."""
        if n >= max_ataques or self.ataques[n].get_pp() <= 0:
            return None
        return self.ataques[n]


class Ataque:

    def __init__(self, dados):
        """Recebe uma lista de dados e cria um ataque."""
        dados.reverse()

        self.nome = dados.pop()
        self.typ = dados.pop()
        self.acu = dados.pop()
        self.pwr = dados.pop()
        self.pp = self.pp_max = dados.pop()

    def mostra(self, full=False):
        """Exibe nome e PP atual/máximo do ataque.
           Se full=True, mostra também informações adicionais."""
        if not full:
            print(self.nome, "(" + str(self.pp) + "/" + str(self.pp_max) + ")")
        else:
            print(self.nome, "(" + str(self.typ.nome) + ")")
            print(str(self.pp) + "/" + str(self.pp_max), "PP")
            print("Acurácia:", self.acu, "\n")
            print("Poder:", self.pwr)

    def get_nome(self):
        return self.nome

    def get_typ(self):
        return self.typ

    def get_acu(self):
        return self.acu

    def get_pwr(self):
        return self.pwr

    def set_pwr(self, pwr):
        self.pwr = pwr

    def get_pp(self):
        return self.pp

    def usa_pp(self):
        self.pp -= 1


class Tipo:

    def __init__(self, numero, nome, especial):
        self.numero = numero
        self.nome = nome
        self.especial = especial

    def mostra(self):
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
