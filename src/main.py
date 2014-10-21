#!/usr/bin/python3

from pokemon import Pokemon, le_tipos
from batalha import batalha
import os

#Para que o script leia tipos.txt mesmo se executado de fora do diretório onde ele está
__diretorio = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
le_tipos(os.path.join(__diretorio, "tipos.txt"))

poke1 = Pokemon()
poke2 = Pokemon()
batalha(poke1, poke2)
