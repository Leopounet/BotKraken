from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Mean"
    description : str = "Looks for the asset for which the current price is the lowest \
compared to the mean of all previous prices."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        return Strategy.normalize(ap.data.mean - ap.data.current)