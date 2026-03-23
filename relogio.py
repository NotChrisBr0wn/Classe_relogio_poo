# relogio.py
class HoraInvalida(Exception):
    """Exceção levantada para horas inválidas."""
    def __init__(self, hora):
        if not isinstance(hora, int):
              mensagem = f"Hora inválida: {hora!r}. A hora deve ser um número inteiro."
        else:
           mensagem = f"Hora inválida: {hora!r}. A hora deve estar entre 0 e 23."
        super().__init__(mensagem)


class MinutoInvalido(Exception):
    """Exceção levantada para minutos inválidos."""

    def __init__(self, minuto):
        if not isinstance(minuto, int):
            mensagem = f"Minuto inválido: {minuto!r}. O minuto deve ser um número inteiro."
        else:
            mensagem = f"Minuto inválido: {minuto!r}. O minuto deve estar entre 0 e 59."
        super().__init__(mensagem)


class SegundoInvalido(Exception):
    """Exceção levantada para segundos inválidos."""
    def __init__(self, segundo):
        if not isinstance(segundo, int):
            mensagem = f"Segundo inválido: {segundo!r}. O segundo deve ser um número inteiro."
        else:
            mensagem = f"Segundo inválido: {segundo!r}. O segundo deve estar entre 0 e 59."
        super().__init__(mensagem)


class Relogio:
    """
    Classe que implementa o armazenamento e manipulação de horários.

    Se for instanciada com valores inválidos, levanta uma exceção específica.
    """

    def __init__(self, horas, minutos, segundos):
        Relogio.validar_hora(horas, minutos, segundos)
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos
        self.alarme = None

    def __str__(self):
        """Retorna a hora no formato HH:MM:SS"""
        return f"{self.horas:02d}:{self.minutos:02d}:{self.segundos:02d}"

    @staticmethod
    def validar_hora(horas, minutos, segundos):
        """
        Valida se o horário é possível. Levanta exceções específicas para casos inválidos.

        :param horas: int - Horas do horário.
        :param minutos: int - Minutos do horário.
        :param segundos: int - Segundos do horário.

        :raises HoraInvalida: Se a hora é inválida (não inteiro ou fora de 0-23).
        :raises MinutoInvalido: Se o minuto é inválido (não inteiro ou fora de 0-59).
        :raises SegundoInvalido: Se o segundo é inválido (não inteiro ou fora de 0-59).
        """
        if not isinstance(horas, int) or not 0 <= horas <= 23:
            raise HoraInvalida(horas)

        if not isinstance(minutos, int) or not 0 <= minutos <= 59:
            raise MinutoInvalido(minutos)

        if not isinstance(segundos, int) or not 0 <= segundos <= 59:
            raise SegundoInvalido(segundos)

    def tick(self):
        """Avança o relógio em um segundo."""
        self.segundos += 1
        if self.segundos == 60:
            self.segundos = 0
            self.minutos += 1
            if self.minutos == 60:
                self.minutos = 0
                self.horas += 1
                if self.horas == 24:
                    self.horas = 0

    def converter_segundos(self):
        """Converte o horário atual para quantidade total de segundos."""
        return self.horas * 3600 + self.minutos * 60 + self.segundos

    def soma(self, outro_relogio):
        """Soma dois horários com retorno no intervalo de 24 horas."""
        if not isinstance(outro_relogio, Relogio):
            raise TypeError("outro_relogio deve ser uma instância de Relogio")

        total = (self.converter_segundos() + outro_relogio.converter_segundos()) % (24 * 3600)
        horas = total // 3600
        minutos = (total % 3600) // 60
        segundos = total % 60
        return Relogio(horas, minutos, segundos)

    def diferenca(self, outro_relogio):
        """Subtrai dois horários com retorno no intervalo de 24 horas."""
        if not isinstance(outro_relogio, Relogio):
            raise TypeError("outro_relogio deve ser uma instância de Relogio")

        total = (self.converter_segundos() - outro_relogio.converter_segundos()) % (24 * 3600)
        horas = total // 3600
        minutos = (total % 3600) // 60
        segundos = total % 60
        return Relogio(horas, minutos, segundos)

    def formato_12h(self):
        """Retorna a hora no formato 12h (AM/PM)."""
        periodo = "AM" if self.horas < 12 else "PM"
        hora_12 = self.horas % 12
        if hora_12 == 0:
            hora_12 = 12

        return f"{hora_12:02d}:{self.minutos:02d}:{self.segundos:02d} {periodo}"

    def definir_alarme(self, horas, minutos, segundos):
        """Define o horário do alarme no formato HH:MM:SS."""
        Relogio.validar_hora(horas, minutos, segundos)
        self.alarme = (horas, minutos, segundos)

    def verificar_alarme(self):
        """Retorna True quando a hora atual coincide com o alarme definido."""
        if self.alarme is None:
            return False

        return (self.horas, self.minutos, self.segundos) == self.alarme

