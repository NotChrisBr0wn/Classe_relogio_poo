# relogio.py
class HoraInvalida(Exception):
    """Exceção levantada para horas inválidas."""
    def __init__(self, hora):
        if not isinstance(hora, int):
           mensagem = f"Hora inválida: {hora}. A hora deve ser um número inteiro."
        else:
           mensagem = f"Hora inválida: {hora}. A hora deve estar entre 0 e 23."
        super().__init__(mensagem)


class MinutoInvalido(Exception):
    """Exceção levantada para minutos inválidos."""

    # def __init__(self, minuto):
    #    super().__init__("Mensagem de erro")
    raise NotImplementedError("To-do")


class SegundoInvalido(Exception):
    """Exceção levantada para segundos inválidos."""

    # def __init__(self, segundo):
    #    super().__init__("Mensagem de erro")
    raise NotImplementedError("To-do")


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

    def __str__(self):
        """Retorna a hora no formato HH:MM:SS"""
        raise NotImplementedError("To-do")

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
        raise NotImplementedError("To-do")

    def tick(self):
        """Avança o relógio em um segundo."""
        raise NotImplementedError("To-do")
