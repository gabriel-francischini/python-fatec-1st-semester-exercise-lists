n = int(input("Digite o N: "))

pi = 4 / 1
for i in range(1, int((n + 1) / 2)):
    pi = pi + (-1 * (-1) ** (i + 1)) * (4 / ((2 * i) + 1))

print(pi)
