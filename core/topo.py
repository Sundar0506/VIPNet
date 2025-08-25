import networkx as nx

def build_topology(devices):
    G = nx.Graph()

    # Step 1: Add devices as nodes
    for dev in devices:
        device_type = "switch" if dev["vlans"] else "router"
        G.add_node(dev["hostname"], device_type=device_type)

    # Step 2: Compare devices to find connections
    for i, dev1 in enumerate(devices):
        for dev2 in devices[i+1:]:
            for if1 in dev1["interfaces"]:
                for if2 in dev2["interfaces"]:

                    # --- Case 1: L3 subnet match ---
                    if if1["network"] and if2["network"]:
                        if if1["network"] == if2["network"]:
                            G.add_edge(
                                dev1["hostname"], dev2["hostname"],
                                type="L3",
                                subnet=if1["network"],
                                mtu=(if1["mtu"], if2["mtu"]),
                                bandwidth=(if1["bandwidth"], if2["bandwidth"])
                            )

                    # --- Case 2: VLAN overlap (Switch ↔ Switch) ---
                    if if1["vlans"] and if2["vlans"]:
                        common_vlans = set(if1["vlans"]) & set(if2["vlans"])
                        if common_vlans:
                            G.add_edge(
                                dev1["hostname"], dev2["hostname"],
                                type="L2",
                                vlans=list(common_vlans)
                            )

                    # --- Case 3: Router ↔ Switch trunk ---
                    if if1["mode"] == "trunk" and not if2["mode"]:
                        G.add_edge(
                            dev1["hostname"], dev2["hostname"],
                            type="L2",
                            vlans=[v["id"] for v in dev1["vlans"]] if dev1["vlans"] else []
                        )
                    if if2["mode"] == "trunk" and not if1["mode"]:
                        G.add_edge(
                            dev1["hostname"], dev2["hostname"],
                            type="L2",
                            vlans=[v["id"] for v in dev2["vlans"]] if dev2["vlans"] else []
                        )

    return G
