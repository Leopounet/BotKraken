from Structures.AssetPair import AssetPair

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Lower All Local Minimums"
    description : str = "Looks for the asset for which the current price is lower \
than all previous local minimums."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        res = 0
        for lm in ap.data.local_minimums:
            if ap.data.current <= ap.data.local_minimums[lm]: res += 1
            else: res -= 1
        return res