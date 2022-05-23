from __future__ import annotations

from typing import Any, Dict, List, Tuple

###############################################################################
############################## VARIABLES ######################################
###############################################################################

###############################################################################
############################## CLASSES ########################################
###############################################################################

class Pair:
    
    def __init__(self : Pair, asset_1 : str, asset_2 : str) -> Pair:
        """
        Creates a new pair of assets.

        :param asset_1: The first asset.
        :param asset_2: The second asset.
        """
        self.asset_1 : str = asset_1
        self.asset_2 : str = asset_2

        # short names
        self.a1 : str = self.asset_1
        self.a2 : str = self.asset_2

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

###############################################################################
############################## MAIN ###########################################
###############################################################################
