from random import randint
from typing import Tuple


def rand_color(minv: int = 0, maxv: int = 255) -> Tuple[int, int, int]:
    """returns a random RGB color with min and max as min and max threshold"""
    return randint(minv, maxv), randint(minv, maxv), randint(minv, maxv)


def rand_bw_color(minv: int, maxv: int) -> Tuple[int, int, int]:
    """returns a random RGB BW color"""
    shade = randint(minv, maxv)
    return shade, shade, shade
