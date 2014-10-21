#!/usr/bin/python3

from pokemon import Pokemon, le_tipos
from batalha import batalha

le_tipos("tipos.txt")

poke1 = Pokemon()
poke2 = Pokemon()
batalha(poke1, poke2)
