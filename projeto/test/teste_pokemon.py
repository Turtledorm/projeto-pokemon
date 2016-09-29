#!/usr/bin/env python3

"""Testa se um Pokémon aleatório e seus ataques são válidos."""

import os
import sys
import random
import unittest
from mock import patch
# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from tipo import le_tipos
le_tipos("tipos.txt")
from pokemon import Pokemon
from random_poke import RandomPoke


class PokeTestCase(unittest.TestCase):

    def setUp(self):
        """Inicializa o teste."""
        sys.stdout = open(os.devnull, 'w')  # Suprime o output de batalha.py
        self.ctrl = RandomPoke()
        self.test = Pokemon(self.ctrl.gera())

    def test_pokemons(self):
        """Verifica se os valores do Pokémon coincidem com os anteriores."""
        self.assertEqual(self.test.nome, self.ctrl.nome)
        self.assertEqual(self.test.lvl, self.ctrl.lvl)
        self.assertEqual(self.test.tipo1.numero, self.ctrl.tipo1)
        self.assertEqual(self.test.tipo2.numero, self.ctrl.tipo2)
        self.assertEqual(self.test.hp, self.ctrl.hp)
        self.assertEqual(self.test.atk, self.ctrl.atk)
        self.assertEqual(self.test.dfs, self.ctrl.dfs)
        self.assertEqual(self.test.spd, self.ctrl.spd)
        self.assertEqual(self.test.spc, self.ctrl.spc)

    def test_ataques(self):
        """Verifica se os ataques coincidem com os valores pré-estipulados."""
        for i in range(len(self.test.ataques)):
            ataque = self.test.ataques[i]
            self.assertEqual(ataque.nome, self.ctrl.ataques[i][0])
            self.assertEqual(ataque.typ.numero, self.ctrl.ataques[i][1])
            self.assertEqual(ataque.acu, self.ctrl.ataques[i][2])
            self.assertEqual(ataque.pwr, self.ctrl.ataques[i][3])
            self.assertEqual(ataque.pp, self.ctrl.ataques[i][4])

    def test_acertou(self):
        chance = (self.test.ataques[0].acu * self.test.ataques[0].acu)/10000
        maior_chance = chance + 0.001
        valores_menores = []
        valores_maiores = []

        for i in range(100):
            valores_menores.append(random.uniform(0, chance))
            valores_maiores.append(random.uniform(maior_chance, 1))
        valores =  valores_menores + valores_maiores

        # Usamos valores conhecidos para testar a unidade do .acertou
        # que usa números pseudo-aleatórios.
        with patch("batalha.random.uniform", side_effect=valores):
            for i in range(100):
                self.assertTrue(self.test.ataques[0].acertou())
            for i in range(100):
                self.assertFalse(self.test.ataques[0].acertou())


    def tearDown(self):
        """Finaliza o teste."""
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__


# Inicializa o unittest, que fará todo o trabalho
if __name__ == '__main__':
    unittest.main()
