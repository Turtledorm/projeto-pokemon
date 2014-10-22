#!/usr/bin/python3

import random
import unittest
import unittest.mock
import os
import sys

# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
import pokemon


class PokeTestCase(unittest.TestCase):

    def setUp(self):
        """Inicializa os dados para teste."""
        pokemon.le_tipos("tipos.txt")

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

        self.atk1 = ["n1", 1, 21, 10, 246]
        self.atk2 = ["n2", 2, 22, 11, 247]
        self.atk3 = ["n3", 3, 23, 12, 248]
        self.atk4 = ["n4", 4, 24, 13, 249]

        self.entrada = [self.nome, self.lvl, self.hp, self.atk,
                        self.dfs, self.spd, self.spc, self.tipo1, self.tipo2]
        self.ataques = [4]  # Nº de ataques a serem passados para o Pokemon.
        self.ataques += self.atk1 + self.atk2 + self.atk3 + self.atk4
        self.entrada += self.ataques  # Todo o input está aqui agora.

        # Faz com que o Pokémon receba entrada do self.entrada e não de stdin.
        pokemon.input = unittest.mock.Mock(side_effect=self.entrada)
        self.t = pokemon.Pokemon()

    def test_pokemons(self):
        """Verifica se os valores do Pokémon coincidem com os anteriores."""
        self.assertEqual(self.t.get_nome(), self.nome)
        self.assertEqual(self.t.get_lvl(), self.lvl)
        self.assertEqual(self.t.get_tipo1().get_numero(), self.tipo1)
        self.assertEqual(self.t.get_tipo2().get_numero(), self.tipo2)
        self.assertEqual(self.t.get_hp(), self.hp)
        self.assertEqual(self.t.get_atk(), self.atk)
        self.assertEqual(self.t.get_dfs(), self.dfs)
        self.assertEqual(self.t.get_spd(), self.spd)
        self.assertEqual(self.t.get_spc(), self.spc)

    def test_ataques(self):
        """Verifica se os ataques coincidem com os valores pré-estipulados."""
        self.ataques.pop(0)
        # Cada 5 elementos da lista self.ataques correspondem aos atributos
        # de um ataque do Pokémon. Então, o primeiro ataque tem como atributos
        # os valores de teste que estão de self.ataques[0] a self.ataques[4].
        for i in range(4):
            ataque = self.t.ataques[i]
            self.assertEqual(ataque.get_nome(), self.ataques[5*i])
            self.assertEqual(ataque.get_typ().get_numero(),
                             self.ataques[5*i + 1])
            self.assertEqual(ataque.get_acu(), self.ataques[5*i + 2])
            self.assertEqual(ataque.get_pwr(), self.ataques[5*i + 3])
            self.assertEqual(ataque.get_pp(), self.ataques[5*i + 4])


# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
