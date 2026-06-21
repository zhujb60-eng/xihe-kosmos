#!/usr/bin/env python3
"""
Xihe Kosmos - Graph Tools
Usage: python graph_tools.py [command] [path]

Commands:
  validate    Validate knowledge.json structure
  analyze     Compute graph statistics
  stat        Quick statistics summary
  export      Export graph data
"""

import json, sys, os
from collections import Counter

def load(fp):
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)

def do_validate(fp):
    data = load(fp)
    errors = []
    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    nids = set()
    req = {"id":str,"label":str,"category":str,"description":str,"color":str}
    depth_fields = {"core_idea":str,"why_it_matters":str,"action_principles":list,"key_thinkers":list,"timeline":list,"cross_domain":list,"open_frontiers":list}

    for i, n in enumerate(nodes):
        nid = n.get("id","")
        nids.add(nid)
        for field, ftype in req.items():
            if field not in n:
                errors.append(f"Node {i} ({nid}): missing {field}")
        if n.get("category") not in ["physics","biology","cs","math","systems","art","philosophy","society"]:
            errors.append(f"Node {i} ({nid}): invalid category \"{n.get('category')}\"")
        if "depth" in n and n["depth"]:
            d = n["depth"]
            for field, ftype in depth_fields.items():
                if field in d and not isinstance(d[field], ftype):
                    errors.append(f"Node {nid}: depth.{field} should be {ftype.__name__}")

    for i, e in enumerate(edges):
        if e.get("source") not in nids:
            errors.append(f"Edge {i}: source \"{e.get('source')}\" not found")
        if e.get("target") not in nids:
            errors.append(f"Edge {i}: target \"{e.get('target')}\" not found")

    if errors:
        for e in errors: print("ERROR:", e)
        return False
    print(f"VALID: {len(nodes)} nodes, {len(edges)} edges - clean")
    return True

def do_analyze(fp):
    data = load(fp)
    nodes = data["nodes"]; edges = data["edges"]
    cats = {n["id"]:n["category"] for n in nodes}
    adj = {n["id"]:set() for n in nodes}

    for e in edges:
        s,t = e["source"], e["target"]
        adj[s].add(t); adj[t].add(s)

    print("=== Xihe Kosmos - Graph Analysis ===\n")
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    print(f"Network density: {2*len(edges)/(len(nodes)*(len(nodes)-1))*100:.2f}%")
    print(f"Avg connections per node: {sum(len(v) for v in adj.values())/len(nodes):.2f}")

    # Category breakdown
    cat_count = Counter(n["category"] for n in nodes)
    print(f"\n--- Categories ---")
    for c, cnt in sorted(cat_count.items()):
        intra = sum(1 for e in edges if cats[e["source"]]==c and cats[e["target"]]==c)
        inter = sum(1 for e in edges if cats[e["source"]]==c or cats[e["target"]]==c)
        depth_nodes = sum(1 for n in nodes if n["category"]==c and "depth" in n)
        print(f"  {c}: {cnt} nodes, {intra} intra, {inter} inter edges, {depth_nodes} depth")

    # Most/least connected
    deg = {nid:len(con) for nid,con in adj.items()}
    print(f"\n--- Most Connected (Top 5) ---")
    for nid in sorted(deg, key=deg.get, reverse=True)[:5]:
        print(f"  {nid} ({cats[nid]}): {deg[nid]} connections")
    print(f"\n--- Least Connected (Bottom 5) ---")
    for nid in sorted(deg, key=deg.get)[:5]:
        print(f"  {nid} ({cats[nid]}): {deg[nid]} connections")

    # Depth stats
    depth_count = sum(1 for n in nodes if "depth" in n and n["depth"])
    max_principles = max(len(n["depth"].get("action_principles",[])) for n in nodes if "depth" in n and n["depth"])
    print(f"\nDepth content: {depth_count}/{len(nodes)} nodes have depth")
    print(f"Max action principles in a node: {max_principles}")

def do_stat(fp):
    data = load(fp)
    n = len(data["nodes"]); e = len(data["edges"])
    cats = Counter(x["category"] for x in data["nodes"])
    depth = sum(1 for x in data["nodes"] if "depth" in x and x["depth"])
    print(f"N:{n} E:{e} D:{depth} C:{len(cats)}")
    for c,cnt in sorted(cats.items()):
        print(f"  {c}:{cnt}")

def do_export(fp):
    data = load(fp)
    base = os.path.dirname(fp)
    nodes = data["nodes"]; edges = data["edges"]
    # CSV export
    with open(os.path.join(base,"nodes.csv"),"w",encoding="utf-8") as f:
        f.write("id,label,category,description,has_depth\n")
        for n in nodes:
            d = "yes" if n.get("depth") else "no"
            desc = n.get("description","").replace('"','""')
            f.write(f'{n["id"]},"{n["label"]}",{n["category"]},"{desc}",{d}\n')
    with open(os.path.join(base,"edges.csv"),"w",encoding="utf-8") as f:
        f.write("source,target,label\n")
        for e in edges:
            f.write(f'{e["source"]},{e["target"]},"{e.get("label","")}"\n')
    print(f"Exported: nodes.csv ({len(nodes)} rows), edges.csv ({len(edges)} rows)")

if __name__ == "__main__":
    cmds = {"validate":do_validate,"analyze":do_analyze,"stat":do_stat,"export":do_export}
    cmd = sys.argv[1] if len(sys.argv)>1 else "stat"
    fp = sys.argv[2] if len(sys.argv)>2 else "data/knowledge.json"
    if cmd in cmds:
        cmds[cmd](fp)
    else:
        print(f"Unknown command: {cmd}. Available: {', '.join(cmds.keys())}")