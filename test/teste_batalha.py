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
from pokemon import Pokemon, Ataque, le_tipos, get_eff
le_tipos("tipos.txt")

import batalha
from batalha import quem_comeca, escolhe_ataque, mostra_pokemons, \
    struggle, acertou, stab, critico, efetividade, realiza_ataque, aleatorio
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
            self.assertEqual(escolhe_ataque(self.poke1), struggle)

        # Testando se escolhe_ataque está retornando os ataques corretos
        for i in range(len(self.poke1.ataques)):
            batalha.input = Mock(return_value=(i+1))
            self.assertEqual(escolhe_ataque(self.poke1), self.poke1.ataques[i])

        # Nesse ponto o escolhe_ataque receberá de input 4 valores "errados"
        # e um certo. O comportamento esperado é que a função não levante
        # exceções com os valores errados e execute normalmente quando chegar
        # o correto.
        valores_errados = [self.poke1.nome,
                           random.uniform(-100, 100), 5, -1, 1]
        batalha.input = Mock(side_effect=valores_errados)
        self.assertTrue(escolhe_ataque(self.poke1) in self.poke1.ataques)

    def test_acertou(self):
        chance = (self.poke1.ataques[0].acu * self.poke1.ataques[0].acu)/10000
        maior_chance = chance + 0.001
        valores_menores = []
        valores_maiores = []

        for i in range(100):
            valores_menores.append(random.uniform(0, chance))
            valores_maiores.append(random.uniform(chance, 1))
        valores = valores_menores + valores_maiores

        # Usamos valores conhecidos para testar a unidade do batalha.acertou
        # que usa números pseudo-aleatórios.
        with patch("batalha.random.uniform", side_effect=valores):
            for i in range(100):
                self.assertTrue(acertou(self.poke1.ataques[0]))
            for i in range(100):
                self.assertFalse(acertou(self.poke1.ataques[0]))

        self.assertRaises(AttributeError, acertou, self.poke1.nome)
        self.assertRaises(AttributeError, acertou, self.poke1.hp)
        self.assertRaises(AttributeError, acertou, None)

    def test_stab(self):
        ataque = self.poke1.ataques[0]
        not_typ = 0
        while not_typ == ataque.typ:
            not_typ = random.randint(0, 255)

        # É esperado que se o typ do ataque for igual ao tipo1 ou tipo2
        # do atacante, batalha.stab devolve 1.5. Caso contrário, devolve 1.
        poke = "pokemon.Pokemon."
        with patch(poke + "tipo1", PropertyMock(return_value=ataque.typ)):
            with patch(poke + "tipo2", PropertyMock(return_value=ataque.typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)
            with patch(poke + "tipo2", PropertyMock(return_value=not_typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)

        with patch(poke + "tipo2", PropertyMock(return_value=ataque.typ)):
            with patch(poke + "tipo1", PropertyMock(return_value=not_typ)):
                self.assertEqual(stab(ataque, self.poke1), 1.5)
                with patch(poke + "tipo2", PropertyMock(return_value=not_typ)):
                    self.assertEqual(stab(ataque, self.poke1), 1)

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

        with patch("batalha.random.uniform", side_effect=valores):
            # Em cada loop, a iteração chamará batalha.critico duas
            # vezes, usando, então, dois valores do side_effect.
            for i in range(50):
                self.assertEqual(critico(self.poke1, 0), 1)
                self.assertEqual(critico(self.poke1,
                                         random.randint(1, 100)), res)
            for i in range(50):
                self.assertEqual(critico(self.poke1, 0), 1)
                self.assertEqual(critico(self.poke1,
                                         random.randint(1, 100)), 1)

        self.assertRaises(AttributeError, critico, self.poke1.nome, None)
        self.assertRaises(AttributeError, critico, self.poke1.hp, None)
        self.assertRaises(AttributeError, critico, None, self.poke1.nome)
        self.assertRaises(AttributeError, critico, None, self.poke1.hp)

    def test_realiza_ataque(self):
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
                if ataque.typ.is_especial:
                    atk = poke1.spc
                    dfs = poke2.spc
                else:
                    atk = poke1.atk
                    dfs = poke2.dfs

                pp = ataque.pp
                hp = poke2.hp
                base = ataque.pwr
                eff = efetividade(ataque, poke2)

                dano = (2*lvl + 10)/250 * atk/dfs * base + 2
                dano *= (stab(ataque, poke1) * critico(poke1, eff)
                         * eff * aleatorio())
                dano = int(dano)

                if (dano > 0):
                    poke1.remove_hp(dano)
                if ataque == struggle:
                    dano //= 2
                    poke2.remove(hp.dano)

                # Verficamos se o batalha.realiza_ataque está diminuindo
                # aplicando corretamente o dano conforme a fórmula.
                realiza_ataque(poke3, poke4, ataque)
                self.assertEquals(pp - 1, ataque.pp)
                self.assertEquals(poke1.hp, poke3.hp)
                self.assertEquals(poke2.hp, poke4.hp)

    def test_efetividade(self):
        """Verifica se o cálculo de efetividade é feito corretamente."""
        # Novamente geramos um novo Pokémon para podermos realizar vários
        # testes com resultados diferentes.
        for i in range(100):
            a = RandomPoke()
            poke1 = Pokemon(a.gera())
            ataque = Ataque(a.gera_ataque())

            # Esta é a fórmula para calcular efetividade
            typ_ataque = ataque.typ.numero
            mult = get_eff(typ_ataque, poke1.tipo1.numero)
            if poke1.tipo2.nome != "Blank":
                mult *= get_eff(typ_ataque, poke1.tipo2.numero)

            self.assertEquals(mult, efetividade(ataque, poke1))

    def tearDown(self):
        """Encerra os testes."""
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
