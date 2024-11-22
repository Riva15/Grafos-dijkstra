import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from tkinter import messagebox, Tk, Label, Entry, Button
import mplcursors

# Definir el grafo como una lista de aristas (origen, destino, peso)
aristas = [
    ('A', 'B', 2),
    ('A', 'D', 1),
    ('B', 'C', 6),
    ('B', 'E', 4),
    ('C', 'F', -3),
    ('D', 'E', 5),
    ('E', 'F', 2)
]

def bellman_ford(aristas, inicio):
    # Inicializar distancias y predecesores
    nodos = set(sum(([u, v] for u, v, _ in aristas), []))
    distancias = {nodo: float('inf') for nodo in nodos}
    distancias[inicio] = 0
    predecesores = {nodo: None for nodo in nodos}

    # Relajación de aristas (|V| - 1) veces
    for _ in range(len(nodos) - 1):
        for u, v, peso in aristas:
            if distancias[u] + peso < distancias[v]:
                distancias[v] = distancias[u] + peso
                predecesores[v] = u

    # Comprobar ciclos negativos
    for u, v, peso in aristas:
        if distancias[u] + peso < distancias[v]:
            return None, None, True  # Hay un ciclo negativo

    return distancias, predecesores, False

def reconstruir_camino(predecesores, inicio, destino):
    camino = []
    nodo = destino
    while nodo is not None:
        camino.insert(0, nodo)
        nodo = predecesores[nodo]
    if camino[0] != inicio:
        return []  # No hay camino
    return camino

def dibujar_grafo(aristas, camino_destacado, inicio, destino):
    # Crear un grafo con NetworkX
    G = nx.DiGraph()
    for u, v, peso in aristas:
        G.add_edge(u, v, weight=peso)

    # Usar el layout spring_layout para una disposición más flexible
    pos = nx.spring_layout(G, seed=42)  # 'seed' es para reproducir el mismo layout

    # Dibujar nodos
    colores_nodos = ['green' if nodo == inicio else
                     'red' if nodo == destino else
                     'lightblue' for nodo in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=colores_nodos, node_size=700, font_size=10, font_weight='bold')

    # Dibujar etiquetas de las aristas
    etiquetas = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

    # Dibujar el camino más corto en rojo
    if camino_destacado:
        edges = list(zip(camino_destacado, camino_destacado[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='red', width=2)

    # Agregar interactividad para mostrar detalles de los nodos
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

    plt.show()

def consulta_interactiva():
    def ejecutar():
        inicio = entrada_inicio.get().upper()
        destino = entrada_destino.get().upper()

        if inicio not in {u for u, _, _ in aristas} or destino not in {v for _, v, _ in aristas}:
            messagebox.showerror("Error", "Nodo de inicio o destino no válido.")
            return

        # Calcular distancias mínimas y predecesores
        distancias, predecesores, ciclo_negativo = bellman_ford(aristas, inicio)

        if ciclo_negativo:
            messagebox.showerror("Ciclo Negativo", "El grafo contiene un ciclo negativo.")
            return

        # Reconstruir el camino más corto
        camino = reconstruir_camino(predecesores, inicio, destino)

        if not camino:
            messagebox.showinfo("Sin Camino", f"No hay camino desde {inicio} hasta {destino}.")
        else:
            messagebox.showinfo("Camino Más Corto", f"Camino más corto de {inicio} a {destino}: {' -> '.join(camino)}")

        # Dibujar el grafo con el camino resaltado
        dibujar_grafo(aristas, camino, inicio, destino)

    # Crear la ventana de consulta
    ventana = Tk()
    ventana.title("Consulta Interactiva: Bellman-Ford")

    Label(ventana, text="Nodo de inicio:").grid(row=0, column=0, padx=10, pady=10)
    entrada_inicio = Entry(ventana)
    entrada_inicio.grid(row=0, column=1, padx=10, pady=10)

    Label(ventana, text="Nodo de destino:").grid(row=1, column=0, padx=10, pady=10)
    entrada_destino = Entry(ventana)
    entrada_destino.grid(row=1, column=1, padx=10, pady=10)

    boton = Button(ventana, text="Calcular", command=ejecutar)
    boton.grid(row=2, column=0, columnspan=2, pady=10)

    ventana.mainloop()

# Ejecutar la consulta interactiva
consulta_interactiva()
