i = int(input("Digite o I: "))
j = int(input("Digite o J: "))
n = int(input("Digite o N: "))

k = 0
while n > 0:
    k = k + 1
    if ((k % i) == 0) or ((k % j) == 0):
        print(k)
        n = n - 1
