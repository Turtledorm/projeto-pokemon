# coding=utf-8

tipos = {0: "Normal", 1: "Fighting", 2: "Flying", 3: "Poison", 4: "Ground",
         5: "Rock", 6: "Bird", 7: "Bug", 8: "Ghost", 9: "Fire", 10: "Water",
         11: "Grass", 12: "Electric", 13: "Psychic", 14: "Ice", 15: "Dragon",
         16: "Blank"}


# -----------------------------------------------------------------------------


class Pokemon:

    ataques = []

    def __init__(self):
        self.nome = input("Nome: ")
        self.lvl = int(input("Nível: "))

        # Leitura dos atributos
        self.hp = self.hp_max = int(input("HP: "))
        self.atk = int(input("ATK: "))
        self.dfs = int(input("DEF: "))
        self.spd = int(input("SPD: "))
        self.spc = int(input("SPC: "))

        # Leitura dos tipos
        self.tipo1 = int(input("Tipo 1: "))
        self.tipo2 = int(input("Tipo 2: "))

        # Leitura dos ataques
        num_ataques = int(input("Nº de ataques: "))
        if num_ataques > 4:
            raise Exception(self.nome + " tem mais de 4 ataques!")
        for i in range(num_ataques):
            self.ataques.append(self.Ataque())

        print("'" + self.nome + "' lido com sucesso!")

    # -------------------------------------------------------------------------

    def info(self):
        print("==== " + self.nome + " ====")
        print("(" + tipos[self.tipo1], end="")
        if self.tipo2 != "Blank":
            print("/" + tipos[self.tipo2] + ")")
        else:
            print(")")
        print("Nível " + str(self.lvl) + "\n")
        print(str(self.hp) + "/" + str(self.hp_max) + " HP")
        print("ATK = " + str(self.atk))
        print("DEF = " + str(self.dfs))
        print("SPD = " + str(self.spd))
        print("SPC = " + str(self.spc))

    # -------------------------------------------------------------------------

    def exibe_ataques(self):
        print("\n<<<Ataques>>>")
        for ataque in self.ataques:
            ataque.info()

    # -------------------------------------------------------------------------

    class Ataque:

        def __init__(self):
            self.nome = input("Nome: ")

            self.typ = int(input("TYP: "))
            if self.typ not in range(16):
                erro_leitura("tipo de um ataque")

            # Leitura dos atributos do ataque
            self.acu = int(input("ACU: "))
            self.pwr = int(input("PWR: "))
            self.pp = self.pp_max = int(input("PP: "))

        # ---------------------------------------------------------------------

        def info(self):
            print(self.nome + " (" + tipos[self.typ] + ")")
            print(str(self.pp) + "/" + str(self.pp_max) + " PP")
            print("Poder: " + str(self.pwr))
            print("Acurácia: " + str(self.acu) + "\n")


# -----------------------------------------------------------------------------


def erro_leitura(mensagem):
    print("Erro ao ler " + mensagem + "!")
    exit(1)
