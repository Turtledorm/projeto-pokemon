#!/usr/bin/env python3

"""Módulo principal.
   Verificação dos argumentos por linha de comando."""

import sys

from entrada import le_pokemon
from batalha import batalha_local, set_debug
from cliente import Cliente
from servidor import Servidor

try:
    # Verifica se algum jogador será controlado pelo CPU e modo debug
    cpu1 = False
    cpu2 = False
    for arg in sys.argv[1:]:
        if arg == "-a":
            cpu1 = cpu2 = True
        elif arg == "-b":
            cpu1 = True
        if arg == "-d":
            set_debug()

    for arg in sys.argv[1:]:
        # Local
        if arg == "-l":
            poke1 = le_pokemon(cpu1)
            poke2 = le_pokemon(cpu2)
            batalha_local(poke1, poke2)

        # Cliente
        elif arg == "-c":
            cliente = Cliente(cpu1)
            cliente.conecta_ao_servidor();
            cliente.rotina()

        # Servidor
        elif arg == "-s":
            servidor = Servidor(cpu1)
            try:
                servidor.app.run(debug=True)
            except OSError:
                print("ERRO: Endereço do servidor já em uso.")

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido.")
    exit(1)
