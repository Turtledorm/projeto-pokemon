#!/usr/bin/python3

import unittest

tipo = {
0: "Normal",
1: "Fighting",
2: "Flying",
3: "Poison",
4: "Ground",
5: "Rock",
6: "Bird",
7: "Bug",
8: "Ghost",
9: "Fire",
10: "Water",
11: "Grass",
12: "Electric",
13: "Psychic",
14: "Ice",
15: "Dragon",
16: "Blank"
}

# ---------------------------------------------------------------------

class Pokemon:

    def __init__(self, base, atributos):
        self.nome  = base[0]
        self.lvl   = base[1]
        self.tipo1 = base[2]
        self.tipo2 = base[3]

        self.hp_max = self.hp = atributos[0]
        self.atk = atributos[1]
        self.defe = atributos[2]
        self.spd = atributos[3]
        self.spc = atributos[4]

        self.ataques = []
    
    def adiciona_ataque(self, base):
        if len(self.ataques) >= 4:
           raise Exception(self.nome + " tem mais de 4 ataques!")
        else:
            self.ataques.append(Ataque(base))
    
    def mostra_pokemon(self):
        print("==== " + self.nome + " ====")
        print("(" + tipo[self.tipo1], end = "")
        if self.tipo2 != 16:
            print("/" + tipo[self.tipo2] + ")")
        else:
            print(")")
        print("Nível " + str(self.lvl) + "\n")
        print(str(self.hp) + "/" + str(self.hp_max) + " HP")
        print("ATK = " + str(self.atk))
        print("DEF = " + str(self.defe))
        print("SPD = " + str(self.spd))
        print("SPC = " + str(self.spc))

    def mostra_ataques(self):
        print("\n<<<Ataques>>>")
        for ataque in self.ataques:
            ataque.mostra_ataque()

# ---------------------------------------------------------------------

class Ataque:

    def __init__(self, base):
        self.nome = base[0]
        self.typ = base[1]
        self.acu = base[2]
        self.pwr = base[3]
        self.pp_max = self.pp = base[4]

    def mostra_ataque(self):
        print(self.nome + " (" + tipo[self.typ] + ")")
        print(str(self.pp) + "/" + str(self.pp_max) + " PP")
        print("Poder: " + str(self.pwr))
        print("Acurácia: " + str(self.acu) + "\n")
