import networkx as nx
from collections import defaultdict
from O_FO import omega_network, flip_omega

def build_resolving_set(zeta, S):

    if S == "O":
        G, pos, labels = omega_network(zeta)
    elif S == "FO":
        G, pos, labels = flip_omega(zeta)
    else:
        raise ValueError("Network must be Omega or Flip-Omega")

    stages = {}
    for node, (i, j) in labels.items():
        stages.setdefault(j, []).append((i, node))

    for j in stages:
        stages[j].sort()
        stages[j] = [n for _, n in stages[j]]

    stage_keys = sorted(stages)
    first_stage = stage_keys[0]
    last_stage = stage_keys[-1]
    middle_stage = zeta

    nodes_first = stages[first_stage]
    nodes_middle = stages[middle_stage]
    nodes_last = stages[last_stage]

    half = 1 << (zeta - 2)
    full = 1 << (zeta - 1)

    R = []

    if S == "O":
        R.extend(nodes_first[:half])
        R.extend(nodes_last[0:full:2])

    else:
        R.extend(nodes_first[0:full:2])
        R.extend(nodes_middle[:half])
        R.extend(nodes_last[0:full:2])

    return list(dict.fromkeys(R)), G, pos, labels

def compute_dist(G, S_nodes):
    dists = [nx.single_source_shortest_path_length(G, s) for s in S_nodes]

    return {
        v: tuple(d.get(v, float('inf')) for d in dists)
        for v in G.nodes()
    }

def check_resolving_set(G, X, verbose=True):
    signatures = compute_dist(G, X)

    groups = defaultdict(list)
    for v, sig in signatures.items():
        groups[sig].append(v)

    unresolved = [grp for grp in groups.values() if len(grp) > 1]

    if not unresolved:
        if verbose:
            print("\nX is a valid resolving set")
            print("Cardinality of the set X:", len(X))
        return {"is_resolving": True}

    if verbose:
        print("\nX is not a valid resolving set")
        print()
        print("Unresolved group(s):", len(unresolved))
        for idx, grp in enumerate(unresolved, start=1):
            formatted = ", ".join(
                f"v({labels[v][0]},{labels[v][1]})"
                for v in grp
            )
            print(f" {idx}) {formatted}")

    return {"is_resolving": False}

def is_minimal_resolving_set(G, X):
    if not check_resolving_set(G, X, verbose=False)["is_resolving"]:
        return False

    for i in range(len(X)):
        X_minus = X[:i] + X[i+1:]

        if check_resolving_set(G, X_minus, verbose=False)["is_resolving"]:
            return False

    return True

if __name__ == "__main__":

    S = input("\nOmega or Flip-Omega Network? (O/FO): ").upper()
    zeta = int(input("\nEnter zeta: "))

    X, G, pos, labels = build_resolving_set(zeta, S)

    net = f"{'Omega' if S=='O' else 'Flip-Omega'} network {'O' if S=='O' else 'FO'}({zeta})"

    print("\nX = {", end="")
    print(", ".join(f"v({labels[n][0]},{labels[n][1]})" for n in X), end="")
    print("}")

    result = check_resolving_set(G, X, verbose=True)

    if result["is_resolving"]:
        if input("\nCheck minimality? (Y/N): ").upper() == 'Y':
            if is_minimal_resolving_set(G, X):
                print(f"\nX is a minimum resolving set for {net}")
            else:
                print(f"\nX is not a minimum resolving set for {net}")
                