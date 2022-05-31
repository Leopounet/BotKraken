from Structures.AssetPair import AssetPair
from Structures.Strategy import BuyStrategy

from BuyStrategies.LowerAllLocalMinimums import Strategy as LALM
from BuyStrategies.Variance import Strategy as V

from typing import Dict, Any

###############################################################################
############################ STRATEGY #########################################
###############################################################################

class Strategy(BuyStrategy):

    name : str = "Variance Lower All Local Minimums"
    description : str = "Looks for the asset for which the current price is lower \
than all previous local minimums."

    @staticmethod
    def strategy(ap : AssetPair) -> float:
        Strategy.other[Strategy.name] = [V, LALM]
        return Strategy.get_res(Strategy.name, ap, None)
