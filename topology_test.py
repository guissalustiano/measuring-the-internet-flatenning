from io import StringIO
from topology import PropagationDirection, build_topology, propagate_paths
import networkx as nx
import matplotlib.pyplot as plt

def test_multiple_paths_to_origin():
    f = StringIO("""\
1|2|-1
1|3|-1
2|4|-1
3|4|-1""")


    topo = build_topology(f)
    paths = propagate_paths(topo, 1)
    paths = set(tuple(p) for p in paths)

    print(*paths, sep='\n')

    assert len(paths) == 5
    assert (1,) in paths
    assert (1,2) in paths
    assert (1,2,4) in paths
    assert (1,3) in paths
    assert (1,3,4) in paths

def test_change_topology():
    f = StringIO("""\
1|2|-1
1|3|-1
2|4|0""")
    
    topo = build_topology(f)
    topo1 = topo.copy()
    topo2 = topo.copy()
    paths1 = propagate_paths(topo1, 2)
    paths2 = propagate_paths(topo2, 2)
    print(paths1)
    print(paths2)
    
    # assert len(paths) == 4
    # assert (2,) in paths
    # assert (2,1) in paths
    # assert (2,1,3) in paths
    # assert (2,4) in paths

    # topo.remove_node(1)
    # paths = propagate_paths(topo.copy(), 2)

    # print(topo.edges(data=True))
    # print(*paths, sep='\n')
    # assert len(paths) == 2

if __name__ == "__main__":
    test_change_topology()