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


def do_query_path(fp, args):
    """Find shortest path between two nodes"""
    data = load(fp)
    nodes = {n["id"]:n for n in data["nodes"]}
    edges = data["edges"]
    adj = {n["id"]:set() for n in data["nodes"]}
    for e in edges:
        adj[e["source"]].add(e["target"]); adj[e["target"]].add(e["source"])
    if len(args)<2: print("Usage: query path [node1] [node2]"); return
    s,t = args[0], args[1]
    if s not in adj or t not in adj: print("Node not found"); return
    visited, queue, parent = {s}, [(s,0)], {s:None}
    while queue:
        cur,dist = queue.pop(0)
        if cur==t:
            path=[]; n=t
            while n: path.append(n); n=parent[n]
            path.reverse()
            print(f"Path ({dist} steps):")
            for i,n in enumerate(path):
                cat = nodes[n].get("category",""); lbl = nodes[n].get("label","")
                print(f"  {i}. {n} ({lbl}) [{cat}]")
            return
        for nb in adj[cur]:
            if nb not in visited:
                visited.add(nb); queue.append((nb,dist+1)); parent[nb]=cur
    print("No path found")

def do_query_neighbors(fp, args):
    """Show neighbors of a node"""
    data = load(fp)
    nodes = {n["id"]:n for n in data["nodes"]}
    edges = data["edges"]
    adj = {n["id"]:set() for n in data["nodes"]}
    edge_map = {}
    for e in edges:
        adj[e["source"]].add(e["target"]); adj[e["target"]].add(e["source"])
        edge_map[(e["source"],e["target"])] = e.get("label","")
        edge_map[(e["target"],e["source"])] = e.get("label","")
    if not args: print("Usage: query neighbors [node_id]"); return
    nid = args[0]
    if nid not in adj: print("Node not found"); return
    n = nodes[nid]
    print(f"Neighbors of {nid} ({n.get("label","")}) [{n.get("category","")}]:")
    for nb in sorted(adj[nid], key=lambda x: nodes[x].get("label","")):
        lbl = nodes[nb].get("label",""); cat = nodes[nb].get("category","")
        el = edge_map.get((nid,nb),"")
        print(f"  {nb} ({lbl}) [{cat}] - {el}")

def do_query_search(fp, args):
    """Search nodes by keyword"""
    data = load(fp)
    if not args: print("Usage: query search [keyword]"); return
    kw = args[0].lower()
    results = []
    for n in data["nodes"]:
        if kw in n["id"].lower() or kw in n.get("label","").lower() or kw in n.get("description","").lower():
            results.append(n)
        if "depth" in n and n["depth"]:
            d = n["depth"]
            for k in ["core_idea","why_it_matters"]:
                if k in d and kw in str(d[k]).lower():
                    results.append(n)
                    break
    print(f"Search results for "{kw}":")
    for n in results[:20]:
        print(f"  {n["id"]} ({n["label"]}) [{n["category"]}]")

def do_query_category(fp, args):
    """List all nodes in a category"""
    data = load(fp)
    if not args: print("Usage: query category [name]"); return
    cat = args[0]
    print(f"Category: {cat}")
    for n in sorted(data["nodes"], key=lambda x: x["id"]):
        if n["category"]==cat:
            d = "\u2713" if n.get("depth") else " "
            print(f"  [{d}] {n["id"]} - {n.get("label","")}")

def do_query(fp, args):
    sub = args[0] if args else ""
    subs = {"path":do_query_path,"neighbors":do_query_neighbors,"search":do_query_search,"category":do_query_category}
    if sub in subs:
        subs[sub](fp, args[1:])
    else:
        print("Query subcommands: path, neighbors, search, category")
if __name__ == "__main__":
    cmds = {"validate":do_validate,"analyze":do_analyze,"stat":do_stat,"export":do_export, "query":do_query}
    cmd = sys.argv[1] if len(sys.argv)>1 else "stat"
    fp = sys.argv[2] if len(sys.argv)>2 else "data/knowledge.json"
    if cmd in cmds:
        cmds[cmd](fp)
    else:
        print(f"Unknown command: {cmd}. Available: {', '.join(cmds.keys())}")