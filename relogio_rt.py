import os
import time

try: #define msvcrt como None em outros sistemas operativos
   import msvcrt
except ImportError:
   msvcrt = None

from relogio import Relogio, HoraInvalida, MinutoInvalido, SegundoInvalido


class MenuRelogio:
    """Controla um relogio em tempo real logico com opcoes interativas."""

    def __init__(self):
        agora = time.localtime()
        self.relogio = Relogio(agora.tm_hour, agora.tm_min, agora.tm_sec)
        self.mostrar_12h = False
        self._ultimo_update = time.monotonic()
        self._alarme_ja_notificado = False

    def atualizar_tempo(self):
        """Avanca o relogio conforme o tempo real decorrido."""
        agora = time.monotonic()
        segundos_decorridos = int(agora - self._ultimo_update)

        if segundos_decorridos <= 0:
            return

        for _ in range(segundos_decorridos):
            self.relogio.tick()

        self._ultimo_update += segundos_decorridos

    def texto_hora(self):
        """Retorna a hora no formato ativo (24h ou 12h)."""
        if self.mostrar_12h:
            return self.relogio.formato_12h()
        return str(self.relogio)

    def limpar_tela(self):
        """Limpa a tela para manter o menu mais organizado."""
        os.system("cls" if os.name == "nt" else "clear")

    def cabecalho(self):
        """Exibe o estado atual do relogio no topo do painel continuo."""
        self.atualizar_tempo()
        self.limpar_tela()

        formato = "12h" if self.mostrar_12h else "24h"
        alarme = (
            f"{self.relogio.alarme[0]:02d}:{self.relogio.alarme[1]:02d}:{self.relogio.alarme[2]:02d}"
            if self.relogio.alarme is not None
            else "nao definido"
        )

        print("=" * 52)
        print("RELOGIO INTERATIVO")
        print("=" * 52)
        print(f"Hora atual: {self.texto_hora()}  |  Formato: {formato}")
        print(f"Fuso horario: UTC{self.relogio.fuso_horario:+d}")
        print(f"Alarme: {alarme}")

        tocando = self.relogio.verificar_alarme()
        if tocando and not self._alarme_ja_notificado:
            print("\n>>> DESPERTADOR: hora do alarme! <<<")
            self._alarme_ja_notificado = True
        if not tocando:
            self._alarme_ja_notificado = False

        print("\nComandos:")
        print("[F] Alternar formato 24h/12h")
        print("[Z] Alterar fuso horario")
        print("[D] Definir despertador")
        print("[R] Remover despertador")
        print("[C] Cronometro: converter segundos em horario")
        print("[A] Cronometro: ajustar relogio por segundos")
        print("[Q] Sair")
        print("(Painel em tempo real continuo)")
        print("-" * 52)

    def ler_int(self, texto):
        """Le um inteiro do terminal, repetindo ate valor valido."""
        while True:
            try:
                return int(input(texto).strip())
            except ValueError:
                print("Valor invalido. Introduz um numero inteiro.")

    def definir_despertador(self):
        """Configura um novo horario de alarme."""
        print("\nDefine o despertador (HH MM SS):")
        horas = self.ler_int("Horas: ")
        minutos = self.ler_int("Minutos: ")
        segundos = self.ler_int("Segundos: ")

        try:
            self.relogio.definir_alarme(horas, minutos, segundos)
            print("Despertador definido com sucesso.")
        except (HoraInvalida, MinutoInvalido, SegundoInvalido) as erro:
            print(erro)

    def cronometro_converter(self):
        """Mostra o horario equivalente para um total de segundos."""
        total = self.ler_int("\nTotal de segundos: ")

        try:
            convertido = Relogio.tot_segundos(total, fuso_horario=self.relogio.fuso_horario)
            print(f"Resultado: {convertido} ({convertido.formato_12h()})")
        except TypeError as erro:
            print(erro)

    def cronometro_aplicar(self):
        """Ajusta o relogio atual com base em segundos totais."""
        total = self.ler_int("\nTotal de segundos para ajustar o relogio: ")

        try:
            novo = Relogio.tot_segundos(total, fuso_horario=self.relogio.fuso_horario)
            self.relogio.horas = novo.horas
            self.relogio.minutos = novo.minutos
            self.relogio.segundos = novo.segundos
            print(f"Relogio ajustado para {self.texto_hora()}.")
        except TypeError as erro:
            print(erro)

    def ler_comando_rapido(self, timeout=1.0):
        """Le uma tecla sem bloquear o painel por muito tempo (Windows)."""
        if msvcrt is None:
            comando = input("\nComando (F/Z/D/R/C/A/Q): ").strip().upper()
            return comando[:1] if comando else ""

        fim = time.monotonic() + timeout
        while time.monotonic() < fim:
            if msvcrt.kbhit():
                tecla = msvcrt.getwch().upper()
                if tecla in {"\r", "\n"}:
                    return ""
                return tecla
            time.sleep(0.05)
        return ""

    def executar(self):
        """Loop principal continuo em tempo real."""
        while True:
            self.cabecalho()
            comando = self.ler_comando_rapido(timeout=1.0)

            if comando == "F":
                self.mostrar_12h = not self.mostrar_12h
            elif comando == "Z":
                novo_fuso = self.ler_int("\nNovo fuso horario (ex.: -3, 0, +1): ")
                self.relogio.fuso_horario = novo_fuso
            elif comando == "D":
                self.definir_despertador()
            elif comando == "R":
                self.relogio.alarme = None
            elif comando == "C":
                self.cronometro_converter()
            elif comando == "A":
                self.cronometro_aplicar()
            elif comando == "Q":
                print("\nA terminar. Ate breve.")
                break


if __name__ == "__main__":
    MenuRelogio().executar()
