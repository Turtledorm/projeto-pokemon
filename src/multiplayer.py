import httplib
import urllib


def inicia_batalha(poke):
    
    battle_state = BattleState(poke)
    path = "/battle/"

    url = "www.python.org"
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "", battle_state)

    resposta = conn.getresponse()

    # Aqui devemos de alguma forma pegar a resposta do oponente
    # e converter em um objeto do tipo Pokémon. Ou talvez não. Boa sorte.
    if True:
        poke_foe = None
        battle_state.add_foe(poke_foe)
    else:
        resposta


def ataque(poke1, poke2, id_ataque):

    battle_state = BattleState(poke1, poke2)
    path = "/battle/attack/" + str(id_ataque)

    url = "www.python.org"
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "")

    resposta = conn.getresponse()


class BattleState:

    def __init__(self, _poke):
        self.poke_server = _poke
    
    def add_foe(self, _poke):
        self.poke_foe = _poke