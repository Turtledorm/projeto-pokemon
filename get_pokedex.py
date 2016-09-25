"""Script que gera arquivos de todos os pokemons da primeira geração.
   Dados são importados do site pokemondb.net. Os status são referentes ao
   nível 100 (sem bônus) e ataques que não causam dano são desconsiderados."""

import os
import pycurl
from io import BytesIO
from bs4 import BeautifulSoup

from projeto.tipo import get_tipo_id

def get_soup(c, url):
    """Recebe um objeto Curl e uma URL.
       Devolve o objeto BeautifulSoup da página em questão."""
    buffer = BytesIO()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    html = buffer.getvalue()
    return BeautifulSoup(html, "html.parser")


#
url_site = "https://pokemondb.net"
c = pycurl.Curl()
c.setopt(pycurl.USERAGENT,  
         "Mozilla/5.0 (compatible; pycurl)") # Evita problema de ass. inválida

# Obtém página com lista de Pokémons da 1ª geração
soup = get_soup(c, url_site + "/pokedex/game/firered-leafgreen")

# Lista de tags de Pokémons
pokes = soup.find_all("span", {"class": "game-red-blue"})

for p in pokes:
    # Coleta nome e tipo(s)
    a = p.find("a", {"class": "ent-name"})
    nome = a.text
    tipos = soup.find_all("a", {"class": "itype"})
    tipo1 = get_tipo_id(tipos[0].text)
    tipo2 = get_tipo_id(tipos[1].text) if len(tipos) == 2 else None

    # Caminho do arquivo a ser gravado
    arq_path = os.path.join("pokemon", nome + ".txt")

    with open(arq_path, "w") as arq:
        # Escreve nome e nível
        lvl = 100
        arq.write(nome + "\n" + str(lvl) + "\n")

        # Página do Pokémon
        url = url_site + "/" + a["href"] 
        soup = get_soup(c, url)

        # Coleta atributos numéricos
        tds = soup.find_all("td", {"class": "num"})
        atribs = [t.text for t in tds[1:17:3]]
        del atribs[4]  # Remove SPC duplicado
        for x in atribs:
            arq.write(x + "\n")

        # Escreve tipos
        arq.write(str(tipo1) + "\n")
        if tipo2:
            arq.write(str(tipo1) + "\n")

        # Página dos ataques da 1ª geração
        url += "/moves/1"
        soup = get_soup(c, url)

        import pdb; pdb.set_trace()

        ataques = []
        table = soup.find("table", {"class": "data-table wide-table"})
        trs = table.tbody.find_all("tr")
        for tr in trs:
            if tr.i.nome == "Status":
                continue
            nome = tr.a.text
            url = url_site + tr.a.href
            soup = get_soup(c, url)
            table = soup.find("table", {"class": "vitals-table key-table"})
            trs = table.tbody.find_all("tr")
            for tr in trs:
                






# Encera curl
c.close()
