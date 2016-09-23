#!/usr/bin/env python3

"""Módulo principal.
   Verificação dos argumentos por linha de comando."""

import sys
from entrada import le_pokemon
from batalha import batalha_local
from cliente import Cliente
from servidor import Servidor

try:
    cpu1 = False
    cpu2 = False
    debug = False

    # Verifica se algum jogador será controlado pelo CPU e modo debug
    for arg in sys.argv[1:]:
        if arg == "-a":
            cpu1 = cpu2 = True
        elif arg == "-b":
            cpu1 = True
        if arg == "-d":
            debug = True

    for arg in sys.argv[1:]:
        # Local
        if arg == "-l":
            poke1 = le_pokemon(cpu1, debug)
            poke2 = le_pokemon(cpu2, debug)
            batalha_local(poke1, poke2)

        # Cliente
        elif arg == "-c":
            cliente = Cliente(cpu1 or cpu2, debug)
            cliente.conecta_ao_servidor()
            while not cliente.acabou_batalha():
                cliente.jogada()
            cliente.finaliza()

        # Servidor
        elif arg == "-s":
            servidor = Servidor(cpu1 or cpu2, debug)
            try:
                servidor.app.run()
            except OSError:
                print("Endereço do servidor já em uso!")

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido!")
    exit(1)
