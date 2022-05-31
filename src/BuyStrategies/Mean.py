from Structures.AssetPair import AssetPair

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy:

    cached_data : Dict[str, Dict[str, Any]] = {}
    name : str = "Mean"
    description : str = "Looks for the asset for which the current price is the lowest \
compared to the mean of all previous prices."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        return ap.data.mean - ap.data.current