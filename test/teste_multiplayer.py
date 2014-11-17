#!/usr/bin/env python3 

"""Testa as funcionalidades do módulo multiplayer como a conversão de um 
   Pokémon para xml e vice-versa e as batalhas multiplayer"""
import unittest
import random
import sys
import os
from mock import patch
sys.path.insert(1, os.path.join(sys.path[0], '../src'))
from pokemon import Pokemon
import multiplayer 
from multiplayer import * 
from random_poke import RandomPoke
import entrada
from batalha import *

class MultiplayerTestCase(unittest.TestCase):

    def setUp(self):
        sys.stdout = open(os.devnull, "w")  # Suprime o output de batalha.py
        sys.stderr = sys.stdout
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.data1 = RandomPoke()
        self.data2 = RandomPoke()
        self.dados1 = self.data1.gera()
        self.dados2 = self.data2.gera()
        self.poke1 = Pokemon(self.dados1)
        self.poke2 = Pokemon(self.dados2)
        
    def test_servidor_ataca(self): #Ver esse nome
        
        t = self.quem_primeiro()    
        poke_server  = t['Server']
        poke_cliente = t['Cliente']
        #dados_server contém as especificações de um pokemón no formato 
        #recebido por entrada.le_entrada.
        dados_server = t['Dados do server']

        #Usamos esse patch para a função entrada.le_pokemon retornar o 
        # poke_server ao invés de ler algum outro do stdin.
        with patch("entrada.input", side_effect=dados_server):
            #Para termos controle sobre os resultados das batalhas
            with patch("batalha.random.uniform", return_value = float(0.5)):
                #O número do ataque nos será pedido pelo stdin, vamos escolher
                #sempre o primeiro.
                with patch("batalha.input", return_value = 1): 
                
                    """Façamos primeiro o teste multiplayer""" 
                    bs_multi = self.app.post("/battle/", 
                                             data=poke_cliente.to_xml())
            
                    #Removendo o b' ' 
                    bs_multi = self.padroniza(bs_multi.data)        
                    
                    """Vamos realizar a mesma batalha agora no modo offline"""
                    
                    realiza_ataque(poke_server, poke_cliente, 
                                   escolhe_ataque(poke_server))
                    
                    """Vamos testar se os resultados são os mesmo se simularmos 
                    no modo offline, já testado pelos outros arquivos de teste 
                    e plenamente operante"""
                    self.assertEqual(cria_bs(poke_cliente, poke_server), 
                                             bs_multi)

    def test_cliente_ataca(self):
        """Vamos proceder da mesma maneira que na função acima mas 
        aqui vamos também testar o ataque do cliente""" 
        t = self.quem_primeiro()    
        poke_server  = t['Server']
        poke_cliente = t['Cliente']
        dados_server = t['Dados do server']
        
        #Mesma coisa que na função teste_servidor_ataca
        with patch("entrada.input", side_effect=dados_server):
            with patch("batalha.random.uniform", return_value = float(0.5)):
                with patch("batalha.input", return_value = 1): 
                   
                    self.app.post("/battle/", data=poke_cliente.to_xml())
                    id = escolhe_ataque(poke_cliente)
                    id = poke_cliente.ataques.index(id) + 1
                    multi_bs = self.app.post("/battle/attack/" + str(id))
                    multi_bs = self.padroniza(multi_bs.data)
                            
                    realiza_ataque(poke_server, poke_cliente, 
                                   escolhe_ataque(poke_server))
                    realiza_ataque(poke_cliente, poke_server,
                       poke_cliente.get_ataque(id-1))
                    
                    if poke_cliente.hp > 0 and poke_server.hp > 0:
                        ataque = escolhe_ataque(poke_server)
                        realiza_ataque(poke_server, poke_cliente, ataque)                  
                    off_bs = cria_bs(poke_cliente, poke_server)                             
                    
                    self.assertEqual(off_bs, multi_bs)
    
    def test_shutdown(self):
        """Como estamos no test_client, não é servidor"""
        self.assertRaises(RuntimeError, self.app.post, "/shutdown/")

    def test_xml(self):
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

    """Converte o resultado da requisição post em uma string BattleState"""
    def padroniza(self, data):
        data = str(data).replace("b'", "")
        data = data[:-1] 
        return data
    
    """Usa dicionários para retornar nessa ordem o pokemon gerado 
    aleatóriamente que ataca primeiro no jogo, o que ataca em segundo e
    uma lista com os dados do pokemon que vai para o server, que é o que começa
    atacando nesses testes""" 
    def quem_primeiro(self):
        if quem_comeca(self.poke1, self.poke2) == self.poke1:
            return {'Server':self.poke1, 'Cliente':self.poke2, 
                    'Dados do server':self.data1.gera_linear()}       
        else:
            return {'Server':self.poke2, 'Cliente':self.poke1, 
                    'Dados do server':self.data2.gera_linear()}  
    
    def tearDown(self):
        """Encerra os testes."""
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    
if __name__ == '__main__':
    unittest.main()
