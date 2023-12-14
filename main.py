from valley_free import load_topology, propagate_paths

# From https://en.wikipedia.org/wiki/Tier_1_network#List_of_Tier_1_networks
TIER1 = set([
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
])

# From: https://en.wikipedia.org/wiki/Tier_2_network
TIER2 = set([
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
])

def hierarchy_free(topo, asn):
    paths = propagate_paths(topo, asn)
    tier1 = TIER1 - set([asn])
    tier2 = TIER2 - set([asn])

    provider_free = set()
    tier1_free = set()
    hierarchy_free = set()
    for path in paths:
        print(path)
        if path[-1] in provider_free:
            print("Skipping because provider free")
            continue

        if any(pr_as in path for pr_as in topo.ases_map[asn].providers):
            continue
        provider_free.add(path[-1])

        if any(t1_as in path for t1_as in tier1):
            continue
        tier1_free.add(path[-1])

        if any(t2_as in path for t2_as in tier2):
            continue
        hierarchy_free.add(path[-1])

    return hierarchy_free, tier1_free, provider_free

if __name__ == "__main__":
    topo = load_topology("20161101.as-rel.txt.bz2")
    ibm_asn = 19604
    hierarchy_free, tier1_free, provider_free = hierachi_free(topo, ibm_asn)
    print(f"IBM AS Number: {ibm_asn}")
    print(f"Hierarchy Free: {hierarchy_free}")
    print(f"Tier1 Free: {tier1_free}")
    print(f"Provider Free: {provider_free}")