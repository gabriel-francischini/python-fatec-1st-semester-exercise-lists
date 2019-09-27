bin = int(input("Digite um número em binário: "))

sum = 0
i = 0
while bin > 0:
    sum = sum + (bin % 10) * (2 ** i)
    bin = bin // 10
    i = i + 1

print(sum)
