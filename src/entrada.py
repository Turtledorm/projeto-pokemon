"""Função para ler Pokémons."""

from pokemon import Pokemon


def le_pokemon(cpu, dados=None):
    """Lê dados da entrada padrão e devolve um objeto Pokémon.
       Alternativamente, recebe uma lista de dados (strings) já pronta."""
    if dados is None:
        dados = []

        # Leitura dos atributos do Pokémon
        for i in range(9):
            dados.append(input())

        # Leitura dos atributos de ataque
        num_ataques = int(input())
        for i in range(5 * num_ataques):
            dados.append(input())

    return Pokemon(dados, cpu)
