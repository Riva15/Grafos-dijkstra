import heapq  # Importación necesaria para las colas de prioridad
import networkx as nx
import matplotlib.pyplot as plt

# Definir el grafo como un diccionario de adyacencia
grafo = {
    'A': {'B': 4, 'D': 2},
    'B': {'C': 7, 'E': 5},
    'C': {'F': 3},
    'D': {'E': 1},
    'E': {'F': 2},
    'F': {}
}

def dijkstra(grafo, inicio, destino):
    # Inicializar distancias como infinito y la distancia al nodo de inicio como 0
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    previos = {nodo: None for nodo in grafo}  # Para reconstruir el camino

    # Cola de prioridad
    cola_prioridad = [(0, inicio)]

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if nodo_actual == destino:
            break

        # Verificar si la distancia actual es mayor que la almacenada (ya procesada)
        if distancia_actual > distancias[nodo_actual]:
            continue

        # Explorar vecinos
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso

            # Si encontramos un camino más corto, actualizamos la distancia y el nodo previo
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                previos[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (distancia, vecino))

    # Reconstruir el camino más corto
    camino = []
    nodo = destino
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = previos[nodo]

    return camino, distancias[destino]

def dibujar_grafo(grafo, camino_destacado, inicio, destino):
    # Crear un grafo con NetworkX
    G = nx.DiGraph()
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)

    pos = nx.spring_layout(G)  # Posiciones de los nodos

    # Dibujar nodos
    colores_nodos = ['green' if nodo == inicio else
                     'red' if nodo == destino else
                     'lightblue' for nodo in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colores_nodos, node_size=700, font_size=10, font_weight='bold')

    # Dibujar etiquetas de las aristas
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    # Dibujar el camino más corto en rojo
    edges = list(zip(camino_destacado, camino_destacado[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2)

    plt.show()

# Solicitar nodo inicial y final al usuario
inicio = input("Ingrese el nodo de inicio: ").strip().upper()
destino = input("Ingrese el nodo de destino: ").strip().upper()

# Calcular el camino más corto
camino, distancia = dijkstra(grafo, inicio, destino)

# Mostrar resultados y graficar
if camino:
    print(f"Camino más corto de {inicio} a {destino}: {' -> '.join(camino)} (Distancia: {distancia})")
    dibujar_grafo(grafo, camino, inicio, destino)
else:
    print(f"No hay un camino desde {inicio} hasta {destino}.")
