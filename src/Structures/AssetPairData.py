from __future__ import annotations
from typing import Dict

class AssetPairData:

    """
    This class holds some data about a pair of assets.
    """

    def __init__(self : AssetPairData) -> AssetPairData:
        """
        Create a new AssetPairData object.
        """
        self.current : float = None
        self.maximum : float = None
        self.minimum : float = None
        self.variance : float = 0
        self.mean : float = 0

        self.longest_ascension : int = None
        self.shortest_ascension : int = None
        self.average_ascension : int = 0
        self.is_ascending : bool = None
        self.current_ascension_duration : int = None
        self.trending_upwards : bool = None

        self.longest_fall : int = None
        self.shortest_fall : int = None
        self.average_fall : int = 0
        self.is_falling : int = None
        self.current_fall_duration : int = None
        self.trending_downwards : bool = None

        self.local_maximums : Dict[int, float] = {}
        self.average_local_max : float = 0
        self.nb_local_max : int = 0

        self.local_minimums : Dict[int, float] = {}
        self.average_local_min : float = 0
        self.nb_local_min : int = 0

    def __str__(self : AssetPairData) -> str:
        """
        """
        s = "Data about this tradable pair of assets:\n"
        s += f"""
        Current:                    {round(self.current, 6)}
        Maximum:                    {round(self.maximum, 6)}
        Minimum:                    {round(self.minimum, 6)}
        Variance:                   {round(self.variance, 6)}
        Mean:                       {round(self.mean, 6)}
        Longest ascension:          {round(self.longest_ascension, 6)}
        Shortest ascension:         {round(self.shortest_ascension, 6)}
        Average ascension:          {round(self.average_ascension, 6)}
        Is ascending:               {self.is_ascending}
        Current ascension duration: {round(self.current_ascension_duration, 6)}
        Trending upwards:           {self.trending_upwards}
        Longest fall:               {round(self.longest_fall, 6)}
        Shortest fall:              {round(self.shortest_fall, 6)}
        Average fall:               {round(self.average_fall, 6)}
        Is falling:                 {self.is_falling}
        Current fall duration:      {round(self.current_fall_duration, 6)}
        Trending downwards:         {self.trending_downwards}
        Average local maximum:      {round(self.average_local_max, 6)}
        Number of local maximums:   {round(self.nb_local_max, 6)}
        Average local minimum:      {round(self.average_local_min, 6)}
        Number of local minimums:   {round(self.nb_local_min, 6)}"""
        return s