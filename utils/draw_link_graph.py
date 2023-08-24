import networkx as nx
import matplotlib.pyplot as plt
import math

def draw_dag_from_matrix_with_dynamic_ranges(A, N, S):
    G = nx.DiGraph()
    num_nodes = len(A)
    G.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if A[i][j] == 1:
                G.add_edge(i, j)
    
    # Determine the ranges based on start times in S
    min_start_time = min(S)
    max_start_time = max(S)
    range_count = math.ceil((max_start_time - min_start_time + 1) / 50)
    ranges = [(min_start_time + i * 50, min_start_time + (i + 1) * 50) for i in range(range_count)]
    
    # Group nodes based on start times and ranges
    groups = {r: [] for r in ranges}
    for node, start_time in enumerate(S):
        for r in ranges:
            if r[0] <= start_time < r[1]:
                groups[r].append(node)
    
    # Assign layers based on groups
    layers = []
    for r in ranges:
        layers.append(groups[r])
    
    pos = nx.shell_layout(G, nlist=layers)
    node_colors = '#66c2a5'
    edge_colors = '#8da0cb'
    arrow_color = '#1f78b4'
    text_color = '#333333'
    node_sizes = 1200
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)
    
    for group, nodes in groups.items():
        for node in nodes:
            nx.draw_networkx_labels(G, {node: pos[node] + [0, 0.05]}, labels={node: N[node]}, font_size=8, font_color=text_color)
            plt.text(pos[node][0], pos[node][1], f"{node}", horizontalalignment='center', verticalalignment='center', fontsize=12, color=text_color)
    
    for edge in G.edges:
        if A[edge[0]][edge[1]] == 1:
            nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=edge_colors, width=2.0, alpha=0.7, arrows=False)
            arrow_pos = ((pos[edge[0]][0] + pos[edge[1]][0]) / 2, (pos[edge[0]][1] + pos[edge[1]][1]) / 2)
            plt.annotate("",
                         xy=pos[edge[1]], xycoords='data',
                         xytext=arrow_pos, textcoords='data',
                         arrowprops=dict(arrowstyle="->", color=arrow_color, linewidth=2))
    
    plt.title("Directed Acyclic Graph (DAG)", fontsize=16, color=text_color)
    plt.gca().xaxis.set_visible(False)
    plt.gca().yaxis.set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.grid(False)
    plt.tight_layout()
    plt.show()
