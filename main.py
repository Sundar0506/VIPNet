from core.parser import parse_router_config
from core.topo import build_topology
import networkx as nx
import matplotlib.pyplot as plt
import json
import os
from pprint import pprint
from tabulate import tabulate  # Ensure reports folder exists

# Step 5 imports
from core.validate import validate_configs
from core.perf import analyze_performance
from core.simulate import (
    simulate_traffic, vlan_reachability, simulate_failure, simulate_vlan_failure,
    bandwidth_utilization, route_convergence
)

# Export
from core.export import export_csv, export_excel

# PyVis
from pyvis.network import Network

if __name__ == "__main__":
    os.makedirs("reports", exist_ok=True)

    # Step 1: Parse all devices
    devices = []
    for fname in ["configs/R1.txt", "configs/R2.txt", "configs/SW1.txt"]:
        devices.append(parse_router_config(fname))

    # Step 2: Build topology
    G = build_topology(devices)

    # Step 3: Print summary
    print("Nodes:", G.nodes(data=True))
    print("Edges:", G.edges(data=True))

    # Step 4: Visualize with Matplotlib
    pos = nx.spring_layout(G, seed=42)
    routers = [n for n, attr in G.nodes(data=True) if attr["device_type"] == "router"]
    switches = [n for n, attr in G.nodes(data=True) if attr["device_type"] == "switch"]

    nx.draw_networkx_nodes(G, pos, nodelist=routers, node_color="skyblue", node_shape="s", node_size=2000, label="Router")
    nx.draw_networkx_nodes(G, pos, nodelist=switches, node_color="lightgreen", node_shape="o", node_size=2000, label="Switch")

    l2_edges = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "L2"]
    l3_edges = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == "L3"]

    nx.draw_networkx_edges(G, pos, edgelist=l2_edges, style="dashed", edge_color="green", width=2, label="L2")
    nx.draw_networkx_edges(G, pos, edgelist=l3_edges, style="solid", edge_color="blue", width=2, label="L3")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    edge_labels = {}
    for u, v, d in G.edges(data=True):
        if d["type"] == "L3":
            edge_labels[(u, v)] = d.get("subnet", "")
        elif d["type"] == "L2":
            edge_labels[(u, v)] = "VLANs: " + ",".join(map(str, d.get("vlans", [])))
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.legend(scatterpoints=1)
    plt.title("Network Topology", fontsize=14)
    plt.tight_layout()
    # Save figure instead of showing
    plt.savefig("reports/network_topology.png", dpi=150)
    print("--- Matplotlib network topology saved as reports/network_topology.png ---")

    # -----------------------------
    # PyVis Interactive HTML
    # -----------------------------
    net = Network(height="750px", width="100%", notebook=False)
    for n, attr in G.nodes(data=True):
        color = "skyblue" if attr["device_type"] == "router" else "lightgreen"
        shape = "box" if attr["device_type"] == "router" else "ellipse"
        net.add_node(n, label=n, color=color, shape=shape)

    for u, v, d in G.edges(data=True):
        title = ""
        if d["type"] == "L3":
            title = d.get("subnet", "")
        elif d["type"] == "L2":
            title = "VLANs: " + ",".join(map(str, d.get("vlans", [])))
        style = "dashed" if d["type"] == "L2" else "solid"
        net.add_edge(u, v, title=title, color="blue" if d["type"]=="L3" else "green", width=2, dashes=(style=="dashed"))

    html_path = os.path.join("reports", "network_topology.html")
    net.write_html(html_path, notebook=False)
    print(f"--- Interactive network topology saved as {html_path} ---")

    # -----------------------------
    # Validation & Performance
    # -----------------------------
    print("\n--- Validation Report ---")
    errors = validate_configs(devices)
    print(errors if errors else "No errors found")

    print("\n--- Performance Report ---")
    perf_report = analyze_performance(G)
    print(perf_report)

    # -----------------------------
    # Simulations
    # -----------------------------
    print("\n--- Simulation ---")
    print("Traffic R1 -> R2:", simulate_traffic(G, "R1", "R2"))
    print("VLAN Reachability:", vlan_reachability(G))

    print("\n--- Failure Simulation ---")
    result = simulate_failure(G, failed_link=("R1", "R2"), src="R1", dst="R2")
    print(result)

    print("\n--- VLAN Failure Simulation ---")
    vlan_result = simulate_vlan_failure(G, vlan_id=10, removed_from=("R1", "SW1"))
    print(vlan_result)

    # -----------------------------
    # Advanced Simulations
    # -----------------------------
    print("\n--- Advanced Simulations ---")
    # Bandwidth utilization
    bw_report = bandwidth_utilization(G)
    print("Bandwidth Utilization Report:")
    for link, info in bw_report.items():
        print(f"{link}: {info}")

    # OSPF/BGP convergence
    ospf_report = route_convergence(G, protocol="OSPF")
    bgp_report = route_convergence(G, protocol="BGP")
    print("\nOSPF Route Convergence:", ospf_report)
    print("BGP Route Convergence:", bgp_report)

    # -----------------------------
    # Export Reports
    # -----------------------------
    reports = {
        "validation": errors if errors else "No errors found",
        "performance": perf_report,
        "simulation": {
            "traffic_R1_R2": simulate_traffic(G, "R1", "R2"),
            "vlan_reachability": vlan_reachability(G)
        },
        "failure_simulation": result,
        "vlan_failure_simulation": vlan_result,
        "bandwidth_utilization": bw_report,
        "route_convergence": {"OSPF": ospf_report, "BGP": bgp_report}
    }

    def stringify_keys(obj):
        if isinstance(obj, dict):
            return {str(k): stringify_keys(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [stringify_keys(i) for i in obj]
        else:
            return obj

    safe_reports = stringify_keys(reports)

    with open("network_report.json", "w") as f:
        json.dump(safe_reports, f, indent=4)
    print("\n--- Reports exported to network_report.json ---")

    export_csv(safe_reports, outdir="reports")
    msg = export_excel(safe_reports, outfile="network_report.xlsx")
    print(f"--- {msg} ---")

    # -----------------------------
    # Live CLI Input Mode
    # -----------------------------
    def live_cli_mode(G):
        print("\n--- Live CLI Mode ---")
        print("Type 'help' to see commands, 'exit' to quit.")
        while True:
            cmd = input(">> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                print("Exiting Live CLI Mode.")
                break
            elif cmd.lower() == "help":
                print("""
Commands:
simulate <src> <dst>       - Simulate traffic from src to dst
vlan_reach                 - Show VLAN reachability
fail <src> <dst>           - Simulate link failure between src and dst
vlan_fail <vlan> <dev1> <dev2> - Simulate VLAN failure
bw_util                    - Show bandwidth utilization
ospf_conv                  - Simulate OSPF convergence
bgp_conv                   - Simulate BGP convergence
exit / quit                - Exit CLI mode
""")
            else:
                parts = cmd.split()
                if not parts:
                    continue
                action = parts[0].lower()
                try:
                    if action == "simulate" and len(parts) == 3:
                        pprint(simulate_traffic(G, parts[1], parts[2]))
                    elif action == "vlan_reach":
                        vlan_map = vlan_reachability(G)
                        table = [[vlan, ", ".join(nodes)] for vlan, nodes in vlan_map.items()]
                        print(tabulate(table, headers=["VLAN ID", "Reachable Nodes"], tablefmt="fancy_grid"))
                    elif action == "fail" and len(parts) == 3:
                        pprint(simulate_failure(G, failed_link=(parts[1], parts[2]), src=parts[1], dst=parts[2]))
                    elif action == "vlan_fail" and len(parts) >= 4:
                        vlan_id = int(parts[1])
                        dev_pair = tuple(parts[2:4])
                        pprint(simulate_vlan_failure(G, vlan_id=vlan_id, removed_from=dev_pair))
                    elif action == "bw_util":
                        report = bandwidth_utilization(G)
                        table = [[f"{u}-{v}", info["actual_kbps"], info["max_kbps"], f"{info['util_percent']}%"] 
                                 for (u, v), info in report.items()]
                        print(tabulate(table, headers=["Link", "Actual (Kbps)", "Max (Kbps)", "Utilization"], tablefmt="fancy_grid"))
                    elif action == "ospf_conv":
                        report = route_convergence(G, "OSPF")
                        table = [[node, time] for node, time in report.items()]
                        print(tabulate(table, headers=["Node", "Convergence Time (ms)"], tablefmt="fancy_grid"))
                    elif action == "bgp_conv":
                        report = route_convergence(G, "BGP")
                        table = [[node, time] for node, time in report.items()]
                        print(tabulate(table, headers=["Node", "Convergence Time (ms)"], tablefmt="fancy_grid"))
                    else:
                        print("Unknown command. Type 'help' for options.")
                except Exception as e:
                    print("Error executing command:", e)

    # Start CLI
    live_cli_mode(G)
