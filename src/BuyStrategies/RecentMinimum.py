from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Recent Minimum"
    description : str = "Looks for the asset which is closer to its previous local \
minimum."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        latest_min = None
        latest_max = None

        for date in ap.data.local_minimums:
            if latest_min == None or date > latest_min:
                latest_min = date

        for date in ap.data.local_maximums:
            if latest_max == None or date > latest_max:
                latest_max = date

        res = Strategy.normalize(latest_min - latest_max)
        return Strategy.get_res(Strategy.name, ap, res)