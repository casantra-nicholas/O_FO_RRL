import networkx as nx

def omega_network(r):
    G = nx.Graph()
    pos = {}

    N = 2**(r-1)

    for l in range(1, r+1):
        for i in range(1, N+1):
            node = (i, l)
            G.add_node(node)

            x = l - r
            y = i
            pos[node] = (y, x)

    for l in range(1, r):
        for i in range(1, N+1):

            j1 = 2*i - 1
            j2 = 2*i
    
            j1 = ((j1 - 1) % N) + 1
            j2 = ((j2 - 1) % N) + 1
    
            G.add_edge((i, l), (j1, l+1))
            G.add_edge((i, l), (j2, l+1))

    labels = {(i, l): (i, l) for (i, l) in G.nodes()}

    return G, pos, labels

def flip_omega(r):

    G = nx.Graph()
    pos = {}

    N = 2**(r-1)
    total_levels = 2*r - 1

    for l in range(1, total_levels + 1):
        for i in range(1, N+1):
            node = (i, l)
            G.add_node(node)

            x = total_levels - l
            y = i
            pos[node] = (y, x)

    for l in range(1, r):
        for i in range(1, N+1):

            k = (i + 1) // 2

            j1 = k
            j2 = k + N//2

            G.add_edge((i, l), (j1, l+1))
            G.add_edge((i, l), (j2, l+1))

    for l in range(r, total_levels):
        for i in range(1, N+1):
    
            j1 = 2*i - 1
            j2 = 2*i
    
            j1 = ((j1 - 1) % N) + 1
            j2 = ((j2 - 1) % N) + 1
    
            G.add_edge((i, l), (j1, l+1))
            G.add_edge((i, l), (j2, l+1))

    labels = {}
    for (i, l) in G.nodes():
        j = total_levels - l + 1
        labels[(i, l)] = (i, j)

    return G, pos, labels