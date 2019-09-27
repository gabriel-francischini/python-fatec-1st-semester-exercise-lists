n = int(input("Digite um número: "))

is_adj = False
while n > 0:
    if (n % 10) == ((n % 100) // 10):
        is_adj = True
    n = n // 10

if is_adj:
    print("Tem algarismos adjacentes")
else:
    print("NÃO tem algarismos adjacentes")
