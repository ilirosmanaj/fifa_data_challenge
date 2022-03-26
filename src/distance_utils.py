import math


def eucledian_distance_in_meters(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    Calculates eucledian distance between two points. Coordinates are in cm, but since we want results in meters we
    divide by 100
    """
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0) / 100
