from __future__ import annotations

from typing import Dict, Callable

from Structures.Asset import Asset
from Structures.AssetPair import AssetPair
from Structures.KrakenAPI import KrakenAPI
from Structures.Error import Error

class AssetHandler:

    """
    This class is used to handle a list of assets, it keeps track of all
    the existing assets and the values associated to them.
    """

    def __init__(self : AssetHandler) -> AssetHandler:
        """
        Creates a new asset handler.
        """
        self.assets : Dict[str, Asset] = {}

        # generic information about the market
        self.pairs : Dict[str, AssetPair] = {}
        self.usd_pairs : Dict[str, AssetPair] = {}

    def update_assets(self : AssetHandler, kapi : KrakenAPI, *, asset : str = None) -> None:
        """
        This methods updates the list of existing assets.

        :param kapi: The already initialized KrakenAPI.
        """
        result = kapi.get_assets(asset=asset)

        if isinstance(result, Error):
            print("An error occurred!")
            return None

        for asset in result:
            self.assets[asset] = Asset.build_asset(asset, result[asset])

    def update_tradable_assets(self : AssetHandler, kapi : KrakenAPI, *, pair : str = None) -> None:
        """
        This methods updates the list of existing tradable assets.
        It does not update the Assets, their value in the trade whatsoever.

        :param kapi: The already initialized KrakenAPI.
        """
        result = kapi.get_tradable_assets(pair=pair)

        if isinstance(result, Error):
            print("An error occurred!")
            return None

        for pair in result:
            self.pairs[pair] = AssetPair.build_asset_pair(pair, result[pair])

            if (self.pairs[pair].base == "ZUSD" or
                self.pairs[pair].quote == "ZUSD" or
                self.pairs[pair].quote == "USD" or
                self.pairs[pair].base == "USD"):

                self.usd_pairs[pair] = self.pairs[pair]

    def update_usd_tradable_prices(self : AssetHandler, kapi : KrakenAPI, *, pair : str = None, total : int = -1) -> None:
        """
        Updates the value of the trades of tradable USD assets.

        :param kapi: The already initialized KrakenAPI.
        """
        if pair != None:
            result = kapi.public_kraken_request(f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval=5")

            if isinstance(result, Error):
                print("An error occurred!")
                return None

            self.pairs[pair].update_prices(result[pair])
            self.pairs[pair].update_data(self.pairs[pair].quote != "ZUSD" and self.pairs[pair].quote != "USD")
        else:
            for p in self.usd_pairs:
                print(p)
                result = kapi.public_kraken_request(f"https://api.kraken.com/0/public/OHLC?pair={p}&interval=5")

                if isinstance(result, Error):
                    print("An error occurred!")
                    return None

                self.pairs[p].update_prices(result[p])
                self.pairs[p].update_data(self.pairs[p].quote != "ZUSD" and self.pairs[p].quote != "USD")

                total -= 1
                if total == 0: break
        print("")

    def get_best_usd_pair(self : AssetHandler, strategy : Callable[[AssetPair], float]) -> AssetPair:
        """
        Returns the best USD pair of tradable assets.

        :param strategy: The strategy to apply, to decide which asset
        is best suited to be bought. This strategy should be a function
        that takes as input an AssetPair object and returns a floating 
        point value.
        
        :returns: The best asset to buy right now.
        """
        best_pair : AssetPair = None
        max_val = None
        best_pair = None

        for pair in self.usd_pairs:
            if not self.usd_pairs[pair].is_init: continue
            p = self.usd_pairs[pair]
            res = strategy(p)
            
            if max_val == None or max_val < res:
                max_val = res if max_val == None else max(res, max_val)
                best_pair = p

        return best_pair

    def __str__(self : AssetHandler) -> str:
        s = "Assets:\n"
        for element in self.assets:
            s += str(self.assets[element]) + "\n"
            s += "-------------------------------------------------\n"
        
        for element in self.pairs:
            s += str(self.pairs[element]) + "\n"
            s += "-------------------------------------------------\n"

        return s.rstrip("\n")