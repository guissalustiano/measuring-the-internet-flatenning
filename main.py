from valley_free import load_topology, propagate_paths
import pandas as pd

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

CLOUD_PROVIDERS = set([
    36351, # IBM
    19604, # IBM Cloud
    15169, # Google
    8075, # Microsoft (Not azure)
    12076, # Microsoft (Azure)
    16509, # Amazon Cloud
])

def calc_hierarchy_free(topo, asn):
    assert(isinstance(asn, int))

    paths = propagate_paths(topo, asn)
    provider = set(topo.ases_map[asn].providers) - set([asn])
    tier1 = TIER1 - set([asn])
    tier2 = TIER2 - set([asn])

    hierarchy_free = set()
    for path in paths:
        if any(t1_as in path for t1_as in tier1):
            # print("Skipping because tier1 in path")
            continue

        if any(t2_as in path for t2_as in tier2):
            # print("Skipping because tier2 in path")
            continue

        assert(isinstance(path[-1], int))
        hierarchy_free.add(path[-1])

    return hierarchy_free

if __name__ == "__main__":
    topo = load_topology("20231201.as-rel.txt.bz2")

    asns = list(TIER1 | TIER2 | CLOUD_PROVIDERS)
    df = pd.DataFrame(data = {
        "asn": asns,
        "hierarchy_free": [len(calc_hierarchy_free(topo, asn)) for asn in asns],
    })

    print(df.head())
    print(df.info())
    print(df.describe())

    df.to_csv("hierarchy_free.csv", index=False)



