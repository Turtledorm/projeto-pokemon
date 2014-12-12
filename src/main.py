#!/usr/bin/env python3

"""Verificação dos argumentos por linha de comando."""

import sys
from entrada import le_pokemon
from batalha import batalha
from cliente import Cliente
import servidor

try:
    for arg in sys.argv[1:]:

        # Local
        if arg == "-l":
            batalha(le_pokemon(), le_pokemon())

        # Cliente
        elif arg == "-c":
            cliente = Cliente()
            cliente.conecta_servidor()
            while not cliente.acabou_batalha():
                cliente.jogada()
            cliente.finaliza()

        # Servidor
        elif arg == "-s":
            servidor = servidor.Servidor()
            try:
                servidor.app.run(debug=True)
            except OSError:
                print("Endereço do servidor já em uso!")

except (KeyboardInterrupt, EOFError):
    print("\nPrograma interrompido!")
