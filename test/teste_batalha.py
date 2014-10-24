#!/usr/bin/python3
import random
import unittest
import os
import sys


# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import Pokemon, Ataque, le_tipos
le_tipos("tipos.txt")
from batalha import *
from random_poke import RandomPoke 



class BatalhaTestCase(unittest.TestCase):
    def setUp(self):
        
        sys.stdout = open(os.devnull, 'w') #Para suprimir o output das funções do bataha
        self.a  = RandomPoke()
        self.b = RandomPoke()
        self.poke1 = Pokemon(self.a.gera())
        self.poke2 = Pokemon(self.b.gera())
        
    def test_ordem_inicio(self):
        """Verifica se a função ordem_inicio retorna a tupla com o pokemon de maior spd primeiro"""
        if self.poke1.spd > self.poke2.spd:
            self.assertEqual(ordem_inicio(self.poke1, self.poke2), (self.poke1, self.poke2))
            self.assertEqual(ordem_inicio(self.poke2, self.poke1), (self.poke1, self.poke2))
        elif self.poke1.spd < self.poke2.spd:
            self.assertEqual(ordem_inicio(self.poke1, self.poke2), (self.poke2, self.poke1))
            self.assertEqual(ordem_inicio(self.poke2, self.poke1), (self.poke2, self.poke1)) 
        
        self.assertRaises(AttributeError, ordem_inicio, None, None)
        self.assertRaises(AttributeError, ordem_inicio, self.poke1 , None)
        self.assertRaises(AttributeError, ordem_inicio, None, self.poke1)

    def tearDown(self):
        sys.stdout.close() #Fechando o os.devnull
        sys.stdout = sys.__stdout__ 



# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()       
