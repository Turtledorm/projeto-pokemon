#!/usr/bin/python3
tipo = {0: "Normal", 1: "Fighting" , 2: "Flying" ,3: "Poison" ,4: "Ground" ,5: "Rock" ,
6: "Bird" ,7: "Bug" ,8: "Ghost" ,9: "Fire" ,10: "Water" ,11: "Grass" ,12: "Electric" ,13: "Psychic"
, 14: "Ice" ,15: "Dragon" ,16: "Blank"}
import unittest 
class Pokemon:
    nome = None
    lvl = None
    hp_atual = None
    tipo1 = None
    tipo2 = None
    atributos = {"HP" : 0 , "ATK" : 0, "DEF" : 0, "SPD" : 0, "SPC" : 0}    

    def __init__(self, nome, lvl, tipo1, tipo2):
        self.nome  = nome
        self.lvl   = lvl
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.ataques_pokemon = []
        
    def cria_atributos(self, hp, atk, df, spd, spc):
        self.atributos["HP" ] = hp
        self.atributos["ATK"] = atk
        self.atributos["DEF"] = df
        self.atributos["SPD"] = spd
        self.atributos["SPC"] = spc
    
    def adiciona_ataque(self, nome, typ, acu, pwr, pp):
        if len(self.ataques_pokemon) >= 4:
           raise Exception("Não pode mais que 4 ataques")
        else:
            self.ataques_pokemon.append(Ataque(nome, typ, acu, pwr, pp))
    
    
    def mostra_ataques(self):
        for ataque in self.ataques_pokemon:
           print(ataque.nome)
           print(ataque.typ)
           print(ataque.acu)
           print(ataque.pwr)
           print(ataque.pp_MAX)
             

class Ataque:

    nome = None
    typ = None
    acu = None
    pwr = None
    pp_MAX = None
    pp_atual = None

    def __init__(self, nome, typ, acu, pwr, pp):
        self.nome = nome
        self.typ = typ
        self.acu = acu
        self.pwr = pwr
        self.pp_MAX = pp
        self.pp_atual = pp

    
