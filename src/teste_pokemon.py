#!/usr/bin/python3

import unittest
import random
import pokemon 
import unittest.mock


class PokeTestCase(unittest.TestCase):

    def setUp(self):
        pokemon.le_tipos("tipos.txt")

        self.nome  = "Pedro" 
        self.lvl   = random.randint(0, 100)
        self.hp    = random.randint(0, 255)
        self.atk   = random.randint(0, 255)
        self.dfs   = random.randint(0, 255)
        self.spd   = random.randint(0, 255)
        self.spc   = random.randint(0, 255)
        self.tipo1 = random.randint(0, 16)
        self.tipo2 = random.randint(0, 16)
        
        self.atk1 = ["n1", 1, 21, 10, 246]
        self.atk2 = ["n2", 2, 22, 11, 247]
        self.atk3 = ["n3", 3, 23, 12, 248]
        self.atk4 = ["n4", 4, 24, 13, 249]
       
        self.entrada = [self.nome, self.lvl, self.hp, self.atk, 
        self.dfs, self.spd, self.spc, self.tipo1, self.tipo2]
        self.ataques = [4] # É o número de ataques que será parassado para o Pokemon.
        self.ataques += self.atk1 + self.atk2 + self.atk3 + self.atk4
        self.entrada += self.ataques #Todo o input está aqui agora.
        
        # Isso faz com que Pokemon receba a entrada do self.entrada e não do stdin.  
        pokemon.input = unittest.mock.Mock(side_effect = self.entrada)
        self.t = pokemon.Pokemon()

    def test_pokemons(self):
        self.assertEqual(self.t.get_nome(), self.nome)
        self.assertEqual(self.t.get_lvl(), self.lvl)
        self.assertEqual(self.t.get_tipo1()(), self.tipo1)
        self.assertEqual(self.t.get_tipo2()(), self.tipo2)
        self.assertEqual(self.t.get_hp(),  self.hp)
        self.assertEqual(self.t.get_atk(), self.atk)
        self.assertEqual(self.t.get_dfs(), self.dfs)
        self.assertEqual(self.t.get_spd(), self.spd)
        self.assertEqual(self.t.get_spc(), self.spc)

    def test_ataques(self):
        self.ataques.pop(0)
        """Cada 5 elementos da lista self.ataques correspondem aos atributos
        de um ataque do Pokémon. Então, o primeiro ataque do Pokémon tem 
        como atributos os valores de teste que estão no self.ataques[0] 
        ao self.ataques[4].""" 
        for i in range(4):             
            self.assertEqual(self.t.ataques[i].get_nome(), self.ataques[5 * i])
            self.assertEqual(self.t.ataques[i].get_typ()(),  self.ataques[5 * i + 1])
            self.assertEqual(self.t.ataques[i].get_acu(),  self.ataques[5 * i + 2])
            self.assertEqual(self.t.ataques[i].get_pwr(),  self.ataques[5 * i + 3])
            self.assertEqual(self.t.ataques[i].get_pp() ,  self.ataques[5 * i + 4])


if __name__ == '__main__':
    unittest.main()