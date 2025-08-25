import networkx as nx

def analyze_performance(G):
    report = {}

    # 1. Connectivity check
    report["connected"] = nx.is_connected(G)

    # 2. Bottleneck detection
    bottlenecks = []
    for u, v, d in G.edges(data=True):
        if d["type"] == "L3":
            mtu = d.get("mtu", (1500, 1500))
            bw = d.get("bandwidth", (1000000, 1000000))

            if min(mtu) < 1500:
                bottlenecks.append((u, v, "MTU mismatch"))
            if min(bw) < 1000000:
                bottlenecks.append((u, v, "Low bandwidth"))

    report["bottlenecks"] = bottlenecks

    # 3. Redundancy / fault-tolerance
    redundancy = {}
    for u in G.nodes:
        for v in G.nodes:
            if u != v:
                try:
                    paths = list(nx.all_simple_paths(G, u, v))
                    if len(paths) > 1:
                        redundancy[(u, v)] = f"{len(paths)} paths available (redundant)"
                    else:
                        redundancy[(u, v)] = "Only 1 path (no redundancy)"
                except nx.NetworkXNoPath:
                    redundancy[(u, v)] = "No path"
    report["redundancy"] = redundancy

    return report
