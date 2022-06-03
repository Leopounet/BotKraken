from __future__ import annotations
import time

from typing import Dict, Type

from Structures.Asset import Asset
import Structures.AssetPair as AP
from Structures.KrakenAPI import KrakenAPI
from Structures.Error import Error, ErrorType
import Structures.Strategy as Strategy

from Utils.StringManipulation import tabulate

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
        self.pairs : Dict[str, AP.AssetPair] = {}
        self.usd_pairs : Dict[str, AP.AssetPair] = {}

        self.log_file : str = "logs.txt"

    def update_assets(self : AssetHandler, kapi : KrakenAPI, *, asset : str = None) -> None:
        """
        This methods updates the list of existing assets.

        :param kapi: The already initialized KrakenAPI.
        """
        result = kapi.get_assets(asset=asset)

        if isinstance(result, Error):
            print("An error occurred!")
            with open(self.log_file, "a") as file:
                file.write(result.error.value + " : " + result.msg + "\n")
            if result.error == ErrorType.RATE_LIMIT:
                time.sleep(200)
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
            with open(self.log_file, "a") as file:
                file.write(result.error.value + " : " + result.msg + "\n")
            if result.error == ErrorType.RATE_LIMIT:
                time.sleep(200)
            return None

        for pair in result:
            self.pairs[pair] = AP.AssetPair.build_asset_pair(pair, self, result[pair])

            if (self.pairs[pair].base.name == "ZUSD" or
                self.pairs[pair].quote.name == "ZUSD" or
                self.pairs[pair].quote.name == "USD" or
                self.pairs[pair].base.name == "USD"):

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
                with open(self.log_file, "a") as file:
                    file.write(result.error.value + " : " + result.msg + "\n")
                if result.error == ErrorType.RATE_LIMIT:
                    time.sleep(200)
                return None

            self.pairs[pair].update_prices(result[pair])
            self.pairs[pair].update_data(self.pairs[pair].quote.name != "ZUSD" and self.pairs[pair].quote.name != "USD")
        else:
            for p in self.usd_pairs:
                # print(p)
                result = kapi.public_kraken_request(f"https://api.kraken.com/0/public/OHLC?pair={p}&interval=5")

                if isinstance(result, Error):
                    print("An error occurred!")
                    with open(self.log_file, "a") as file:
                        file.write(result.error.value + " : " + result.msg + "\n")
                    if result.error == ErrorType.RATE_LIMIT:
                        time.sleep(200)
                    return None

                self.pairs[p].update_prices(result[p])
                self.pairs[p].update_data(self.pairs[p].quote.name != "ZUSD" and self.pairs[p].quote.name != "USD")

                total -= 1
                if total == 0: break

    def get_best_usd_pair(self : AssetHandler, bs : Type[Strategy.BuyStrategy]) -> AP.AssetPair:
        """
        Returns the best USD pair of tradable assets.

        :param strategy: The strategy to apply, to decide which asset
        is best suited to be bought. This strategy should be a function
        that takes as input an AssetPair object and returns a floating 
        point value.
        
        :returns: The best asset to buy right now.
        """
        best_pair : AP.AssetPair = None
        max_val = None
        best_pair = None

        for pair in self.usd_pairs:
            if not self.usd_pairs[pair].is_init: continue
            p = self.usd_pairs[pair]
            res = bs.strategy(p)
            
            if max_val == None or max_val < res:
                max_val = res if max_val == None else max(res, max_val)
                best_pair = p

        return best_pair

    def __str__(self : AssetHandler) -> str:
        s = "Assets:\n"
        for element in self.assets:
            s += f"Asset {self.assets[element].name}: \n"
            s += tabulate(str(self.assets[element])) + "\n"
            s += "-------------------------------------------------\n"
        
        for element in self.pairs:
            s += f"Asset {self.pairs[element].name}: \n"
            s += tabulate(str(self.pairs[element])) + "\n"
            s += "-------------------------------------------------\n"

        for element in self.usd_pairs:
            s += f"Asset {self.usd_pairs[element].name}: \n"
            s += tabulate(str(self.usd_pairs[element])) + "\n"
            s += "-------------------------------------------------\n"

        return s.rstrip("\n")