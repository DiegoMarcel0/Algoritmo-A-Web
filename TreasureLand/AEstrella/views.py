import json
from math import sqrt
from django.shortcuts import render
from django.http import JsonResponse
import networkx as nx
import heapq
from .models import Grafo

def guardar_grafo(request):
    data = json.loads(request.body)
    g = Grafo.objects.create(
        nombre=data['nombre'],
        size=data['size'],
        inicio=data['start'],
        fin=data['end'],
        muros=data['walls'],
    )
    return JsonResponse({'status': 'ok', 'grafo_id': g.id})

def obtener_grafos(request):
    grafos = Grafo.objects.all().values('id', 'nombre')
    print(grafos)
    return JsonResponse(list(grafos), safe=False)

def cargar_grafo(request, grafo_id):
    try:
        grafo = Grafo.objects.get(id=grafo_id)
        return JsonResponse({
            'size': grafo.size,
            'start': grafo.inicio,
            'end': grafo.fin,
            'walls': grafo.muros
        })
    except Grafo.DoesNotExist:
        return JsonResponse({'error': 'Grafo no encontrado papu'}, status=404)

def grafo_json(request):
    G = nx.Graph()
    G.add_weighted_edges_from([
        ('A', 'B', 1),
        ('B', 'C', 2),
        ('A', 'C', 4),
        ('C', 'D', 1)
    ])

    nodes = [{'data': {'id': node}} for node in G.nodes]
    edges = [
        {'data': {'source': u, 'target': v, 'weight': d['weight']}}
        for u, v, d in G.edges(data=True)
    ]

    return JsonResponse({'nodes': nodes, 'edges': edges})

def grafo(request):
    return render(request, "AE/grafo.html") 

def grafo2(request):
    return render(request, "AE/grafo2.html") 

def ejecutar_astar(request):
    G = nx.Graph()
    G.add_weighted_edges_from([
        ('A', 'B', 2),
        ('B', 'C', 2),
        ('B', 'D', 3),
        ('A', 'C', 1),
        ('C', 'D', 1),
        ('C', 'E', 2),
        ('D', 'F', 10),
    ])
    
    # Ejecutar A*
    path = nx.astar_path(G, 'A', 'F')

    # Convertir el grafo a un formato compatible con Cytoscape.js
    nodes = [{'data': {'id': node}} for node in G.nodes]
    edges = [
        {'data': {'source': u, 'target': v, 'weight': d['weight']}}
        for u, v, d in G.edges(data=True)
    ]

    return JsonResponse({
        'nodes': nodes,
        'edges': edges,
        'path': path
    })

def grilla_con_obstaculos(request):
    return render(request, 'AE/grilla_astar.html', { 'size': 10 })

def resolver_astar(request):
    data = json.loads(request.body)

    size = data['size']
    start = tuple(data['start'])
    end = tuple(data['end'])
    walls = [tuple(w) for w in data['walls']]
    heuristica = data.get('heuristica', 'manhattan')

    G = nx.grid_2d_graph(size, size)
    for wall in walls:
        G.remove_node(wall)

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def euclidiana(a, b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

    def chebyshev(a, b):
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    def zero(a, b):
        return 0
    # Elegir heurística
    if heuristica == 'manhattan':
        h = manhattan
    elif heuristica == 'euclidiana':
        h = euclidiana
    elif heuristica == 'chebyshev':
        h = chebyshev
    elif heuristica == 'zero':
        h = zero
    else:
        h = manhattan  # Default
        print("watafa amigo, vos estas reloco")

    # A* con heurística seleccionada
    open_set = [(0 + h(start, end), 0, start)]
    came_from = {}
    g_score = {start: 0}
    visitados = []

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        visitados.append(current)
        if current == end:
            break

        for neighbor in G.neighbors(current):
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor, end)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    if path:
        path.append(start)
        path.reverse()

    return JsonResponse({
        'visitados': visitados,
        'camino': path
    })


