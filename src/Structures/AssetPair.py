from __future__ import annotations

from typing import Dict, List, Any

from Structures.Asset import Asset
from Structures.AssetPairData import AssetPairData
import Structures.AssetHandler as AH

from datetime import datetime

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

        self.data : AssetPairData = None
        self.is_init : bool = False

    @staticmethod
    def __compute_fee(df : List[float]):
        maximum = 0
        for element in df:
            if float(element[1]) >= maximum:
                maximum = float(element[1])
        return maximum

    @staticmethod
    def build_asset_pair(name : str, ah : AH.AssetHandler, data : Dict[str, Any]) -> AssetPair:
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
        ap.base = ah.assets[data["base"]]
        ap.quote = ah.assets[data["quote"]]
        ap.fee = AssetPair.__compute_fee(data["fees"])
        ap.order_min = data["ordermin"]

        return ap

    def update_prices(self : AssetPair, data : List[List[float]]) -> None:
        """
        Updates the price of the current AssetPair.

        :param data: The data holding the prices.
        """
        for i in range(0, len(data)):
            self.history[int(data[i][0])] = float(data[i][4])

    def update_data(self : AssetPair, invert : bool = False) -> None:
        """
        Updates all the data related to this pair of asset. The data is
        calculated from the history of recorded prices in the last 
        48 hours.

        :param invert: If True, the quote and base are inverted.
        """
        history = self.history
        keys = sorted(list(history.keys()))
        data = AssetPairData()

        # renaming
        ascension_fall_threshold = 3
        aft = ascension_fall_threshold

        # used to detect ascension, falls, local min and max
        ascension = -1
        fall = 0
        values  = []

        for i, date in enumerate(keys):
            if history[date] == 0: continue
            value = history[date] if not invert else 1 / history[date]

            # maximum and minimum overall values
            data.maximum = value if data.maximum == None else max(data.maximum, value)
            data.minimum = value if data.minimum == None else min(data.minimum, value)
            data.mean += value

            # get the mean of the aft previous values to determine current trend
            tmp_slice = values[max(i - aft, 0):i]
            mean_last_values = sum(tmp_slice) / len(tmp_slice) if len(tmp_slice) != 0 else 0

            # computing ascension 
            if value >= mean_last_values:
                ascension += 1
                
                # was it a local maximum ?
                if fall == aft:
                    data.local_maximums[keys[i - fall]] = history[keys[i - fall]]
                    data.longest_fall = fall if data.longest_fall == None else max(data.longest_fall, fall)
                    data.shortest_fall = fall if data.shortest_fall == None else min(data.shortest_fall, fall)
                    data.average_fall += fall
                    data.nb_local_max += 1

                if value > mean_last_values:fall = 0
            
            # computing fall
            if value <= mean_last_values:
                fall += 1

                # was it a local minimum ?
                if ascension == aft:
                    data.local_minimums[keys[i - ascension]] = history[keys[i - ascension]]
                    data.longest_ascension = ascension if data.longest_ascension == None else max(data.longest_ascension, ascension)
                    data.shortest_ascension = ascension if data.shortest_ascension == None else min(data.shortest_ascension, ascension)
                    data.average_ascension += ascension
                    data.nb_local_min += 1

                if value < mean_last_values: ascension = 0

            values.append(value)

        # variance of the currency
        data.variance = 1 - (data.minimum / data.maximum) if data.maximum != 0 else 0

        # mean of the currency
        data.mean = data.mean / len(keys) if len(keys) != 0 else 0
        
        # average local min and max
        data.average_local_max = sum(data.local_maximums.values()) / len(data.local_maximums) if len(data.local_maximums) != 0 else 0
        data.average_local_min = sum(data.local_minimums.values()) / len(data.local_minimums) if len(data.local_minimums) != 0 else 0 

        # average ascension and fall
        data.average_ascension = data.average_ascension / data.nb_local_max if data.nb_local_max != 0 else 0
        data.average_fall = data.average_fall / data.nb_local_min if data.nb_local_min != 0 else 0

        # current state of the curve
        data.is_ascending = ascension >= aft
        data.current_ascension_duration = ascension
        data.is_falling = fall >= aft
        data.current_fall_duration = fall

        # true if upward (resp. true if downward)
        data.trending_upwards = history[keys[-1]] / history[keys[0]] >= 1 if history[keys[0]] != 0 else False
        data.trending_downwards = history[keys[-1]] / history[keys[0]] <= 1 if history[keys[0]] != 0 else False

        data.current = history[keys[-1]]

        self.data = data
        self.is_init = True

    def copy(self : AssetPair) -> AssetPair:
        """
        Creates and returns a copy of this AssetPair object.
        """
        ap = AssetPair()
        ap.name = self.name
        ap.altname = self.altname
        ap.wsname = self.wsname
        ap.base = self.base.copy()
        ap.quote = self.quote.copy()
        ap.fee = self.fee
        ap.order_min = self.order_min
        ap.history = self.history.copy()

        ap.data = self.data.copy()
        ap.is_init = self.is_init
        return ap


    def __str__(self : AssetPair) -> str:
        s = ""
        s += f"Name: {self.name}\n"
        s += f"Altname: {self.altname}\n"
        s += f"Wsname: {self.wsname}\n"
        s += f"Base: {self.base}\n"
        s += f"Quote: {self.quote}\n"
        s += f"Fee: {self.fee}\n"
        s += f"Min order: {self.order_min}\n"
        
        s += str(self.data) + "\n"
        s += str(self.is_init)
        return s.rstrip("\n")

    def str(self : AssetPair) -> str:
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
        
        s += str(self.data) + "\n"
        s += str(self.is_init)
        return s.rstrip("\n")