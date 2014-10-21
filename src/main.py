#!/usr/bin/python3

from pokemon import Pokemon, le_tipos
import batalha

le_tipos("tipos.txt")

poke1 = Pokemon()
poke2 = Pokemon()
batalha.loop(poke1, poke2)
