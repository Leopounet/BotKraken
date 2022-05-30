from __future__ import annotations
from enum import Enum
import random

class Color(Enum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"

____colors = [Color.RED, Color.GREEN, Color.YELLOW,
              Color.BLUE, Color.MAGENTA, Color.CYAN, Color.WHITE]

def random_color() -> Color:
    """
    Returns a random color.
    """
    return random.choice(____colors)