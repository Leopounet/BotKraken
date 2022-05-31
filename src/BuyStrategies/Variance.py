from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Variance"
    description : str = "Looks for the asset which has the highest Variance."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        return Strategy.normalize(ap.data.variance)