from __future__ import annotations

from datetime import datetime

from Error import Error
from typing import Any, Dict, Set, List, Tuple

from KrakenAPI import KrakenAPI

###############################################################################
############################## CLASSES ########################################
###############################################################################

class __CachedData:

    """
    This class is used to store some cached data.
    """

    def __init__(self : __CachedData) -> __CachedData:
        """
        Creates a new object to store data.
        """
        pass

class Asset:

    """
    This class represents an asset.
    """

    def __init__(self : Asset) -> Asset:
        """
        Creates a new asset.
        """
        self.name : str = None
        self.altname : str = None
        self.decimals : int = None
        self.display_decimals : int = None

    @staticmethod
    def build_asset(name : str, data : Dict[str, Any]) -> Asset:
        """
        This methods builds a new asset and returns it.

        :param name: The name of the asset being created.
        :param data: Data returned from Kraken corresponding to
        this asset.

        :returns: The constructed Asset.
        """

        # the new asset and shorter names
        asset = Asset()
        asset.name = name

        asset.altname = data["altname"]
        asset.decimals = data["decimals"]
        asset.display_decimals = data["display_decimals"]

        return asset

    # @staticmethod
    # def update_asset(asset : Asset, data : Dict[str, any]) -> Asset:
    #     """
    #     Updates an existing Asset and returns it.

    #     :param asset: The asset to update.
    #     :param data: Data returned from Kraken corresponding to
    #     this asset.

    #     :returns: The same Asset object but update.
    #     """
    #     asset.altname = data["altname"]
    #     asset.decimals = data["decimals"]
    #     asset.display_decimals = data["display_decimals"]
    #     return asset

    def __str__(self : Asset) -> str:
        s = f"Name = {self.name}\n"
        s += f"Altname = {self.altname}\n"
        s += f"decimals = {self.decimals}\n"
        s += f"displayed_decimals = {self.display_decimals}"
        return s

class AssetPair:

    """
    This class represents a pair of tradable assets.
    """

    def __init__(self : AssetPair) -> AssetPair:
        """
        Creates a new AssetPair object.
        """
        self.name : str = None
        self.altname : str = None
        self.wsname : str = None
        self.base : Asset = None
        self.quote : Asset = None
        self.fee : float = None
        self.order_min : float = None
        self.history : Dict[int, float] = {}

    @staticmethod
    def __compute_fee(df : List[float]):
        maximum = 0
        for element in df:
            if float(element[1]) >= maximum:
                maximum = float(element[1])
        return maximum

    @staticmethod
    def build_asset_pair(name : str, data : Dict[str, Any]) -> AssetPair:
        """
        This methods builds a new pair of assets and returns it.

        :param name: The name of the asset being created.
        :param data: Data returned from Kraken corresponding to
        this asset.

        :returns: The constructed AssetPair.
        """
        ap = AssetPair()

        ap.name = name
        ap.altname = data["altname"]
        ap.wsname = data["wsname"]
        ap.base = data["base"]
        ap.quote = data["quote"]
        ap.fee = AssetPair.__compute_fee(data["fees"])
        ap.order_min = data["ordermin"]

        return ap

    def update_prices(self : AssetPair, data : List[List[float]]) -> None:
        """
        Updates the price of the current AssetPair.

        :param data: The data holding the prices.
        """
        for i in range(-1, -len(data) - 1, -1):
            if int(data[i][0]) in self.history:
                break
            self.history[int(data[i][0])] = float(data[i][4])

    def __str__(self : AssetPair) -> str:
        s = ""
        s += f"Name: {self.name}\n"
        s += f"Altname: {self.altname}\n"
        s += f"Wsname: {self.wsname}\n"
        s += f"Base: {self.base}\n"
        s += f"Quote: {self.quote}\n"
        s += f"Fee: {self.fee}\n"
        s += f"Min order: {self.order_min}\n"
        
        for t in self.history:
            date = datetime.fromtimestamp(t).strftime("%A, %B %d, %Y %I:%M:%S")
            s += f"{date}: {self.history[t]}\n"
        return s.rstrip("\n")

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

    def update_usd_tradable_prices(self : AssetHandler, kapi : KrakenAPI, *, pair : str = None) -> None:
        """
        Updates the value of the trades of tradable USD assets.

        :param kapi: The already initialized KrakenAPI.
        """
        if pair != None:
            result = kapi.public_kraken_request(f"https://api.kraken.com/0/public/OHLC?pair={pair}")

            if isinstance(result, Error):
                print("An error occurred!")
                return None

            self.pairs[pair].update_prices(result[pair])
        else:
            for p in self.usd_pairs:
                print(p)
                result = kapi.public_kraken_request(f"https://api.kraken.com/0/public/OHLC?pair={p}")

                if isinstance(result, Error):
                    print("An error occurred!")
                    return None

                self.pairs[p].update_prices(result[p])

    @staticmethod
    def evaluate_history(f : Dict[int, float], invert = False) -> int:
        """
        """
        keys = sorted(list(f.keys()))
        maximum = None
        minimum = None

        for date in keys:
            value = f[date] if not invert else 1 / f[date]

            # maximum and minimum overall values
            maximum = value if maximum == None else max(maximum, value)
            minimum = value if minimum == None else min(minimum, value)

        # variance of the currency
        var = 1 - (minimum / maximum)

        # true if upward
        upward_trend = f[keys[-1]] / f[keys[0]] >= 1

        if var >= 0.1 and not upward_trend:
            return None

        return var

    def get_best_usd_pair(self : AssetHandler) -> AssetPair:
        """
        """
        best_pair : AssetPair = None
        max_val = None
        best_pair = None

        for pair in self.usd_pairs:
            print(pair)
            p = self.usd_pairs[pair]
            date_value = p.history
            res = self.evaluate_history(date_value, invert = p.quote != "ZUSD")

            if res == None:
                continue
            
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
