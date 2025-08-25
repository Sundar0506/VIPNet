import networkx as nx

def simulate_traffic(G, src, dst):
    try:
        path = nx.shortest_path(G, src, dst)
        return {"src": src, "dst": dst, "path": path}
    except nx.NetworkXNoPath:
        return {"src": src, "dst": dst, "path": None}

def vlan_reachability(G):
    vlan_map = {}
    for u, v, d in G.edges(data=True):
        if d["type"] == "L2":
            for vlan in d.get("vlans", []):
                vlan_map.setdefault(vlan, set()).update([u, v])
    return {vlan: list(nodes) for vlan, nodes in vlan_map.items()}

# NEW: Failure simulation
def simulate_failure(G, failed_link, src, dst):
    """
    Simulate link failure and check if traffic is still possible.
    failed_link: tuple ("R1", "R2")
    src, dst: nodes to test communication
    """
    G_copy = G.copy()
    
    if G_copy.has_edge(*failed_link):
        G_copy.remove_edge(*failed_link)
    else:
        return {"error": f"Link {failed_link} not found in topology"}
    
    try:
        path = nx.shortest_path(G_copy, src, dst)
        return {
            "failed_link": failed_link,
            "src": src,
            "dst": dst,
            "status": "Traffic still possible (rerouted)",
            "new_path": path
        }
    except nx.NetworkXNoPath:
        return {
            "failed_link": failed_link,
            "src": src,
            "dst": dst,
            "status": "Traffic FAILED (no alternate path)",
            "new_path": None
        }

def simulate_vlan_failure(G, vlan_id, removed_from):
    """
    Simulate VLAN failure by removing vlan_id from a specific link (u, v).
    vlan_id: VLAN number to remove (e.g., 10)
    removed_from: tuple ("R1", "SW1") = link where VLAN is pruned
    """
    G_copy = G.copy()

    if G_copy.has_edge(*removed_from):
        edge_data = G_copy[removed_from[0]][removed_from[1]]
        if edge_data.get("type") == "L2" and vlan_id in edge_data.get("vlans", []):
            # Remove VLAN from this link
            edge_data["vlans"].remove(vlan_id)
        else:
            return {"error": f"VLAN {vlan_id} not present on link {removed_from}"}
    else:
        return {"error": f"Link {removed_from} not found"}

    # Recompute reachability
    vlan_map = {}
    for u, v, d in G_copy.edges(data=True):
        if d["type"] == "L2":
            for vlan in d.get("vlans", []):
                vlan_map.setdefault(vlan, set()).update([u, v])

    return {
        "failed_vlan": vlan_id,
        "removed_from": removed_from,
        "new_vlan_reachability": {v: list(nodes) for v, nodes in vlan_map.items()}
    }

# -----------------------------
# NEW: Advanced Simulation functions
# -----------------------------
def bandwidth_utilization(G):
    """
    Returns bandwidth utilization info for each L3 link.
    Assumes 'bandwidth' field in edge data as tuple (actual, max) in Kbps.
    """
    report = {}
    for u, v, d in G.edges(data=True):
        if d["type"] == "L3" and "bandwidth" in d:
            actual, max_bw = d["bandwidth"]
            percent = round((actual/max_bw)*100, 2) if max_bw else 0
            report[(u, v)] = {"actual_kbps": actual, "max_kbps": max_bw, "util_percent": percent}
    return report

def route_convergence(G, protocol="OSPF"):
    """
    Simulate OSPF or BGP route convergence time (mock values for demonstration).
    Returns dictionary of nodes with convergence time in ms.
    """
    nodes = G.nodes()
    # Mock convergence times
    if protocol.upper() == "OSPF":
        conv_time = {n: 50 + i*5 for i, n in enumerate(nodes)}  # OSPF faster
    elif protocol.upper() == "BGP":
        conv_time = {n: 200 + i*20 for i, n in enumerate(nodes)}  # BGP slower
    else:
        conv_time = {n: None for n in nodes}
    return conv_time
