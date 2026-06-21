#!/usr/bin/env python3
"""Validate knowledge.json structure and content."""
import json, sys
def validate(fp):
    with open(fp,"r",encoding="utf-8") as f: data=json.load(f)
    errors=[]; nodes=data.get("nodes",[]); edges=data.get("edges",[])
    node_ids=set()
    for i,n in enumerate(nodes):
        nid=n.get("id",""); node_ids.add(nid)
        for f in ["id","label","category","description","color"]:
            if f not in n: errors.append(f"Node {i}: missing {f}")
    for i,e in enumerate(edges):
        if e.get("source")not in node_ids: errors.append(f"Edge {i}: source unknown")
        if e.get("target")not in node_ids: errors.append(f"Edge {i}: target unknown")
    if errors:
        for e in errors: print("ERROR: "+e)
        return False
    print(f"VALID: {len(nodes)} nodes, {len(edges)} edges")
    return True
if __name__=="__main__":
    fp=sys.argv[1] if len(sys.argv)>1 else "data/knowledge.json"
    sys.exit(0 if validate(fp) else 1)
