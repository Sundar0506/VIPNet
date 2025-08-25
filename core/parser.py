import re
from ipaddress import IPv4Network

def mask_to_prefixlen(mask: str) -> int:
    """Convert subnet mask to prefix length (/24, /30, etc.)"""
    return IPv4Network(f"0.0.0.0/{mask}").prefixlen

def compute_network(ip: str, mask: str) -> str:
    """Return the network (e.g., 192.168.1.0/24) from IP + mask"""
    prefix = mask_to_prefixlen(mask)
    net = IPv4Network(f"{ip}/{prefix}", strict=False)
    return str(net)

def parse_router_config(file_path):
    router_data = {
        "hostname": None,
        "interfaces": [],
        "vlans": [],
        "routing_protocols": {"ospf": [], "bgp": [], "static": []},
        "features": {"cdp": False, "lldp": False}
    }

    with open(file_path, "r") as f:
        lines = f.readlines()

    current_interface = None
    current_vlan = None
    inside_ospf = False
    inside_bgp = False

    for line in lines:
        line = line.strip()

        # Hostname
        if line.startswith("hostname"):
            router_data["hostname"] = line.split()[1]

        # Interface block
        elif line.startswith("interface"):
            current_interface = {
                "name": line.split()[1],
                "description": None,
                "ip": None,
                "mask": None,
                "prefixlen": None,
                "network": None,
                "mtu": None,
                "bandwidth": None,
                "vlans": [],
                "mode": None
            }
            router_data["interfaces"].append(current_interface)

        elif line.startswith("description") and current_interface:
            current_interface["description"] = line.split(" ", 1)[1]

        elif line.startswith("ip address") and current_interface:
            parts = line.split()
            ip, mask = parts[2], parts[3]
            current_interface["ip"] = ip
            current_interface["mask"] = mask
            current_interface["prefixlen"] = mask_to_prefixlen(mask)
            current_interface["network"] = compute_network(ip, mask)

        elif line.startswith("mtu") and current_interface:
            current_interface["mtu"] = int(line.split()[1])

        elif line.startswith("bandwidth") and current_interface:
            current_interface["bandwidth"] = int(line.split()[1])  # Kbps

        elif line.startswith("switchport mode") and current_interface:
            current_interface["mode"] = line.split()[-1]  # access/trunk

        elif line.startswith("switchport access vlan") and current_interface:
            current_interface["vlans"] = [int(line.split()[-1])]

        elif line.startswith("switchport trunk allowed vlan") and current_interface:
            vlan_list = []
            tokens = line.split()[-1].split(",")
            for token in tokens:
                if "-" in token:
                    start, end = map(int, token.split("-"))
                    vlan_list.extend(range(start, end + 1))
                else:
                    vlan_list.append(int(token))
            current_interface["vlans"] = vlan_list

        # VLAN block
        elif line.startswith("vlan"):
            vlan_id = int(line.split()[1])
            current_vlan = {"id": vlan_id, "name": None}
            router_data["vlans"].append(current_vlan)

        elif line.startswith("name") and current_vlan:
            current_vlan["name"] = line.split(" ", 1)[1]

        # Routing protocols
        elif line.startswith("router ospf"):
            inside_ospf = True
            inside_bgp = False
            router_data["routing_protocols"]["ospf"].append({"networks": []})

        elif inside_ospf and line.startswith("network"):
            parts = line.split()
            router_data["routing_protocols"]["ospf"][-1]["networks"].append(
                {"network": parts[1], "wildcard": parts[2], "area": parts[4]}
            )

        elif line.startswith("router bgp"):
            inside_bgp = True
            inside_ospf = False
            asn = int(line.split()[2])
            router_data["routing_protocols"]["bgp"].append({"asn": asn, "neighbors": []})

        elif inside_bgp and line.startswith("neighbor"):
            parts = line.split()
            router_data["routing_protocols"]["bgp"][-1]["neighbors"].append(
                {"ip": parts[1], "remote_as": int(parts[3])}
            )

        # Static route
        elif line.startswith("ip route"):
            parts = line.split()
            router_data["routing_protocols"]["static"].append(
                {"prefix": parts[2], "mask": parts[3], "next_hop": parts[4]}
            )

        # Features
        elif line == "cdp run":
            router_data["features"]["cdp"] = True

        elif line == "lldp run":
            router_data["features"]["lldp"] = True

    return router_data
