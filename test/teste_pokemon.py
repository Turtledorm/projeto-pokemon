#!/usr/bin/python3

import random
import unittest
import unittest.mock
import os
import sys

# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import Pokemon, Ataque, tipos, le_tipos


class PokeTestCase(unittest.TestCase):

    def setUp(self):
        """Inicializa os dados para teste."""
        le_tipos("tipos.txt")

        self.nome = "Pedro"
        self.lvl = random.randint(0, 100)
        self.hp = random.randint(0, 255)
        self.atk = random.randint(0, 255)
        self.dfs = random.randint(0, 255)
        self.spd = random.randint(0, 255)
        self.spc = random.randint(0, 255)
        self.tipo1 = random.randint(0, 15)
        while True:
            self.tipo2 = random.randint(0, 16)
            if (self.tipo2 != self.tipo1):
                break

        self.ataques = [["n1", 1, 21, 10, 246],
                        ["n2", 2, 22, 11, 247],
                        ["n3", 3, 23, 12, 248],
                        ["n4", 4, 24, 13, 249]]

        # Cria Pokémon com os dados gerados anteriormente
        dados = [self.nome, self.lvl, self.hp, self.atk, self.dfs,
                 self.spd, self.spc, self.tipo1, self.tipo2,
                 [Ataque(self.ataques[i]) for i in range(4)]]
        self.t = Pokemon(dados)

    def test_pokemons(self):
        """Verifica se os valores do Pokémon coincidem com os anteriores."""
        self.assertEqual(self.t.nome, self.nome)
        self.assertEqual(self.t.lvl, self.lvl)
        self.assertEqual(self.t.tipo1.numero, self.tipo1)
        self.assertEqual(self.t.tipo2.numero, self.tipo2)
        self.assertEqual(self.t.hp, self.hp)
        self.assertEqual(self.t.atk, self.atk)
        self.assertEqual(self.t.dfs, self.dfs)
        self.assertEqual(self.t.spd, self.spd)
        self.assertEqual(self.t.spc, self.spc)

    def test_ataques(self):
        """Verifica se os ataques coincidem com os valores pré-estipulados."""
        for i in range(4):
            ataque = self.t.ataques[i]
            self.assertEqual(ataque.nome, self.ataques[i][0])
            self.assertEqual(ataque.typ.numero, self.ataques[i][1])
            self.assertEqual(ataque.acu, self.ataques[i][2])
            self.assertEqual(ataque.pwr, self.ataques[i][3])
            self.assertEqual(ataque.pp, self.ataques[i][4])


# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
