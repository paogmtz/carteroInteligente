from itertools import permutations


mapa = [
    [0,  0,  0,  0,  0,  0,  0,  0,  7,  6,  0],
    [15, 14, 13, 12,  0,  9,  0,  8,  0,  0,  1],
    [0,  0,  0,  0,  0, 10,  0,  0,  0,  3,  0],
    [0, 16,  0,  0, 11,  0,  0,  0,  0,  2,  0],
    [0, 17,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [0, 18,  0,  0, 19,  0,  4,  0,  5,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  20,  0, 0,  0]
]


zonas = [
    {12, 13, 14, 15},
    {2, 3, 4, 5, 20},
    {1, 6, 7, 8},
    {9, 10, 11, 19},
    {16, 17, 18}
]


# Guardar las posiciones de cada nodo
posiciones = {}

for fila in range(len(mapa)):
    for columna in range(len(mapa[fila])):

        nodo = mapa[fila][columna]

        if nodo != 0:
            posiciones[nodo] = (fila, columna)


# Distancia entre dos nodos
def distancia(a, b):

    f1, c1 = posiciones[a]
    f2, c2 = posiciones[b]

    return abs(f1 - f2) + abs(c1 - c2)


# Buscar la zona de un nodo
def obtener_zona(nodo):

    for zona in zonas:

        if nodo in zona:
            return zona


def costo_recorrido(inicio, orden):
    """Suma las distancias desde inicio hasta el último nodo del orden."""
    recorrido = (inicio,) + tuple(orden)
    return sum(distancia(a, b) for a, b in zip(recorrido, recorrido[1:]))


def elegir_orden_zona(actual, visitados):
    """Compara los órdenes locales y añade el costo de salir a otra zona."""
    zona = obtener_zona(actual)
    pendientes = zona - visitados
    fuera = set(posiciones) - visitados - zona

    def puntuacion(orden):
        costo_local = costo_recorrido(actual, orden)
        costo_salida = min(
            (distancia(orden[-1], nodo) for nodo in fuera),
            default=0,
        )
        # En empates preferimos menor costo local y después orden numérico.
        return costo_local + costo_salida, costo_local, orden

    # Como las zonas tienen como máximo cinco nodos, son pocos órdenes.
    return min(permutations(sorted(pendientes)), key=puntuacion)


def construir_ruta(inicio=10):
    actual = inicio
    visitados = {inicio}
    ruta = [inicio]
    costo = 0

    while len(visitados) < len(posiciones):
        pendientes_zona = obtener_zona(actual) - visitados

        if pendientes_zona:
            # Elegimos todo el orden una sola vez, manteniendo la salida.
            orden = elegir_orden_zona(actual, visitados)
        else:
            pendientes = set(posiciones) - visitados
            siguiente = min(
                pendientes,
                key=lambda nodo: (distancia(actual, nodo), nodo),
            )
            orden = (siguiente,)

        for siguiente in orden:
            costo += distancia(actual, siguiente)
            actual = siguiente
            visitados.add(actual)
            ruta.append(actual)

    return ruta, costo


if __name__ == "__main__":
    ruta, costo = construir_ruta()
    print("Ruta:")
    print(" -> ".join(map(str, ruta)))
    print("\nDistancia total:", costo)
