from random import randint, choice
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import le_tipos, Ataque
from string import ascii_lowercase, ascii_uppercase

class RandomPoke: 
    def __init__(self):
        
        """Inicializa os dados para teste."""
        le_tipos("tipos.txt")
    
        self._nome = ''.join(choice(ascii_lowercase + ascii_uppercase) for x in range(randint(2, 20)))
        self._lvl = randint(0, 100)
        self._hp = randint(0, 255)
        self._atk = randint(0, 255)
        self._dfs = randint(0, 255)
        self._spd = randint(0, 255)
        self._spc = randint(0, 255)
        self._tipo1 = randint(0, 15)
        while True:
            self._tipo2 = randint(0, 16)
            if (self._tipo2 != self._tipo1):
                break
    
        self._ataques = [["n1", 1, 21, 10, 246],
                        ["n2", 2, 22, 11, 247],
                        ["n3", 3, 23, 12, 248],
                        ["n4", 4, 24, 13, 249]]
    
        self.dados = [self._nome, self._lvl, self._hp, self._atk, self._dfs,
                 self._spd, self._spc, self._tipo1, self._tipo2,
                 [Ataque(self._ataques[i]) for i in range(4)]]
                
    
    def gera(self):
        """Retorna a lista que deve ser passada para pokemon.Pokemon 
        para criar um pokemon com os valores acima gerados."""
        return self.dados             

    @property
    def nome(self):
        return self._nome
   
    @property
    def lvl(self):
        return self._lvl
    
    @property
    def hp(self):
        return self._hp
   
    @property
    def atk(self):
        return self._atk        
   
    @property
    def dfs(self):
        return self._dfs
   
    @property              
    def spd(self):
        return self._spd
   
    @property
    def spc(self):
        return self._spc
    
    @property
    def tipo1(self):
        return self._tipo1        
    
    @property
    def tipo2(self):
        return self._tipo2 
    
    @property
    def ataques(self):
        return self._ataques  
       
