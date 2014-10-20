# coding=utf-8

# Possíveis tipos que um pokémon pode assumir
tipos = {0: "Normal", 1: "Fighting", 2: "Flying", 3: "Poison", 4: "Ground",
         5: "Rock", 6: "Bird", 7: "Bug", 8: "Ghost", 9: "Fire", 10: "Water",
         11: "Grass", 12: "Electric", 13: "Psychic", 14: "Ice", 15: "Dragon",
         16: "Blank"}


class Pokemon:

    ataques = [] # lista de ataques

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
        num_ataques = int(input())
        if num_ataques > 4:
            raise Exception(self.nome + " tem mais de 4 ataques!")
        for i in range(num_ataques):
            self.ataques.append(self.Ataque())

        print("'" + self.nome + "' lido com sucesso!")

    def __call__(self):
        """Exibe informações do pokémon."""
        print("==== " + self.nome + " ====")

        print("(" + tipos[self.tipo1], end="")
        if tipos[self.tipo2] != "Blank":
            print("/" + tipos[self.tipo2] + ")")
        else:
            print(")")

        print("Nível " + str(self.lvl) + "\n")
        print(str(self.hp) + "/" + str(self.hp_max) + " HP")
        print("ATK = " + str(self.atk))
        print("DEF = " + str(self.dfs))
        print("SPD = " + str(self.spd))
        print("SPC = " + str(self.spc))

    def exibe_ataques(self):
        """Mostra lista de ataques do pokémon."""
        print("\n<<<Ataques>>>")
        for ataque in self.ataques:
            ataque()

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


def erro_leitura(mensagem):
    """Imprime mensagem de erro."""
    print("Erro ao ler " + mensagem + "!")
    exit(1)
