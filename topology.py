from enum import Enum
from typing import TextIO
import networkx as nx

class ASRelationship(Enum):
    CUSTOMER = -1
    PEER = 0
    PROVIDER = 1

class PropagationDirection(Enum):
    UP = 0
    DOWN = 1
    PEER = 2

def build_topology(textIO: TextIO) -> nx.MultiDiGraph:
    topo = nx.MultiDiGraph()
    for i, line in enumerate(textIO):
        if line[0] == "#":
            continue

        asn1, asn2, relationship, *_ = line.split("|")
        asn1 = int(asn1)
        asn2 = int(asn2)
        relationship = int(relationship.strip())

        match relationship:
            case 0:
                topo.add_edge(asn1, asn2, relationship=ASRelationship.PEER)
                topo.add_edge(asn2, asn1, relationship=ASRelationship.PEER)
            case -1:
                topo.add_edge(asn1, asn2, relationship=ASRelationship.CUSTOMER)
                topo.add_edge(asn2, asn1, relationship=ASRelationship.PROVIDER)
            case other:
                raise ValueError(f"Unknown relationship type {relationship} in line {i}")
    return topo

# Based on https://github.com/bgpkit/valley-free/blob/494291624e1af5bc9358e03afc28cf40cb70a9ee/src/lib.rs#L207
def propagate_paths(
        topo: nx.MultiDiGraph, 
        origin: int,
        direction: PropagationDirection = PropagationDirection.UP,
        _path: tuple[int] = (),
        _visited: set[int] = set(),
) -> list[tuple[int]]:
    # detect loop
    if origin in _path:
        return []

    _path = tuple(list(_path) + [origin])

    # we have seen this AS from other branches, meaning we have tried propagation from
    # this AS already. so we skip propagation here.
    # NOTE: we still add this path to the paths list. TODO: we probably don't want to do this.
    if origin in _visited:
        return [_path]

    _visited.add(origin)

    connections = topo.edges(origin, data=True)
    destinations = []
    match direction:
        case PropagationDirection.UP:
            for asn1, asn2, data in connections:
                print("CONNECTION", asn1, asn2, data)
                assert asn1 == origin # sanity check
                relationship = data["relationship"]
                match relationship:
                    case ASRelationship.CUSTOMER:
                        destinations.extend(
                            propagate_paths(
                                topo,
                                asn2,
                                PropagationDirection.DOWN,
                                _path,
                                _visited
                            )
                        )
                    case ASRelationship.PEER:
                        print("PEER", asn2)
                        destinations.extend(
                            propagate_paths(
                                topo,
                                asn2,
                                PropagationDirection.PEER,
                                _path,
                                _visited
                            )
                        )
                    case ASRelationship.PROVIDER:
                        destinations.extend(
                            propagate_paths(
                                topo,
                                asn2,
                                PropagationDirection.UP,
                                _path,
                                _visited
                            )
                        )
        case PropagationDirection.DOWN | PropagationDirection.PEER:
            for asn1, asn2, data in connections:
                assert asn1 == origin # sanity check
                relationship = data["relationship"]
                match relationship:
                    case ASRelationship.CUSTOMER:
                        destinations.extend(
                            propagate_paths(
                                topo,
                                asn2,
                                PropagationDirection.DOWN,
                                _path,
                                _visited
                            )
                        )
                    ## PEER is not propagated??
    return [_path] + destinations
