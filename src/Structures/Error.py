from __future__ import annotations
from enum import Enum

from typing import Any, Dict, List, Tuple

###############################################################################
############################## VARIABLES ######################################
###############################################################################

###############################################################################
############################## CLASSES ########################################
###############################################################################

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