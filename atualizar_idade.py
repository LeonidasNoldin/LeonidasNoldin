"""
Script de atualização automática de idade - Perfil GitHub de Leônidas Noldin

Este script calcula a idade atual com base na data de nascimento (referência: 18/02)
e atualiza o número entre os marcadores <!--AGE_START--> e <!--AGE_END--> no README.md.

Como funciona:
- A "data de nascimento de referência" é 18/02/2009, pois o Leônidas tinha 17 anos
  em 18/02/2026 (17 = 2026 - 2009).
- O script roda todo dia (ver workflow do GitHub Actions), mas só efetivamente
  troca o número no dia em que o aniversário (18/02) já passou ou é hoje.
"""

import re
import sys
from datetime import date

# Ano em que ele fez 17 anos no dia 18/02 -> ano de nascimento de referência
ANO_REFERENCIA = 2026
IDADE_REFERENCIA = 17
ANO_NASCIMENTO = ANO_REFERENCIA - IDADE_REFERENCIA  # 2009

DIA_ANIVERSARIO = 18
MES_ANIVERSARIO = 2

README_PATH = "README.md"


def calcular_idade(hoje: date) -> int:
    """Calcula a idade atual com base na data de hoje."""
    idade = hoje.year - ANO_NASCIMENTO
    # Se ainda não chegou o dia 18/02 deste ano, ainda não fez aniversário
    if (hoje.month, hoje.day) < (MES_ANIVERSARIO, DIA_ANIVERSARIO):
        idade -= 1
    return idade


def atualizar_readme(idade: int) -> bool:
    """Atualiza o número da idade no README.md. Retorna True se houve alteração."""
    with open(README_PATH, "r", encoding="utf-8") as f:
        conteudo = f.read()

    padrao = r"(<!--AGE_START-->)\d+(<!--AGE_END-->)"
    novo_conteudo, n_substituicoes = re.subn(
        padrao, rf"\g<1>{idade}\g<2>", conteudo
    )

    if n_substituicoes == 0:
        print("Aviso: marcadores <!--AGE_START-->/<!--AGE_END--> não encontrados no README.md")
        return False

    if novo_conteudo == conteudo:
        print(f"Idade já está atualizada ({idade} anos). Nada para fazer.")
        return False

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(novo_conteudo)

    print(f"Idade atualizada para {idade} anos.")
    return True


def main():
    hoje = date.today()
    idade = calcular_idade(hoje)
    mudou = atualizar_readme(idade)

    # Usado pelo workflow do GitHub Actions para decidir se faz commit ou não
    if "--ci" in sys.argv:
        with open("idade_mudou.txt", "w") as f:
            f.write("true" if mudou else "false")


if __name__ == "__main__":
    main()
