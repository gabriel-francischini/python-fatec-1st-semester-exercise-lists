# Enunciado:
#   7. Dados um número inteiro N (N >= 10) verificar se este tem dois algarismos
#   adjacentes iguais.
#
#
# Variáveis:
#
#            digit
#              ⭡
#              │
#              │
#   number = 123456789
#             │ └──┬─┘
#             │    │
#             │    └────⭢ next_digits
#             ⭣
#         last_digit
#
#  number: Variável do tipo int, contendo o valor N do enunciado (digitado
#    pelo usuário).
#  digit: Algarismo sendo considerado em questão, para ver se é o mesmo número
#    do algarismo anterior. Tipo int.
#  last_digit: Algarismo que vimos na posição decimal anterior.
#  next_digits: Variável contendo os próximos algarismos que iremos processar
#    no futuro. Tipo int.
#  are_digits_next: Representa se encontramos algarismos adjacentes até o
#    momento. Tipo boolean.
#
#
# Dica:
#   Se você pegar um número inteiro qualquer, ABCDE, e dividir inteiramente esse
#   número por 10, o resultado da divisão será ABCD e o resto da divisão será E.
#   Essa propriedade é válida para qualquer número representado em base decimal.
#   A mesma coisa acontece se você dividir um número binário por 2 ou um número
#   hexadecimal por 16.
#   O resto de uma divisão em python é representado pelo operador "%", que vem
#   da matemática (veja https://pt.wikipedia.org/wiki/Aritm%C3%A9tica_modular).
#
#                 │  ┌──────┐
#   ABCDE │ 10    │  │   1234 │ 10
#         └─────  │  │        └─────
#  -ABCD0   ABCD  │  │   1←─────123
#   ─────         │  │   12←────┘│
#       E         │  │   10       │
#                 │  │   ────     │
#                 │  │    2       │
#                 │  │    23←────┘
#                 │  │   -20
#                 │  │   ────
#                 │  │     3
#                 │  │     34
#                 │  │    -30
#                 │  │    ────
#                 │  └────→4
#                 │
#
#
# Pseudo-código
#   1. Receba um número "number" digitado pelo usuário.
#   2. O número anterior que usaremos no proxímo passo, "last_digit", começa com
#     um valor qualquer (nesse caso foi escolhida a string vazia, "", para
#     ser esse valor inicial qualquer).
#   3. Como não vimos nenhum número ainda, parta do pressuposto que esse número
#     não tem algarismos adjacentes. Caso estejamos errados, podemos corrigir
#     esse "chute" depois. Use a variável "are_digits_next" marcar que, por
#     enquanto, achamos que os algarismos não são adjacentes.
#   3. Veja cada um dos algarismos presente nesse número, usando o seguinte
#     algoritmo:
#     3.1 O número atual é "next_digits".
#     3.2 O algarismo que estamos considerando é o algarismo mais à direita do
#         número "next_digits" (algarismo das unidades). Esse algarismo, "digit",
#         é o resultado da divisão do número "next_digits" por 10.
#     3.3 Preste atenção se o algarismo que você viu na passagem anterior é
#         igual ao algarismo que você esta vendo agora. Se ambos forem iguais,
#         use a variável "are_digits_next" para se lembrar de mostrar para o
#         usuário que existem algarismos adjacentes nesse número.
#     3.4 Da próxima vez que executarmos o passo 3, o valor de "last_digit" (que
#         representa o último algarismo que vimos, tem que ser o valor "digit"
#         do algarismo que estamos vendo agora).
#   4. Caso, durante o passo 3, tivermos descoberto que o número tem algarismos
#     adjacentes, mostre isso para o usuário. Caso tivermos descoberto que não
#     tem algarismos adjacentes, mostre isso também.
#

number = int(input("Coloque o número N: "))

# Ambas essas variáveis serão usadas no while a seguir
next_digits = number
last_digit = ""
are_digits_next = False

# Veja cada um dos algarismos presente nesse número
while next_digits != 0:
    # O algarismo que estamos considerando é o algarismo mais à direita do
    # número "" (algarismo das unidades). Esse algarismo, "digit", é o
    # resultado da divisão do número "next_digits" por 10.
    digit = next_digits % 10

    # Caso esse algarismo e anterior sejam iguais, mostre para o usuário que
    # eles são iguais.
    if digit == last_digit:
        are_digits_next = True

    last_digit = digit
    next_digits = next_digits // 10

if are_digits_next:
    print("Tem algarismos adjacentes")
else:
    print("Não tem algarismos adjacentes")
