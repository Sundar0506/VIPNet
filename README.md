VIPNet – Virtual Intelligent Packet Network
1. Overview

VIPNet is a network simulation and analysis tool built in Python that allows users to:

Parse network device configurations (routers and switches).

Automatically build a network topology.

Analyze network performance, connectivity, and redundancy.

Validate device configurations for issues like MTU mismatch or low bandwidth.

Simulate traffic flows, link failures, and VLAN failures.

Perform advanced simulations like bandwidth utilization and OSPF/BGP route convergence.

Visualize the network interactively using Matplotlib and PyVis.

Export reports in JSON, CSV, and Excel formats.

Provide a Live CLI mode for interactive testing and simulations.

2. Key Features

Topology Builder

Automatically constructs a graph of devices and links using NetworkX.

Differentiates between Layer 2 (L2) and Layer 3 (L3) connections.

Configuration Validation

Checks interfaces for IP configuration issues.

Detects MTU mismatches and bandwidth limitations.

Performance Analysis

Connectivity check: whether the network is fully connected.

Bottleneck detection: identifies links with MTU or bandwidth issues.

Redundancy analysis: checks if multiple paths exist between nodes.

Simulations

Traffic simulation between any two nodes.

VLAN reachability for Layer 2 networks.

Link failure simulation with rerouting analysis.

VLAN failure simulation to see impact on network connectivity.

Advanced metrics: bandwidth utilization and OSPF/BGP convergence times.

Visualization

Matplotlib for static network topology diagrams.

PyVis for interactive HTML visualizations with clickable nodes and links.

Report Generation

Exports validation, performance, simulation, and convergence data.

Supports JSON, CSV, and Excel formats.

Live CLI Mode

Users can type commands interactively to test traffic, simulate failures, and view reports.

Commands include:

simulate <src> <dst>
vlan_reach
fail <src> <dst>
vlan_fail <vlan> <dev1> <dev2>
bw_util
ospf_conv
bgp_conv

3. Technologies Used

Python 3.x

NetworkX – for network graph creation and path analysis.

Matplotlib – for static network visualization.

PyVis – for interactive HTML network visualization.

Tabulate & pprint – for CLI-friendly tabular output.

JSON, CSV, Excel (openpyxl/pandas) – for exporting reports.

4. Project Structure
vipnet/
├── configs/                # Device configuration files (R1.txt, R2.txt, SW1.txt)
├── core/
│   ├── parser.py           # Parses device configs
│   ├── topo.py             # Builds network topology
│   ├── validate.py         # Configuration validation functions
│   ├── perf.py             # Performance analysis functions
│   ├── simulate.py         # Simulation functions
│   ├── export.py           # Export functions (CSV, Excel)
├── reports/                # Generated reports and topology visualizations
├── main.py                 # Main script to run the project
├── README.md               # Project explanation
└── requirements.txt        # Python dependencies

5. Sample Output

Validation Report:

['R2:GigabitEthernet0/0 MTU below standard']


Performance Report:

{'connected': True, 'bottlenecks': [('R1', 'R2', 'MTU mismatch')], 'redundancy': {...}}


VLAN Reachability:

{10: ['SW1', 'R1', 'R2'], 20: ['SW1', 'R1', 'R2']}


Bandwidth Utilization Table (CLI):

╒════════╤═════════════════╤══════════════╤═══════════════╕
│ Link   │   Actual (Kbps) │   Max (Kbps) │ Utilization   │
╞════════╪═════════════════╪══════════════╪═══════════════╡
│ R1-R2  │         1000000 │      1000000 │ 100.0%        │
╘════════╧═════════════════╧══════════════╧═══════════════╛

6. Use Cases

Network engineers can validate configurations before deployment.

Students can learn network topologies, traffic flow, and redundancy.

IT teams can simulate link or VLAN failures and see impact on connectivity.
