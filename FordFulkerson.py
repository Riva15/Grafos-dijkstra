import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Definir los nodos y las capacidades del grafo
nodos = ['S', 'A', 'B', 'C', 'D', 'T']
capacidad = {
    ('S', 'A'): 10,
    ('S', 'C'): 8,
    ('A', 'B'): 5,
    ('C', 'D'): 9,
    ('D', 'B'): 6,
    ('B', 'T'): 8,  # Cambié la arista B->T directamente aquí
    ('D', 'B'): 6
}

# Crear la matriz de capacidades
capacidad_matriz = np.zeros((len(nodos), len(nodos)))

for (i, j), cap in capacidad.items():
    capacidad_matriz[nodos.index(i), nodos.index(j)] = cap

# Función DFS para encontrar el camino aumentante
def dfs(capacidad_matriz, fuente, sumidero, flujo):
    visited = [False] * len(capacidad_matriz)
    parent = [-1] * len(capacidad_matriz)
    
    def dfs_rec(current_node, flow):
        if current_node == sumidero:
            return flow
        visited[current_node] = True
        for next_node in range(len(capacidad_matriz)):
            if not visited[next_node] and capacidad_matriz[current_node][next_node] > 0:
                parent[next_node] = current_node
                new_flow = min(flow, capacidad_matriz[current_node][next_node])
                res = dfs_rec(next_node, new_flow)
                if res > 0:
                    # Actualizar las capacidades de las aristas
                    capacidad_matriz[current_node][next_node] -= res
                    capacidad_matriz[next_node][current_node] += res
                    return res
        return 0
    
    return dfs_rec(fuente, float('Inf'))

# Función principal de Ford-Fulkerson con visualización paso a paso
def ford_fulkerson(capacidad_matriz, fuente, sumidero):
    flujo_maximo = 0
    paso = 1  # Para mostrar el proceso paso a paso
    
    while True:
        flujo_aumentante = dfs(capacidad_matriz, fuente, sumidero, float('Inf'))
        if flujo_aumentante == 0:
            break
        flujo_maximo += flujo_aumentante
        
        # Mostrar el proceso con actualización
        print(f"Paso {paso}: Flujo aumentado = {flujo_aumentante}")
        print("Capacidades actuales del grafo:")
        mostrar_grafo(capacidad_matriz)
        
        paso += 1
    
    return flujo_maximo

# Función para visualizar el grafo con capacidades
def mostrar_grafo(capacidad_matriz):
    print(capacidad_matriz)
    G = nx.DiGraph()
    
    # Añadir nodos y aristas
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if capacidad_matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], capacity=capacidad_matriz[i][j])
    
    # Visualización
    pos = nx.spring_layout(G, seed=42)  # Para mantener el grafo ordenado
    plt.figure(figsize=(8, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold", arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Grafo de flujo con capacidades")
    plt.show()

# Calcular el flujo máximo
flujo_maximo = ford_fulkerson(capacidad_matriz, nodos.index('S'), nodos.index('T'))
print(f"El flujo máximo es: {flujo_maximo}")
