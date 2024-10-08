import sys
from cubo import *
from problemaRubik import *
from busqueda import *
from heurisitca import *
cubo = Cubo()

print("CUBO SIN MEZCLAR:\n" + cubo.visualizar())

movs=int(sys.argv[1])

movsMezcla = cubo.mezclar(movs)

print("MOVIMIENTOS ALEATORIOS:",movs)
for m in movsMezcla:
    print(cubo.visualizarMovimiento(m) + " ")
print()

print("CUBO INICIAL (MEZCLADO):\n" + cubo.visualizar())





#Descomentar una vez se implemente la búsqueda en anchura
#Creación de un problema
problema = Problema(EstadoRubik(cubo), BusquedaVoraz(heuristica_manhattan))


print("SOLUCION:")
opsSolucion = problema.obtenerSolucion()

if opsSolucion != None:
    for o in opsSolucion:
        print(cubo.visualizarMovimiento(o.getEtiqueta()) + " ")
        cubo.mover(o.movimiento)
    print()
    print("CUBO FINAL:\n" + cubo.visualizar())
else:
    print("no se ha encontrado solución")


