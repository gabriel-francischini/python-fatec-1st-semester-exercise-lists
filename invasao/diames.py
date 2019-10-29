import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')
import datetime
import calendar


ano_vigente = now = datetime.datetime.now().year

class DiaMes():
    def __init__(self, dia, mes):
        self._dia = dia
        self._mes = mes
        self._date = self._corrigir_dia_e_mes()

    def _corrigir_dia_e_mes(self):
        if self._mes == 0:
            mes = 12
        else:
            mes = self._mes

        if self._dia == 0:
            dia = 31
        else:
            dia = self._dia

        # see: https://stackoverflow.com/questions/42950
        first_mday, last_mday = calendar.monthrange(ano_vigente, mes)

        # Dia do próximo mês
        if dia > last_mday:
            dia -= last_mday
            mes += 1

        date = datetime.date(ano_vigente, mes, dia)

        self._mes = date.month
        self._dia = date.day
        return date

    def __repr__(self):
        # Acts like a tuple
        return str((self._dia, self._mes))

    def __str__(self):
        return self._date.strftime("%d de %B")
