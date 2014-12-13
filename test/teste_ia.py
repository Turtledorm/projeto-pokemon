import os
import sys
from random import randint, choice
from string import ascii_lowercase, ascii_uppercase
import unittest
from mock import Mock, patch, PropertyMock
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from tipo import le_tipos
le_tipos("tipos.txt")
from ia import mais_preciso, melhor_ataque
import pokemon
from pokemon import Pokemon
from random_poke import RandomPoke
from ataque import Ataque
class IaTestCase(unittest.TestCase):
        
    def teste_melhor_ataque(self):
        """ Vamos testar se a função melhor_ataque dá realmente o 
            ataque com a melhor relação dano x acurácia testando 
            todos os ataques do pokemon atacante no pokemon defensor."""

        for j in range(100):
            #Cria um pokemon atacante e um defensor
            dados_atk = RandomPoke()
            dados_def = RandomPoke()
            atacante = Pokemon(dados_atk.gera())
            defensor = Pokemon(dados_def.gera())
           
            
            melhor = melhor_ataque(atacante, defensor)
            danos = []
            if atacante.hp < atacante.hp_max/5:
                estado_critico = True
            else:
                estado_critico = False
            for ataque in atacante.ataques:
                if ataque.pp > 0 and estado_critico is False:
                    dano = ataque.calcula_dano(atacante, defensor, is_basico=True)
                    danos.append(dano * ataque.acu/100)  
                elif ataque.pp > 0 and estado_critico is True:
                    dano = ataque.calcula_dano(atacante, defensor, is_basico=True)    
            
            # Caso não tire todo o hp, escolhe o que causa (em média) o maior
            # dano usando a relação dano x acurácia.
            if max(danos) < defensor.hp:
                self.assertAlmostEqual(max(danos), melhor, 1)

    def teste_mais_preciso(self):
        """Para testarmos se a função escolhe o ataque mais preciso, geramos
        pokemons cujos ataques mais precisos sempre serão os últimos na 
        lista de ataques do pokemon""" 
        for j in range(50):
            poke = self.gera_poke()    
            self.assertEqual(mais_preciso(poke, [i for i in range(4)]), poke.get_ataque(3))                  
    
    def gera_ataque(self, acu, pwr, pp):
        """Gera um ataque com atributos aleatórios."""
        return [''.join(choice(ascii_lowercase + ascii_uppercase)
                        for x in range(randint(2, 10))),
                randint(1, 15),
                acu,
                pwr,
                pp]
    
    def gera_poke(self):
        """Gera pokemons tais que os ataques estão ordenados em ordem 
        crescente de pwr e acu."""
        t = RandomPoke()
        dados = t.gera()
        dados = dados[:9] #Tiramos a lista de ataques aleatórios
        ataque = []
        rand_num = randint(1, 97)
        for i in range(4): #Criamos ataques ordenados
            ataque.append(self.gera_ataque(i + rand_num, i + rand_num, 
                                           randint(1, 255)))
        
        ataques = [Ataque(ataque[i]) for i in range(4)]
        dados.append(ataques)   
        poke = Pokemon(dados) #Agora nosso pokemón contém os ataques ordenados 
        return poke

# Inicializa o unittest, que cuidará do resto
if __name__ == '__main__':
    unittest.main()
    
