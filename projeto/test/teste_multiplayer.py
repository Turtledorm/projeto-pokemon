#!/usr/bin/env python3

"""Testa as funcionalidades do módulo multiplayer, como a conversão de um
   Pokémon para xml (e vice-versa) e as batalhas entre cliente e servidor."""

import unittest
import random
import sys
import os
from mock import patch, Mock
sys.path.insert(1, os.path.join(sys.path[0], "../src"))
from tipo import le_tipos
le_tipos("tipos.txt")
from pokemon import Pokemon
from cliente import *
from servidor import *
from random_poke import RandomPoke
import entrada, batalha, pokemon, servidor
from batalha import *
from battle_state import *


class MultiplayerTestCase(unittest.TestCase):

    def setUp(self):
        """Inicializa dados para teste."""
        sys.stdout = open(os.devnull, "w")  # Suprime o output de batalha.py
        sys.stderr = sys.stdout
        self.srv = Servidor(False)
        self.srv.app.config["TESTING"] = True
        self.app = self.srv.app.test_client()
        self.data1 = RandomPoke()
        self.data2 = RandomPoke()
        self.dados1 = self.data1.gera()
        self.dados2 = self.data2.gera()
        self.poke1 = Pokemon(self.dados1)
        self.poke2 = Pokemon(self.dados2)

    def test_servidor_ataca(self):
        """Teste de ataques do servidor."""
        t = self.quem_primeiro()
        poke_servidor = t["Servidor"]
        poke_cliente = t["Cliente"]

        # dados_servidor contém as especificações de um Pokémón no formato
        # recebido por le_pokemon().
        dados_servidor = t["Dados do servidor"]

        # Usamos esse patch para a função le_pokemon() retornar o
        # poke_servidor ao invés de ler algum outro do stdin.
        with patch("entrada.input", side_effect=dados_servidor):

            # Para termos controle sobre os resultados das batalhas
            with patch("batalha.random.uniform", return_value=float(0.5)):

                # O número do ataque nos será pedido pelo stdin; vamos escolher
                # sempre o primeiro.
                with patch("batalha.input", return_value=1):
                    pokemon.input = Mock(return_value="\n")
                        
                    # Façamos primeiro o teste multiplayer
                    bs_multi = self.app.post("/battle/",
                                             data=poke_cliente.to_xml())

                    # Removendo o b" "
                    bs_multi = self.padroniza(bs_multi.data)

                    # Vamos realizar a mesma batalha agora no modo offline
                    poke_servidor.realiza_ataque(escolhe_ataque(poke_servidor, 
                                                 poke_cliente), poke_cliente)

                    # Vamos testar se os resultados são os mesmo se simularmos
                    # no modo offline, já testado pelos outros arquivos de
                    # teste e plenamente operante.
                    self.assertEqual(cria_bs(poke_cliente, poke_servidor),
                                     bs_multi)
        
    def test_cliente_ataca(self):
        """Procedemos da mesma maneira que no método test_servidor_ataca(),
           mas aqui também testamos o ataque do cliente."""
        t = self.quem_primeiro()
        poke_servidor = t["Servidor"]
        poke_cliente = t["Cliente"]
        dados_servidor = t["Dados do servidor"]

        # Mesma coisa que no método teste_servidor_ataca
        with patch("entrada.input", side_effect=dados_servidor):
            with patch("batalha.random.uniform", return_value=float(0.5)):
                with patch("batalha.input", return_value=1):

                    pokemon.input = Mock(return_value="\n")
                    self.app.post("/battle/", data=poke_cliente.to_xml())
                    id = escolhe_ataque(poke_cliente, poke_servidor)
                    id = poke_cliente.ataques.index(id) + 1
                    multi_bs = self.app.post("/battle/attack/" + str(id))
                    multi_bs = self.padroniza(multi_bs.data)

                    poke_servidor.realiza_ataque(escolhe_ataque(poke_servidor, 
                                                 poke_cliente), poke_cliente)
                    poke_cliente.realiza_ataque(poke_cliente.get_ataque(id-1),
                                                poke_servidor)

                    if poke_cliente.hp > 0 and poke_servidor.hp > 0:
                        ataque = escolhe_ataque(poke_servidor, poke_cliente)
                        poke_servidor.realiza_ataque(ataque, poke_cliente)
                    off_bs = cria_bs(poke_cliente, poke_servidor)

                    self.assertEqual(off_bs, multi_bs)
    
    def test_shutdown(self):
        """Verifica se o programa está sendo encerrado corretamente."""
        self.assertRaises(RuntimeError, self.app.post, "/shutdown/")
    
    def test_locked(self):
        """Como no setUp iniciamos o app, todas as vezes que tentarmos
           mandar um POST para /battle/ resultará no erro 423."""
        self.srv.app.config["TESTING"] = False
        with patch("entrada.input", side_effect=self.data1.gera_linear()):
            self.app.post("/battle/")
            erro_423 = self.app.post("/battle/")
            erro_423 = self.padroniza(erro_423.data)
            self.assertTrue("Locked" in erro_423)

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

    def padroniza(self, data):
        """Converte o resultado da requisição em uma string BattleState."""
        data = str(data).replace("b'", "")
        data = data[:-1]
        return data

    def quem_primeiro(self):
        """Usa dicionários para retornar nessa ordem o Pokémon gerado
           aleatoriamente que ataca primeiro no jogo, o que ataca em segundo e,
           por fim, uma lista com os dados do Pokémon a ser usado pelo
           servidor, que é o que começa atacando nestes testes"""
        if quem_comeca(self.poke1, self.poke2) == self.poke1:
            return {"Servidor": self.poke1, "Cliente": self.poke2,
                    "Dados do servidor": self.data1.gera_linear()}
        else:
            return {"Servidor": self.poke2, "Cliente": self.poke1,
                    "Dados do servidor": self.data2.gera_linear()}

    def tearDown(self):
        """Encerra os testes."""
        sys.stdout.close()  # Fechando o os.devnull
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__


if __name__ == "__main__":
    unittest.main()
