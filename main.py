from topology import build_topology, propagate_paths, PropagationDirection

asn = 1031

with open("20231201.as-rel2.txt") as f:
    topo = build_topology(f)
paths = propagate_paths(topo, asn, direction=PropagationDirection.DOWN)

print(f"AS{asn} has {len(paths)} paths")
