from __future__ import annotations
from enum import Enum

from typing import Any, Dict, List, Tuple

###############################################################################
############################## VARIABLES ######################################
###############################################################################

###############################################################################
############################## CLASSES ########################################
###############################################################################

class Asset:

    """
    This class represents an asset.
    """

    def __init__(self : Asset, asset : str) -> Asset:
        """
        Creates a new asset.

        :param asset: The name of the asset.
        """
        self.name : str = asset.upper()

        # short names
        self.n : str = self.name

class Pair:

    """
    This class represents a pair of assets.
    """
    
    def __init__(self : Pair, asset_1 : Asset, asset_2 : Asset) -> Pair:
        """
        Creates a new pair of assets.

        :param asset_1: The first asset.
        :param asset_2: The second asset.
        """
        self.asset_1 : Asset = asset_1
        self.asset_2 : Asset = asset_2
        
        # short names
        self.a1 : Asset = self.asset_1
        self.a2 : Asset = self.asset_2

        self.name : str = self.get_pair_name()
        self.n : str = self.name

    def get_pair_name(self : Pair) -> str:
        """
        Returns the concat name of both assets.

        :returns: The concat name of both assets.
        """
        return min(self.a1.n, self.a2.n) + max(self.a1.n, self.a2.n)

class ErrorType(Enum):

    """
    Enumeration of all the error types possible.
    """

    INVALID_ARGUMENT = "EGeneral:Invalid arguments"
    INDEX_UNAVAILABLE = "EGeneral:Invalid arguments:Index unavailable"
    UNAVAILABLE = "EService:Unavailable"
    MARKET_CANCEL_ONLY = "EService:Market in cancel_only mode"
    MARKET_POST_ONLY = "EService:Market in post_only mode"
    DEADLINE_ELAPSED = "EService:Deadline elapsed"
    INVALID_KEY = "EAPI:Invalid key"
    INVALID_SIGNATURE = "EAPI:Invalid signature"
    INVALID_NONCE = "EAPI:Invalid nonce"
    PERMISSION_DENIED = "EGeneral:Permission denied"
    CANNOT_OPEN = "EOrder:Cannot open position"
    MARGIN_ALLOWANCE_EXCEEDED = "EOrder:Margin allowance exceeded"
    MARGIN_TOO_LOW = "EOrder:Margin level too low"
    MARGIN_SIZE_EXCEEDED = "EOrder:Margin position size exceeded"
    INSUFFICIENT_MARGIN = "EOrder:Insufficient margin"
    INSUFFICIENT_FUNDS = "EOrder:Insufficient funds"
    ORDER_MIN = "EOrder:Order minimum not met"
    ORDER_LIMIT = "EOrder:Orders limit exceeded"
    RATE_LIMIT = "EOrder:Rate limit exceeded"
    POSITIONS_LIMIT = "EOrder:Positions limit exceeded"
    UNKNOWN_POSITION = "EOrder:Unknown position"
    UNKNOWN_ERROR = "Unknown error generated"

class Error:

    """
    Used to determine which error occurred.
    """

    def __init__(self : Error, error : str) -> Error:
        """
        Creates a new error.

        :param error: The error message received.
        """
        self.msg : str = error
        self.error : ErrorType = self.msg_to_error(error)

    def msg_to_error(self : Error, msg : str) -> ErrorType:
        """
        Returns the error type depending on the error message.

        :param msg: The error message.

        :returns: The error type, DefaultError if the message does
        not correspond to any ErrorType.
        """
        for error in ErrorType:
            if error.value == error:
                return error
        return ErrorType.UNKNOWN_ERROR


class Response:

    """
    Response from a KrakenAPI method.
    """

    def __init__(self : Response, key : str) -> Response:
        """
        Creates a new response error.

        :param key: The key that was used to get the response.
        :param result: the result, if any.
        :param error: The error, if any.
        """
        self.key : str = key
        self.result : Any = None
        self.error : Error = None

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################

###############################################################################
############################## MAIN ###########################################
###############################################################################
