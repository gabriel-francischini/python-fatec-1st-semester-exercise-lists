# 10. Dada uma seqüência de letras terminada pelo caracter Z. Imprima a
# quantidade de vogais lidas.

quantidade_vogais = 0
letra = input("Insira uma letra: ")

while letra != "z":
    for vogal in "aeiou":
        if letra == vogal:
            quantidade_vogais = quantidade_vogais + 1

    letra = input("Insira uma letra: ")

print(quantidade_vogais)
