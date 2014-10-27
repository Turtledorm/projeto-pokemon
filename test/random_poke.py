import os
import sys
from random import randint, choice
from string import ascii_lowercase, ascii_uppercase

sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import Pokemon, Ataque, le_tipos


class RandomPoke(Pokemon):

    """Representa um Pokémon. Ao invés de receber dados pré-lidos, porém,
       gera os atributos aleatoriamente."""

    def __init__(self):
        """Inicializa os dados para teste."""
        le_tipos("tipos.txt")

        self._nome = ''.join(choice(ascii_lowercase + ascii_uppercase)
                             for x in range(randint(2, 20)))
        self._lvl = randint(0, 100)
        self._hp = randint(10, 255)
        self._atk = randint(1, 255)
        self._dfs = randint(1, 255)
        self._spd = randint(0, 255)
        self._spc = randint(1, 255)
        self._tipo1 = randint(0, 15)
        while True:
            self._tipo2 = randint(0, 16)
            if (self._tipo2 != self._tipo1):
                break

        self._ataques = [self.gera_ataque(),
                         self.gera_ataque(),
                         self.gera_ataque(),
                         self.gera_ataque()]

        self.dados = [self._nome, self._lvl, self._hp, self._atk, self._dfs,
                      self._spd, self._spc, self._tipo1, self._tipo2,
                      [Ataque(self._ataques[i]) for i in range(4)]]

    def gera_ataque(self):
        """Gera um ataque com atributos aleatórios."""
        return [''.join(choice(ascii_lowercase + ascii_uppercase)
                        for x in range(randint(2, 10))),
                randint(0, 16),
                randint(1, 100),
                randint(1, 100),
                randint(1, 255)]

    def gera(self):
        """Retorna a lista que deve ser passada a pokemon.Pokemon
           para criar um pokemon com os valores acima gerados."""
        return self.dados
