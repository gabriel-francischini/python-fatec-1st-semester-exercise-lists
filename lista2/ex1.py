m = 0
while m != "999":
    m = input("MATRICULA: ")
    if m != "999":
        n1 = int(input("NOTA1: "))
        n2 = int(input("NOTA2: "))
        n3 = int(input("NOTA3: "))
        mf = (2 * n1 + 3 * n2 + 4 * n3) / 9
        if mf >= 7.0:
            print("APROVADO MATRICULA: "+str(m)+" MEDIAL FINAL: "+str(mf))
        else:
            print("REPROVADO MATRICULA: "+str(m)+" MEDIAL FINAL: "+str(mf))
