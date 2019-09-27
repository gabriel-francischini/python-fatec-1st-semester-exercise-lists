dec = int(input("Digite um número: "))

bin = ''
i = 0
while dec > 0:
    bin = str(dec % 2) + bin
    dec = dec // 2
    i = i + 1

print(bin)
