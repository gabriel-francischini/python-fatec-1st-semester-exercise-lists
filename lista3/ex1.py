n = int(input("Digite um número: "))

i = 0
tng = False
while (i * (i + 1) * (i + 2)) <= n:
    if (i * (i + 1) * (i + 2)) == n:
        print("É triangular")
        tng = True
    i = i + 1

if tng == False:
    print("NÃO é triangular")
