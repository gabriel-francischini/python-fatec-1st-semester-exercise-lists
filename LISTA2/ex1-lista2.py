matrícula = 0

while matrícula != 999:

        matrícula = int(input('digite seu número de matrícula: '))
        if matrícula == 999:
                break
        nota1 = float(input('digite a nota 1: '))
        nota2 = float(input('digite a nota 2: '))
        nota3 = float(input('digite a nota 3: '))
        media = (2 * nota1 + 3 * nota2 + 4 *nota3) / 9
        if media >= 7.0:
                print('APROVADO ALUNO',matrícula,':sua média é ',media)
        else:
                print('REPROVADO ALUNO:',matrícula,'sua média é ',media)	
