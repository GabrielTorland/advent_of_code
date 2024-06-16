from collections import defaultdict, Counter
import re
import random
import copy
import matplotlib.pyplot as plt
import networkx as nx

def parse_input(input_path):
    graph = defaultdict(list)
    for line in open(input_path).readlines():
        node, neighbors = re.search(r'(\w+): (\w+(?: \w+)*)', line).groups()
        graph[node] = neighbors.split(' ') 
    new_graph = defaultdict(list)
    for graph_node, neighbors in graph.items():
        for neighbor in neighbors:
            new_graph[graph_node].append(neighbor)
            new_graph[neighbor].append(graph_node)
    return new_graph

def get_all_vertices(graph):
    vertices = set()
    for node, neighbors in graph.items():
        vertices.add(node)
        vertices.update(neighbors)
    return vertices

def integrity_check(graph):
    for node, neighbors in graph.items():
        for neighbor, freq in Counter(neighbors).items():
            if graph[neighbor].count(node) != freq:
                return False
    return True

def karger_min_cut(graph):
    def contract(graph_tmp, u, v):
        for node in graph_tmp[v]:
            if node != u:
                graph_tmp[u].append(node)
                graph_tmp[node].append(u)
                graph_tmp[node].remove(v)
        while v in graph_tmp[u]:
            graph_tmp[u].remove(v)
        del graph_tmp[v] 

    for _ in range(len(graph) ** 2):
        temp_graph = copy.deepcopy(graph)
        clusters = defaultdict(list)
        for node in temp_graph.keys():
            clusters[node] = [node]
        while len(temp_graph) > 2:
            u = random.choice(list(temp_graph.keys()))
            v = random.choice(temp_graph[u])
            contract(temp_graph, u, v)
            clusters[u] += clusters[v]
            del clusters[v]
        clusters = list(clusters.values())
        c1 = clusters[0]
        c2 = clusters[1]
        cut_size = len(next(iter(temp_graph.values())))
        if cut_size <= 3:
            print(f'Cut size: {cut_size}')
            print("Part 1: ", len(c1)*len(c2))
            plot_graph(graph, clusters)
            break

def plot_graph(graph, clusters=None):
    G = nx.Graph()
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    if clusters:
        # Generate a color for each cluster
        colors = ['#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in clusters]
        
        # Create a mapping from node to color
        node_colors = []
        for node in G.nodes():
            for cluster_idx, cluster in enumerate(clusters):
                if node in cluster:
                    node_colors.append(colors[cluster_idx])
                    break
            else:
                node_colors.append('#000000')  # Default color if node is not in any cluster
    else:
        node_colors = '#1f78b4'  # Default color

    nx.draw(G, with_labels=True, node_color=node_colors, node_size=500, font_size=10, font_color='white')
    plt.show()

def main():
    graph = parse_input('input.txt')
    if not integrity_check(graph):
        print('Graph integrity check failed')
    karger_min_cut(graph)
    
    

if __name__ == '__main__':
    main()