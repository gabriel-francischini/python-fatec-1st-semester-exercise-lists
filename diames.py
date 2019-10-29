# numero_de_dias_por_mes = {
#     'Dezembro': 31,
#     'Janeiro': 31,
#     'Fevereiro': 28,
#     'Março': 31,
#     'Abril': 30,
#     'Maio': 31,
#     'Junho': 30,
#     'Julho': 31,
#     'Agosto': 31,
#     'Setembro': 30,
#     'Outubro': 31,
#     'Novembro': 30,
# }

mes_de_cada_numero = {
    '0': "Dezembro",
    '1': "Janeiro",
    '2': "Fevereiro",
    '3': "Março",
    '4': "Abril",
    '5': "Maio",
    '6': "Junho",
    '7': "Julho",
    '8': "Agosto",
    '9': "Setembro",
    '10': "Outubro",
    '11': "Novembro",
}



class DiaMes():
    def __init__(self, dia, mes):
        self._dia = dia
        self._mes = mes
        self.corrigir_dia_e_mes()

    def corrigir_dia_e_mes(self):


    def __repr__(self):
        # Acts like a tuple
        return str((self._dia, self._mes))

    def __str__(self):
        return str(self._dia) + " de " + mes_de_cada_numero[self._mes]
