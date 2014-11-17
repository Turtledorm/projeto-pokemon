#!/usr/bin/env python3

"""Verificação dos argumentos por linha de comando."""

import sys
from multiplayer import programa_cliente, programa_servidor, cria_bs
from entrada import le_pokemon
from batalha import batalha

try:
    for arg in sys.argv[1:]:
        if arg == "-c":
            programa_cliente()
        elif arg == "-s":
            programa_servidor()
        elif arg == "-l":
            batalha(le_pokemon(), le_pokemon())

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido!")
