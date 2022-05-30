from Structures.AssetPair import AssetPair

###############################################################################
############################ STRATEGY #########################################
###############################################################################

def strategy(ap : AssetPair) -> float:
    res = 0
    for lm in ap.data.local_minimums:
        if ap.data.current <= ap.data.local_minimums[lm]: res += 1
        else: res -= 1
    return res