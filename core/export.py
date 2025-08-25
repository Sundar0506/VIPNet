# core/export.py
import os
import csv

def _stringify_keys(obj):
    if isinstance(obj, dict):
        return {str(k): _stringify_keys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_stringify_keys(i) for i in obj]
    else:
        return obj

def _listify_path(path):
    if path is None:
        return None
    if isinstance(path, (list, tuple)):
        return " -> ".join(map(str, path))
    return str(path)

def _rows_from_reports(reports):
    """
    Transform the nested 'reports' dict into simple row lists
    for CSV/Excel sheets.
    Returns a dict: {sheet_name: [ {col: val, ...}, ... ] }
    """
    rows = {}

    # Validation
    val = reports.get("validation")
    if isinstance(val, list):
        rows["validation"] = [{"error": e} for e in val]
    else:
        rows["validation"] = [{"status": str(val)}]

    # Performance: bottlenecks
    perf = reports.get("performance", {})
    bnecks = perf.get("bottlenecks", [])
    rows["bottlenecks"] = [
        {"node_u": u, "node_v": v, "issue": issue}
        for u, v, issue in bnecks
    ]

    # Performance: redundancy (keys might be tuple-like strings already)
    red = perf.get("redundancy", {})
    red_rows = []
    for k, status in red.items():
        # k could be a tuple or a string like "('R1','R2')"
        if isinstance(k, (list, tuple)):
            u, v = k
        else:
            # best effort parse
            u, v = str(k), ""
        red_rows.append({"pair": f"{u}-{v}" if v else str(k), "status": status})
    rows["redundancy"] = red_rows

    # Simulation: traffic
    sim = reports.get("simulation", {})
    traffic = sim.get("traffic_R1_R2", {})
    rows["traffic"] = [{
        "src": traffic.get("src"),
        "dst": traffic.get("dst"),
        "path": _listify_path(traffic.get("path"))
    }]

    # Simulation: vlan reachability
    vl_reach = sim.get("vlan_reachability", {})
    rows["vlan_reachability"] = [
        {"vlan": str(vlan), "nodes": ", ".join(sorted(map(str, nodes)))}
        for vlan, nodes in vl_reach.items()
    ]

    # Failure simulation
    fs = reports.get("failure_simulation", {})
    rows["failure_simulation"] = [{
        "failed_link": str(fs.get("failed_link")),
        "src": fs.get("src"),
        "dst": fs.get("dst"),
        "status": fs.get("status"),
        "new_path": _listify_path(fs.get("new_path")),
    }]

    # VLAN failure simulation
    vfs = reports.get("vlan_failure_simulation", {})
    vfs_reach = vfs.get("new_vlan_reachability", {})
    rows["vlan_failure_simulation"] = [{
        "failed_vlan": vfs.get("failed_vlan"),
        "removed_from": str(vfs.get("removed_from")),
    }]
    rows["vlan_failure_reachability"] = [
        {"vlan": str(vlan), "nodes": ", ".join(sorted(map(str, nodes)))}
        for vlan, nodes in vfs_reach.items()
    ]

    return rows

def export_csv(reports, outdir="reports"):
    """
    Write multiple CSVs into ./reports folder.
    """
    os.makedirs(outdir, exist_ok=True)
    # Ensure keys are JSON/CSV-safe strings
    safe = _stringify_keys(reports)
    sheets = _rows_from_reports(safe)

    for name, rowlist in sheets.items():
        path = os.path.join(outdir, f"{name}.csv")
        if not rowlist:
            # Write an empty file with a placeholder header
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("empty\n")
            continue

        # infer headers from union of keys
        headers = set()
        for r in rowlist:
            headers.update(r.keys())
        headers = list(headers)

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for r in rowlist:
                writer.writerow(r)

def export_excel(reports, outfile="network_report.xlsx"):
    """
    Write a single Excel workbook with multiple sheets.
    Requires pandas + openpyxl/xlsxwriter installed.
    """
    try:
        import pandas as pd
    except Exception as e:
        return f"Skipped Excel export (pandas not installed): {e}"

    safe = _stringify_keys(reports)
    sheets = _rows_from_reports(safe)

    try:
        with pd.ExcelWriter(outfile) as xw:
            for name, rowlist in sheets.items():
                df = pd.DataFrame(rowlist)
                df.to_excel(xw, sheet_name=name[:31], index=False)  # Excel sheet name limit
        return f"Excel exported to {outfile}"
    except Exception as e:
        return f"Excel export failed: {e}"
