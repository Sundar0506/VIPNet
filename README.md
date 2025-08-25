# VIPNet - Virtual IP Network Simulator

VIPNet is a Python-based network simulation and analysis tool that allows you to model, validate, and simulate network topologies with routers and switches. It provides interactive visualizations, performance analysis, and live CLI-based simulations for traffic, VLANs, link failures, and routing protocol convergence.

---

## Features

- Parse router and switch configurations from text files
- Automatically build network topology as a graph
- Validate configurations (MTU, IP addresses, bandwidth)
- Analyze network performance:
  - Connectivity check
  - Bottleneck detection
  - Redundancy and fault tolerance
- Simulate network operations:
  - Traffic simulation between devices
  - VLAN reachability
  - Link failure simulation
  - VLAN failure simulation
- Advanced simulations:
  - Bandwidth utilization
  - OSPF/BGP route convergence
- Interactive visualizations:
  - Static topology with Matplotlib
  - Interactive HTML topology with PyVis
- Export reports:
  - JSON
  - CSV
  - Excel
- Live CLI mode to interactively run simulations and view network statistics

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/vipnet.git
cd vipnet
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Usage
Prepare configuration files for your devices (routers and switches) under the configs/ folder, e.g.:

Copy
Edit
configs/R1.txt
configs/R2.txt
configs/SW1.txt
Run the main script:

bash
Copy
Edit
python main.py
The script will:

Display a summary of nodes and edges

Generate a Matplotlib static topology image: reports/network_topology.png

Generate an interactive HTML topology: reports/network_topology.html

Validate configurations and show errors

Perform performance analysis

Run simulations (traffic, VLAN reachability, failures)

Export reports to JSON, CSV, and Excel

Launch a live CLI mode for interactive commands

Live CLI Commands
pgsql
Copy
Edit
simulate <src> <dst>       - Simulate traffic from src to dst
vlan_reach                 - Show VLAN reachability
fail <src> <dst>           - Simulate link failure between src and dst
vlan_fail <vlan> <dev1> <dev2> - Simulate VLAN failure
bw_util                    - Show bandwidth utilization
ospf_conv                  - Simulate OSPF convergence
bgp_conv                   - Simulate BGP convergence
exit / quit                - Exit CLI mode
help                       - Show available commands
Report Files
All generated reports are saved under the reports/ folder:

network_topology.png → Static Matplotlib topology

network_topology.html → Interactive PyVis topology

network_report.json → Complete report in JSON

network_report.xlsx → Excel report

CSV files for each module (validation, performance, simulations)

Requirements
Python 3.11+ with the following packages (see requirements.txt):

nginx
Copy
Edit
networkx
matplotlib
pyvis
tabulate
pandas
openpyxl
Example Output
CLI Simulation:

ruby
Copy
Edit
>> vlan_reach
╒════════╤═════════════════════════╕
│ VLAN ID│ Reachable Nodes         │
╞════════╪═════════════════════════╡
│ 10     │ R1, SW1, R2            │
│ 20     │ R1, SW1, R2            │
╘════════╧═════════════════════════╛
JSON Report:

json
Copy
Edit
{
    "validation": ["R2:GigabitEthernet0/0 MTU below standard"],
    "performance": {
        "connected": true,
        "bottlenecks": [["R1", "R2", "MTU mismatch"]],
        ...
    }
}
License
MIT License

Author
Sundara Mahalingam M