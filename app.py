import streamlit as st
from core.parser import parse_router_config
from core.topo import build_topology
from core.validate import validate_configs
from core.perf import analyze_performance
from core.simulate import simulate_traffic, vlan_reachability, simulate_failure, simulate_vlan_failure, bandwidth_utilization, route_convergence
from core.export import export_csv, export_excel
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import os
from io import BytesIO

# Ensure reports folder exists
os.makedirs("reports", exist_ok=True)

# Load devices and topology
devices = [parse_router_config("configs/R1.txt"),
           parse_router_config("configs/R2.txt"),
           parse_router_config("configs/SW1.txt")]
G = build_topology(devices)

st.title("VIPNet Network Simulator")
st.sidebar.header("Simulation Options")

# Sidebar options
simulation_type = st.sidebar.selectbox(
    "Choose Simulation Type",
    ["Validation", "Performance", "Traffic", "VLAN Reachability", "Link Failure", "VLAN Failure", "Advanced Simulations"]
)

# ------------------------------
# Run Simulations / Reports
# ------------------------------
if simulation_type == "Validation":
    st.subheader("Validation Report")
    errors = validate_configs(devices)
    st.write(errors if errors else "No errors found")

elif simulation_type == "Performance":
    st.subheader("Performance Report")
    perf_report = analyze_performance(G)
    st.json(perf_report)

elif simulation_type == "Traffic":
    st.subheader("Traffic Simulation")
    src = st.text_input("Source Device", "R1")
    dst = st.text_input("Destination Device", "R2")
    if st.button("Simulate Traffic"):
        result = simulate_traffic(G, src, dst)
        st.json(result)

elif simulation_type == "VLAN Reachability":
    st.subheader("VLAN Reachability")
    if st.button("Show VLAN Map"):
        vlan_map = vlan_reachability(G)
        st.json(vlan_map)

elif simulation_type == "Link Failure":
    st.subheader("Link Failure Simulation")
    src = st.text_input("Source Device", "R1")
    dst = st.text_input("Destination Device", "R2")
    if st.button("Simulate Link Failure"):
        result = simulate_failure(G, failed_link=(src, dst), src=src, dst=dst)
        st.json(result)

elif simulation_type == "VLAN Failure":
    st.subheader("VLAN Failure Simulation")
    vlan_id = st.number_input("VLAN ID", min_value=1, value=10)
    dev1 = st.text_input("Device 1", "R1")
    dev2 = st.text_input("Device 2", "SW1")
    if st.button("Simulate VLAN Failure"):
        vlan_result = simulate_vlan_failure(G, vlan_id=vlan_id, removed_from=(dev1, dev2))
        st.json(vlan_result)

elif simulation_type == "Advanced Simulations":
    st.subheader("Bandwidth Utilization")
    bw_report = bandwidth_utilization(G)
    st.json(bw_report)

    st.subheader("Route Convergence")
    ospf_report = route_convergence(G, "OSPF")
    bgp_report = route_convergence(G, "BGP")
    st.write("OSPF:", ospf_report)
    st.write("BGP:", bgp_report)

# ------------------------------
# Network Topology Visualization
# ------------------------------
st.subheader("Network Topology (Matplotlib)")
pos = nx.spring_layout(G)
plt.figure(figsize=(8,6))
nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000)
st.pyplot(plt)

st.subheader("Network Topology (Interactive HTML)")
net = Network(height="500px", width="100%", notebook=False)
for n, attr in G.nodes(data=True):
    color = "skyblue" if attr["device_type"]=="router" else "lightgreen"
    shape = "box" if attr["device_type"]=="router" else "ellipse"
    net.add_node(n, label=n, color=color, shape=shape)
for u,v,d in G.edges(data=True):
    title = d.get("subnet", "") if d["type"]=="L3" else "VLANs: " + ",".join(map(str, d.get("vlans", [])))
    style = "dashed" if d["type"]=="L2" else "solid"
    net.add_edge(u,v, title=title, color="blue" if d["type"]=="L3" else "green", width=2, dashes=(style=="dashed"))

html_path = os.path.join("reports","network_topology.html")
net.write_html(html_path)
st.markdown(f"[Download Interactive HTML Topology]({html_path})")
