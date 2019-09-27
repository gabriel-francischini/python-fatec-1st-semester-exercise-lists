n = int(input("Digite o N: "))
x = int(input("Digite o X: "))

cos = 1
fat = 1
for i in range(2, n + 1, 2):
    fat = fat * i * (i - 1)
    cos = cos + ((-1) ** (i / 2)) * (x ** i) / (fat)

print(cos)
