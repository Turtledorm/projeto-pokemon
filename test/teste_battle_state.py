"""Testa as funcionalidades do módulo battle_state"""
import os
import sys
import unittest
from random_poke import RandomPoke
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from battle_state import *


class BattleStateTest(unittest.TestCase):
    def test_xml(self):
        """Verifica integridade e corretude dos xmls gerados."""
        for i in range(300):
            data1 = RandomPoke()
            data2 = RandomPoke()
            dados1 = data1.gera()
            dados2 = data2.gera()
            poke1 = Pokemon(dados1)
            poke2 = Pokemon(dados2)

            # Testando to_xml
            bs_poke1 = poke1.to_xml()
            bs_poke2 = poke2.to_xml()
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
            for i in range(len(poke1.ataques)):
                self.assertEqual(atk_dados1[i].nome, atk_test1[i].nome)
                self.assertEqual(atk_dados1[i].typ, atk_test1[i].typ)
                self.assertEqual(atk_dados1[i].acu, atk_test1[i].acu)
                self.assertEqual(atk_dados1[i].pwr, atk_test1[i].pwr)
                self.assertEqual(atk_dados1[i].pp, atk_test1[i].pp)
# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
