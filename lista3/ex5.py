sum = 0
for i in range(1, 10 + 1):
    sum = sum + ((-1) ** (i + 1)) * 1 / i
    print("Termo #" + str(i), ": ", ((-1) ** (i + 1)) * 1 / i)

print("Soma dos termos: " + str(sum))
