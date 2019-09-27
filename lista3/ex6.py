n = int(input("Digite o N: "))
mseq = 0
lalg = "qualquer coisa"

while n > 0:
    alg = int(input("Digite um número: "))
    if alg == lalg:
        seq = seq + 1
    else:
        seq = 1
    if seq > mseq:
        mseq = seq
    n = n - 1
    lalg = alg

print(mseq)
