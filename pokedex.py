#!/usr/bin/env python3

"""Script que gera arquivos de todos os pokemons da primeira geração.
   Dados são importados do site pokemondb.net. Os status são referentes ao
   nível 100 (sem bônus) e ataques que não causam dano são desconsiderados."""

import os

import requests
from bs4 import BeautifulSoup

from projeto.tipo import get_tipo_id, get_num_tipos

# Endereço do site
SITE_URL = "https://pokemondb.net"


def get_soup(url):
    """Recebe uma URL e devolve o objeto
       BeautifulSoup da página em questão."""
    r = requests.get(url)
    return BeautifulSoup(r.text, "html.parser")


# Obtém página com lista de Pokémons da 1ª geração
soup = get_soup(SITE_URL + "/pokedex/game/firered-leafgreen")

# Lista de tags de Pokémons
pokes = soup.find_all("span", {"class": "game-red-blue"})

for p in pokes:
    # Coleta nome e tipo(s)
    a = p.find("a", {"class": "ent-name"})
    nome = a.text
    tipos = p.find_all("a", {"class": "itype"})
    tipo1 = get_tipo_id(tipos[0].text)
    tipo2 = get_tipo_id(tipos[1].text) if len(tipos) == 2 else get_num_tipos()

    # Caminho do arquivo a ser gravado
    arq_path = os.path.join("pokemon", nome + ".txt")

    with open(arq_path, "w") as arq:
        # Escreve nome e nível
        lvl = "100"
        arq.write(nome + "\n" + lvl + "\n")

        # Página do Pokémon
        url = SITE_URL + "/" + a["href"]
        soup = get_soup(url)

        # Coleta atributos numéricos
        tds = soup.find_all("td", {"class": "num"})
        atribs = [t.text for t in tds[1:17:3]]
        del atribs[4]  # Remove SPC duplicado
        for atrib in atribs:
            arq.write(atrib + "\n")

        # Escreve tipos
        arq.write(str(tipo1) + "\n" + str(tipo2) + "\n")

        # Página dos ataques da 1ª geração
        url += "/moves/1"
        soup = get_soup(url)

        # Cria lista e itera-se entre os ataques
        ataques = []
        table = soup.find("table", {"class": "data-table wide-table"})
        trs = table.tbody.find_all("tr")
        for tr in trs:
            # Se poder for nulo, ignora
            if tr.find_all("td")[4].text == "-":
                continue
            atk_nome = tr.a.text
            # Se ataque já existir na lista, ignora
            if atk_nome in [atk[0] for atk in ataques]:
                continue

            # Vamos para a página do ataque (para pegar o maldito PP)
            url = SITE_URL + tr.a["href"]
            soup = get_soup(url)

            # Obtém-se atributos e coloca-os na lista
            table = soup.find("table", {"class": "vitals-table key-table"})
            trs = table.tbody.find_all("tr")
            vals = [tr.td.text for tr in trs]
            typ = str(get_tipo_id(vals[0])) if vals[0] != "Dark" else "0"
            acu = vals[3] if vals[3] != "∞" else "100"
            pwr = vals[2]
            pp = vals[4].split()[0]
            ataques.append([atk_nome, typ, acu, pwr, pp])

        # Finalmente, escreve-se os ataques
        num_ataques = len(ataques)
        arq.write(str(num_ataques) + "\n")
        for ataque in ataques:
            for atrib in ataque:
                arq.write(atrib + "\n")

        print(nome, "criado com sucesso!")
