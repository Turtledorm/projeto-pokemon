"""Contém a classe Tipo e tabela de efetividades."""

import os

tipos = []       # Lista de tipos
tabela_eff = []  # Tabela com multiplicadores de efetividade


class Tipo:
    """Representa um tipo de Pokémon/ataque."""

    def __init__(self, numero, nome, especial):
        """Inicializa o tipo."""
        self._numero = numero
        self._nome = nome
        self._especial = especial

    def info(self):
        """Exibe informações do tipo."""
        print(str(self.numero) + ":", self.nome,
              "(Especial)" if self.especial else "")

    @property
    def numero(self):
        return self._numero

    @property
    def nome(self):
        return self._nome

    @property
    def especial(self):
        return self._especial

    def get_eff_contra(self, outro):
        """Devolve o valor da efetividade de um ataque do tipo contra outro."""
        return tabela_eff[self.numero][outro.numero]


def le_tipos(nome_arquivo):
    """Lê tipos do arquivo, guarda-os e constrói a tabela de efetividade."""
    # Encontra o arquivo mesmo estando fora do diretório de execução
    #   __file__: caminho relativo do programa sendo executado
    #   os.path.dirname(__file__): caminho relativo do diretório
    diretorio = os.path.dirname(__file__)
    caminho = os.path.join(diretorio, nome_arquivo)

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

    global num_tipos
    num_tipos = n


def get_num_tipos():
    return num_tipos


def get_tipo(i):
    """Devolve o tipo de número 'i'."""
    return tipos[i]


def get_tipo_id(nome):
    """Devolve o índice na lista do tipo de respectivo nome."""
    for i in range(get_num_tipos()):
        if tipos[i].nome == nome:
            return i


# Lê de arquivo tipos e tabela de efetividade
le_tipos("tipos.txt")
