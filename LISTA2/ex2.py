dividendo = int(input("dividendo="))
divisor = int(input("divisor="))

count = 0
vezes_somadas = 0

while count <= dividendo:
    count = count + divisor

    if count <= dividendo:
        vezes_somadas = vezes_somadas + 1

print(vezes_somadas)
