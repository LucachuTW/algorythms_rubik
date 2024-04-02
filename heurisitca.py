from cubo import *
from nodos import *
from busqueda import *
from problemaRubik import *
from problema import *
# Función de heurística de Manhattan
# Definición de la función de heurística de Manhattan
"""def heuristica_manhattan(estado_rubik):
    cubo = estado_rubik.cubo
    distancia_total = 0
    # Itera sobre cada cara del cubo
    for cara in cubo.caras:
        # Itera sobre cada casilla de la cara
        for casilla in cara.casillas:
            # Obtén las posiciones actual y correcta de la casilla
            pos_actual = casilla.posicionActual()
            pos_correcta = casilla.posicionCorrecta
            # Calcula la distancia de Manhattan para la casilla actual y su posición correcta
            distancia_total += abs(pos_correcta[0] - pos_actual[0]) + abs(pos_correcta[1] - pos_actual[1])
    return distancia_total

# Llamar al método buscarSolucion con el estado inicial del cubo
# solucion = busqueda_voraz.buscarSolucion(estado_inicial)


# Uso de la búsqueda voraz con la heurística de Manhattan
#busqueda_voraz = BusquedaVoraz(heuristica_manhattan)"""

def heuristica_manhattan(estado_rubik):
    cubo = estado_rubik.cubo
    distancia_total = 0
    # Itera sobre cada cara del cubo
    for cara in cubo.caras:
        # Itera sobre cada casilla de la cara
        for casilla in cara:
            # Obtén las posiciones actual y correcta de la casilla
            pos_actual = casilla.posicionActual()
            pos_correcta = casilla.posicionCorrecta
            # Calcula la distancia de Manhattan para la casilla actual y su posición correcta
            distancia_total += abs(pos_correcta - pos_actual)
    return distancia_total
