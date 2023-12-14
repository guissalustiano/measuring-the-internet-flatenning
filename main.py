from valley_free import load_topology, propagate_paths

# From https://en.wikipedia.org/wiki/Tier_1_network#List_of_Tier_1_networks
tier1 = [
    7018,
    3320,
    3257,
    6830,
    3356,
    2914,
    5511,
    3491,
    1239,
    6453,
    6762,
    1299,
    12956,
    701,
    6461,
]

# From: https://en.wikipedia.org/wiki/Tier_2_network
tier2 = [
    6939,
    7713,
    9002,
    1764,
    34549,
    4766,
    9304,
    22652,
    9318,
    3292,
    2497,
    1273,
    2516,
    23947,
    4134,
    4809,
    4837,
    3462,
    5400,
    7922,
    1257,
    12390,
    2711,
    8002,
    14744,
    38930,
    33891,
    41327,
    7473,
    24482,
    9121,
    6663,
]

topo = load_topology("20161101.as-rel.txt.bz2")
paths = propagate_paths(topo, 15169)

reachable_as = set()
for path in paths:
    if 7018 in path:
        continue
    reachable_as.add(path[-1])

print(len(reachable_as))