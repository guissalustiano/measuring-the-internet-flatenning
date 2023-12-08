from io import StringIO
from topology import build_topology, propagate_paths

def multiple_paths_to_origin():
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

if __name__ == '__main__':
    multiple_paths_to_origin()
