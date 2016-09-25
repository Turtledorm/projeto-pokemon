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
    if "-a" in sys.argv:
        cpu1 = cpu2 = True
    elif "-b" in sys.argv:
        cpu1 = True
    if "-d" in sys.argv:
        set_debug()

    # Local
    if "-l" in sys.argv:
        poke1 = le_pokemon(cpu1)
        poke2 = le_pokemon(cpu2)
        batalha_local(poke1, poke2)

    # Cliente
    elif "-c" in sys.argv:
        cliente = Cliente(cpu1)
        cliente.conecta_ao_servidor()
        cliente.loop()

    # Servidor
    elif "-s" in sys.argv:
        servidor = Servidor(cpu1)
        try:
            servidor.app.run(debug=True)
        except OSError:
            print("ERRO: Endereço do servidor já em uso.")

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido.")
    exit(1)
