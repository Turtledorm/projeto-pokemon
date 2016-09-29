#!/usr/bin/env python3

"""Testa se a batalha entre dois Pokémons está ocorrendo
   segundo os conformes. O programa gera pokémons aleatórios
   e simula uma entrada consistindo de ataques."""

import os
import sys
import random
import unittest
from mock import Mock, patch, PropertyMock

# Diz onde procurar pelo módulo pokemon
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from tipo import le_tipos
from entrada import le_ataque
le_tipos("tipos.txt")
import pokemon
from pokemon import Pokemon
from ataque import Ataque
import batalha
from batalha import quem_comeca,  mostra_pokemons
from random_poke import RandomPoke


class BatalhaTestCase(unittest.TestCase):

    def setUp(self):
        """Inicializa os dois Pokémons aleatórios para os testes."""
        sys.stdout = open(os.devnull, "w")  # Suprime o output de batalha.py
        sys.stderr = sys.stdout
        self.a = RandomPoke()
        self.b = RandomPoke()
        self.poke1 = Pokemon(self.a.gera())
        self.poke2 = Pokemon(self.b.gera())
        self.struggle = Ataque(["Struggle", 0, 100, 50, 10])

    def test_quem_comeca(self):
        """Verifica se a função quem_comeca retorna
           a tupla com o Pokemon de maior SPD primeiro."""
        primeiro = (self.poke1 if self.poke1.spd > self.poke2.spd
                    else self.poke2)
        segundo = self.poke2 if primeiro == self.poke1 else self.poke1

        self.assertEqual(quem_comeca(primeiro, segundo), primeiro)
        self.assertEqual(quem_comeca(segundo, primeiro), primeiro)

        self.assertRaises(AttributeError, quem_comeca, None, None)
        self.assertRaises(AttributeError, quem_comeca, self.poke1, None)
        self.assertRaises(AttributeError, quem_comeca, None, self.poke1)

    def test_mostra(self):
        """Apenas verifica se a função levanta erros de atributos."""
        self.assertRaises(AttributeError, mostra_pokemons, None, None)
        self.assertRaises(AttributeError, mostra_pokemons, self.poke1, None)
        self.assertRaises(AttributeError, mostra_pokemons, None, self.poke1)

    def test_escolhe_ataque(self):
        """Faz diversas verificações de input na escolha dos ataques."""
        # Primeiro testamos como se nosso pokemons estivesse sem pp.
        # O comportamento esperado é que utilize Struggle.
        batalha.input = Mock(return_value="ok")
        with patch("pokemon.Pokemon.todos_ataques_sem_pp", return_value=True):
            self.assertEqual(self.poke2.todos_ataques_sem_pp(), True)
            self.assertEqual((escolhe_ataque(self.poke1, self.poke2)).nome,
                              self.struggle.nome)

        # Testando se escolhe_ataque está retornando os ataques corretos
        for i in range(len(self.poke1.ataques)):
            batalha.input = Mock(return_value=(i+1))
            self.assertEqual(escolhe_ataque(self.poke1, self.poke2),
                             self.poke1.ataques[i])

        # Nesse ponto o escolhe_ataque receberá de input 4 valores "errados"
        # e um certo. O comportamento esperado é que a função não levante
        # exceções com os valores errados e execute normalmente quando chegar
        # o correto.
        valores_errados = [self.poke1.nome,
                           random.uniform(-100, 100), 5, -1, 1]
        batalha.input = Mock(side_effect=valores_errados)
        self.assertTrue(escolhe_ataque(self.poke1, self.poke2) in self.poke1.ataques)

    def test_realiza_ataque_e_calcula_dano(self):
        """Verifica se ataque e suas consequências ocorrem sem problemas."""
        batalha.input = Mock(return_value="ok")

        # Geramos novos Pokémons para podermos realizar vários
        # testes sem acabar com todo o HP deles.
        for i in range(100):
            a = RandomPoke()
            b = RandomPoke()
            poke3 = poke1 = Pokemon(a.gera())
            poke4 = poke2 = Pokemon(b.gera())

            # Assumindo que o ataque sempre vai acertar
            with patch('batalha.random.uniform', return_value=1.0):
                # Aqui começa o cálculo do dano
                lvl = poke1.lvl
                ataque = Ataque(a.gera_ataque())
                if ataque.typ.especial:
                    atk = poke1.spc
                    dfs = poke2.spc
                else:
                    atk = poke1.atk
                    dfs = poke2.dfs

                pp = ataque.pp
                hp = poke2.hp
                base = ataque.pwr
                eff = efetividade(ataque, poke2, False)

                dano = (2*lvl + 10)/250 * atk/dfs * base + 2
                dano *= (stab(ataque, poke1) * critico(poke1, eff)
                         * eff * aleatorio())
                dano = int(dano)
                #Testa o dano.calcula_dano
                self.assertEqual(dano, calcula_dano(ataque, poke1, poke2))
                if (dano > 0):
                    poke1.remove_hp(dano)
                if ataque == self.struggle:
                    dano //= 2
                    poke2.remove(hp.dano)

                # Verficamos se o Pokemon.realiza_ataque está
                # aplicando corretamente o dano conforme a fórmula.
                pokemon.input = Mock(return_value="\n")
                poke3.realiza_ataque(ataque, poke4)
                self.assertEquals(pp - 1, ataque.pp)
                self.assertEquals(poke1.hp, poke3.hp)
                self.assertEquals(poke2.hp, poke4.hp)

    def tearDown(self):
        """Encerra os testes."""
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
