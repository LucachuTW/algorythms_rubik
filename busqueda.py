from abc import abstractmethod, ABCMeta

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
    def __init__(self):
        self.heuristica = heuristica_cuborubik

    def buscarSolucion(self, inicial):
        nodoActual = None
        actual, hijo = None, None
        solucion = False
        abiertos = []
        abiertos.append(NodoVoraz(inicial, None, None, self.heuristica(inicial)))
        while not solucion and len(abiertos) > 0:
            nodoActual = min(abiertos, key=lambda x: x.heuristica)
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

    def heuristica_cuborubik(self, estado):
        return self.contar_caras_mal_colocadas(estado.cubo)

    def contar_caras_mal_colocadas(self, cubo):
        caras_mal_colocadas = 0
        for i in range(len(cubo.estado)):
            for j in range(len(cubo.estado[0])):
                color_actual = cubo.estado[i][j]
                cara_actual = cubo.estado[i]
                color_norte = cubo.estado[vecinoNorte[cara_actual]][i]
                color_este = cubo.estado[vecinoEste[cara_actual]][i]
                color_sur = cubo.estado[vecinoSur[cara_actual]][i]
                color_oeste = cubo.estado[vecinoOeste[cara_actual]][i]
                if color_actual != color_norte:
                    caras_mal_colocadas += 1
                if color_actual != color_este:
                    caras_mal_colocadas += 1
                if color_actual != color_sur:
                    caras_mal_colocadas += 1
                if color_actual != color_oeste:
                    caras_mal_colocadas += 1
        return caras_mal_colocadas
