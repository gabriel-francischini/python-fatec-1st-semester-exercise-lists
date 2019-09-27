sum = 0
len = -1
inp = 0

while inp != 99.99:
    sum = sum + inp
    len = len + 1

    inp = float(input("Digite um número: "))

print(sum/len)
