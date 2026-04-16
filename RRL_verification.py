import networkx as nx
from Minimum_Resolving import build_resolving_set

def o_aleph_label(vij, zeta):
    labels = {}

    for node, (i, j) in vij.items():

        if j == 1:
            if 1 <= i <= 2**(zeta - 2):
                V = i
            else:
                V = 2**(zeta - 1) + i
        
        elif 2 <= j <= zeta - 1:
            V = i + 2 * 2**(zeta - 1) + abs(j - 2) * 2**(zeta - 1)
        
        elif j == zeta:
            if i % 2 == 1:  
                k = (i + 1) // 2
                V = 2**(zeta - 2) + k
            else: 
                k = i // 2
                V = 2**(zeta - 1) + k

        else:
            V = None

        labels[node] = V

    return labels

def fo_aleph_label(vij, r):
    zeta = r
    labels = {}

    for node, (i, j) in vij.items():

        if j == 1:
            if 1 <= i <= 2**(zeta - 1):
                if i % 2 == 1:
                    V = (i + 1) // 2
                else:
                    V = 3 * (2**(zeta - 2)) + (i + 1) // 2

        elif 2 <= j <= zeta - 1:
            V = i + 3 * 2**(zeta - 1) + abs(j - 2) * (2**(zeta - 1))

        elif j == zeta:
            if 1 <= i <= 2**(zeta - 2):
                V = 2**(zeta - 2) + i
            else:
                V = 3 * (2**(zeta - 2)) + i

        elif zeta + 1 <= j <= 2 * zeta - 2:
            V = i + 1*2**(zeta - 1) + abs(j - 1) * (2**(zeta - 1))

        elif j == 2 * zeta - 1:
            if 1 <= i <= 2**(zeta - 1):
                if i % 2 == 1:
                    V = 2**(zeta - 1) + (i + 1) // 2
                else:
                    V = 5 * (2**(zeta - 2)) + (i + 1) // 2
            else:
                V = None
        else:
            V = None

        labels[node] = V

    return labels

def verify_radio_resolving(G, psi, resolving_set, non_resolving_set):
    H = G.to_undirected()
    diam = nx.diameter(H)
    violations = []

    for rnode in resolving_set:
        for snode in non_resolving_set:
            try:
                dsr = nx.shortest_path_length(H, snode, rnode)
            except nx.NetworkXNoPath:
                dsr = float('inf')

            psir = psi[rnode]
            psis = psi[snode]

            if dsr + abs(psis - psir) < 1 + diam:
                violations.append((snode, rnode, dsr, abs(psis - psir)))

    return violations

if __name__ == "__main__":

    S = input("\nOmega or Flip-Omega? (O/FO): ").upper()
    zeta = int(input("\nEnter zeta: "))

    X, G, pos, vij = build_resolving_set(zeta, S)

    if S == "O":
        psi = o_aleph_label(vij, zeta)
        net = f"Omega network O({zeta})"
    else:
        psi = fo_aleph_label(vij, zeta)
        net = f"Flip-Omega network FO({zeta})"
        
    X = sorted(X, key=lambda x: (vij[x][1], vij[x][0]))

    print(f"\n{net}")
    print("\nX = {", end="")
    print(", ".join(f"v({vij[node][0]},{vij[node][1]})" for node in X), end="")
    print("}")

    print("\nCardinality of the set X:", len(X))

    non_X = [v for v in G.nodes() if v not in X]

    print("\nℵ = {", end="")
    print(", ".join(
        f"v({vij[node][0]},{vij[node][1]}): {int(psi[node])}"
        for node in X
    ), end="")
    print("}")

    resolving_labels = {int(psi[node]) for node in X}
    all_labels = {int(psi[node]) for node in G.nodes()}
    non_resolving_labels = all_labels - resolving_labels

    resolving_nodes = []
    non_resolving_nodes = []

    for node in G.nodes():
        if int(psi[node]) in resolving_labels:
            resolving_nodes.append(node)
        else:
            non_resolving_nodes.append(node)

    label_to_node = {int(psi[v]): v for v in G.nodes()}

    resolving_set = [label_to_node[l] for l in resolving_labels if l in label_to_node]
    non_resolving_set = [label_to_node[l] for l in non_resolving_labels if l in label_to_node]

    violations = verify_radio_resolving(G, psi, resolving_set, non_resolving_set)
    diam = nx.diameter(G)

    print("\nVertex cardinality:", G.number_of_nodes())
    print(f"\nMaximum ℵ labeling assigned: {max(int(psi[v]) for v in G.nodes())}")

    if violations:
        print(f"\nGraph diameter = {diam}")
        print(f"Violations found ({len(violations)}):")

        for a, c, dsr, diff in violations[:50]:
            psis = psi[a]
            psir = psi[c]

            print(
                f"a=v({vij[a][0]},{vij[a][1]}) (ℵ ={int(psis)}), "
                f"c=v({vij[c][0]},{vij[c][1]}) (ℵ={int(psir)}), "
                f"d={dsr}, |Δℵ|={int(diff)}, d+|Δℵ|={dsr + diff}"
            )
    else:
        print(f"\nℵ labeling satisfies radio-resolving condition (diam={diam})")