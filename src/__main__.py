#!/usr/bin/env python3

"""Módulo principal.
   Verificação dos argumentos por linha de comando."""

import sys
from entrada import le_pokemon
from batalha import batalha_local
from cliente import Cliente
from servidor import Servidor

try:
    is_cpu1 = False
    is_cpu2 = False

    # Verifica se algum jogador será controlado pelo CPU
    for arg in sys.argv[1:]:
        if arg == "-a":
            is_cpu1 = is_cpu2 = True
        elif arg == "-b":
            is_cpu1 = True

    for arg in sys.argv[1:]:
        # Local
        if arg == "-l":
            batalha_local(le_pokemon(is_cpu1), le_pokemon(is_cpu2))

        # Cliente
        elif arg == "-c":
            cliente = Cliente(is_cpu1 or is_cpu2)
            cliente.conecta_ao_servidor()
            while not cliente.acabou_batalha():
                cliente.jogada()
            cliente.finaliza()

        # Servidor
        elif arg == "-s":
            servidor = Servidor(is_cpu1 or is_cpu2)
            try:
                servidor.app.run(debug=False)
            except OSError:
                print("Endereço do servidor já em uso!")

    exit(0)

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido!")
    exit(1)

print("Nenhuma opção (local, cliente, servidor) digitada...")
