# coding=utf-8

# Possíveis tipos que um pokémon pode assumir
tipos = {0: "Normal", 1: "Fighting", 2: "Flying", 3: "Poison",
         4: "Ground", 5: "Rock", 6: "Bird", 7: "Bug", 8: "Ghost",
         9: "Fire", 10: "Water", 11: "Grass", 12: "Electric",
         13: "Psychic", 14: "Ice", 15: "Dragon", 16: "Blank"}

fisico = 8     # Último tipo que causa dano físico
especial = 15  # Último tipo que causa dano especial


class Pokemon:

    def __init__(self):
        """Recebe dados, atributos e ataques e cria um pokémon."""
        self.nome = input()
        self.lvl = int(input())

        # Leitura dos atributos
        self.hp = self.hp_max = int(input())
        self.atk = int(input())
        self.dfs = int(input())
        self.spd = int(input())
        self.spc = int(input())

        # Leitura dos tipos
        self.tipo1 = int(input())
        self.tipo2 = int(input())

        # Leitura dos ataques
        self.ataques = []
        num_ataques = int(input())
        if num_ataques > 4:
            raise Exception(self.nome + " tem mais de 4 ataques!")
        for i in range(num_ataques):
            self.ataques.append(Ataque())

        print("'" + self.nome + "' lido com sucesso!")

    def __call__(self):
        """Exibe informações do pokémon."""
        print("==== " + self.nome + " ====")

        print("(" + tipos[self.tipo1], end = "")
        if tipos[self.tipo2] != "Blank":
            print("/" + tipos[self.tipo2] + ")")
        else:
            print(")")

        print("Nível", self.lvl, "\n")
        print(str(self.hp) + "/" + str(self.hp_max), "HP")
        print("ATK =", self.atk)
        print("DEF =", self.dfs)
        print("SPD =", self.spd)
        print("SPC =", self.spc)

    def exibe_ataques(self):
        """Mostra lista de ataques do pokémon."""
        print("\n<<<Ataques>>>")
        for ataque in self.ataques:
            ataque()
        return len(self.ataques)

    def dano(self, dano):
        self.hp -= dano

    def get_nome(self):
        return self.nome

    def get_lvl(self):
        return self.lvl

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.atk

    def get_dfs(self):
        return self.dfs

    def get_spd(self):
        return self.spd

    def get_spc(self):
        return self.spc

    def get_tipos(self):
        return self.tipo1, self.tipo2

    def get_ataque(self, num):
        return self.ataques[num]

    def sem_pp(self):
        for ataque in self.ataques:
            if ataque.get_pp() > 0:
                return False
        return True

class Ataque:

    def __init__(self):
        """Recebe dados e atributos do ataque."""
        self.nome = input()

        # Leitura do tipo
        self.typ = int(input())
        if self.typ not in range(16):
            erro_leitura("tipo de um ataque")

        # Leitura dos atributos do ataque
        self.acu = int(input())
        self.pwr = int(input())
        self.pp = self.pp_max = int(input())

    def __call__(self):
        """Exibe informações do ataque."""
        print(self.nome + " (" + tipos[self.typ] + ")")
        print(str(self.pp) + "/" + str(self.pp_max) + " PP")
        print("Poder: " + str(self.pwr))
        print("Acurácia: " + str(self.acu) + "\n")

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


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    print("Erro ao ler " + mensagem + "!")
    exit(1)
