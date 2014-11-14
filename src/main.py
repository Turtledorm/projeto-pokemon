#!/usr/bin/env python3
"""Verificação dos argumentos por linha de comando."""

import sys
from multiplayer import programa_cliente, programa_server
from entrada import le_pokemon
from batalha import batalha

for arg in sys.argv[1:]:
    if arg == "-c":
        programa_cliente()
    elif arg == "-s":
        programa_server()
    elif arg == "-l":
        batalha(le_pokemon(), le_pokemon())
