#!/usr/bin/python3  

# from pokemon import Pokemon

tipos = {}

# Cria tabela de efetividades inicialmente com 1s
tabela_eff = [[1 for i in range(16)] for j in range(16)]

arq = open("tipos.txt", "r")
for i in range(16):
    tipos[i] = arq.readline()
    
    super_eff = arq.readline().split(" ")
    if len(super_eff) > 1:
        for j in super_eff:
            tabela_eff[i][int(j)] = 2

    not_eff = arq.readline().split(" ")
    if len(not_eff) > 1:
        for j in not_eff:
            tabela_eff[i][int(j)] = 0.5

    no_effect = arq.readline().split(" ")
    if len(no_effect) > 1:
        for j in no_effect:
            tabela_eff[i][int(j)] = 0

arq.close()

for line in tabela_eff:
    print(line)

poke = Pokemon()
poke()
poke.exibe_ataques()
