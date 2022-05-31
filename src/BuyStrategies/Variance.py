from Structures.AssetPair import AssetPair

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Variance"
    description : str = "Looks for the asset which has the highest Variance."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        return ap.data.variance