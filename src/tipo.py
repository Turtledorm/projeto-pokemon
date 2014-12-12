"""Contém a classe que representa os tipos."""

import os

tipos = []       # Lista de tipos
tabela_eff = []  # Tabela com multiplicadores de efetividade


class Tipo:

    """Representa um tipo de Pokémon/ataque."""

    def __init__(self, numero, nome, is_especial):
        """Inicializa o tipo."""
        self._numero = numero
        self._nome = nome
        self._is_especial = is_especial

    def mostra(self):
        """Exibe informações do tipo."""
        print(str(self.numero) + ":", self.nome,
              "(Especial)" if self.is_especial else "")

    @property
    def numero(self):
        return self._numero

    @property
    def nome(self):
        return self._nome

    @property
    def is_especial(self):
        return self._is_especial

    def get_eff_contra(self, outro):
        """Devolve o valor da efetividade de um ataque do tipo contra outro."""
        return tabela_eff[self.numero][outro.numero]


def le_tipos(nome_arquivo):
    """Lê tipos do arquivo, guarda-os e constrói a tabela de efetividade."""
    # Permite que o script leia o arquivo mesmo
    # se executado de fora do diretório de onde ele está.
    diretorio = os.path.join(os.getcwd(), os.path.dirname(__file__))
    caminho = (os.path.join(diretorio, nome_arquivo))

    with open(caminho) as arquivo:
        n = int(arquivo.readline())

        # Leitura dos nomes e categoria
        for i in range(n):
            nome, especial = arquivo.readline().split()
            tipos.append(Tipo(i, nome, bool(int(especial))))

        # Adiciona o tipo Blank ao final da lista
        tipos.append(Tipo(n, "Blank", False))

        # Leitura da tabela de tipos
        for i in range(n):
            linha = arquivo.readline().split()
            linha = list(map(float, linha))
            tabela_eff.append(linha)

    return n


def get_tipo(i):
    """Devolve o tipo de número 'i'."""
    return tipos[i]
