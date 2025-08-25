def validate_configs(devices):
    errors = []

    for dev in devices:
        for iface in dev["interfaces"]:
            # Routers should have IPs on L3 interfaces
            if dev["vlans"] == [] and iface["ip"] is None:
                errors.append(f"{dev['hostname']}:{iface['name']} has no IP")

            # MTU check
            if iface["mtu"] is not None and iface["mtu"] < 1500:
                errors.append(f"{dev['hostname']}:{iface['name']} MTU below standard")

            # Bandwidth check
            if iface["bandwidth"] is not None and iface["bandwidth"] < 1000000:
                errors.append(f"{dev['hostname']}:{iface['name']} Low bandwidth")

    return errors
