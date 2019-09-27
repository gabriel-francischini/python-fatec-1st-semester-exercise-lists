n = int(input("Digite o N: "))

is_primo = True
for i in range(2, n):
    if ((n % i) == 0) and (is_primo == True):
        is_primo = False
        print("NÃO é primo")

if is_primo == True:
    print("É primo")
