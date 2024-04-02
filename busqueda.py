from abc import abstractmethod, ABCMeta
from nodos import *
from cubo import *
# Interfaz genérico para algoritmos de búsqueda
class Busqueda(metaclass=ABCMeta):
    @abstractmethod
    def buscarSolucion(self, inicial):
        pass

# Implementa una búsqueda en Anchura genérica (independiente de Estados y Operadores) controlando repetición de estados.
# Usa lista ABIERTOS (lista) y lista CERRADOS (diccionario usando Estado como clave)
class BusquedaAnchura(Busqueda):
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoAnchura(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop(0)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                cerrados[actual.cubo.visualizar()] = nodoActual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys():
                        abiertos.append(NodoAnchura(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaProfundidad(Busqueda):
    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        cerrados = dict()
        abiertos.append(NodoProfundidad(inicial, None, None))
        cerrados[inicial.cubo.visualizar()] = inicial
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                cerrados[actual.cubo.visualizar()] = nodoActual
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in cerrados.keys() and hijo.cubo.visualizar() not in abiertos:
                        abiertos.append(NodoProfundidad(hijo, nodoActual, operador))
                        cerrados[hijo.cubo.visualizar()] = hijo
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaProfundidadAcotada(Busqueda):
    def buscarSolucion(self, inicial, cota):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        abiertos.append(NodoProfundidadAcotada(inicial, None, None, 0))
        while not solucion and len(abiertos) > 0:
            nodoActual = abiertos.pop()
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            elif nodoActual.profundidad < cota:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in abiertos:
                        abiertos.append(NodoProfundidadAcotada(hijo, nodoActual, operador, nodoActual.profundidad + 1))
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class BusquedaProfundidadIterativa(Busqueda):
    def buscarSolucion(self, inicial):
        profundidad_maxima = 26
        for profundidad_actual in range(profundidad_maxima + 1):
            solucion = BusquedaProfundidadAcotada().buscarSolucion(inicial, profundidad_actual)
            if solucion is not None:
                return solucion
        return None

class BusquedaVoraz(Busqueda):
    def __init__(self, heuristica):
        self.heuristica = heuristica

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica(inicial)))

        while not solucion and len(abiertos) > 0:
            nodoActual = min(abiertos, key=lambda x: self.heuristica(x.estado))

            abiertos.remove(nodoActual)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    if hijo.cubo.visualizar() not in abiertos:
                        abiertos.append(NodoVoraz(hijo, nodoActual, operador, self.heuristica(hijo)))
        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:  # Asciende hasta la raíz
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None


class AEstrella(Busqueda):
    def __init__(self, heuristica):
        self.heuristica = heuristica

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        abiertos.append(NodoAEstrella(inicial, None, None, 0, self.heuristica(inicial)))
        CERRADOS = []

        while not solucion and abiertos:
            nodoActual = min(abiertos, key=lambda x: x.f)

            abiertos.remove(nodoActual)
            CERRADOS.append(nodoActual)
            actual = nodoActual.estado
            if actual.esFinal():
                solucion = True
            else:
                for operador in actual.operadoresAplicables():
                    hijo = actual.aplicarOperador(operador)
                    g = nodoActual.g + operador.getCoste()
                    f = g + self.heuristica(hijo)
                    encontrado_abiertos = next((nodo for nodo in abiertos if nodo.estado.equals(hijo)), None)
                    encontrado_cerrados = next((nodo for nodo in CERRADOS if nodo.estado.equals(hijo)), None)

                    if encontrado_abiertos:
                        if encontrado_abiertos.g > g:
                            encontrado_abiertos.padre = nodoActual
                            encontrado_abiertos.operador = operador
                            encontrado_abiertos.g = g
                            encontrado_abiertos.f = f
                    elif not encontrado_cerrados:
                        abiertos.append(NodoAEstrella(hijo, nodoActual, operador, g, f))

            abiertos.sort(key=lambda x: x.f)

        if solucion:
            lista = []
            nodo = nodoActual
            while nodo.padre is not None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

class IDAEstrella(Busqueda):
    def __init__(self, heuristica):
        self.heuristica = heuristica

    def buscarSolucion(self, inicial):
        cota = self.heuristica(inicial)
        nueva_cota = float('inf')
        resuelto = False

        while not resuelto:
            cota = nueva_cota
            nueva_cota = float('inf')
            abiertos = [NodoIDAEstrella(inicial, None, None, 0, self.heuristica(inicial))]
            while abiertos and not resuelto:
                actual = abiertos[0]
                abiertos.pop(0)
                if actual.estado.esFinal():
                    resuelto = True
                else:
                    for operador in actual.estado.operadoresAplicables():
                        nuevo_estado = actual.estado.aplicarOperador(operador)
                        f = actual.g + operador.getCoste() + self.heuristica(nuevo_estado)
                        if f <= cota:
                            abiertos.insert(0, NodoIDAEstrella(nuevo_estado, actual, operador, actual.g + operador.getCoste(), f))
                        else:
                            nueva_cota = min(nueva_cota, f)

        if resuelto:
            lista = []
            nodo = actual
            while nodo.padre is not None:
                lista.insert(0, nodo.operador)
                nodo = nodo.padre
            return lista
        else:
            return None

