import sys

from itertools import cycle, chain, product, repeat
from functools import reduce
from random import shuffle, choice, random

from introducir import (
    solicitar_introducir_numero_extremo,
    solicitar_introducir_si_o_no,
    solicitar_introducir_letra,
    solicitar_introducir_palabra,
    solicitar_introducir_casilla,
)


LONGITUDES_BARCOS = [2, 3, 3, 4, 4, 5]
ORDINAL = 0x2680

CASO_NO_JUGADO = chr(0x2610)
CASO_TOCADO = chr(0x2611)
CASO_AGUA = chr(0x2612)

HORIZONTAL = 0
VERTICAL = 1

ORIENTACIONES = (VERTICAL, HORIZONTAL)


class Conventions:
    """Clase que contiene los atributos y los métodos estáticos"""

    tablero_num_lineas = 10
    tablero_num_columnas = 10

    barcos_longitud = [2, 3, 3, 4, 4, 5]

    @staticmethod
    def generar_num_linea(x):
        return chr(65 + x)

    @staticmethod
    def generar_num_columna(y):
        return str(y)

    @staticmethod
    def generar_nombre_casilla(x, y):
        return Conventions.generar_num_linea(x) +\
               Conventions.generar_num_columna(y)


class Case:
    instances = {}
    jugadas = set()

    def __init__(self, x, y):
        # Adición de las coordenadas
        self.x = x
        self.y = y
        # Queremos poder acceder a una casilla a partir de sus coordenadas
        Case.instances[x, y] = self

        # Generación del nombre de la casilla
        self._generar_nombre()
        # Queremos poder acceder a una casilla a partir de su nombre
        Case.instances[self.nombre] = self

        # Evolución de la casilla
        self.jugada = False
        self.barco = None  # No toca a un barco de momento.

    def _generar_nombre(self):
        """Este método puede ser sobrecargado fácilmente"""
        self.nombre = Conventions.generar_nombre_casilla(self.x, self.y)

    def jugar(self):
        """Describe qué pasa cuando jugamos una casilla"""
        self.jugada = True
        self.jugadas.add(self)

        if self.barco is not None:
            if len(casilla.barco.casillas - self.casillas_jugadas) == 0:
                print("Hundido !!")
            else:
                print("Tocado !")
        else:
            print("Agua !")

    @classmethod
    def generar_casillas(cls):
        for x, y in product(range(Conventions.tablero_num_lineas),
                            range(Conventions.tablero_num_columnas)):
            Case(x, y)

    def __str__(self):
        """Sobrecarga del método de transformación en cadena"""
        if not self.jugada:
            return CASO_NO_JUGADO
        elif self.barco is None:
            return CASO_AGUA
        return CASO_TOCADO


class Barco:
    instances = []
    casillas_ocupadas = set()

    def __init__(self, longitud):
        self.longitud = longitud
        self.orientacion = choice(ORIENTACIONES)
        self.tocado = False
        self.hundido = False

        # performance / legibilidad:
        num_lineas = Conventions.tablero_num_lineas
        num_columnas = Conventions.tablero_num_columnas
        num2l = Conventions.generar_num_linea
        num2c = Conventions.generar_num_columna

        while True:
            if self.orientacion == HORIZONTAL:
                rang = choice(range(num_lineas))
                primero = choice(range(num_columnas + 1 - longitud))
                letra = num2l(rang)
                cifras = [num2c(x) for x in range(primero, primero + longitud)]
                self.casillas = {Case.instances[l + c]
                              for l, c in product(repeat(letra, longitud), cifras)}
            else:
                rang = choice(range(num_columnas))
                primero = choice(range(num_lineas + 1 - longitud))
                cifra = num2c(rang)
                letras = [num2l(x) for x in range(primero, primero + longitud)]
                # Crear el barco
                self.casillas = {Case.instances[l + c]
                              for l, c in product(letras, repeat(cifra, longitud))}

            for existente in Barco.instances:
                if self.casillas.intersection(existente.casillas):
                    break  # break relativo al "for existente in barcos:"
            else:
                # Agregar el barco en el contenedor de barcos
                Barco.instances.append(self)
                # Informar la casilla que contiene un barco.
                for casilla in self.casillas:
                    casilla.barco = self
                # Agregar estas casillas a las casillas ocupadas :
                Barco.casillas_ocupadas |= self.casillas
                break  # break relativo al "while True:"

    @classmethod
    def generar_barcos(cls):
        for longitud in Conventions.barcos_longitud:
            Barco(longitud)


class Tablero:

    def __init__(self):
        # Creamos las casillas:
        Case.generar_casillas()

        # Creamos los barcos:
        Barco.generar_barcos()

        # performance / legibilidad:
        num_lineas = Conventions.tablero_num_lineas
        num_columnas = Conventions.tablero_num_columnas
        num2l = Conventions.generar_num_linea
        num2c = Conventions.generar_num_columna

        # Creamos la herramienta para poder seguir la situación
        self.casillas_jugadas = set()

        # Generamos aquí los etiquetas para facilitar la visualización
        self.etiqueta_lineas = [num2l(x) for x in range(num_lineas)]
        self.etiqueta_columnas = [num2c(x) for x in range(num_columnas)]

    trazo_horizontal = " --" + "+---" * 10 + "+"

    def ver(self):
        print("   |", " | ".join(self.etiqueta_columnas), "|")

        iter_etiqueta_lineas = iter(self.etiqueta_lineas)

        for x, y in product(range(Conventions.tablero_num_lineas),
                            range(Conventions.tablero_num_columnas)):

            # Trazo horizontal para cada nueva línea
            if y == 0:
                print(self.trazo_horizontal)
                print(" {}".format(next(iter_etiqueta_lineas)), end="")

            casilla = Case.instances[x, y]
            print(" |", casilla, end="")

            # Ver la barra vertical derecha de la tabla:
            if y == 9:
                print(" |")
        # Ver la última línea horizontal
        print(self.trazo_horizontal + "\n\n")


    def probar_fin_juego(self):
        """Permite probar si el juego ha terminado o no"""
        if len(Barco.casillas_ocupadas - self.casillas_jugadas) == 0:
            print("Bravo. El juego ha terminado !")
            return True

        return False


    def jugar_tirada(self):
        """Permite gestionar el dato introducido de una tirada"""
        while True:
            nombre_casilla = solicitar_introducir_casilla(
                "Seleccionar una casilla (letra + cifra)")
            # Encontrar la casilla a partir de su nombre
            casilla = Case.instances[nombre_casilla]
            # Probar si la casilla ya ha sido jugada
            if casilla.jugada:
                print("Esta casilla ya ha sido jugada, elija otra",
                    file=sys.stderr)
            else:
                casilla.jugar()
                break

def jugar_una_partida():
    """Algoritmo de una partida"""
    # Creamos un tablero de juego vacío

    tablero = Tablero()

    while True:
        tablero.ver()

        tablero.jugar_tirada()

        if tablero.probar_fin_juego():
            # Si el juego ha terminado, salimos de la función
            tablero.ver()
            return


def elegir_jugarOtra():
    return solicitar_introducir_si_o_no(
        "¿Desea volver a jugar? ? [s/n]")


def jugar():
    while True:
        jugar_una_partida()

        if not elegir_jugarOtra():
            return