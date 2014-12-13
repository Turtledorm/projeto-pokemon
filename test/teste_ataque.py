
import os
import sys
import unittest
import random
from mock import patch, PropertyMock
sys.path.insert(1, os.path.join(sys.path[0], "../src"))
from tipo import le_tipos
le_tipos("tipos.txt")
from pokemon import Pokemon
from random_poke import RandomPoke
from ataque import Ataque


class DanoTestCase(unittest.TestCase):
    
    def setUp(self):
            sys.stdout = open(os.devnull, "w")  # Suprime o output de batalha.py
            sys.stderr = sys.stdout
            self.a = RandomPoke()
            self.poke1 = Pokemon(self.a.gera())
        
    def test_critico(self):
        """Verifica se o cálculo de golpes críticos está funcionando OK."""
        res = (2 * self.poke1.lvl + 5)/(self.poke1.lvl + 5)
        chance = self.poke1.spd/512
        maior_chance = chance + 0.001
        valores_menores = []
        valores_maiores = []

        # Novamente usamos valores conhecidos para testar a unidade do
        # batalha.critico que usa números pseudo-aleatórios. Os primeiros
        # 100 valores serão menores que a chance e os outros 100, maiores.
        for i in range(100):
            valores_menores.append(random.uniform(0.0, chance))
            valores_maiores.append(random.uniform(maior_chance, 1.0))
        valores = valores_menores + valores_maiores
        a = RandomPoke()
        ataque = Ataque(a.gera_ataque())
        with patch("batalha.random.uniform", side_effect=valores):
            # Em cada loop, a iteração chamará dano.critico duas
            # vezes, usando, então, dois valores do side_effect.
            for i in range(50):
                self.assertEqual(ataque.critico(self.poke1, 0), 1)
                self.assertEqual(ataque.critico(self.poke1,
                                         random.randint(1, 100)), res)
            for i in range(50):
                self.assertEqual(ataque.critico(self.poke1, 0), 1)
                self.assertEqual(ataque.critico(self.poke1,
                                         random.randint(1, 100)), 1)
        """
        self.assertRaises(AttributeError, critico, self.poke1.nome, None)
        self.assertRaises(AttributeError, critico, self.poke1.hp, None)
        self.assertRaises(AttributeError, critico, None, self.poke1.nome)
        self.assertRaises(AttributeError, critico, None, self.poke1.hp)
        """
    def test_efetividade(self):
        """Verifica se o cálculo de efetividade é feito corretamente."""
        # Novamente geramos um novo Pokémon para podermos realizar vários
        # testes com resultados diferentes.
        for i in range(100):
            a = RandomPoke()
            poke1 = Pokemon(a.gera())
            ataque = Ataque(a.gera_ataque())

            # Esta é a fórmula para calcular efetividade
            mult = ataque.typ.get_eff_contra(poke1.tipo1)
            if poke1.tipo2.nome != "Blank":
                mult *= ataque.typ.get_eff_contra(poke1.tipo2)

            self.assertEquals(mult, ataque.efetividade(poke1, False))
    def test_stab(self):
        ataque = self.poke1.ataques[0]
        not_typ = 0
        while not_typ == ataque.typ:
            not_typ = random.randint(0, 255)

        # É esperado que se o typ do ataque for igual ao tipo1 ou tipo2
        # do atacante, dano.stab devolve 1.5. Caso contrário, devolve 1.
        poke = "pokemon.Pokemon."
        with patch(poke + "tipo1", PropertyMock(return_value=ataque.typ)):
            with patch(poke + "tipo2", PropertyMock(return_value=ataque.typ)):
                self.assertEqual(ataque.stab(self.poke1), 1.5)
            with patch(poke + "tipo2", PropertyMock(return_value=not_typ)):
                self.assertEqual(ataque.stab(self.poke1), 1.5)

        with patch(poke + "tipo2", PropertyMock(return_value=ataque.typ)):
            with patch(poke + "tipo1", PropertyMock(return_value=not_typ)):
                self.assertEqual(ataque.stab(self.poke1), 1.5)
                with patch(poke + "tipo2", PropertyMock(return_value=not_typ)):
                    self.assertEqual(ataque.stab(self.poke1), 1)

    
    def tearDown(self):
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__     

# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
