num1 = float(input("Digite um número: "))
num2 = float(input("Digite um número: "))

if num1 > num2:
    m = num1
    n = num2
else:
    n = num1
    m = num2

if n == m:
    print("São iguais")
else:
    print("Maior: " + str(m) + "   Menor: " + str(n))
