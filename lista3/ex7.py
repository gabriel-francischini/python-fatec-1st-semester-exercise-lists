i = int(input("Digite um número: "))
k = int(input("Digite um número: "))
j = int(input("Digite um número: "))

if (((i ** 2 + k ** 2) == (j ** 2))
    or ((k ** 2 + j ** 2) == (i ** 2))
    or ((i ** 2 + k ** 2) == (j ** 2))):
    print("Formam os lados de um triângulo retângulo.")
else:
    print("NÃO formam os lados de um triângulo retângulo.")
