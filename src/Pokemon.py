tipo = {0: "Normal", 1: "Fighting" , 2: "Flying" ,3: "Poison" ,4: "Ground" ,5: "Rock" ,
6: "Bird" ,7: "Bug" ,8: "Ghost" ,9: "Fire" ,10: "Water" ,11: "Grass" ,12: "Electric" ,13: "Psychic"
, 14: "Ice" ,15: "Dragon" ,16: "Blank"}

class Pokemon:
    nome = None
    lvl = None
    hpAtual = None
    tipo1 = None
    tipo2 = None
    atributos = {"HP" : 0 , "ATK" : 0, "DEF" : 0, "SPD" : 0, "SPC" : 0}

    def __init__(self,nome,lvl,tipo1,tipo2):
        self.nome = nome
        self.lvl = lvl
        self.tipo1=tipo1
        self.tipo2=tipo2
        
    def criaAtibutos(self , HP,ATK,DEF,SPD,SPC):
        self.atributos[HP] = hp
        self.atributos[ATK] = ATK
        self.atributos[DEF] = DEF
        self.atributos[SPD] = SPD
        self.atributos[SPC] = SPC


class Ataque:

    nome = None
    typ = None
    acu = None
    pwr = None
    ppMAX = None
    ppAtual = None

    def __init__(self,nome,typ,acu,pwr,pp):
        self.nome = nome
        self.typ = typ
        self.acu = acu
        self.pwr = pwr
        self.ppMAX = pp
        self.ppAtual = pp

    
