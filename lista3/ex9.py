n = int(input("Digite um número: "))

is_crescente = True

while n > 0:
    if ((n % 10) < ((n % 100) // 10)) and (is_crescente == True):
        is_crescente = False
        print("NÃO é estritamente crescente")
    n = n // 10

if is_crescente == True:
    print("É estritamente crescente")
