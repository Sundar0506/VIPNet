# VIPNet – Virtual Intelligent Packet Network

## Overview
VIPNet is a **network simulation and analysis tool** built in Python. It allows users to:

- Parse network device configurations (routers and switches).  
- Automatically build a network topology.  
- Analyze **network performance**, **connectivity**, and **redundancy**.  
- Validate device configurations for issues like MTU mismatch or low bandwidth.  
- Simulate **traffic flows**, **link failures**, and **VLAN failures**.  
- Perform advanced simulations like **bandwidth utilization** and **OSPF/BGP route convergence**.  
- Visualize the network interactively using **Matplotlib** and **PyVis**.  
- Export reports in **JSON, CSV, and Excel** formats.  
- Interact via a **Live CLI mode** for testing and simulations.

---

## Features
1. **Topology Builder**: Automatically constructs a network graph using **NetworkX**.  
2. **Configuration Validation**: Detects MTU mismatches and IP/bandwidth issues.  
3. **Performance Analysis**: Checks connectivity, identifies bottlenecks, and evaluates redundancy.  
4. **Simulations**:
   - Traffic simulation between any two nodes.  
   - VLAN reachability mapping.  
   - Link and VLAN failure simulations.  
   - Bandwidth utilization and OSPF/BGP route convergence.  
5. **Visualization**:
   - Static diagrams with **Matplotlib**.  
   - Interactive HTML visualizations with **PyVis**.  
6. **Report Generation**: Export validation, performance, simulation, and convergence data in **JSON, CSV, and Excel**.  
7. **Live CLI Mode**: Interactively run simulations and view results.

---

## Technologies Used
- Python 3.x  
- NetworkX  
- Matplotlib  
- PyVis  
- Tabulate & pprint  
- JSON, CSV, Excel (openpyxl/pandas)

---

## Project Structure
 
 <img width="710" height="459" alt="Screenshot 2025-08-25 145253" src="https://github.com/user-attachments/assets/595fb2c6-a967-43b9-9808-99016a69063d" />

 
---

## Sample CLI Commands
 <img width="624" height="325" alt="Screenshot 2025-08-25 145536" src="https://github.com/user-attachments/assets/9624c769-4fe8-4b52-9c0d-96a705bd1792" />



---

## Installation
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/vipnet.git
cd vipnet


2.Install dependencies:
pip install -r requirements.txt


3.Run the main program:

python main.py

Sample Output

Validation Report: ['R2:GigabitEthernet0/0 MTU below standard']

Performance Report: Shows connected network, bottlenecks, and redundancy.

VLAN Reachability: {10: ['SW1', 'R1', 'R2'], 20: ['SW1', 'R1', 'R2']}

Bandwidth Utilization Table:
╒════════╤═════════════════╤══════════════╤═══════════════╕
│ Link   │   Actual (Kbps) │   Max (Kbps) │ Utilization   │
╞════════╪═════════════════╪══════════════╪═══════════════╡
│ R1-R2  │         1000000 │      1000000 │ 100.0%        │
╘════════╧═════════════════╧══════════════╧═══════════════╛

Use Cases:

Validate network configurations before deployment.

Learn network topologies, traffic flow, and redundancy.

Simulate link or VLAN failures to understand connectivity impact.
