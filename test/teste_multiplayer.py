#!/usr/bin/env python3

import unittest
import random
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], '../src'))

from pokemon import Pokemon
from multiplayer import cria_bs, xml_to_poke, bs_to_poke
from random_poke import RandomPoke


# OBS: Soltando warning de deprecated para o BSoup
class MultiplayerTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_xml(self):
        for i in range(100):
            data1 = RandomPoke()
            data2 = RandomPoke()
            dados1 = data1.gera()
            dados2 = data2.gera()
            poke1 = Pokemon(data1.gera())
            poke2 = Pokemon(data2.gera())
            # Testando to_xml
            bs_poke1 = poke1.to_xml()
            bs_poke2 = poke2.to_xml()
            # TODO: Ver como validar esses xmls com xsd!!
            data_teste1 = xml_to_poke(bs_poke1)
            data_teste2 = xml_to_poke(bs_poke2)
            for i in range(9):
                self.assertEqual(data_teste1[i], dados1[i])
                self.assertEqual(data_teste2[i], dados2[i])

            pos_atk = 9  # Posição da lista de ataques na lista de dados
            atk_dados1 = dados1[pos_atk]
            atk_dados2 = dados2[pos_atk]
            atk_test1 = data_teste1[pos_atk]
            atk_test2 = data_teste2[pos_atk]
            for i in range(4):  # Cada um tem 4 ataques pelo random_poke. Mudar isso.
                self.assertEqual(atk_dados1[i].nome, atk_test1[i].nome)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
