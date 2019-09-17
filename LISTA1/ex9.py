#  9. Dada uma seqüência de letras terminadas pelo caracter Z. Imprima a
# quantidade de caracteres digitados.


quantidade = 0
letra = input("Digite uma letra: ")

while letra != "z":
    quantidade = quantidade + 1
    letra = input("Digite uma letra: ")

print(quantidade)
