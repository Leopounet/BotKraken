from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Lower All Local Minimums"
    description : str = "Looks for the asset for which the current price is lower \
than all previous local minimums."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        res = 0
        for lm in ap.data.local_minimums:
            if ap.data.current < ap.data.local_minimums[lm]: res += 1
            else: res -= 1
        res = Strategy.normalize(res)
        return Strategy.get_res(Strategy.name, ap, res)
